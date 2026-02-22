from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_budget(db: Session, budget: schemas.BudgetCreate):
    db_budget = models.Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Budget).offset(skip).limit(limit).all()

def create_sale(db: Session, sale: schemas.SaleCreate):
    # Calculate total amount based on product price
    product = get_product(db, sale.product_id)
    if not product:
        return None
    
    total_amount = product.selling_price * sale.quantity
    
    # Update inventory
    product.stock_quantity -= sale.quantity

    # Update Budget (if exists for category and active period)
    today = sale.sale_date or datetime.utcnow()
    # Find active budget for this category
    active_budget = db.query(models.Budget).filter(
        models.Budget.category == product.category,
        models.Budget.period_start <= today,
        models.Budget.period_end >= today
    ).first()

    if active_budget:
        active_budget.current_spend += product.cost_price * sale.quantity # Track COST or REVENUE? Usually budget is for purchasing (cost). 
        # But if this is a "Sales Budget" (Target), we track Revenue. 
        # User said "Budget Planning", usually implies spending limits for inventory. 
        # But let's assume "Inventory Budget" -> Cost. 
        # "Sales Forecasting" -> Revenue.
        # "Budget Planning" in context of "Inventory" usually means "Don't spend more than X on stock".
        # However, here we are RECORDING A SALE (Inventory OUT).
        # So maybe Budget is "Sales Target"? 
        # Let's assume Budget is "Sales Target" for now (Logic: We want to hit the budget).
        # OR Budget is "Inventory Restocking Budget". 
        # Let's stick to the prompt: "Budget Planning" ... "Sales Forecasting".
        # Use Case: "Drafting a budget for next year".
        # Let's track Revenue against a Sales Target Budget?
        # Re-reading prompt: "budget planning".
        # Let's track REVENUE generated against a TARGET.
        # OR: limit expenses.
        # Let's go with: Budget = "Expense Limit". But we don't have "Purchase" endpoints, only "Sale" (Inventory Decrease).
        # So maybe Budget = "Sales Target" (Goal).
        # Let's implement it as "Revenue Goal Tracking".
        active_budget.current_spend += total_amount # Tracking Revenue against Target

    db_sale = models.Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_amount=total_amount,
        sale_date=sale.sale_date or datetime.utcnow()
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()
