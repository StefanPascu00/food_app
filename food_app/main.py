from flask import Flask, render_template, request, redirect, url_for
import caesar
import food_app
import os
from werkzeug.utils import secure_filename
from tkinter import messagebox as msg
import admin_order_message as adm

app = Flask(__name__)
config = food_app.read_config()
users = food_app.read_users(config=config)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            with open('user.txt', "w") as f:
                f.write(user)
            if user == 'admin':
                return render_template("home_admin.html", data=data)
            else:
                return render_template("home_user.html", data=data)
        return render_template("login.html", error="Parola este incorectă.")
    return render_template("login.html", error="Utilizatorul nu există.")


@app.route("/log_out")
def log_out():
    with open('user.txt', "w") as f:
        user = f.write("")
    return redirect(url_for('open_page'))


@app.route("/add_products", methods=['POST'])
def add_products():
    try:
        product_name = request.form['product_name']
        ingredients = request.form['ingredients']
        price = request.form['price']
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = f"/{app.config['UPLOAD_FOLDER']}/{filename}"

            query = (f"INSERT INTO burger_grill.products (name, ingredients, price, image_url) "
                     f"VALUES ('{product_name}', '{ingredients}', {price}, '{image_url}')")
            food_app.execute_query(sql_query=query, config=config)
            data = food_app.read_products(config=config)
            return render_template("home_admin.html", data=data)
        else:
            return render_template("home_admin.html", error="Fișierul încărcat nu este valid.")
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


@app.route("/order", methods=['GET', 'POST'])
def order_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            address = request.form['address']
            with open('user.txt', "r") as f:
                user = f.read()
            if user is None:
                return {"ERROR": "Utilizatorul nu a fost găsit."}
            total_price = 0
            fast_food = ""
            if len(phone) == 10 and phone.startswith("07"):

                products = food_app.read_products(config=config)

                for product in products:
                    quantity = int(request.form.get(f'quantity_{product["id"]}', 0))
                    if quantity > 0:
                        fast_food += f"{product['name']}->{quantity},"
                        price = int(product['price']) * int(quantity)
                        total_price += price
                food_app.insert_order(user_name=name, order_name=str(fast_food), addres=address, phone=phone, config=config)

            else:
                msg.showerror("Error", "Numarul nu are 10 cifre sau nu incepe cu 07")

            data = food_app.read_products(config=config)
            return render_template("order_succes.html", name=name, phone=phone,
                                   address=address, total_price=total_price,
                                   message="Comanda a fost plasată cu succes!")
        except Exception as e:
            return {"ERROR": f"404 NOT FOUND {e}"}
    else:
        data = food_app.read_products(config=config)
        return render_template("home_user.html", data=data)


if __name__ == '__main__':
    # data = adm.order_from_database(config)
    # while True:
    #     new_data = adm.order_from_database(config)
    #     if data[-1] != new_data[-1]:
    #         data = new_data
    #         adm.show_order(data)

        app.run()

