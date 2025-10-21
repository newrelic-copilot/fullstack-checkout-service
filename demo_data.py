from models import Product

# Demo product catalog
DEMO_PRODUCTS = [
    Product(
        id=1,
        name="Wireless Headphones",
        description="High-quality wireless headphones with noise cancellation",
        price=99.99,
        image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        stock=50
    ),
    Product(
        id=2,
        name="Smart Watch",
        description="Fitness tracking smart watch with heart rate monitor",
        price=199.99,
        image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        stock=30
    ),
    Product(
        id=3,
        name="Laptop Stand",
        description="Ergonomic aluminum laptop stand for better posture",
        price=49.99,
        image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
        stock=100
    ),
    Product(
        id=4,
        name="Mechanical Keyboard",
        description="RGB mechanical keyboard with cherry MX switches",
        price=129.99,
        image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400",
        stock=45
    ),
    Product(
        id=5,
        name="Wireless Mouse",
        description="Ergonomic wireless mouse with precision tracking",
        price=39.99,
        image_url="https://images.unsplash.com/photo-1527814050087-3793815479db?w=400",
        stock=75
    ),
    Product(
        id=6,
        name="USB-C Hub",
        description="7-in-1 USB-C hub with HDMI and card reader",
        price=59.99,
        image_url="https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400",
        stock=60
    ),
    Product(
        id=7,
        name="Phone Case",
        description="Protective phone case with shock absorption",
        price=19.99,
        image_url="https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400",
        stock=200
    ),
    Product(
        id=8,
        name="Portable Charger",
        description="20000mAh portable battery pack with fast charging",
        price=34.99,
        image_url="https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400",
        stock=80
    )
]


def get_product_by_id(product_id: int):
    """Get a product by its ID"""
    for product in DEMO_PRODUCTS:
        if product.id == product_id:
            return product
    return None
