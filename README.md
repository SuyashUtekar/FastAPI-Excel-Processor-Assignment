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

#### Example Response
```json
GET /get_table_details?table_name=INITIAL INVESTMENT

```



