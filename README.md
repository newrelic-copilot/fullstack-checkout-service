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
- **New Relic APM Monitoring** with distributed tracing and logs in context

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

3. Configure New Relic (Optional but Recommended):

To enable New Relic APM monitoring, you need to configure your New Relic license key:

a. Copy the example environment file:
```bash
cp .env.example .env
```

b. Edit `.env` and add your New Relic license key:
```bash
NEW_RELIC_LICENSE_KEY=your_license_key_here
```

You can get your license key from [New Relic API Keys](https://one.newrelic.com/api-keys).

c. (Optional) Customize the application name and environment:
```bash
NEW_RELIC_APP_NAME=Fullstack Checkout Service
NEW_RELIC_ENVIRONMENT=development
```

If you don't configure New Relic, the application will run normally without monitoring.

## Running the Application

### Option 1: Run with New Relic monitoring (Recommended)

If you have configured New Relic in the `.env` file:

```bash
python main.py
```

The application will automatically initialize New Relic APM and start monitoring your application.

### Option 2: Run without New Relic

If you haven't configured New Relic, the application will still run normally:

```bash
python main.py
```

### Option 3: Use uvicorn directly
```bash
python main.py
```

### Option 3: Use uvicorn directly

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note:** When using uvicorn directly, make sure your environment variables are set first.
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
├── static/              # Frontend files
│   ├── index.html      # Main HTML page
│   ├── style.css       # Styles
│   └── app.js          # JavaScript logic
└── README.md           # Documentation
```

## Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **New Relic**: Application Performance Monitoring (APM) with distributed tracing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: For making HTTP requests

## New Relic Monitoring

This application includes New Relic APM integration for comprehensive monitoring:

### Features
- **Application Performance Monitoring (APM)**: Track response times, throughput, and errors
- **Distributed Tracing**: Follow requests across your entire stack
- **Logs in Context**: Automatically correlate logs with transactions
- **Error Analytics**: Detailed error tracking with stack traces
- **Custom Attributes**: Request parameters are captured for deeper insights
- **Transaction Tracing**: Detailed breakdown of slow transactions

### Configuration

The New Relic agent is configured via the `newrelic.ini` file and environment variables:

**Required Environment Variables:**
- `NEW_RELIC_LICENSE_KEY`: Your New Relic license key (required)

**Optional Environment Variables:**
- `NEW_RELIC_APP_NAME`: Application name (default: "Fullstack Checkout Service")
- `NEW_RELIC_ENVIRONMENT`: Environment name (default: "development")
- `NEW_RELIC_CONFIG_FILE`: Path to config file (default: "newrelic.ini")
- `NEW_RELIC_LOG`: Log output destination (default: stdout)
- `NEW_RELIC_LOG_LEVEL`: Logging level (default: "info")

### Viewing Your Data

After starting the application with New Relic configured:

1. Log in to [New Relic One](https://one.newrelic.com)
2. Navigate to **APM & Services**
3. Find your application (e.g., "Fullstack Checkout Service")
4. Explore:
   - **Summary**: Overview of performance metrics
   - **Transactions**: Response times for each endpoint
   - **Errors**: Error rates and details
   - **Distributed tracing**: Request flows
   - **Logs**: Application logs in context

### Testing the Integration

A test script is provided to generate sample transactions in New Relic:

```bash
# Make sure the application is running first
python main.py

# In another terminal, run the test script
python test_newrelic.py
```

The test script will:
- Make API calls to all endpoints
- Generate successful transactions
- Trigger error conditions (404, 400)
- Display results in the console

After running the test, check your New Relic dashboard to see the captured transactions.

### Monitored Endpoints

All API endpoints are automatically instrumented:
- `GET /api/products` - Product catalog
- `GET /api/products/{product_id}` - Single product details
- `POST /api/checkout` - Order processing
- `GET /api/orders` - All orders
- `GET /api/orders/{order_id}` - Order details

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