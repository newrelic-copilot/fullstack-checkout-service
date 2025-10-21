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

3. Configure New Relic monitoring (optional):

Copy the `.env.example` file to `.env` and add your New Relic license key:
```bash
cp .env.example .env
```

Edit `.env` and set your New Relic license key:
```bash
NEW_RELIC_LICENSE_KEY=your_license_key_here
NEW_RELIC_APP_NAME=Fullstack Checkout Service
```

You can obtain a New Relic license key from: https://one.newrelic.com/launcher/api-keys-ui.api-keys-launcher

Load environment variables from `.env` file before running the application:
```bash
export $(cat .env | xargs)
```

Alternatively, you can run the application with New Relic admin wrapper:
```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python main.py
```

For more information about New Relic configuration, see the [New Relic Python Agent documentation](https://docs.newrelic.com/docs/apm/agents/python-agent/getting-started/introduction-new-relic-python/).

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
├── .env.example         # Environment variables template
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
- **New Relic**: Application performance monitoring and observability

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

## New Relic Monitoring

This application is instrumented with New Relic APM for performance monitoring and observability.

### Features Enabled

- **Application Performance Monitoring (APM)**: Track response times, throughput, and errors
- **Distributed Tracing**: Follow requests across services and components
- **Error Tracking**: Automatic capture and reporting of exceptions
- **Transaction Tracing**: Detailed insights into slow transactions
- **Logs in Context**: Application logs correlated with traces and errors

### Configuration

New Relic can be configured in three ways:

1. **Environment Variables** (recommended for production):
   ```bash
   export NEW_RELIC_LICENSE_KEY=your_license_key_here
   export NEW_RELIC_APP_NAME="Fullstack Checkout Service"
   python main.py
   ```

2. **Configuration File** (`newrelic.ini`):
   The application includes a pre-configured `newrelic.ini` file. Update the `license_key` field with your New Relic license key.

3. **Using newrelic-admin wrapper**:
   ```bash
   newrelic-admin run-program python main.py
   ```

### Monitoring Dashboard

Once configured, you can view your application's performance metrics at:
- https://one.newrelic.com

### Custom Instrumentation

To add custom instrumentation to specific functions, you can use the New Relic Python agent decorators:

```python
import newrelic.agent

@newrelic.agent.function_trace()
def my_custom_function():
    # Your code here
    pass
```

For more details, see the [New Relic Python Agent documentation](https://docs.newrelic.com/docs/apm/agents/python-agent/).

## License

This is a demo application for educational purposes.

## Author

Built with ❤️ using FastAPI