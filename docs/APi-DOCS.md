# HubSpot Deals ETL Service – API Documentation

## 📋 Overview

The **hubspot_deals ETL service** provides REST APIs to extract Deals data from
the HubSpot CRM platform using a DLT-based extraction pipeline.

The service allows:
- Starting a HubSpot Deals extraction
- Monitoring extraction status
- Performing health checks

---

## 🔐 Authentication

All extraction requests require authentication using a **HubSpot Private App
Access Token**.

### Required Header
Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json

yaml
Copy code

---

## 🌐 Base URLs

### Development
http://localhost:5200

shell
Copy code

### API Documentation
http://localhost:5200/docs

yaml
Copy code

---

## 📊 Common Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully"
}
Error Response
json
Copy code
{
  "status": "error",
  "message": "Description of the error"
}
🔌 API Endpoints
1. Health Check
GET /health

Checks whether the service is running and healthy.

Response
json
Copy code
{
  "status": "healthy",
  "service": "hubspot_deals",
  "timestamp": "2025-12-18T18:00:00Z"
}
Status Codes
200 – Service is healthy

503 – Service unavailable

2. Start Deals Extraction
POST /extract/deals

Starts a new HubSpot Deals extraction job.

Request Body
json
Copy code
{
  "scan_id": "hubspot-deals-scan-001",
  "tenant_id": "tenant_123"
}
Response
json
Copy code
{
  "scan_id": "hubspot-deals-scan-001",
  "status": "started",
  "message": "Deals extraction started successfully"
}
Status Codes
202 – Extraction started

400 – Invalid request

401 – Unauthorized

409 – Extraction already running

500 – Internal server error

3. Get Extraction Status
GET /extract/status/{scan_id}

Returns the status of a previously started extraction job.

Path Parameters
Parameter	Type	Description
scan_id	string	Unique extraction identifier

Response
json
Copy code
{
  "scan_id": "hubspot-deals-scan-001",
  "status": "completed",
  "records_extracted": 5,
  "started_at": "2025-12-18T17:30:00Z",
  "completed_at": "2025-12-18T17:31:12Z",
  "error_message": null
}
Status Values
pending

running

completed

failed

⚠️ Error Handling
Error Response Format
json
Copy code
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "HubSpot API rate limit exceeded"
}
Common Errors
HTTP Code	Reason
400	Invalid request payload
401	Invalid or missing access token
429	HubSpot rate limit exceeded
500	Internal server error

📚 Example Requests
Start Extraction
bash
Copy code
curl -X POST http://localhost:5200/extract/deals \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_id": "hubspot-test-001",
    "tenant_id": "tenant_abc"
  }'
Check Extraction Status
bash
Copy code
curl http://localhost:5200/extract/status/hubspot-test-001
⚡ Rate Limiting
HubSpot API limit: 150 requests per 10 seconds

The service applies retry logic with backoff when rate limits are reached

🧾 Changelog
v1.0.0
Initial version of HubSpot Deals ETL API

Supports deal extraction and status tracking

yaml
Copy code

---