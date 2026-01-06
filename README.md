# Fullstack Checkout Service

A full-stack checkout service application built with Python FastAPI backend and vanilla JavaScript frontend. This demo application provides basic e-commerce functionality including product catalog, shopping cart, and checkout flow.

## Features

### Backend (FastAPI)
- RESTful API with automatic interactive documentation
- Product catalog management
- Shopping cart functionality
- Order processing and management
- In-memory data storage with demo products
- CORS enabled for frontend integration
- **New Relic APM integration** for performance monitoring and distributed tracing

### Frontend (HTML/CSS/JavaScript)
- Responsive product catalog grid
- Interactive shopping cart with quantity management
- Checkout form with customer details
- Order confirmation display
- Modern UI with gradient themes
- Mobile-friendly design

## Demo Products

The application comes with 8 pre-loaded demo products:
1. Wireless Headphones - $99.99
2. Smart Watch - $199.99
3. Laptop Stand - $49.99
4. Mechanical Keyboard - $129.99
5. Wireless Mouse - $39.99
6. USB-C Hub - $59.99
7. Phone Case - $19.99
8. Portable Charger - $34.99

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- New Relic account and license key (for monitoring features)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/shivang10/fullstack-checkout-service.git
cd fullstack-checkout-service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure New Relic (Optional but recommended):
   
   Create a `.env` file or set environment variables:
   ```bash
   export NEW_RELIC_LICENSE_KEY="your_license_key_here"
   export NEW_RELIC_APP_NAME="fullstack-checkout-service"
   export NEW_RELIC_ENVIRONMENT="development"
   ```
   
   You can obtain your New Relic license key from [New Relic API Keys](https://one.newrelic.com/launcher/api-keys-ui.api-keys-launcher).
   
   See `.env.example` for reference.

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **Frontend**: http://localhost:8000/shop
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{product_id}` - Get a specific product

### Checkout
- `POST /api/checkout` - Process checkout and create an order
  - Request body:
    ```json
    {
      "items": [
        {"product_id": 1, "quantity": 2}
      ],
      "customer_name": "John Doe",
      "customer_email": "john@example.com",
      "shipping_address": "123 Main St, City, Country",
      "payment_method": "credit_card"
    }
    ```

### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/{order_id}` - Get a specific order

## Usage

1. **Browse Products**: Visit http://localhost:8000/shop to see the product catalog
2. **Add to Cart**: Click "Add to Cart" on any product
3. **View Cart**: Click the shopping cart icon in the header to view your cart
4. **Manage Quantities**: Use +/- buttons to adjust quantities or remove items
5. **Checkout**: Click "Proceed to Checkout" and fill in your details
6. **Place Order**: Submit the form to complete your purchase
7. **Order Confirmation**: View your order details and confirmation

## Project Structure

```
fullstack-checkout-service/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models for data validation
├── demo_data.py         # Demo product catalog
├── requirements.txt     # Python dependencies
├── newrelic.ini         # New Relic configuration file
├── .env.example         # Example environment variables
├── static/              # Frontend files
│   ├── index.html      # Main HTML page
│   ├── style.css       # Styles
│   └── app.js          # JavaScript logic
└── README.md           # Documentation
```

## New Relic Monitoring

This application is integrated with New Relic APM for comprehensive performance monitoring, error tracking, and distributed tracing.

### Features
- **Application Performance Monitoring (APM)**: Track response times, throughput, and errors
- **Distributed Tracing**: Follow requests across your application
- **Custom Attributes**: Business context including:
  - Order details (order ID, total amount, status)
  - Customer information (email, payment method)
  - Cart metrics (items count)
- **Error Tracking**: Automatic capture and reporting of exceptions
- **Transaction Traces**: Deep dive into slow transactions

### Setup
1. Sign up for a New Relic account at [newrelic.com](https://newrelic.com)
2. Get your license key from [API Keys page](https://one.newrelic.com/launcher/api-keys-ui.api-keys-launcher)
3. Set environment variables:
   ```bash
   export NEW_RELIC_LICENSE_KEY="your_license_key"
   export NEW_RELIC_APP_NAME="fullstack-checkout-service"
   export NEW_RELIC_ENVIRONMENT="production"  # or development, staging
   ```
4. Start the application - monitoring will begin automatically

### Configuration
The New Relic agent is configured via `newrelic.ini` with the following key settings:
- Distributed tracing enabled
- Transaction tracing enabled
- Error collection enabled
- Browser monitoring enabled

You can customize the configuration by editing `newrelic.ini` or setting environment variables. See [New Relic Python Agent Configuration](https://docs.newrelic.com/docs/apm/agents/python-agent/configuration/python-agent-configuration/) for details.

### Viewing Data
After running the application and generating some traffic:
1. Log into [New Relic One](https://one.newrelic.com)
2. Navigate to APM & Services
3. Select your application name
4. Explore dashboards, transactions, errors, and distributed traces

## Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **New Relic Python Agent**: Application performance monitoring

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: For making HTTP requests

## Development

The application uses in-memory storage, so all data is reset when the server restarts. This is intentional for demo purposes.

### API Testing

Use the built-in Swagger UI documentation at http://localhost:8000/docs to test API endpoints interactively.

### Customization

- Modify `demo_data.py` to change or add products
- Update `models.py` to add new fields or validation rules
- Customize the UI by editing files in the `static/` directory

## License

This is a demo application for educational purposes.

## Author

Built with ❤️ using FastAPI