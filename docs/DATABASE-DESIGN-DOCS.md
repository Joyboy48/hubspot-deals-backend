# 📊 Database Design – HubSpot Deals ETL Service

## Overview

This document defines the database schema used by the **hubspot_deals ETL service**
to store Deals data extracted from the HubSpot CRM API.

The schema is designed to be:
- Simple and task-focused
- Optimized for analytics and reporting
- Suitable for incremental ETL runs
- Supportive of multi-tenant use cases

The database technology assumed is **PostgreSQL**.

---

## Design Principles

- One record represents one HubSpot Deal
- HubSpot `deal_id` is used as the primary key
- ETL metadata is stored alongside business data
- Schema is easy to extend in the future
- Indexes support common query patterns

---

## Core Table: `hubspot_deals`

### Purpose

Stores all Deals extracted from the HubSpot CRM API.

---

## Table Schema

```sql
CREATE TABLE hubspot_deals (
    deal_id BIGINT PRIMARY KEY,
    deal_name TEXT,
    amount NUMERIC(12, 2),
    deal_stage TEXT,
    pipeline TEXT,
    close_date TIMESTAMP,

    created_at TIMESTAMP,
    updated_at TIMESTAMP,

    -- ETL metadata
    _extracted_at TIMESTAMP NOT NULL,
    _scan_id VARCHAR(255) NOT NULL,
    _tenant_id VARCHAR(255) NOT NULL
);


Column Descriptions

Name	        Data Type	  Description
deal_id	        BIGINT	    Unique HubSpot Deal identifier
deal_name	    TEXT	    Name of the deal
amount	        NUMERIC	    Deal value
deal_stage	    TEXT	    Current stage of the deal
pipeline	    TEXT	    Sales pipeline name
close_date	    TIMESTAMP	Expected or actual close date
created_at	    TIMESTAMP	Deal creation time
updated_at	    TIMESTAMP	Last update time
_extracted_at	TIMESTAMP	Timestamp when record was extracted
_scan_id	    VARCHAR	    Unique ETL run identifier
_tenant_id	    VARCHAR	    Tenant or account identifier

Indexing Strategy
Indexes are added to improve query performance.

sql
Copy code
CREATE INDEX idx_hubspot_deals_tenant
ON hubspot_deals (_tenant_id);

CREATE INDEX idx_hubspot_deals_stage
ON hubspot_deals (deal_stage);

CREATE INDEX idx_hubspot_deals_close_date
ON hubspot_deals (close_date);


Data Flow
-Deals are fetched from HubSpot CRM API
-Response fields are mapped to database columns
-ETL metadata fields are added
-Records are inserted or updated using deal_id
-Extraction runs are tracked using _scan_id

Multi-Tenancy Support

-Each deal record contains a _tenant_id
-Enables isolation between different HubSpot accounts
-Allows parallel extraction jobs without data collision

Data Integrity Considerations

-Primary key ensures uniqueness of deals
-Numeric type avoids precision loss for monetary values
-Metadata fields provide auditability
-Timestamp fields support debugging and replay

Future Enhancements

-Add history table for deal stage transitions
-Add foreign keys for owners and companies
-Partition table by tenant or extraction date
-Add JSONB column for dynamic deal properties

Summary

This database schema provides a clean, production-ready structure
for storing HubSpot Deals data and supports reliable ETL processing
with clear tracking, scalability, and extensibility.