import json
import random
import string
import caesar


def add_client(new_client: dict, path: str = "clients.json", auth_path: str = "auth.json"):
    # generate new id
    id = "".join(random.choices(string.ascii_letters + string.digits, k=4))
    new_client["id"] = id

    with open(path, "r+") as f:
        clients = json.loads(f.read())
        f.seek(0)
        clients["clients"].append(new_client)
        f.write(json.dumps(clients, indent=4))
    with open(auth_path, "r+") as f:
        users = json.loads(f.read())
        new_pass = "".join(random.choices(string.digits, k=3))
        users[id] = caesar.encrypt(new_pass)
        print(f"Client-ul {new_client['nume']} cu userul {id} are parola {new_pass}")
        f.seek(0)
        f.write(json.dumps(users, indent=4))


def login(path: str = "auth.json") -> str:
    with open(path, "r") as f:
        credentials = json.loads(f.read())

    user_name = input("Introduceti user-ul: ")

    while user_name not in credentials:
        user_name = input("Wrong user. ")

    password = input('PW: ')
    atempt = 1
    while caesar.encrypt(password) != credentials[user_name]:
        password = input("Parola gresita. Reintrodu: ")
        atempt += 1
        if atempt % 3 == 0:
            client = get_client(user_name)
            change_pass = input("Daca ati uitat parola introduceti forgot pass: ")
            match change_pass:
                case "forgot pass":
                    while True:
                        real_name = input("Care este numele dumneavoastra? ")
                        real_town = input("Care este orasul in care locuiti? ")
                        phone_number = input("Introduceti numarul de telefon: ")
                        if ((real_name == client['nume'] and real_town == client['oras'])
                                and phone_number == client['telefon']):
                            new_pass = input("Scrieti noua parola: ")
                            confirm_pass = input("Repetati noua parola: ")
                            if new_pass == confirm_pass:
                                credentials[user_name] = caesar.encrypt(new_pass)
                                with open(path, "w") as f:
                                    f.write(json.dumps(credentials, indent=4))
                                break
                case _:
                    continue

    return user_name


def get_all_clients(path: str = "clients.json") -> list:
    with open(path, "r") as f:
        clients = json.loads(f.read())
        clients = clients['clients']
    return clients


def get_client(username: str, path: str = "clients.json", clients: list | None = None) -> dict:
    if not clients:
        with open(path, "r") as f:
            clients = json.loads(f.read())
            clients = clients['clients']
    for client in clients:
        if username == client['id']:
            return client
    return {}


def change_pass(user_name: str, path: str = "auth.json"):
    with open(path, "r") as f:
        credentials = json.loads(f.read())

    while True:
        old_pass = input("Scrieti parola veche: ")
        if caesar.encrypt(old_pass) == credentials[user_name]:
            new_pass = input("Scrieti noua parola: ")
            confirm_pass = input("Repetati noua parola: ")
            if new_pass == confirm_pass:
                credentials[user_name] = caesar.encrypt(new_pass)
                with open(path, "w") as f:
                    f.write(json.dumps(credentials, indent=4))
                print("\n\nPassword was changed !!")
                break


if __name__ == '__main__':

    MENU = """
        1. Adauga client
        2. Sing out
        3. Schimba parola
        4. Arata parola
        5. Exit
        Pick: """

    user_name = login()

    user_pick = input(MENU)

    while user_pick.lower() != "exit":
        if user_pick in ["1", "2", "3", "4", "5"]:
            match user_pick:
                # add clients
                case "1":
                    if user_name == "admin":
                        client_info = input("Introduceti datele in ordinea data "
                                            "(nume, telefon, oras, balanta): ")
                        client_info = client_info.split()
                        new_client = {"nume": client_info[0], "telefon": client_info[1],
                                      "oras": client_info[2], "balanta": int(client_info[3])}
                        add_client(new_client, "clients.json")
                    else:
                        print("Nu ai autorizatie!!!")
                # Log Out
                case "2":
                    user_name = login()
                # Change pass
                case "3":
                    change_pass(user_name)
                # Show pass
                case "4":
                    with open("auth.json", "r") as f:
                        credit = json.loads(f.read())
                    clients = get_all_clients()
                    if user_name == "admin":
                        for client in clients:
                            id_client = client['id']
                            print(f"Dl/D-na {client['nume']} are parola {caesar.decrypt(credit[id_client])}")
                    else:
                        print(f"Parola dumneavoastra este : {caesar.decrypt(credit[user_name])} ")
                # Exit
                case "5":
                    exit()
        else:
            print("Nu ati introdus un numar din lista curenta .")

        print("\n")
        user_pick = input(MENU + " ")
