import requests
import random
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8001"

def run():
    print("Creating Product...")
    prod = {
        "name": "Super Widget",
        "category": "Widgets",
        "cost_price": 10.0,
        "selling_price": 20.0,
        "stock_quantity": 5000
    }
    r = requests.post(f"{BASE_URL}/products/", json=prod)
    if r.status_code != 200:
        print("Error creating product:", r.text)
        return
    product = r.json()
    pid = product["id"]
    print(f"Product Created: ID {pid}")

    print("Seeding 60 days of sales...")
    today = datetime.now()
    for i in range(60, 0, -1):
        d = today - timedelta(days=i)
        # Trend: quantity increases over time
        qty = int(20 + (60-i) * 0.5 + random.randint(-5, 5))
        sale = {
            "product_id": pid,
            "quantity": qty,
            "sale_date": d.isoformat()
        }
        r = requests.post(f"{BASE_URL}/sales/", json=sale)
        if r.status_code != 200:
            print(f"Error sale {i}: {r.text}")

    print("Requesting Forecast...")
    forecast_req = {"product_id": pid, "days": 7}
    r = requests.post(f"{BASE_URL}/forecast/", json=forecast_req)
    if r.status_code != 200:
        print("Forecast failed:", r.text)
    else:
        print("Forecast Results:")
        print(json.dumps(r.json(), indent=2))

    print("Creating Budget...")
    budget_req = {
        "category": "Widgets",
        "amount_limit": 10000.0,
        "period_start": (today - timedelta(days=90)).isoformat(),
        "period_end": (today + timedelta(days=90)).isoformat()
    }
    r = requests.post(f"{BASE_URL}/budgets/", json=budget_req)
    if r.status_code != 200:
        print("Budget creation failed", r.text)
    else:
        print("Budget Created for Widgets. ID:", r.json()["id"])
        
    print("Checking Budget Status...")
    r = requests.get(f"{BASE_URL}/budgets/")
    budgets = r.json()
    for b in budgets:
        print(f"Budget Category: {b['category']}, Limit: {b['amount_limit']}, Spend/Revenue: {b['current_spend']}")

    print("Adding new sale to test Budget Tracking...")
    new_sale = {
        "product_id": pid,
        "quantity": 10,
        "sale_date": datetime.now().isoformat()
    }
    r = requests.post(f"{BASE_URL}/sales/", json=new_sale)
    if r.status_code == 200:
        print("New Sale Added.")
    
    print("Re-checking Budget Status...")
    r = requests.get(f"{BASE_URL}/budgets/")
    budgets = r.json()
    for b in budgets:
        print(f"Budget Category: {b['category']}, Limit: {b['amount_limit']}, Spend/Revenue: {b['current_spend']}")
        if b['current_spend'] > 0:
            print("SUCCESS: Budget tracking updated!")



if __name__ == "__main__":
    run()
