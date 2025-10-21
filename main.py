import newrelic.agent

# Initialize New Relic agent
# Configuration can be provided via newrelic.ini file or environment variables:
# - NEW_RELIC_CONFIG_FILE: path to newrelic.ini (default: ./newrelic.ini)
# - NEW_RELIC_LICENSE_KEY: your New Relic license key
# - NEW_RELIC_APP_NAME: application name (default: from newrelic.ini)
newrelic.agent.initialize()

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from datetime import datetime
import uuid

from models import Product, CheckoutRequest, Order, OrderItem, OrderStatus
from demo_data import DEMO_PRODUCTS, get_product_by_id

app = FastAPI(
    title="Checkout Service API",
    description="A simple checkout service with product catalog and order management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for orders
orders_db = {}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Checkout Service API", "docs": "/docs"}


@app.get("/api/products", response_model=List[Product])
async def get_products():
    """Get all available products"""
    return DEMO_PRODUCTS


@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


@app.post("/api/checkout", response_model=Order, status_code=status.HTTP_201_CREATED)
async def checkout(checkout_request: CheckoutRequest):
    """Process a checkout request and create an order"""
    
    if not checkout_request.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    order_items = []
    total_amount = 0.0
    
    # Validate items and calculate totals
    for cart_item in checkout_request.items:
        product = get_product_by_id(cart_item.product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {cart_item.product_id} not found"
            )
        
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}. Available: {product.stock}"
            )
        
        subtotal = product.price * cart_item.quantity
        total_amount += subtotal
        
        order_item = OrderItem(
            product_id=product.id,
            product_name=product.name,
            quantity=cart_item.quantity,
            price=product.price,
            subtotal=subtotal
        )
        order_items.append(order_item)
        
        # Update stock (in real app, this would be in a database transaction)
        product.stock -= cart_item.quantity
    
    # Create order
    order_id = str(uuid.uuid4())
    order = Order(
        order_id=order_id,
        customer_name=checkout_request.customer_name,
        customer_email=checkout_request.customer_email,
        shipping_address=checkout_request.shipping_address,
        payment_method=checkout_request.payment_method,
        items=order_items,
        total_amount=round(total_amount, 2),
        status=OrderStatus.COMPLETED,
        created_at=datetime.now()
    )
    
    # Store order
    orders_db[order_id] = order
    
    return order


@app.get("/api/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order details by ID"""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return order


@app.get("/api/orders", response_model=List[Order])
async def get_all_orders():
    """Get all orders"""
    return list(orders_db.values())


# Mount static files for frontend
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/shop")
    async def serve_shop():
        """Serve the shop page"""
        return FileResponse("static/index.html")
except Exception:
    # Static directory doesn't exist yet
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
