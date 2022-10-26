from connection import get_conn
from contextlib import closing


create_db_sql_ = """
CREATE TABLE IF NOT EXISTS Products (
    id serial PRIMARY KEY, 
    name text not null 
);
CREATE TABLE IF NOT EXISTS Categories (
    id serial PRIMARY KEY, 
    name text not null 
);
CREATE TABLE IF NOT EXISTS Links (
    id serial PRIMARY KEY, 
    product_id integer REFERENCES Products (id), 
    category_id integer REFERENCES Categories (id),
    UNIQUE (product_id, category_id)
);
"""

print("init db")
with closing(get_conn()) as conn:
    with conn.cursor() as cursor:
        cursor.execute(create_db_sql_)
        conn.commit()
print("init complete")
