import json
import customtkinter
import database_function as db


def order_from_database(config: dict) -> list:
    """Citeste din baza de date comenzile efectuate de clienti, retureneza ultima comanda efectuata si aranjeaza textul"""
    data = db.read_products(config, "burger_grill.user_orders")
    data = data[-1]
    order = data['order_name'].split(",")
    new_order = ""
    for item in order:
        new_order += item + "\n"
    order_show = [data['user_name'] + "\n", new_order, data['adress'], data['phone']]
    return order_show


def text_order(fast_food_order: list) -> str:
    """Ia textul cu produsele comandate si le aseaza unele sub celelalte"""
    textbox = ""
    for product in fast_food_order:
        textbox += f"{product}\n"
    return textbox


def show_order(fast_food_order: list):
    """Aici cream o fereastra unde vedem numele, produsele comandate, adresa si numarul de telefon"""
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("320x480")
    app.title("New Order")

    title = customtkinter.CTkLabel(app, text="New Order")
    title.pack(padx=10, pady=10)
    order = customtkinter.CTkLabel(app, text=str(text_order(fast_food_order)))
    order.pack(padx=20, pady=30)

    return app


def new_order():
    """Aici rulam un loop pentru a citi mereu din baza de date iar cand apare o comanda noua sa ne-o returneze"""
    try:
        config = db.read_config()
        data = order_from_database(config)
        while True:
            new_data = order_from_database(config)
            if data != new_data:
                data = new_data
                show_order(data).mainloop()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    new_order()
