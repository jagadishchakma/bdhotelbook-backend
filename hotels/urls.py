from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('reviews', views.HotelReviewViewSet, basename='hotelreview')
urlpatterns = [
    path('', include(router.urls)),
    path('reviews/<slug:slug>/all/', views.HotelReviewViewSet.as_view({'get': 'list'}), name='review_filter'),
    path('districts/', views.DistrictView.as_view(), name="district"),
    path('<slug:slug>/', views.HotelView.as_view(), name="hotels"),
    path('<slug:slug1>/<slug:slug2>/', views.HotelDetailView.as_view(), name="hotel"),
    path('room/booked/<slug:slug>/', views.HotelRoomBookedView.as_view(), name="room_booked")
]
