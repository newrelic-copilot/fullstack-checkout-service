// API Base URL
const API_URL = window.location.origin;

// Cart state
let cart = [];
let products = [];

// New Relic helper functions
function trackNewRelicEvent(eventType, attributes = {}) {
    if (window.newrelic && window.newrelic.addPageAction) {
        window.newrelic.addPageAction(eventType, attributes);
    } else {
        console.log('[New Relic Mock]', eventType, attributes);
    }
}

function setNewRelicAttribute(name, value) {
    if (window.newrelic && window.newrelic.setCustomAttribute) {
        window.newrelic.setCustomAttribute(name, value);
    }
}

function trackNewRelicError(error, customAttributes = {}) {
    if (window.newrelic && window.newrelic.noticeError) {
        window.newrelic.noticeError(error, customAttributes);
    } else {
        console.error('[New Relic Mock Error]', error, customAttributes);
    }
}

// Initialize the app
async function init() {
    // Set session-level custom attributes
    setNewRelicAttribute('userSessionId', generateSessionId());
    setNewRelicAttribute('pageType', 'shop');
    
    // Track page view
    trackNewRelicEvent('PageView', {
        pageName: 'Shop',
        pageUrl: window.location.href
    });
    
    await loadProducts();
    updateCartUI();
}

// Generate a simple session ID
function generateSessionId() {
    let sessionId = sessionStorage.getItem('userSessionId');
    if (!sessionId) {
        // Use crypto.randomUUID() if available (modern browsers), otherwise fallback to timestamp-based ID
        if (typeof crypto !== 'undefined' && crypto.randomUUID) {
            sessionId = 'session_' + crypto.randomUUID();
        } else {
            // Fallback for older browsers - just use timestamp
            sessionId = 'session_' + Date.now() + '_' + Date.now().toString(36);
        }
        sessionStorage.setItem('userSessionId', sessionId);
    }
    return sessionId;
}

// Load products from API
async function loadProducts() {
    const startTime = Date.now();
    
    try {
        const response = await fetch(`${API_URL}/api/products`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        products = await response.json();
        displayProducts(products);
        
        // Track successful product load
        trackNewRelicEvent('ProductsLoaded', {
            productCount: products.length,
            loadTime: Date.now() - startTime
        });
    } catch (error) {
        console.error('Error loading products:', error);
        
        // Track error to New Relic
        trackNewRelicError(error, {
            errorType: 'ProductLoadError',
            endpoint: '/api/products'
        });
        
        alert('Failed to load products. Please try again.');
    }
}

// Display products in the grid
function displayProducts(products) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image_url}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description}</div>
                <div class="product-footer">
                    <div>
                        <div class="product-price">$${product.price.toFixed(2)}</div>
                        <div class="product-stock">Stock: ${product.stock}</div>
                    </div>
                </div>
                <button 
                    class="btn btn-add" 
                    onclick="addToCart(${product.id})"
                    ${product.stock === 0 ? 'disabled' : ''}
                >
                    ${product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                </button>
            </div>
        </div>
    `).join('');
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product || product.stock === 0) return;

    const existingItem = cart.find(item => item.product_id === productId);
    
    if (existingItem) {
        if (existingItem.quantity < product.stock) {
            existingItem.quantity++;
        } else {
            alert(`Cannot add more. Only ${product.stock} items available.`);
            return;
        }
    } else {
        cart.push({
            product_id: productId,
            quantity: 1
        });
    }
    
    updateCartUI();
    
    // Calculate cart value
    const cartValue = calculateCartTotal();
    
    // Track add to cart event in New Relic
    trackNewRelicEvent('AddToCart', {
        productId: productId,
        productName: product.name,
        productPrice: product.price,
        quantity: existingItem ? existingItem.quantity : 1,
        cartValue: cartValue,
        cartItemCount: cart.length
    });
    
    // Update custom attribute with current cart value
    setNewRelicAttribute('cartValue', cartValue);
    
    // Show a brief animation
    const cartIcon = document.querySelector('.cart-icon');
    cartIcon.style.animation = 'none';
    setTimeout(() => {
        cartIcon.style.animation = 'bounce 0.5s';
    }, 10);
}

// Helper function to calculate cart total
function calculateCartTotal() {
    return cart.reduce((total, item) => {
        const product = products.find(p => p.id === item.product_id);
        return total + (product ? product.price * item.quantity : 0);
    }, 0);
}

// Update cart quantity
function updateQuantity(productId, delta) {
    const item = cart.find(item => item.product_id === productId);
    if (!item) return;
    
    const product = products.find(p => p.id === productId);
    const newQuantity = item.quantity + delta;
    
    if (newQuantity <= 0) {
        removeFromCart(productId);
    } else if (newQuantity <= product.stock) {
        const oldQuantity = item.quantity;
        item.quantity = newQuantity;
        updateCartUI();
        
        // Track quantity update
        trackNewRelicEvent('CartQuantityUpdate', {
            productId: productId,
            productName: product.name,
            oldQuantity: oldQuantity,
            newQuantity: newQuantity,
            cartValue: calculateCartTotal()
        });
    } else {
        alert(`Cannot add more. Only ${product.stock} items available.`);
    }
}

// Remove item from cart
function removeFromCart(productId) {
    const product = products.find(p => p.id === productId);
    const item = cart.find(item => item.product_id === productId);
    
    cart = cart.filter(item => item.product_id !== productId);
    updateCartUI();
    
    // Track item removal
    if (item && product) {
        trackNewRelicEvent('RemoveFromCart', {
            productId: productId,
            productName: product.name,
            quantity: item.quantity,
            cartValue: calculateCartTotal(),
            cartItemCount: cart.length
        });
    }
}

// Update cart UI
function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    const checkoutBtn = document.getElementById('checkoutBtn');
    
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
        cartTotal.textContent = '$0.00';
        checkoutBtn.disabled = true;
    } else {
        let total = 0;
        cartItems.innerHTML = cart.map(item => {
            const product = products.find(p => p.id === item.product_id);
            const subtotal = product.price * item.quantity;
            total += subtotal;
            
            return `
                <div class="cart-item">
                    <img src="${product.image_url}" alt="${product.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <div class="cart-item-name">${product.name}</div>
                        <div class="cart-item-price">$${product.price.toFixed(2)}</div>
                        <div class="cart-item-quantity">
                            <button class="quantity-btn" onclick="updateQuantity(${product.id}, -1)">-</button>
                            <span>${item.quantity}</span>
                            <button class="quantity-btn" onclick="updateQuantity(${product.id}, 1)">+</button>
                            <button class="quantity-btn" onclick="removeFromCart(${product.id})" style="margin-left: auto;">🗑️</button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        cartTotal.textContent = `$${total.toFixed(2)}`;
        checkoutBtn.disabled = false;
    }
}

