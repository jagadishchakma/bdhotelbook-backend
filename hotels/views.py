from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,viewsets
from rest_framework.generics import ListAPIView
from .models import District,Hotels,HotelRoom,HotelReview
from accounts.models import Profile,RoomBooked
from .serializers import DistrictSerializer, HotelSerializer,HotelReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# districtview
class DistrictView(APIView):
    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

#hotels view via district
class HotelView(ListAPIView):
    serializer_class = HotelSerializer
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Hotels.objects.filter(district__slug=slug)

#hotel details view via district and title
class HotelDetailView(ListAPIView):
    serializer_class = HotelSerializer
    def get_queryset(self):
        slug1 = self.kwargs['slug1']
        slug2 = self.kwargs['slug2']
        district = District.objects.get(slug=slug1)
        return Hotels.objects.filter(district=district, slug=slug2)

#hotel room booked
class HotelRoomBookedView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        user = request.user
        try:
            profile = user.profile
            auth_profile = Profile.objects.get(pk=profile.id)
            hotel_room = HotelRoom.objects.get(slug=slug)
        except HotelRoom.DoesNotExist:
            return Response({'error': 'HotelRoom not found'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create or get a RoomBooked instance 
        room_booked = RoomBooked.objects.create()
        
        # Add the hotel room to the RoomBooked instance
        room_booked.room.add(hotel_room)
        room_booked.save()

        # Add the RoomBooked instance to the profile and room
        profile.room_booked.add(room_booked)
        profile.save()
        hotel_room.room_booked = True
        auth_profile.balance -= hotel_room.room_price
        hotel_room.save(
            update_fields=['room_booked']
        )
        auth_profile.save(
            update_fields= ['balance']
        )


        #send email to user
        details = {
            'room_name':hotel_room.room_name,
            'room_price':hotel_room.room_price,
            'room_bed':hotel_room.room_bed,
        }
        mail_subject = "Room Booked Message"
        mail_body = render_to_string('room_booked.html', details)
        send_mail = EmailMultiAlternatives(mail_subject,'',to=[user.email])
        send_mail.attach_alternative(mail_body, 'text/html')
        send_mail.send()
        

        return Response({'message': 'Hotel room booked successfully'}, status=status.HTTP_200_OK)



#hotel review 
class HotelReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class HotelReviewViewSet(viewsets.ModelViewSet):
    serializer_class = HotelReviewSerializer
    pagination_class = HotelReviewPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = HotelReview.objects.all().order_by('-id')
        slug = self.kwargs.get('slug')
        if slug:
            queryset = queryset.filter(hotel__slug=slug)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        slug = request.data['slug']
        hotel = Hotels.objects.get(slug=slug);
        if serializer.is_valid():
            serializer.save(user=request.user, hotel=hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)