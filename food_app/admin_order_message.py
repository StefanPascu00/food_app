import json
import customtkinter
import food_app
import tkinter as tk

i = 0


def order_from_database(config):
    data = food_app.read_products(config, "burger_grill.user_orders")
    data = data[-1]
    order = data['order_name'].split(",")
    new_order = ""
    for item in order:
        new_order += item + "\n"
    order_show = [data['user_name'] + "\n", new_order, data['adress'], data['phone']]
    return order_show


def text_order(fast_food_order: list) -> str:
    textbox = ""
    for product in fast_food_order:
        textbox += f"{product}\n"
    return textbox


def show_order(fast_food_order: list):
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("320x480")
    app.title("New Order")

    title = customtkinter.CTkLabel(app, text="New Order")
    title.pack(padx=10, pady=10)
    order = customtkinter.CTkLabel(app, text=str(text_order(fast_food_order)))
    order.pack(padx=20, pady=30)

    app.mainloop()


if __name__ == '__main__':
    # with open("config.json", "r") as f:
    #     config = json.loads(f.read())
    # data = order_from_database(config)
    # while True:
    #     new_data = order_from_database(config)
    #     if data != new_data:
    #         data = new_data
    #         show_order(data)
    fas = ["1", "2", "3"]
    show_order(fas)
