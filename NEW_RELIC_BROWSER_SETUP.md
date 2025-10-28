# New Relic Browser Monitoring Setup Guide

## Overview

This document describes the New Relic Browser monitoring implementation for the fullstack-checkout-service application. The implementation provides Real User Monitoring (RUM), custom event tracking, error monitoring, and performance insights for the e-commerce frontend.

## Features Implemented

### 1. Real User Monitoring (RUM)
- Page load performance tracking
- AJAX request monitoring
- Distributed tracing enabled
- User session tracking

### 2. Custom Events Tracking
The following custom events are tracked throughout the user journey:

- **PageView**: Tracks when a user visits the shop page
  - Attributes: `pageName`, `pageUrl`

- **ProductsLoaded**: Tracks successful product catalog loading
  - Attributes: `productCount`, `loadTime`

- **AddToCart**: Tracks when a user adds an item to their cart
  - Attributes: `productId`, `productName`, `productPrice`, `quantity`, `cartValue`, `cartItemCount`

- **CartQuantityUpdate**: Tracks when a user changes item quantities
  - Attributes: `productId`, `productName`, `oldQuantity`, `newQuantity`, `cartValue`

- **RemoveFromCart**: Tracks when a user removes an item from cart
  - Attributes: `productId`, `productName`, `quantity`, `cartValue`, `cartItemCount`

- **CheckoutInitiated**: Tracks when a user begins the checkout process
  - Attributes: `cartValue`, `itemCount`, `productIds`

- **OrderCompleted**: Tracks successful order completion
  - Attributes: `orderId`, `orderValue`, `itemCount`, `paymentMethod`, `checkoutTime`, `customerEmail`

### 3. Custom Attributes
Session-level and transaction-level attributes:

- `userSessionId`: Unique session identifier (persisted in sessionStorage)
- `pageType`: Current page type (e.g., "shop")
- `cartValue`: Current cart total value
- `lastOrderId`: Most recent order ID
- `lastOrderValue`: Most recent order value

### 4. Error Tracking
Comprehensive error monitoring including:

- **ProductLoadError**: Errors when loading the product catalog
- **CheckoutError**: Errors during the checkout process
- **UncaughtError**: Global JavaScript errors
- **UnhandledPromiseRejection**: Unhandled promise rejections

All errors include contextual attributes for debugging.

### 5. Performance Monitoring
- API request timing (product loading, checkout)
- Checkout flow performance metrics
- Page load and interaction timing

## Configuration Steps

### 1. Update Browser Agent Configuration

In `static/index.html`, replace the placeholder values:

```javascript
NREUM.info = {
    beacon: "bam.nr-data.net",
    errorBeacon: "bam.nr-data.net",
    licenseKey: "NRJS-YOUR-LICENSE-KEY-HERE",  // ← Replace this
    applicationID: "YOUR-APP-ID-HERE",          // ← Replace this
    sa: 1,
    agent: ""
};
```

### 2. Add Browser Agent Loader Script

After updating the configuration, add the New Relic Browser agent loader script. There are two options:

#### Option A: SPA Agent (Recommended for this app)
Add this script tag after the NREUM configuration block:

```html
<script type="text/javascript" src="https://js-agent.newrelic.com/nr-loader-spa-current.min.js"></script>
```

**Security Note**: For production environments, consider adding Subresource Integrity (SRI) to verify the script hasn't been tampered with. New Relic provides SRI hashes in their UI when you generate the Browser agent snippet. Example:

```html
<script type="text/javascript" 
        src="https://js-agent.newrelic.com/nr-loader-spa-current.min.js"
        integrity="sha384-HASH-VALUE-HERE"
        crossorigin="anonymous"></script>
```

#### Option B: Copy/Paste from New Relic UI
1. Log in to New Relic One
2. Go to Browser → Select your application (or create a new one)
3. Go to Application Settings → Copy/paste JavaScript code
4. Copy the full script snippet and replace the existing NREUM configuration in `index.html`

### 3. Obtain License Key and Application ID

