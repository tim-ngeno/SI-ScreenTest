# Django Orders & Customers Management System with OpenID Connect Authentication

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Getting Started](#getting-started)
5. [Environment Variables](#environment-variables)
6. [Docker Setup](#docker-setup)
7. [Database Configuration](#database-configuration)
8. [API Endpoints](#api-endpoints)
9. [Authentication Flow](#authentication-flow)
10. [SMS Notifications](#sms-notifications)
11. [Running Tests](#running-tests)


## Project Overview

This project is a **Django-based** web application designed to manage customers and orders with authentication using **OpenID Connect (OIDC)**. The app integrates with **Okta** for authentication and uses **PostgreSQL** as its database. When a user logs in, they are registered as a customer and can place orders. An SMS notification is sent to the customer upon successful order creation using **Africa’s Talking SMS Gateway**.

## Features

- **OpenID Connect (OIDC) Authentication**: Users authenticate using Okta via the OpenID Connect protocol.
- **Customer & Order Management**: Ability to create and view customer details and orders.
- **REST API**: Input and upload customer and order details through a REST API.
- **SMS Notifications**: Send SMS notifications to customers when an order is placed.
- **Dockerized Setup**: Easily deployable using Docker and Docker Compose.
- **PostgreSQL**: Use PostgreSQL as the primary database.
  
## Technology Stack

- **Backend**: Django 5.1.1, Django Rest Framework (DRF), Python 3.11
- **Authentication**: Mozilla Django OIDC Provider, Okta
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **SMS Gateway**: Africa's Talking Sandbox
- **Web Server**: Gunicorn

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL
- Africa’s Talking account (for SMS sandbox usage)
- Okta account (for OIDC configuration)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tim-ngeno/SI-ScreenTest.git
   cd yourproject
   ```

2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (see [Environment Variables](#environment-variables) below).

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

You can now visit the app at `http://localhost:8000`.

## Environment Variables

Create a `.env` file in the root of your project and define the following variables:

```bash
DEBUG=True
SECRET_KEY=your-secret-key  # random_secret_key provisioned
ALLOWED_HOSTS=localhost, 127.0.0.1
DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME} 
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=5432

# Okta OIDC
OIDC_RP_CLIENT_ID=your-okta-client-id
OIDC_RP_CLIENT_SECRET=your-okta-client-secret
OIDC_OP_AUTHORIZATION_ENDPOINT=https://your-okta-domain/oauth2/default/v1/authorize
OIDC_OP_TOKEN_ENDPOINT=https://your-okta-domain/oauth2/default/v1/token
OIDC_OP_USER_ENDPOINT=https://your-okta-domain/oauth2/default/v1/userinfo
OIDC_OP_JWKS_ENDPOINT=https://your-okta-domain/oauth2/default/v1/keys

# Africa’s Talking
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=your-api-key
```

## Docker Setup

**Build and run the Docker image**:
   ```bash
   docker compose up --build
   ```

Your app should be running on `http://localhost:8000`, and PostgreSQL will be running in the container `db`.

## Database Configuration

### Local Development

To set up PostgreSQL locally, follow these steps:

1. Install PostgreSQL on your local machine.
2. Create a new database:
   ```bash
   createdb mydb
   ```
3. Create a user and grant privileges:
   ```bash
   createuser myuser --pwprompt
   ```
4. Configure the database URL in your `.env` file:
   ```bash
   DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydb
   ```

### Docker

In the Docker Compose file, PostgreSQL is automatically set up with environment variables from `.env`.

## API Endpoints

The project exposes a few REST API endpoints for managing customers and orders:

### Customers API

- `GET /customers/`: List all customers
- `POST /customers/`: Create a new customer

### Orders API

- `GET /orders/`: List all orders
- `POST /orders/`: Place a new order

You can interact with the API on the web since Django Rest Framework offers a pretty intuitive and simple interface, or by using tools like Postman, or `curl`.

## Authentication Flow

1. A user visits the login page.
2. The user is redirected to the Okta login portal for authentication.
3. Upon successful authentication, the user is redirected back to the application.
4. The user is automatically registered as a customer if they don't already exist.
5. The user can now place orders.

## SMS Notifications

When a new order is placed, an SMS notification is sent to the customer’s phone number using **Africa’s Talking SMS Gateway**. This feature uses the Africa’s Talking sandbox in development mode.

## Running Tests

To run tests, use the following command:
```bash
python manage.py test
```

You can also configure the project to run tests within Docker or your CI/CD pipeline.

---
