from flask import Flask, render_template, request, redirect, url_for
import caesar
import food_app

app = Flask(__name__)
config = food_app.read_config()
users = food_app.read_users(config=config)


@app.route("/")
def open_page():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def web_login():
    user = request.form['username']
    passwd = request.form['password']
    if user in users.keys():
        if passwd == caesar.decrypt(users[user]):
            data = food_app.read_products(config=config)
            if user == 'admin':
                return render_template("home_admin.html", data=data)
            else:
                return render_template("home_user.html", data=data)
        return render_template("login.html", error="Parola este incorectă.")
    return render_template("login.html", error="Utilizatorul nu există.")


@app.route("/log_out")
def delog():
    return redirect(url_for('open_page'))


@app.route("/add_products", methods=['POST'])
def add_products():
    try:
        product_name = request.form['product_name']
        ingredients = request.form['ingredients']
        price = request.form['price']
        query = (f"INSERT INTO burger_grill.products (name, ingredients, price) "
                 f"VALUES ('{product_name}', '{ingredients}', {price})")
        food_app.execute_query(sql_query=query, config=config)
        data = food_app.read_products(config=config)
        return render_template("home_admin.html", data=data)
    except Exception as e:
        return {"ERROR": f"404 NOT FOUND {e}"}


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            fullname = request.form['fullname']
            username = request.form['username']
            mail = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                query = (f"INSERT INTO burger_grill.food_app_user(fullname, username, email, password) "
                         f"VALUES ('{fullname}', '{username}', '{mail}', '{caesar.encrypt(password)}')")
                food_app.execute_query(sql_query=query, config=config)
                return redirect(url_for('open_page'))
            else:
                return render_template("signup.html", error="Parolele nu se potrivesc.")
        except Exception as e:
            return {"ERROR": f"404 NOT FOUND {e}"}
    return render_template("signup.html")


@app.route("/order", methods=['POST'])
def order_product():
    try:
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        user = request.form['username']
        user_id = next((u['id'] for u in users if u['username'] == user), None)
        if user_id is not None:
            food_app.insert_order(int(user_id), int(product_id), int(quantity), config)
            data = food_app.read_products(config=config)
            return render_template("home_user.html", data=data, message="Comanda a fost plasată cu succes!",
                                   username=user)
        else:
            return {"ERROR": "Utilizatorul nu a fost găsit."}
    except Exception as e:
        return {"ERROR": f"404 NOT FOUND {e}"}


if __name__ == '__main__':
    app.run()
