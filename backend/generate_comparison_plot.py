from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

# Generate synthetic seasonal sales data
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=60, freq='D')
# Weekly seasonality (7 days) + Trend
quantity = 20 + 0.5 * np.arange(60) + 10 * np.sin(2 *
                                                  np.pi * np.arange(60) / 7) + np.random.normal(0, 2, 60)
df = pd.DataFrame({'date': dates, 'quantity': quantity})


# Split data for evaluation
train_df = df.iloc[:-14]
test_df = df.iloc[-14:]

# Add ordinal column for linear regression
df['ordinal'] = df['date'].apply(lambda x: x.toordinal())
train_df['ordinal'] = train_df['date'].apply(lambda x: x.toordinal())
test_df['ordinal'] = test_df['date'].apply(lambda x: x.toordinal())


# 1. Linear Regression Evaluation
X_train = train_df[['ordinal']]
y_train = train_df['quantity']
X_test = test_df[['ordinal']]
y_test = test_df['quantity']

lr_eval_model = LinearRegression().fit(X_train, y_train)
lr_eval_preds = lr_eval_model.predict(X_test)

lr_rmse = np.sqrt(mean_squared_error(y_test, lr_eval_preds))
lr_mae = mean_absolute_error(y_test, lr_eval_preds)

# 2. SARIMA Evaluation
sarima_eval_model = SARIMAX(train_df['quantity'], order=(
    1, 1, 1), seasonal_order=(1, 1, 1, 7)).fit(disp=False)
sarima_eval_preds = sarima_eval_model.forecast(steps=14)

sar_rmse = np.sqrt(mean_squared_error(test_df['quantity'], sarima_eval_preds))
sar_mae = mean_absolute_error(test_df['quantity'], sarima_eval_preds)

print(f"METRICS_START")
print(f"LR_RMSE: {lr_rmse:.2f}")
print(f"LR_MAE: {lr_mae:.2f}")
print(f"SARIMA_RMSE: {sar_rmse:.2f}")
print(f"SARIMA_MAE: {sar_mae:.2f}")
print(f"METRICS_END")

# Plotting (Full data)
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['quantity'],
         label='Actual Sales', color='black', alpha=0.5)
plt.plot(test_df['date'], lr_eval_preds,
         label='Linear Regression (Test Preds)', linestyle='--', color='blue')
plt.plot(test_df['date'], sarima_eval_preds,
         label='SARIMA (Test Preds)', linestyle='-', color='green')

plt.title('Sales Forecasting Model Performance: Actual vs Predicted')
plt.xlabel('Date')
plt.ylabel('Quantity Sold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

save_path = '/Users/olakay/.gemini/antigravity/brain/89ac17c9-6998-4aea-a56c-780e93041837/model_comparison_plot.png'
plt.savefig(save_path)
print(f"Plot saved to {save_path}")
