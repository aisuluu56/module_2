import psycopg2
from psycopg2.extras import RealDictCursor
from models import Product
from contextlib import closing
from datetime import date, timedelta


def get_connection():
    return psycopg2.connect(
        dbname="shop",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )


def get_products():
    first_day_this_month = date.today().replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)

    with closing(get_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                    p.id,
                    p.name,
                    p.category,
                    p.manufacturer,
                    p.composition,
                    p.image,
                    p.price,
                    COALESCE(SUM(s.quantity), 0) AS quantity,
                    EXISTS (
                        SELECT 1
                        FROM order_items oi
                        JOIN stock_items si ON oi.stock_item_id = si.id
                        JOIN orders o       ON oi.order_number = o.order_number
                        WHERE si.product_id = p.id
                          AND o.order_date >= %s
                          AND o.order_date <  %s
                    ) AS had_orders_last_month
                FROM products p
                LEFT JOIN stock_items s ON p.id = s.product_id
                GROUP BY p.id
                """,
                (first_day_last_month, first_day_this_month)
            )

            return [
                Product(
                    product_id=row["id"],
                    name=row["name"],
                    category=row["category"],
                    manufacturer=row["manufacturer"],
                    composition=row["composition"],
                    image=row["image"],
                    price=float(row["price"]),
                    quantity=int(row["quantity"]),
                    had_orders_last_month=row["had_orders_last_month"],
                )
                for row in cursor.fetchall()
            ]