import json

import credientials


if __name__ == '__main__':

    MENU = """
        1. Adauga client
        2. Sing out
        3. Schimba parola
        4. Arata parola
        5. Exit
        Pick: """

    user_name = credientials.login()

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
                        credientials.add_client(new_client, "clients.json")
                    else:
                        print("Nu ai autorizatie!!!")
                # Log Out
                case "2":
                    user_name = credientials.login()
                # Change pass
                case "3":
                    credientials.change_pass(user_name)
                # Show pass
                case "4":
                    with open("auth.json", "r") as f:
                        credit = json.loads(f.read())
                    clients = credientials.get_all_clients()
                    if user_name == "admin":
                        for client in clients:
                            id_client = client['id']
                            print(f"Dl/D-na {client['nume']} are parola "
                                  f"{credientials.caesar.decrypt(credit[id_client])}")
                    else:
                        print(f"Parola dumneavoastra este : {credientials.caesar.decrypt(credit[user_name])} ")
                # Exit
                case "5":
                    exit()
        else:
            print("Nu ati introdus un numar din lista curenta .")

        print("\n")
        user_pick = input(MENU)