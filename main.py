from fastapi import FastAPI, Query, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI(
    title="Excel Processor API",
    description="Processes financial tables from Excel and returns insights.",
    version="1.0.0"
)

EXCEL_FILE = os.path.join("Data", "capbudg.xls")


df = pd.read_excel(EXCEL_FILE, header=None)


def detect_tables(df: pd.DataFrame) -> List[dict]:
    tables = []
    seen = set()

    for row_idx in range(len(df)):
        for col_idx in range(len(df.columns)):
            val = df.iat[row_idx, col_idx]
            if (
                isinstance(val, str)
                and val.strip().isupper()
                and (val.strip(), col_idx) not in seen
            ):
                
                if "=" not in val.strip() and len(val.strip()) > 2:
                    tables.append({
                        "name": val.strip(),
                        "row_idx": row_idx,
                        "col_idx": col_idx
                    })
                    seen.add((val.strip(), col_idx))
    return tables


detected_tables = detect_tables(df)
table_names = [t["name"] for t in detected_tables]

@app.get("/list_tables")
def list_tables():
    return {"tables": table_names}


@app.get("/get_table_details")
def get_table_details(table_name: str = Query(..., description="Name of the table")):
    table = next((t for t in detected_tables if t["name"] == table_name), None)
    if not table:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")

    row_idx = table["row_idx"] + 1
    col_idx = table["col_idx"]
    row_names = []

    while row_idx < len(df):
        cell = df.iat[row_idx, col_idx]
        if pd.isna(cell):
            break
        row_names.append(str(cell).strip())
        row_idx += 1

    return {
        "table_name": table_name,
        "row_names": row_names
    }


@app.get("/row_sum")
def row_sum(
    table_name: str = Query(...),
    row_name: str = Query(...)
):
    table = next((t for t in detected_tables if t["name"] == table_name), None)
    if not table:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found.")

    start_row_idx = table["row_idx"] + 1
    end_row_idx = len(df)

    row_found = False
    target_row_idx = None
    label_col_idx = None

    # Step 1: Find the row containing the row_name
    for r in range(start_row_idx, end_row_idx):
        row = df.iloc[r]
        if all(pd.isna(cell) for cell in row):
            break  # End of table
        for c in range(len(row)):
            if isinstance(row[c], str) and row[c].strip() == row_name.strip():
                target_row_idx = r
                label_col_idx = c
                row_found = True
                break
        if row_found:
            break

    if not row_found:
        raise HTTPException(status_code=404, detail=f"Row '{row_name}' not found in table '{table_name}'.")

    # Step 2: Start summing from the next non-NaN cell after label_col_idx
    total = 0.0
    started = False
    for col in range(label_col_idx + 1, df.shape[1]):
        val = df.iat[target_row_idx, col]

        if not started and pd.isna(val):
            continue  # Skip leading NaNs

        if pd.isna(val):
            break  # Stop on first NaN after summing started

        if isinstance(val, (int, float)):
            started = True
            # Convert to percentage if value is less than 1
            total += val * 100 if 0 < val < 1 else val

    return {
        "table_name": table_name,
        "row_name": row_name,
        "sum": round(total, 2)
    }