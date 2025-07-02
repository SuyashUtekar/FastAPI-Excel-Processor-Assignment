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
## Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload --port 9090
```

## File Structure

```bash
.
├── Data/
│   └── capbudg.xls                # Excel file to parse
├── .gitignore
├── main.py                        # FastAPI server implementation
├── postman_collection.json        # Collection of sample requests for testing
├── requirements.txt               # Required packages
└── README.md                      # Project documentation
```

## Testing with Postman

- Use the included postman_collection.json to test all endpoints.
- Base URL: http://localhost:9090
- Import the collection into Postman and run the requests interactively.

## Potential Improvements

- Support .xlsx files using openpyxl
- Include POST endpoint for uploading Excel files dynamically
- Add response caching for repeated queries
- Add error messages for table/row not found
- Create a Streamlit frontend for non-technical users

## Missed Edge Cases

- Duplicate table names
- Tables with mixed types in rows
- Inconsistent row names (merged or multiline cells)
- Completely empty Excel files
- Malformed numeric formats or hidden characters

## Author Notes

- Designed with reusability and clarity in mind
- All responses follow JSON format
- All logic is contained in a single main.py for simplicity (can be modularized)

## License

This repository is created as part of a technical assignment for evaluation purposes.
