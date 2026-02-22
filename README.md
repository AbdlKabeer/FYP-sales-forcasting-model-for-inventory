# Sales Forecasting Model for Inventory and Budget Planning

This project is a full-stack web application designed to help businesses optimize their inventory levels and manage budgets through data-driven predictive analytics. It uses machine learning to forecast future sales and integrates these predictions directly into inventory and budget tracking workflows.

## Features

- **Dual-Model Forecasting:** Compare predictions between a baseline **Linear Regression** model (great for stable trends) and an advanced **SARIMA** model (Seasonal Autoregressive Integrated Moving Average, excellent for capturing weekly/monthly seasonal patterns).
- **Automated Inventory Tracking:** Recording a sale automatically decrements the stock quantity for that product.
- **Real-Time Budget Monitoring:** Sales and inventory costs are tracked against predefined budget categories in real-time.
- **Interactive Dashboard:** A modern UI built with Next.js to visualize sales data, forecast charts, and budget status.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy (SQLite Database)
- **Machine Learning:** Scikit-Learn (Linear Regression), Statsmodels (SARIMA), Pandas
- **Frontend:** TypeScript, Next.js (React), Tailwind CSS, Recharts

## Project Structure

```
.
├── backend/                  # FastAPI server and ML logic
│   ├── app/                  # API endpoints, database models, and crud operations
│   │   ├── ml.py             # Forecasting engine (Linear Regression & SARIMA)
│   │   └── main.py           # FastAPI application setup
│   ├── requirements.txt      # Python dependencies
│   ├── seed_and_test.py      # Script to populate dummy data and test endpoints
│   └── generate_comparison_plot.py # Script to generate ML comparison plots
├── frontend/                 # Next.js user interface
│   ├── app/                  # Next.js page routing
│   ├── components/           # Reusable UI components (e.g., ForecastChart)
│   └── lib/                  # API data fetching utilities
└── RESEARCH_REPORT.md        # Detailed academic report of the methodology and results
```

## Getting Started

### 1. Backend Setup

Open a terminal and navigate to the backend directory:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

Run the backend development server:
```bash
uvicorn app.main:app --reload --port 8001
```
*The API will be available at `http://127.0.0.1:8001` and interactive docs at `http://127.0.0.1:8001/docs`.*

### 2. Seeding Data (Optional)

If you need dummy data to test the dashboard, run the seed script while the backend server is running:
```bash
cd backend
# Make sure your virtual environment is active
python seed_and_test.py
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install the Node dependencies:
```bash
npm install
```

Run the Next.js development server:
```bash
npm run dev
```
*The dashboard will be available at `http://localhost:3000`.*

---
*Created for a final year academic project.*