// Toggle cart sidebar
function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    sidebar.classList.toggle('active');
}

// Show checkout form
function showCheckoutForm() {
    if (cart.length === 0) {
        alert('Your cart is empty');
        return;
    }
    
    // Track checkout initiation
    trackNewRelicEvent('CheckoutInitiated', {
        cartValue: calculateCartTotal(),
        itemCount: cart.length,
        productIds: cart.map(item => item.product_id).join(',')
    });
    
    document.getElementById('checkoutModal').classList.add('active');
    toggleCart(); // Close cart sidebar
}

// Close checkout form
function closeCheckoutForm() {
    document.getElementById('checkoutModal').classList.remove('active');
}

// Submit checkout
async function submitCheckout(event) {
    event.preventDefault();
    
    const startTime = Date.now();
    const checkoutData = {
        items: cart,
        customer_name: document.getElementById('customerName').value,
        customer_email: document.getElementById('customerEmail').value,
        shipping_address: document.getElementById('shippingAddress').value,
        payment_method: document.getElementById('paymentMethod').value
    };
    
    try {
        const response = await fetch(`${API_URL}/api/checkout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(checkoutData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Checkout failed');
        }
        
        const order = await response.json();
        const checkoutTime = Date.now() - startTime;
        
        // Track successful order completion
        trackNewRelicEvent('OrderCompleted', {
            orderId: order.order_id,
            orderValue: order.total_amount,
            itemCount: order.items.length,
            paymentMethod: order.payment_method,
            checkoutTime: checkoutTime,
            customerEmail: order.customer_email
        });
        
        // Set order attributes
        setNewRelicAttribute('lastOrderId', order.order_id);
        setNewRelicAttribute('lastOrderValue', order.total_amount);
        
        // Clear cart
        cart = [];
        updateCartUI();
        
        // Close checkout form
        closeCheckoutForm();
        
        // Show confirmation
        showOrderConfirmation(order);
        
        // Reload products to update stock
        await loadProducts();
        
    } catch (error) {
        console.error('Checkout error:', error);
        
        // Track checkout error to New Relic
        trackNewRelicError(error, {
            errorType: 'CheckoutError',
            cartValue: calculateCartTotal(),
            itemCount: cart.length,
            paymentMethod: checkoutData.payment_method
        });
        
        alert(`Checkout failed: ${error.message}`);
    }
}

// Show order confirmation
function showOrderConfirmation(order) {
    const modal = document.getElementById('confirmationModal');
    const details = document.getElementById('orderDetails');
    
    details.innerHTML = `
        <div class="order-info">
            <p><strong>Order ID:</strong> ${order.order_id}</p>
            <p><strong>Customer:</strong> ${order.customer_name}</p>
            <p><strong>Email:</strong> ${order.customer_email}</p>
            <p><strong>Shipping Address:</strong> ${order.shipping_address}</p>
            <p><strong>Payment Method:</strong> ${order.payment_method}</p>
            <p><strong>Status:</strong> ${order.status}</p>
        </div>
        <div class="order-items">
            <h3>Order Items:</h3>
            ${order.items.map(item => `
                <div class="order-item">
                    <span>${item.product_name} x ${item.quantity}</span>
                    <span>$${item.subtotal.toFixed(2)}</span>
                </div>
            `).join('')}
        </div>
        <div class="order-total">
            <span>Total Amount:</span>
            <span>$${order.total_amount.toFixed(2)}</span>
        </div>
    `;
    
    modal.classList.add('active');
}

// Close confirmation
function closeConfirmation() {
    document.getElementById('confirmationModal').classList.remove('active');
    document.getElementById('checkoutForm').reset();
}

// Add bounce animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
`;
document.head.appendChild(style);

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);

// Global error handler for uncaught errors
window.addEventListener('error', function(event) {
    trackNewRelicError(event.error || new Error(event.message), {
        errorType: 'UncaughtError',
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
    });
});

// Global handler for unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    trackNewRelicError(new Error(event.reason), {
        errorType: 'UnhandledPromiseRejection',
        reason: String(event.reason)
    });
});
