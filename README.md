# FastAPI Excel Processor

A FastAPI-based project to process and expose data from an Excel `.xls` file via a RESTful API. This assignment demonstrates the ability to work with tabular data, extract structure programmatically, and build robust endpoints using FastAPI.

---

## Project Overview

The goal of this project is to build a FastAPI application that:
- Parses a provided Excel sheet (`Data/capbudg.xls`)
- Dynamically detects structured tables based on uppercase headers and NaN logic
- Exposes endpoints for table listing, row inspection, and row-wise numeric summarization

---

## Features

### Excel Sheet Structure Recognition

- Detects **tables** based on **uppercase cells** followed by `NaN` in adjacent columns
- Associates **row names** with the table if they immediately follow a table name
- Stops parsing a table's rows when a `NaN` is encountered in the first column

### REST API Endpoints

Base URL: `http://localhost:9090`

---

### 1. `GET /list_tables`

**Description**: Lists all table names detected in the Excel file.  
**Logic**: A table is recognized as a fully **uppercase** cell with all NaNs in the rest of the row.

#### Example Response
```json
{
  "tables": [
    "INITIAL INVESTMENT",
    "CASHFLOW DETAILS",
    "WORKING CAPITAL",
    "GROWTH RATES",
    "YEAR",
    "SALVAGE VALUE",
    "OPERATING CASHFLOWS",
    "BOOK VALUE & DEPRECIATION"
  ]
}
```

### 2. `GET /get_table_details?table_name=...`

**Description**: Lists all row names under the specified table.  
**Query Parameter**: 
- **table_name** (required): Name of the table, must match one from **/list_tables**.

#### Example Request
```sql
GET /get_table_details?table_name=INITIAL INVESTMENT

```

#### Example Response
```json
{
  "tables": [
    "INITIAL INVESTMENT",
    "CASHFLOW DETAILS",
    "WORKING CAPITAL",
    "GROWTH RATES",
    "YEAR",
    "SALVAGE VALUE",
    "OPERATING CASHFLOWS",
    "BOOK VALUE & DEPRECIATION"
  ]
}
```

### 3. `GET /row_sum?table_name=...&row_name=...`

**Description**: Returns the sum of numeric values for the given row under the specified table.
**Logic**: 
- Skips initial NaNs
- Starts summing once a numeric value is found
- Stops when it encounters a NaN after starting
- Interprets values like 0.1 (with a trailing % implied) as 10.0

#### Example Request
```sql
GET /row_sum?table_name=INITIAL INVESTMENT&row_name=Tax Credit (if any )=

```

#### Example Response
```json
{
  "table_name": "INITIAL INVESTMENT",
  "row_name": "Tax Credit (if any )=",
  "sum": 10.0
}
```


