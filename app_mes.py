from clcrypto import check_password
from models import Messages, User


def list_messages():
    user_name_input = input("Podaj nazwę użytkownika: ")
    password_input = input("Podaj hasło: ")
    user = User.load_user_by_username(user_name_input)
    if not user:
        print("Podany użytkownik nie istnieje")
    elif check_password(password_input, user.hashed_password):
        messages = Messages.load_all_messages()
        print(f'Wiadomości do użytkownika {user.username}:')
        for message in messages:
            if message.to_id == user.id:
                sender = User.load_user_by_id(message.from_id)
                print(100 * '-')
                print(f"Od: {sender.username}")
                print(f"Data: {message.creation_data}")
                print(f"'{message.text}'")
                print(100 * '-')
        print()
    else:
        print("Niepoprawne hasło")


def send_message():
    user_name_input = input("Podaj nazwę użytkownika: ")
    password_input = input("Podaj hasło: ")
    user = User.load_user_by_username(user_name_input)
    if not user:
        print("Podany użytkownik nie istnieje")
    elif check_password(password_input, user.hashed_password):
        addresser_input = input("Podaj adresata: ")
        to_user = User.load_user_by_username(addresser_input)
        if not to_user:
            print("Podany użytkownik nie istnieje")
        else:
            text = input("""Podaj treść wiadomości:""")
            if len(text) > 255:
                print("Wiadomośc jest za długa")
                return
            message = Messages(user.id, to_user.id, text)
            message.save_to_db()
            print("Wysłano wiadomość")
    else:
        print("Niepoprawne hasło")


def app_mes():
    while True:
        try:
            user_choice = int(input("""Wybierz polecenie:
                1 - wysyłanie wiadomości,
                2 - listowanie wiadomości,
                3 - zakończ program.
                """))

            if user_choice == 1:
                send_message()
            elif user_choice == 2:
                list_messages()
            elif user_choice == 3:
                break
            else:
                print('Nieprawidłowe polecenie')
        except ValueError:
            print('Nieprawidłowa wartość')


if __name__ == '__main__':
    app_mes()
