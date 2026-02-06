# Moulin Rouge REST API

RESTful API backend for a restaurant management system built with Django and Django REST Framework.

[![Django](https://img.shields.io/badge/Django_4.2.18-darkgreen)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/Django_Rest_Framework_3.15.2-darkgreen)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-red)](https://www.python.org/)
[![License](https://img.shields.io/badge/Polyform_Perimeter_License_1.0.0-darkred)](LICENSE.md)

## Description

**Moulin Rouge REST API** is a comprehensive backend system designed for restaurant operations. It provides endpoints for managing menu items, user authentication, reservations, deliveries, comments, ratings, and promotional events. The API implements JWT authentication, rate limiting, custom permissions, and supports image uploads for menu items and events.

The codebase follows Django best practices, implements RESTful API design principles, includes comprehensive validation, and supports multiple authentication methods.

## Main Features

- **User Authentication**: JWT-based authentication with email verification, user registration, login, and logout
- **Menu Management**: Complete CRUD operations for courses (menu items) and categories with image support
- **Rating System**: User comments and ratings that automatically calculate course average ratings
- **Reservation System**: Table reservation management with date validation and event-based pricing
- **Delivery Orders**: Order management system with JSON-based course selection and automatic price calculation
- **Event Management**: Promotional events with discount calculations applied to reservations and deliveries
- **Rate Limiting**: Configurable throttling for different endpoints to prevent abuse
- **Custom Permissions**: Role-based access control with admin and main user permissions
- **Image Handling**: Support for course and event image uploads with media file management
- **Pagination**: Efficient data pagination for large datasets

## Technologies Used

| Category | Technologies |
| :--- | :--- |
| **Backend Framework** | Django 4.2.18, Django REST Framework 3.15.2 |
| **Language** | Python 3 |
| **Authentication** | JWT (djangorestframework-simplejwt), Session Authentication |
| **Database** | SQLite3 (development), PostgreSQL support (psycopg2) |
| **Image Processing** | Pillow |
| **API Documentation** | CoreAPI |
| **Permissions** | django-guardian, Custom Permissions |
| **Filtering** | django-filter |
| **CORS** | django-cors-headers |
| **Version Control** | Git, GitHub |
| **Testing** | Django Test Framework |

## Project Structure

```bash
molino_rojo/
├── main_app/              # Main application for restaurant operations
│   ├── api/              # API views, serializers, permissions, throttling
│   ├── models.py         # Course, Category, Comment, Reservation, Delivery, Event models
│   └── migrations/       # Database migrations
├── user_app/             # User authentication and management
│   ├── api/              # User API views and serializers
│   ├── models.py         # Custom User model
│   └── migrations/       # Database migrations
├── molino_rojo/          # Project settings and configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── media/                # Uploaded images and media files
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## API Endpoints

### User Endpoints (`/user/`)

- `POST /user/verify/` - Email verification code generation
- `POST /user/register/` - User registration
- `POST /user/login/` - User login
- `POST /user/logout/` - User logout
- `POST /user/token/` - Obtain JWT token pair
- `POST /user/token/refresh/` - Refresh JWT access token

### Main Application Endpoints (`/main/`)

#### Main View

- `GET /main/` - Get main page data (top 5 courses by rating and active events)

#### Categories

- `POST /main/categorys/post/` - Create category (Admin only)
- `GET /main/categorys/` - List all categories (Admin only)
- `GET /main/categorys/<id>/` - Get category details (Admin only)
- `PUT /main/categorys/<id>/` - Update category (Admin only)

#### Courses

- `POST /main/courses/post/` - Create course (Admin only)
- `GET /main/courses/` - List courses by category (Public, query param: `category`)
- `GET /main/courses/<id>/` - Get course details (Admin only)
- `PUT /main/courses/<id>/` - Update course (Admin only)

#### Comments

- `POST /main/courses/<id>/comments/post/` - Add comment to course (Authenticated)
- `GET /main/courses/<id>/comments/` - List comments for a course (Public)
- `GET /main/comments/<id>/` - Get comment details (Author or Admin)
- `PUT /main/comments/<id>/` - Update comment (Author or Admin)
- `DELETE /main/comments/<id>/` - Delete comment (Author or Admin)

#### Reservations

- `POST /main/reservations/post/` - Create reservation (Authenticated)
- `GET /main/reservations/` - List reservations (Author or Admin, query param: `user`)
- `GET /main/reservations/<id>/` - Get reservation details (Author or Admin)
- `PUT /main/reservations/<id>/` - Update reservation (Author or Admin)
- `DELETE /main/reservations/<id>/` - Delete reservation (Author or Admin)

#### Deliveries

- `POST /main/deliverys/post/` - Create delivery order (Authenticated)
- `GET /main/deliverys/` - List deliveries (Author or Admin, query param: `user`)
- `GET /main/deliverys/<id>/` - Get delivery details (Author or Admin)
- `PUT /main/deliverys/<id>/` - Update delivery (Author or Admin)
- `DELETE /main/deliverys/<id>/` - Delete delivery (Author or Admin)

#### Events

- `POST /main/events/post/` - Create event (Admin only)
- `GET /main/events/` - List all events (Admin only)
- `GET /main/events/<id>/` - Get event details (Admin only)
- `PUT /main/events/<id>/` - Update event (Admin only)
- `DELETE /main/events/<id>/` - Delete event (Admin only)

## Local Installation and Use

Follow these steps to run the project on your local machine.

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package manager)
- [Git](https://git-scm.com/downloads) (optional, for cloning)

### Steps

1. **Clone the repository**

    ```bash
    git clone <repository-url>
    cd molino_rojo
    ```

2. **Create a virtual environment** (recommended)

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

    Create a `.env` file in the project root with the following variables:

    ```env
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-email-password
    ```

5. **Run database migrations**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (optional, for admin access)

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`

8. **Access the admin panel** (optional)

    Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Courses Rate**: 30 requests per minute
- **Comments Rate**: 5 requests per minute
- **Add Rate**: 10 requests per day
- **List Rate**: 10 requests per minute
- **Detail Rate**: 15 requests per minute

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

- **Access Token Lifetime**: 30 minutes
- **Refresh Token Lifetime**: 1 day
- **Token Rotation**: Enabled
- **Token Blacklisting**: Enabled after rotation

To authenticate, include the JWT token in the Authorization header:

```bash
Authorization: Bearer <your-access-token>
```

## Database Models

### User Model

- Custom user model with email as username field
- Fields: name, username, email, phone_number, group
- Supports admin, staff, and superadmin roles

### Course Model

- Menu items with category, image, description, gramage, price
- Automatic rating calculation from user comments
- Availability status

### Category Model

- Menu categories (e.g., Pizza, Pasta, etc.)

### Comment Model

- User reviews with rating (1-5) and text
- One comment per user per course
- Automatically updates course rating

### Reservation Model

- Table reservations with date, number of people
- Automatic price calculation with event discounts
- Date validation (minimum 1 day in advance)

### Delivery Model

- Delivery orders with JSON course selection
- Location and delivery date
- Automatic price calculation with event discounts
- Prevents overlapping deliveries (5-hour window)

### Event Model

- Promotional events with discount percentage
- Date range (start and end dates)
- Applied to reservations and deliveries

## License

This project is licensed under the [PolyForm Perimeter License 1.0.0](LICENSE.md)

### Key Restrictions

- Free use for **non-commercial projects**.
- Use **prohibited** in businesses that compete with the owner.
- **Contact the owner** for a commercial license.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the repository or contact the project maintainers.
