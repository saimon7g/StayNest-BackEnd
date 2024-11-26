# StayNest Backend

A microservices-based backend system for a property rental and booking platform built with Django REST Framework. The system consists of multiple services handling different aspects of the application, including property management, booking, user authentication, and negotiations.

## System Architecture

The backend is structured into several microservices:

### 1. Host Service
- Property registration and management
- Property availability management
- Host profile management
- Property analytics and insights

### 2. Guest Service
- Booking management
- Payment processing
- Review system
- Guest notifications

### 3. API Gateway
- Authentication and authorization
- Request routing
- Cross-origin resource sharing
- Token management

### 4. Negotiation Service
- Price negotiation system
- Real-time status updates
- Communication handling between hosts and guests

## Tech Stack

- **Framework:** Django REST Framework
- **Database:** PostgreSQL (Supabase)
- **Authentication:** Token-based authentication
- **API Documentation:** REST API
- **Deployment:** AWS
- **Additional Tools:**
  - django-cors-headers
  - psycopg2-binary
  - python-dateutil
  - requests

## Key Features

### Authentication & Authorization
- Token-based authentication system
- Role-based access control (Host/Guest)
- Secure password handling
- Session management

### Property Management
- Multi-step property registration
- Location and amenities management
- Availability calendar
- Pricing and discount management
- Photo management

### Booking System
- Real-time availability checking
- Multiple booking types:
  - Standard stay
  - Stay with meals
  - Paying guest
- Meal planning and management
- Dynamic pricing
- Booking status management

### Negotiation System
- Real-time price negotiation
- Status tracking
- Multiple negotiation stages
- Automated notifications

### User Profile Management
- Separate host and guest profiles
- Profile verification
- Document management (NID, Passport)
- Super host status

## Database Schema

### Key Models
```python
# Property Registration
- PropertyRegistration
- Location
- SomeBasics
- PropertyStep2-7
- RegularAmenities
- StandoutAmenities

# Booking Management
- Booking
- Payment
- Meal
- SelectedDate

# User Management
- UserProfile
- GuestNotification
- TemporaryBooking



API Endpoints


Authentication
CopyPOST /auth/login/
POST /auth/signup/
POST /auth/hostsignup/
POST /auth/logout/

Property Management
CopyPOST /api/property_registration/step1/
PUT  /api/property_registration/step{2-7}/<registration_id>/
GET  /api/properties/search/
GET  /api/property/<property_id>/

Booking
CopyPOST /api/reserve/
GET  /api/booking_details/<booking_id>/
PUT  /api/booking/<booking_id>/status/
GET  /api/upcoming_bookings/as_guest/
GET  /api/upcoming_bookings/as_host/

Negotiation
CopyGET  /api/nego/as_guest/
GET  /api/nego/as_host/
POST /api/nego/start_negotiation_by_guest/
PUT  /api/nego/update_status/<negotiation_id>/

Setup Instructions

Clone the repository

bashCopygit clone <repository-url>

Create and activate virtual environment

bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

bashCopypip install -r requirements.txt

Configure environment variables

bashCopy# Create .env file with the following:
DATABASE_URL=your_supabase_database_url
SECRET_KEY=your_django_secret_key

Run migrations

bashCopypython manage.py migrate

Start the development server

bashCopypython manage.py runserver
Testing
bashCopypython manage.py test
Deployment
The system is designed to be deployed as separate microservices, each handling specific functionality. Current deployment uses:

AWS for hosting
Supabase for database
CORS enabled for frontend integration





















































Here's a combined summary of the StayNest property rental platform:
StayNest is a full-stack property rental platform offering multiple accommodation types (standard stays, meal-inclusive packages, and paying guest arrangements) with sophisticated booking and negotiation features.
Architecture:

Frontend: Next.js 13+ with App Router, using Tailwind CSS and Flowbite React
Backend: Django REST Framework-based microservices (Host, Guest, API Gateway, Negotiation)
Database: PostgreSQL (Supabase)
Deployment: AWS

Key Features:

Property Management


Multi-step registration process
Location/amenities management
Availability calendar
Dynamic pricing


Booking System


Real-time availability checking
Multiple accommodation types
Meal planning integration
Status tracking


User Features


Role-based access (Host/Guest)
Profile management
Document verification
Booking/hosting history


Technical Features


Token-based authentication
Map integration (MapTiler SDK)
Real-time negotiations
Secure payment processing
Responsive design
API Gateway for service orchestration

The system follows a microservices architecture with separate frontend and backend codebases, enabling scalable and maintainable development while providing comprehensive property rental functionality for both hosts and guests.