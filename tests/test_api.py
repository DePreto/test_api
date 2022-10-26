import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.connection import get_conn
from contextlib import closing
from collections import defaultdict


client = TestClient(app)


@pytest.fixture()
def clear_db():
    clear_tables_sql_ = """
    TRUNCATE TABLE links, products, categories;
    """

    yield

    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(clear_tables_sql_)
            conn.commit()


@pytest.fixture()
def load_db(clear_db):
    test_products = (
        (1, "prod1",),
        (2, "prod2",),
        (3, "prod3",),
    )

    test_categories = (
        (1, "cat1",),
        (2, "cat2",),
        (3, "cat3",)
    )

    test_links = (
        (1, 1, 1),
        (2, 1, 2),
        (3, 2, 1)
    )

    load_products_sql_ = f"""
    INSERT INTO Products VALUES (%s, %s);
    """
    load_categories_sql_ = f"""
    INSERT INTO categories VALUES (%s, %s);
    """
    load_links_sql_ = """
    INSERT INTO links VALUES (%s, %s, %s);
    """

    with closing(get_conn()) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(load_products_sql_, test_products)
            cursor.executemany(load_categories_sql_, test_categories)
            cursor.executemany(load_links_sql_, test_links)
            conn.commit()

    yield test_products, test_categories, test_links


class TestAPI:
    def test_success_get_categories(self, load_db):
        test_products, test_categories, test_links = load_db

        expected_result = defaultdict(list)
        for pair in test_links:
            link, prod_id, cat_id = pair
            prod_name = tuple(filter(lambda x: x[0] == prod_id, test_products))[0][1]
            cat_name = tuple(filter(lambda x: x[0] == cat_id, test_categories))[0][1]
            expected_result[cat_name].append(prod_name)

        for category in test_categories:
            if category[1] not in expected_result:
                expected_result[category[1]] = None

        fmt_expected_result = []
        for key, value in expected_result.items():
            if value:
                fmt_expected_result.append([key, ','.join(map(str, value))])
            else:
                fmt_expected_result.append([key, None])

        response = client.get("/categories")
        result = response.json()

        assert response.status_code == 200
        assert all([item in result for item in fmt_expected_result])

    def test_success_get_products(self, load_db):
        test_products, test_categories, test_links = load_db

        expected_result = defaultdict(list)
        for pair in test_links:
            link, prod_id, cat_id = pair
            prod_name = tuple(filter(lambda x: x[0] == prod_id, test_products))[0][1]
            cat_name = tuple(filter(lambda x: x[0] == cat_id, test_categories))[0][1]
            expected_result[prod_name].append(cat_name)

        for product in test_products:
            if product[1] not in expected_result:
                expected_result[product[1]] = None

        fmt_expected_result = []
        for key, value in expected_result.items():
            if value:
                fmt_expected_result.append([key, ','.join(map(str, value))])
            else:
                fmt_expected_result.append([key, None])

        response = client.get("/products")
        result = response.json()

        assert response.status_code == 200
        assert all([item in result for item in fmt_expected_result])

    def test_success_get_pairs(self, load_db):
        test_products, test_categories, test_links = load_db

        expected_result = []
        for pair in test_links:
            link, prod_id, cat_id = pair
            prod_name = tuple(filter(lambda x: x[0] == prod_id, test_products))[0][1]
            cat_name = tuple(filter(lambda x: x[0] == cat_id, test_categories))[0][1]
            expected_result.append([prod_name, cat_name])

        response = client.get("/pairs")
        result = response.json()

        assert response.status_code == 200
        assert all([item in result for item in expected_result])
