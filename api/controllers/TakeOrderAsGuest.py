# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

# ----- Database Setup -----
def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        special_instructions TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ----- Guest Order Form -----
class GuestOrder(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=50)
    item: str = Field(..., min_length=2, max_length=100)
    quantity: int = Field(..., gt=0)
    special_instructions: str | None = None

# ----- POST Endpoint -----
@app.post("/orders/")
def create_order(order: GuestOrder):
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_name, item, quantity, special_instructions)
            VALUES (?, ?, ?, ?)
        """, (order.customer_name, order.item, order.quantity, order.special_instructions))
        conn.commit()
        order_id = cursor.lastrowid
        conn.close()
        return {"message": "Order created successfully", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Optional: GET all orders (for testing) -----
@app.get("/orders/")
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return {"orders": rows}
