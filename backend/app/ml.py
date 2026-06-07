import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")


def generate_forecast(db: Session, product_id: int, days: int = 30, model_type: str = "linear"):
    # Fetch sales for the product
    sales = db.query(models.Sale).filter(models.Sale.product_id ==
                                         product_id).order_by(models.Sale.sale_date).all()

    if not sales or len(sales) < 5:
        return {"error": "Not enough data points to forecast (need at least 5)"}

    # Prepare DataFrame
    data = []
    for s in sales:
        data.append({"date": s.sale_date.date(), "quantity": s.quantity})

    df = pd.DataFrame(data)
    df = df.groupby("date").sum().reset_index()

    if model_type == "sarima":
        return generate_sarima_forecast(df, days)
    else:
        return generate_linear_forecast(df, days)


def generate_linear_forecast(df, days):
    # Convert dates to ordinal for regression
    df["date_ordinal"] = df["date"].apply(lambda x: x.toordinal())

    X = df[["date_ordinal"]]
    y = df["quantity"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict future
    last_date = df["date"].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]
    future_ordinals = [[d.toordinal()] for d in future_dates]

    predictions = model.predict(future_ordinals)
    
    # Calculate training metrics
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    train_preds = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, train_preds))
    mae = mean_absolute_error(y, train_preds)
    r2 = r2_score(y, train_preds)

    forecast = []
    for d, q in zip(future_dates, predictions):
        forecast.append({
            "date": datetime.combine(d, datetime.min.time()),
            "predicted_quantity": max(0, round(float(q), 2))
        })
    return {
        "forecast": forecast,
        "metrics": {
            "training_rmse": round(float(rmse), 2),
            "training_mae": round(float(mae), 2),
            "r2_score": round(float(r2), 2)
        }
    }


def generate_sarima_forecast(df, days):
    # Set index for time series
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    # Resample to ensure daily continuity
    df = df.resample('D').sum().fillna(0)

    try:
        # Simple SARIMA parameters - in a real app these might be tuned
        # Seasonal order assumes weekly seasonality (7 days)
        model = SARIMAX(df['quantity'],
                        order=(1, 1, 1),
                        seasonal_order=(1, 1, 1, 7),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        model_fit = model.fit(disp=False)

        forecast_values = model_fit.forecast(steps=days)
        
        # Calculate training metrics
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        train_preds = model_fit.fittedvalues
        rmse = np.sqrt(mean_squared_error(df['quantity'], train_preds))
        mae = mean_absolute_error(df['quantity'], train_preds)
        r2 = r2_score(df['quantity'], train_preds)

        last_date = df.index.max()
        future_dates = [last_date + timedelta(days=i)
                        for i in range(1, days + 1)]

        forecast = []
        for d, q in zip(future_dates, forecast_values):
            forecast.append({
                "date": d,
                "predicted_quantity": max(0, round(float(q), 2))
            })
        return {
            "forecast": forecast,
            "metrics": {
                "training_rmse": round(float(rmse), 2),
                "training_mae": round(float(mae), 2),
                "r2_score": round(float(r2), 2)
            }
        }
    except Exception as e:
        return {"error": f"SARIMA model failed: {str(e)}"}
