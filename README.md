# E-commerce API

This project is a robust and scalable E-commerce API built using Python, Django, and Django REST Framework (DRF). It provides a comprehensive backend solution for online stores, offering a wide range of functionalities from user management to order processing.

## Key Features

*   **User Authentication:** Secure user registration and login using JSON Web Tokens (JWT).
*   **Product Management:** Full CRUD (Create, Read, Update, Delete) operations for products. Administrators can manage product details, including name, description, price, and inventory. Regular users have read-only access.
*   **Shopping Cart:** Persistent shopping cart functionality allowing users to add, view, update, and remove items.
*   **Order Processing:** Streamlined checkout process, order creation, and order history tracking for users.
*   **Product Ratings & Reviews:** (If `ratings` app is fully implemented and exposed via API) Users can rate and review products.
*   **Admin Interface:** Django Admin integration for easy management of all data models.
*   **Filtering and Searching:** Advanced filtering and searching capabilities for products.
*   **Pagination:** Efficient pagination for lists of resources.
*   **Permissions:** Role-based access control for different API endpoints.


## Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   PostgreSQL

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory_name>
    ```

2.  **Navigate to the project directory:**
    The main project files (like `manage.py`) are located in the `ecommerce` subdirectory.
    ```bash
    cd ecommerce
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure environment variables:**
    Copy the example environment file and update it with your local settings.
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your actual database credentials, secret key, etc.
    ```
    # .env
    SECRET_KEY=your_actual_strong_secret_key
    DEBUG=True # Set to False in production

    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost # Or your DB host
    # DB_PORT=5432 # Uncomment and set if not default
    ```

6.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser (optional but recommended):**
    This will allow you to access the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up a username, email, and password.

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API should now be accessible at `http://127.0.0.1:8000/`.


## API Endpoints

The API base URL is `/api/v1/`. All endpoints require JWT authentication unless otherwise specified. Send your JWT token in the `Authorization` header as `Bearer <token>`.

### Accounts (`/api/v1/accounts/`)

*   **`POST /api/v1/accounts/register/`**: Register a new user.
    *   Payload: `{ "username": "newuser", "email": "user@example.com", "password": "password123", "phone_number": "1234567890" }`
*   **`POST /api/v1/accounts/login/`**: Obtain JWT by providing username and password.
    *   Payload: `{ "username": "testuser", "password": "password123" }`
    *   Response: `{ "access": "your_access_token", "refresh": "your_refresh_token" }`
*   **`POST /api/v1/accounts/token/refresh/`**: Refresh an expired access token.
    *   Payload: `{ "refresh": "your_refresh_token" }`
    *   Response: `{ "access": "new_access_token" }`
*   **`GET, PUT, PATCH /api/v1/accounts/profile/`**: Manage user profile (View, Update).

### Products (`/api/v1/products/`)

Managed by a `ModelViewSet`. Supports searching, filtering, and ordering.
*   **`GET /api/v1/products/`**: List all available products. Publicly accessible.
*   **`POST /api/v1/products/`**: Create a new product. (Admin access required)
*   **`GET /api/v1/products/{product_id}/`**: Retrieve details of a specific product. Publicly accessible.
*   **`PUT /api/v1/products/{product_id}/`**: Update a specific product. (Admin access required)
*   **`PATCH /api/v1/products/{product_id}/`**: Partially update a specific product. (Admin access required)
*   **`DELETE /api/v1/products/{product_id}/`**: Delete a product. (Admin access required)

### Cart (`/api/v1/`)

The cart endpoints are available under `/api/v1/cart/` and addresses under `/api/v1/address/`.

*   **`/api/v1/cart/`**: Manages the user's shopping cart (e.g., add item, view cart, update item, remove item).
    *   Typically: `GET` to view cart, `POST` to add/update items, `DELETE` to remove items or clear cart.
*   **`/api/v1/address/`**: Manages user addresses (CRUD operations).
    *   Typically: `GET` to list addresses, `POST` to create an address, `GET /api/v1/address/{address_id}/` to retrieve, `PUT/PATCH` to update, `DELETE` to remove.

### Orders (`/api/v1/order/`)

*   **`POST /api/v1/order/checkout/`**: Create a new order from the items in the user's cart.
*   **`GET /api/v1/order/orders/`**: List orders for the authenticated user (or all orders for admin).
*   **`GET /api/v1/order/orders/{order_id}/`**: Retrieve details of a specific order.
*   **`GET /api/v1/order/order-items/`**: List all items across all orders (potentially admin) or for a specific order if filtered.
*   **`GET, PUT, PATCH /api/v1/order/order-items/{item_id}/`**: View or update a specific order item (likely admin functionality for updates).

**Note:** Specific request/response payloads for Cart and Order item operations might vary. Refer to the serializers and viewset actions in `cart/views.py` and `orders/views.py` for exact details. Common features like pagination are enabled by default for list views.


## Authentication

This API uses JSON Web Tokens (JWT) for authentication. Most endpoints (unless specified as public) require an access token to be included in the `Authorization` header of your requests.

The token should be prefixed with `Bearer `:

```
Authorization: Bearer <your_access_token>
```

### Token Management

*   **Obtain Token:** Send a `POST` request with your username and password to `/api/v1/accounts/login/`.
*   **Refresh Token:** If your access token expires, send a `POST` request with your refresh token to `/api/v1/accounts/token/refresh/` to get a new access token.


## Project Structure

The project is organized into several Django apps, each responsible for a specific domain of functionality:

*   **`ecommerce/`**: The main project directory containing `settings.py`, root `urls.py`, and `wsgi.py`.
    *   **`accounts/`**: Manages user authentication (registration, login, token management) and user profiles.
    *   **`products/`**: Handles product catalog, product details, and inventory.
    *   **`cart/`**: Implements shopping cart functionality and user address management.
    *   **`orders/`**: Manages order creation, checkout process, and order history.
    *   **`ratings/`**: (Potential Feature) Designed for product ratings and reviews. Its API endpoints may not be fully exposed yet.
*   **`manage.py`**: Django's command-line utility for administrative tasks.
*   **`requirements.txt`**: Lists project dependencies.
*   **`.env.example`**: Example file for environment variable configuration.

Each app typically contains:
*   `models.py`: Database models.
*   `views.py`: API view logic (often using DRF ViewSets).
*   `serializers.py`: Data serialization for API request/response.
*   `urls.py`: URL routing for the app.
*   `admin.py`: Configuration for Django admin interface.
*   `tests.py`: Application-specific tests.
