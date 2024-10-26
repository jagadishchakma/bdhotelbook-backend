# BD Hotel Book API

[Live Demo](https://bdhotelapi.tfbfoundation.org/)

BD Hotel Book API is a backend service for the BD Hotel Book platform, providing a set of endpoints for hotel management, bookings, user authentication, and account management. The API is built using Django and Django REST Framework.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Admin Access](#admin-access)
  - [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Hotel Management**: Create, update, and manage hotel information.
- **Room Booking**: Book rooms in different hotels.
- **Reviews**: Add and view reviews for hotels.
- **User Authentication**: Secure registration, login, logout, and password management.
- **Account Management**: Update user profiles and balance management.

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Django REST Framework

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/jagadishchakma/bdhotelbook-backend
    ```
2. Navigate to the project directory:
    ```bash
    cd bd-hotel-book-api
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the migrations:
    ```bash
    python manage.py migrate
    ```
5. Start the development server:
    ```bash
    python manage.py runserver
    ```
6. Access the API at `http://localhost:8000`.

## Usage

### Admin Access
Access the admin panel for administrative tasks:

[Admin Panel](https://bdhotelapi.tfbfoundation.org/admin/)

- **Username**: `admin`
- **Password**: `123`

### API Endpoints

#### For Hotels
- `GET /`: List all hotels.
- `GET /reviews/<slug:slug>/all/`: View reviews for a specific hotel.
- `GET /districts/`: Get a list of districts.
- `GET /<slug:slug>/`: View hotel details.
- `GET /<slug:slug1>/<slug:slug2>/`: View detailed information about a specific hotel.
- `GET /room/booked/<slug:slug>/`: View booked rooms for a specific hotel.

#### For Accounts
- `POST /register/`: Register a new user.
- `GET /active/<uid64>/<token>/`: Activate a user account.
- `POST /login/`: User login.
- `POST /logout/`: User logout.
- `POST /balance/update/`: Update the account balance.
- `POST /pass_change/`: Change the user's password.
- `POST /upload/profile/`: Upload a profile picture.
- `PATCH /update/profile/`: Update profile information.
- `PATCH /update/user/`: Update user information.

## Technologies Used
- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL
- **Hosting**: Vercel (Frontend), Heroku (Backend)

## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