1. Log in to [New Relic](https://one.newrelic.com/)
2. Navigate to Browser → Add data
3. Select "Copy/paste JavaScript code" deployment option
4. Create a new application or select an existing one
5. Copy the `licenseKey` and `applicationID` from the generated script
6. Update the values in `static/index.html`

## Testing the Implementation

### Without New Relic Agent (Mock Mode)
The current implementation includes mock logging when the New Relic agent is not loaded. You can test the implementation by:

1. Start the application: `python main.py`
2. Open browser console and navigate to `http://localhost:8000/shop`
3. Look for `[New Relic Mock]` log messages in the console
4. Perform actions: add to cart, checkout, complete order
5. Verify events are logged with correct attributes

### With New Relic Agent (Production)
After configuring the real agent:

1. Complete steps 1-3 in Configuration Steps above
2. Start the application
3. Navigate to the shop page
4. Perform user actions (browse, add to cart, checkout)
5. In New Relic One:
   - Go to Browser → Your Application
   - Check "Page views" for RUM data
   - Check "Session traces" for user sessions
   - Check "JavaScript errors" for any errors
   - Check "AJAX requests" for API call performance
   - Query custom events using NRQL:
     ```sql
     SELECT * FROM PageAction WHERE actionName = 'AddToCart' SINCE 1 hour ago
     SELECT * FROM PageAction WHERE actionName = 'OrderCompleted' SINCE 1 day ago
     SELECT count(*) FROM PageAction FACET actionName SINCE 1 hour ago
     ```

## Monitored User Journeys

### 1. Product Browsing
- Page load → ProductsLoaded event
- Product images and catalog data

### 2. Shopping Cart Management
- Add to cart → AddToCart event
- Quantity updates → CartQuantityUpdate event
- Remove items → RemoveFromCart event
- Real-time cart value tracking

### 3. Checkout Process
- Checkout initiation → CheckoutInitiated event
- Form submission and validation
- Order completion → OrderCompleted event
- Error tracking for failed checkouts

## NRQL Query Examples

Here are some useful NRQL queries to analyze the tracked data:

### Cart Analytics
```sql
-- Average cart value when items are added
SELECT average(cartValue) FROM PageAction 
WHERE actionName = 'AddToCart' SINCE 1 day ago

-- Most popular products added to cart
SELECT count(*) FROM PageAction 
WHERE actionName = 'AddToCart' 
FACET productName SINCE 7 days ago
```

### Checkout Funnel
```sql
-- Checkout conversion rate
SELECT funnel(
  PageAction WHERE actionName = 'AddToCart',
  PageAction WHERE actionName = 'CheckoutInitiated',
  PageAction WHERE actionName = 'OrderCompleted'
) SINCE 1 day ago

-- Average checkout time
SELECT average(checkoutTime) FROM PageAction 
WHERE actionName = 'OrderCompleted' SINCE 1 day ago
```

### Error Monitoring
```sql
-- JavaScript errors by type
SELECT count(*) FROM JavaScriptError 
FACET errorMessage SINCE 1 day ago

-- Checkout errors
SELECT * FROM PageAction 
WHERE actionName = 'CheckoutError' SINCE 1 day ago
```

### Performance Metrics
```sql
-- Product load performance
SELECT average(loadTime) FROM PageAction 
WHERE actionName = 'ProductsLoaded' SINCE 1 hour ago

-- Orders by payment method
SELECT count(*) FROM PageAction 
WHERE actionName = 'OrderCompleted' 
FACET paymentMethod SINCE 7 days ago
```

## File Modifications

### static/index.html
- Added New Relic Browser agent configuration in `<head>` section
- Configured NREUM object with placeholders for license key and app ID
- Added setup instructions as HTML comments

### static/app.js
- Added New Relic helper functions: `trackNewRelicEvent()`, `setNewRelicAttribute()`, `trackNewRelicError()`
- Enhanced `init()` to set session attributes and track page views
- Added session ID generation and persistence
- Enhanced `loadProducts()` with error tracking and performance monitoring
- Enhanced `addToCart()` with event tracking and cart value updates
- Enhanced `updateQuantity()` with quantity change tracking
- Enhanced `removeFromCart()` with removal event tracking
- Enhanced `showCheckoutForm()` with checkout initiation tracking
- Enhanced `submitCheckout()` with order completion tracking and error handling
- Added global error handlers for uncaught errors and promise rejections
- Added `calculateCartTotal()` helper function

## Browser Support

The New Relic Browser agent supports:
- Chrome (latest and previous version)
- Firefox (latest and previous version)
- Safari (latest and previous version)
- Edge (latest and previous version)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Privacy Considerations

- Session IDs are generated client-side and stored in sessionStorage
- Customer email is only tracked on successful order completion
- No sensitive payment data is tracked (only payment method type)
- All tracking respects browser privacy settings via `privacy: { cookies_enabled: true }`

## Next Steps

1. **Configure New Relic Account**: Set up your New Relic Browser application
2. **Update Configuration**: Replace placeholder values with your actual license key and app ID
3. **Add Loader Script**: Include the Browser agent loader script
4. **Test in Staging**: Verify all events are tracked correctly before production deployment
5. **Set Up Alerts**: Create alerts for error rates, performance degradation, and conversion drops
6. **Create Dashboards**: Build custom dashboards to visualize your e-commerce metrics

## Support

For issues or questions about New Relic Browser monitoring:
- New Relic Documentation: https://docs.newrelic.com/docs/browser/
- New Relic Support: https://support.newrelic.com/
- Application-specific questions: Contact your development team

## License

This implementation follows the application's existing license terms.
