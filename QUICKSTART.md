# Quick Start Guide

Get started with the Checkout Service in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 1.5: Configure New Relic (Optional)

For application monitoring with New Relic:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your New Relic license key
# NEW_RELIC_LICENSE_KEY=your_license_key_here
```

Get your license key from [New Relic API Keys](https://one.newrelic.com/api-keys).

**Note:** The application works without New Relic configuration, but you'll miss out on monitoring features.

## Step 2: Start the Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Open the Application

Open your web browser and navigate to:
- **Shop**: http://localhost:8000/shop
- **API Docs**: http://localhost:8000/docs

## What's Included?

### 8 Demo Products
- Wireless Headphones ($99.99)
- Smart Watch ($199.99)
- Laptop Stand ($49.99)
- Mechanical Keyboard ($129.99)
- Wireless Mouse ($39.99)
- USB-C Hub ($59.99)
- Phone Case ($19.99)
- Portable Charger ($34.99)

### Features to Try
1. **Browse Products**: View the catalog on the homepage
2. **Add to Cart**: Click "Add to Cart" on any product
3. **Manage Cart**: Click the cart icon (🛍️) to view and manage items
4. **Checkout**: Fill in your details and place an order
5. **View Order**: See your order confirmation with order ID

## API Endpoints

Test the API directly:

### Get All Products
```bash
curl http://localhost:8000/api/products
```

### Get Single Product
```bash
curl http://localhost:8000/api/products/1
```

### Checkout
```bash
curl -X POST http://localhost:8000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": 1, "quantity": 2}],
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "shipping_address": "123 Main St",
    "payment_method": "credit_card"
  }'
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Visit the interactive API docs at http://localhost:8000/docs
- All data is stored in-memory and resets when you restart the server

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

That's it! Enjoy using the Checkout Service! 🛒
