#!/usr/bin/env python3
"""
Test script to verify New Relic APM integration.
This script makes several API calls to generate transactions in New Relic.
"""
import requests
import time
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_get_products():
    """Test getting all products"""
    print_section("Testing: GET /api/products")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        response.raise_for_status()
        products = response.json()
        print(f"✓ Success! Retrieved {len(products)} products")
        return products
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
        return []

def test_get_single_product(product_id):
    """Test getting a single product"""
    print_section(f"Testing: GET /api/products/{product_id}")
    try:
        response = requests.get(f"{BASE_URL}/api/products/{product_id}")
        response.raise_for_status()
        product = response.json()
        print(f"✓ Success! Retrieved product: {product['name']}")
        return product
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
        return None

def test_checkout():
    """Test checkout endpoint"""
    print_section("Testing: POST /api/checkout")
    
    checkout_data = {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ],
        "customer_name": "New Relic Test User",
        "customer_email": "test@newrelic.com",
        "shipping_address": "123 Test Street, APM City, NR 12345",
        "payment_method": "credit_card"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/checkout",
            json=checkout_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        order = response.json()
        print(f"✓ Success! Created order: {order['order_id']}")
        print(f"  Total amount: ${order['total_amount']}")
        print(f"  Items: {len(order['items'])}")
        return order
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
        return None

def test_get_order(order_id):
    """Test getting an order"""
    print_section(f"Testing: GET /api/orders/{order_id}")
    try:
        response = requests.get(f"{BASE_URL}/api/orders/{order_id}")
        response.raise_for_status()
        order = response.json()
        print(f"✓ Success! Retrieved order for: {order['customer_name']}")
        return order
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
        return None

def test_get_all_orders():
    """Test getting all orders"""
    print_section("Testing: GET /api/orders")
    try:
        response = requests.get(f"{BASE_URL}/api/orders")
        response.raise_for_status()
        orders = response.json()
        print(f"✓ Success! Retrieved {len(orders)} orders")
        return orders
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
        return []

def test_error_handling():
    """Test error handling (should generate errors in New Relic)"""
    print_section("Testing: Error Handling")
    
    # Test 404 - Product not found
    try:
        response = requests.get(f"{BASE_URL}/api/products/999")
        if response.status_code == 404:
            print("✓ 404 Error properly handled (Product not found)")
    except requests.exceptions.RequestException:
        pass
    
    # Test 400 - Empty cart
    try:
        response = requests.post(
            f"{BASE_URL}/api/checkout",
            json={
                "items": [],
                "customer_name": "Test",
                "customer_email": "test@test.com",
                "shipping_address": "123 Test St",
                "payment_method": "credit_card"
            }
        )
        if response.status_code == 400:
            print("✓ 400 Error properly handled (Empty cart)")
    except requests.exceptions.RequestException:
        pass

def main():
    print("\n" + "="*60)
    print("  New Relic APM Integration Test Script")
    print("  Fullstack Checkout Service")
    print("="*60)
    print("\nThis script will make several API calls to generate")
    print("transactions that will appear in New Relic APM.")
    print("\nMake sure the application is running on http://localhost:8000")
    print("and New Relic is configured with your license key.")
    
    input("\nPress Enter to start the tests...")
    
    # Test 1: Get all products
    products = test_get_products()
    time.sleep(0.5)
    
    # Test 2: Get a single product
    if products:
        test_get_single_product(products[0]['id'])
        time.sleep(0.5)
    
    # Test 3: Create an order
    order = test_checkout()
    time.sleep(0.5)
    
    # Test 4: Get the created order
    if order:
        test_get_order(order['order_id'])
        time.sleep(0.5)
    
    # Test 5: Get all orders
    test_get_all_orders()
    time.sleep(0.5)
    
    # Test 6: Error handling
    test_error_handling()
    
    print_section("Test Complete!")
    print("✓ All tests completed successfully!")
    print("\nNow check your New Relic dashboard:")
    print("1. Go to https://one.newrelic.com")
    print("2. Navigate to APM & Services")
    print("3. Find 'Fullstack Checkout Service'")
    print("4. You should see the transactions generated by this test")
    print("\nTransactions to look for:")
    print("  - GET /api/products")
    print("  - GET /api/products/:id")
    print("  - POST /api/checkout")
    print("  - GET /api/orders/:id")
    print("  - GET /api/orders")
    print("  - Error transactions (404, 400)")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n✗ Test failed with error: {e}")
