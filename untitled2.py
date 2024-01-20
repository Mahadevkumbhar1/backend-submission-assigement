# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FuIr-Uv0IgBGNiagH07ijIkk41idtlhc
"""

# Filename: volatility_calculator.py
# Filename: volatility_calculator.py

from fastapi import FastAPI, UploadFile, Form, HTTPException, File
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io

app = FastAPI()

# ... (rest of the code remains unchanged)


def calculate_daily_returns(close_prices):
    return close_prices.pct_change()

def calculate_daily_volatility(daily_returns):
    return np.std(daily_returns)

def calculate_annualized_volatility(daily_volatility, length_of_data):
    return daily_volatility * np.sqrt(length_of_data)

@app.post("/compute_volatility")
async def compute_volatility(file: UploadFile = File(None), file_path: str = Form(None)):
    """
    Computes Daily and Annualized Volatility from a given CSV file or a file path.

    Parameters:
    - file: Upload a CSV file.
    - file_path: Provide the path to an existing CSV file.

    Returns:
    - JSONResponse containing Daily and Annualized Volatility.
    """
    if not file and not file_path:
        raise HTTPException(status_code=400, detail="Either 'file' or 'file_path' parameter is required.")

    if file:
        content = await file.read()
        data = pd.read_csv(io.StringIO(content.decode('utf-8')))
    elif file_path:
        data = pd.read_csv(file_path)

    try:
        close_prices = data['Close']
    except KeyError:
        raise HTTPException(status_code=400, detail="Column 'Close' not found in the dataset.")

    daily_returns = calculate_daily_returns(close_prices)
    daily_volatility = calculate_daily_volatility(daily_returns)
    length_of_data = len(data)
    annualized_volatility = calculate_annualized_volatility(daily_volatility, length_of_data)

    result = {
        "Daily Volatility": round(daily_volatility, 4),
        "Annualized Volatility": round(annualized_volatility, 4)
    }

    return JSONResponse(content=result)

# To run the application, use the following command in the terminal:
# uvicorn volatility_calculator:app --reload