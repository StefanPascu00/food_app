import base64
import json
import psycopg2 as ps


def read_config(path: str = "config.json"):
    with open(path, "r") as f:
        config = json.loads(f.read())

    return config


def read_users(config: dict, table: str = "burger_grill.food_app_user"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select username, password from {table}"
            cursor.execute(sql_query)
            users = cursor.fetchall()
            all_users = {}
            for user in users:
                all_users[user[0]] = user[1]
            return all_users


def read_products(config: dict, table: str = "burger_grill.products"):
    with ps.connect(**config) as conn:
        with conn.cursor() as cursor:
            sql_query = f"select * from {table}"
            cursor.execute(sql_query)
            products = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            products_list = []
            for item in products:
                products_list.append(dict(zip(columns, item)))

            return products_list


def execute_query(sql_query: str, config: dict):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                print("Successfully executed")
                return cursor.statusmessage

    except Exception as e:
        print(f"Failure on reading on database. Error : {e}")
        return False


def insert_order(user_name, product_name, quantity, addres, phone, config):
    query = (f"INSERT INTO burger_grill.user_orders (user_name, product_name, quantity, adress, phone) "
             f"VALUES ('{user_name}', '{product_name}', {quantity}, '{addres}', '{phone}')")
    execute_query(query, config)


if __name__ == '__main__':
    config = read_config()
    admins = read_users(config)
    products = read_products(config)
