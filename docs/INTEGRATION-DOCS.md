# 📋 HubSpot Deals API Integration Documentation

## Overview

This document describes the integration between the **hubspot_deals ETL service** and the **HubSpot CRM API v3** for extracting **Deals** data.  
The integration is designed for reliable and scalable data extraction using secure authentication, cursor-based pagination, and rate-limit-aware API access.

The extracted Deals data is intended for analytics, reporting, and downstream ETL processing.

---

## Platform Details

- **Platform**: HubSpot CRM
- **API Version**: v3
- **Object Type**: Deals
- **Base URL**:
https://api.hubapi.com

yaml
Copy code

---

## Authentication

HubSpot APIs are accessed using **Private App Access Tokens**.

### Authentication Header

Authorization: Bearer <HUBSPOT_PRIVATE_APP_ACCESS_TOKEN>
Content-Type: application/json

yaml
Copy code

> 🔐 The access token must be stored securely using environment variables and must never be committed to source control.

### Required Scope

- `crm.objects.deals.read`

---

## Primary API Endpoint (Required)

### Get Deals

**Endpoint**
GET /crm/v3/objects/deals

yaml
Copy code

This endpoint is sufficient for complete Deals extraction and provides all required deal properties.

---

## Query Parameters

| Parameter | Type | Description |
|---------|------|-------------|
| `limit` | integer | Number of records per request (maximum 100) |
| `after` | string | Cursor token for pagination |
| `properties` | string | Comma-separated list of deal properties |
| `archived` | boolean | Include archived deals (default: false) |

### Example Request

GET https://api.hubapi.com/crm/v3/objects/deals?limit=100&archived=false
Authorization: Bearer <TOKEN>

yaml
Copy code

---

## Pagination Strategy (Cursor-Based)

HubSpot uses cursor-based pagination.

### Pagination Flow

1. Make an initial request without the `after` parameter
2. Read `paging.next.after` from the response
3. Pass the `after` value in the next request
4. Repeat until the `paging` object is no longer present

### Pagination Example

"paging": {
"next": {
"after": "MjAyNQ",
"link": "https://api.hubapi.com/crm/v3/objects/deals?after=MjAyNQ"
}
}

yaml
Copy code

---

## Sample API Response

{
"results": [
{
"id": "123456789",
"properties": {
"dealname": "Enterprise Software Deal",
"amount": "50000",
"dealstage": "closedwon",
"pipeline": "default",
"closedate": "2025-12-01T00:00:00Z"
},
"createdAt": "2025-11-01T10:15:30Z",
"updatedAt": "2025-12-01T12:00:00Z",
"archived": false
}
]
}

yaml
Copy code

---

## Deal Properties Extracted

The following deal properties are extracted by default:

- `dealname`
- `amount`
- `dealstage`
- `pipeline`
- `closedate`
- `createdate`
- `hs_lastmodifieddate`

Additional properties can be included using the `properties` query parameter if required.

---

## Rate Limiting

HubSpot enforces the following API limits:

- **150 requests per 10 seconds per app**
- Exceeding the limit returns **HTTP 429 – Too Many Requests**

### Rate Limit Handling Strategy

- Respect the `Retry-After` response header
- Apply exponential backoff before retrying
- Log rate-limit events for monitoring and debugging

---

## Error Handling

| HTTP Status | Description | Handling Strategy |
|------------|-------------|------------------|
| 400 | Bad Request | Validate request parameters |
| 401 | Unauthorized | Verify access token |
| 403 | Forbidden | Ensure required API scopes |
| 429 | Rate Limited | Retry after delay |
| 500 | Server Error | Retry with backoff |

### Example Error Response

{
"status": "error",
"message": "Rate limit exceeded",
"category": "RATE_LIMIT"
}

yaml
Copy code

---

## Data Extraction Flow

1. Authenticate using a HubSpot Private App access token
2. Call `/crm/v3/objects/deals` with `limit=100`
3. Read deal records from the `results` array
4. Extract pagination cursor from `paging.next.after`
5. Repeat requests until all records are retrieved
6. Persist extracted records in the destination database

---

## Best Practices

- Request only required deal properties to reduce payload size
- Fully exhaust pagination to ensure complete data extraction
- Monitor rate limits during large data syncs
- Log extraction checkpoints to support resume and retry

---

## Reference Documentation

- HubSpot Deals API:  
  https://developers.hubspot.com/docs/api/crm/deals
- Private App Authentication:  
  https://developers.hubspot.com/docs/api/private-apps

---

