from contextlib import closing
from fastapi import FastAPI

from app.connection import get_conn

app = FastAPI()


get_products_sql_ = """
select Products.name, string_agg(Categories.name, ',') as name_list
from Products LEFT JOIN Links ON Products.id = Links.product_id
LEFT JOIN Categories ON Categories.id = Links.category_id
group by Products.id;
"""

get_categories_sql_ = """
select Categories.name, string_agg(Products.name, ',') as name_list
from Categories LEFT JOIN Links ON Categories.id = Links.category_id
LEFT JOIN Products ON Products.id = Links.product_id
group by Categories.id;
"""

get_pairs_sql_ = """
select Products.name, Categories.name from Links
JOIN Products ON Products.id = Links.product_id
JOIN Categories ON Categories.id = Links.category_id
"""


@app.get("/products")
def get_products():
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(get_products_sql_)
            return cursor.fetchall()


@app.get("/categories")
def get_categories():
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(get_categories_sql_)
            return cursor.fetchall()


@app.get("/pairs")
def get_pairs():
    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(get_pairs_sql_)
            return cursor.fetchall()
