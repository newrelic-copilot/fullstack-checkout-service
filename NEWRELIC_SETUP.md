# New Relic Monitoring Setup Guide

This document describes how to configure and use New Relic monitoring for the fullstack-checkout-service application.

## Overview

The application is instrumented with New Relic APM (Application Performance Monitoring) to provide:
- **Application Performance Monitoring**: Track response times, throughput, and errors
- **Distributed Tracing**: Follow requests through your distributed system
- **Custom Business Metrics**: Track order completions, revenue, and customer behavior
- **Error Tracking**: Automatic capture and reporting of exceptions
- **Real User Monitoring**: Browser-side performance tracking (when enabled)

## Prerequisites

- New Relic account (sign up at https://newrelic.com/)
- New Relic License Key (available from your New Relic account settings)

## Installation

The New Relic Python agent is already included in the requirements.txt file:

```bash
pip install -r requirements.txt
```

## Configuration

### Option 1: Using Configuration File (Recommended)

The repository includes a `newrelic.ini` configuration file. Set the following environment variables:

```bash
export NEW_RELIC_LICENSE_KEY="your_license_key_here"
export NEW_RELIC_APP_NAME="Fullstack Checkout Service"
export NEW_RELIC_ENVIRONMENT="production"  # or "development", "staging", "test"
```

Then run the application normally:

```bash
python main.py
```

### Option 2: Using Environment Variables Only

If you prefer to configure entirely via environment variables (e.g., in Docker or cloud environments):

```bash
export NEW_RELIC_LICENSE_KEY="your_license_key_here"
export NEW_RELIC_APP_NAME="Fullstack Checkout Service"
export NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
export NEW_RELIC_LOG_LEVEL=info
```

The agent will initialize with these settings even without the configuration file.

### Option 3: Running with newrelic-admin

For maximum compatibility and instrumentation coverage:

```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python main.py
```

Or with uvicorn:

```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEW_RELIC_LICENSE_KEY` | Your New Relic license key | None | Yes |
| `NEW_RELIC_APP_NAME` | Application name in New Relic UI | None | Yes |
| `NEW_RELIC_ENVIRONMENT` | Environment (development/test/staging/production) | development | No |
| `NEW_RELIC_CONFIG_FILE` | Path to newrelic.ini file | newrelic.ini | No |
| `NEW_RELIC_LOG_LEVEL` | Logging level (debug/info/warning/error) | info | No |
| `NEW_RELIC_DISTRIBUTED_TRACING_ENABLED` | Enable distributed tracing | true | No |

## Custom Instrumentation

The application includes custom instrumentation for business-critical operations:

### Custom Attributes

The checkout endpoint automatically adds these attributes to transactions:
- `customer_email`: Customer's email address
- `payment_method`: Payment method used
- `item_count`: Number of items in the order
- `order_id`: Unique order identifier
- `order_total`: Total order amount

### Custom Events

The application records custom events for important business activities:

#### OrderCompleted Event
Recorded when a checkout is successfully processed:
```python
{
    'orderId': 'uuid',
    'totalAmount': 123.45,
    'itemCount': 3,
    'customerEmail': 'customer@example.com',
    'paymentMethod': 'credit_card'
}
```

You can query these events in New Relic using NRQL:
```sql
SELECT count(*) FROM OrderCompleted SINCE 1 day ago
SELECT sum(totalAmount) FROM OrderCompleted SINCE 1 day ago
SELECT average(totalAmount) FROM OrderCompleted FACET paymentMethod SINCE 1 week ago
```

## Verification

After starting the application with New Relic configured:

1. **Check Application Startup Logs**: Look for New Relic agent initialization messages
2. **Visit New Relic APM**: Go to https://one.newrelic.com and find your application
3. **Generate Test Traffic**: Make some API calls to generate data
4. **View Data**: Within 1-2 minutes, you should see data appearing in New Relic

### Test the Integration

```bash
# Test the checkout endpoint
curl -X POST http://localhost:8000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product_id": 1, "quantity": 2}],
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "shipping_address": "123 Test St",
    "payment_method": "credit_card"
  }'
```

## Monitoring Features

### Automatic Instrumentation

The New Relic Python agent automatically instruments:
- **FastAPI**: All endpoint calls, including timing and parameters
- **HTTP Requests**: External HTTP calls (if any)
- **Database Queries**: SQL queries (if database is added)
- **Exceptions**: Unhandled exceptions and error traces

### Distributed Tracing

Distributed tracing is enabled by default. This allows you to:
- Track requests across microservices
- Identify bottlenecks in distributed systems
- Understand service dependencies

### Error Tracking

All exceptions are automatically captured and sent to New Relic with:
- Full stack traces
- Request parameters (configurable)
- Custom attributes
- Environment context

## Dashboard Queries

### Useful NRQL Queries

**Average Response Time by Endpoint:**
```sql
SELECT average(duration) FROM Transaction 
WHERE appName = 'Fullstack Checkout Service' 
FACET name 
SINCE 1 hour ago
```

**Total Revenue (from OrderCompleted events):**
```sql
SELECT sum(totalAmount) as 'Total Revenue' 
FROM OrderCompleted 
SINCE 1 day ago
```

**Error Rate:**
```sql
SELECT percentage(count(*), WHERE error IS true) 
FROM Transaction 
SINCE 1 hour ago
```

**Orders by Payment Method:**
```sql
SELECT count(*) FROM OrderCompleted 
FACET paymentMethod 
SINCE 1 day ago
```

**Average Order Value:**
```sql
SELECT average(totalAmount) as 'AOV' 
FROM OrderCompleted 
SINCE 1 week ago
```

## Alerting

Consider setting up alerts for:

1. **High Error Rate**: Alert when error rate exceeds 5%
   ```sql
   SELECT percentage(count(*), WHERE error IS true) FROM Transaction
   ```

2. **Slow Transactions**: Alert when average response time exceeds threshold
   ```sql
   SELECT average(duration) FROM Transaction WHERE name = 'WebTransaction/Function/checkout'
   ```

3. **Low Order Volume**: Alert when order count drops significantly
   ```sql
   SELECT count(*) FROM OrderCompleted
   ```

## Troubleshooting

### Agent Not Reporting Data

1. **Check License Key**: Ensure `NEW_RELIC_LICENSE_KEY` is set correctly
2. **Check Network**: Ensure the application can reach `collector.newrelic.com`
3. **Check Logs**: Look for error messages in application logs
4. **Verify Initialization**: Check that `newrelic.agent.initialize()` is called before other imports

### Missing Custom Events

- Ensure the transaction is being tracked
- Check that custom events are being recorded without exceptions
- Verify events appear in New Relic Insights within a few minutes

### Performance Impact

The New Relic agent has minimal performance impact:
- Typical overhead: < 3% CPU
- Memory overhead: 10-20 MB
- Can be disabled in development by setting `monitor_mode = false`

## Development Mode

In development, you may want to disable New Relic to avoid sending test data:

```bash
export NEW_RELIC_ENVIRONMENT="development"
```

The `newrelic.ini` file is configured to disable monitoring in development mode.

## Production Best Practices

1. **Use Configuration Management**: Store license key in secrets manager
2. **Enable High Security Mode**: If handling sensitive data
3. **Configure Log Files**: Set appropriate log file location and rotation
4. **Monitor Agent Health**: Set up alerts for agent connectivity issues
5. **Regular Updates**: Keep the New Relic agent updated
6. **Tag Deployments**: Use deployment markers to track changes

## Adding Deployment Markers

Track deployments in New Relic:

```bash
curl -X POST 'https://api.newrelic.com/v2/applications/{APP_ID}/deployments.json' \
  -H 'Api-Key:YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "deployment": {
      "revision": "1.2.3",
      "changelog": "Added New Relic monitoring",
      "description": "Release 1.2.3",
      "user": "deploy_user"
    }
  }'
```

## Additional Resources

- [New Relic Python Agent Documentation](https://docs.newrelic.com/docs/apm/agents/python-agent/)
- [Python Agent API](https://docs.newrelic.com/docs/apm/agents/python-agent/python-agent-api/)
- [Custom Instrumentation](https://docs.newrelic.com/docs/apm/agents/python-agent/custom-instrumentation/python-custom-instrumentation/)
- [NRQL Query Language](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)
- [New Relic Best Practices](https://docs.newrelic.com/docs/new-relic-solutions/best-practices-guides/)

## Support

For issues or questions:
- New Relic Support: https://support.newrelic.com/
- New Relic Community: https://discuss.newrelic.com/
- Documentation: https://docs.newrelic.com/
