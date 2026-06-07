import requests
import random
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8001"

def run():
    categories = ["Electronics", "Clothing", "Food", "Tools", "Furniture", "Toys"]
    
    # Optional: We will just append products to the DB
    print("Generating 100 Products...")
    
    for p_idx in range(1, 101):
        cat = random.choice(categories)
        cost = round(random.uniform(5.0, 50.0), 2)
        selling = round(cost * random.uniform(1.2, 2.5), 2)
        
        prod = {
            "name": f"Product {random.randint(1000, 9999)} - {cat}",
            "category": cat,
            "cost_price": cost,
            "selling_price": selling,
            "stock_quantity": random.randint(100, 5000)
        }
        
        r = requests.post(f"{BASE_URL}/products/", json=prod)
        if r.status_code != 200:
            print(f"Error creating product {p_idx}:", r.text)
            continue
            
        product = r.json()
        pid = product["id"]
        
        # Seed 60 days of sales
        today = datetime.now()
        base_qty = random.randint(5, 30)
        trend = random.choice([-0.2, 0.1, 0.3, 0.5])
        
        for i in range(60, 0, -1):
            d = today - timedelta(days=i)
            # Add some noise and trend
            qty = max(0, int(base_qty + (60-i) * trend + random.randint(-5, 10)))
            sale = {
                "product_id": pid,
                "quantity": qty,
                "sale_date": d.isoformat()
            }
            requests.post(f"{BASE_URL}/sales/", json=sale)
            
        if p_idx % 10 == 0:
            print(f"Seeded {p_idx}/100 products...")

    print("Creating Budgets for categories...")
    for cat in categories:
        budget_req = {
            "category": cat,
            "amount_limit": round(random.uniform(5000.0, 20000.0), 2),
            "period_start": (today - timedelta(days=90)).isoformat(),
            "period_end": (today + timedelta(days=90)).isoformat()
        }
        requests.post(f"{BASE_URL}/budgets/", json=budget_req)

    print("Seeding complete!")


if __name__ == "__main__":
    run()
