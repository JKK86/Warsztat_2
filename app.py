from clcrypto import check_password
from models import User
import psycopg2.errors


def create_user():
    user_name_input = input("Podaj nazwę użytkownika: ")
    password_input = input("Podaj hasło (min. 8 znaków): ")
    if len(password_input) < 8:
        print("Podane hasło jest za krótkie")
    else:
        try:
            user = User(user_name_input, password_input)
            user.save_to_db()
            print("Dodano użytkownika")
        except psycopg2.errors.UniqueViolation:
            print(f"Użytkownik {user_name_input} już istnieje")

def change_password():
    user_name_input = input("Podaj nazwę użytkownika: ")
    password_input = input("Podaj hasło: ")
    user = User.load_user_by_username(user_name_input)
    if not user:
        print("Podany użytkownik nie istnieje")
    elif check_password(password_input, user.hashed_password) == True:
        new_password = input("Podaj nowe hasło (min. 8 znaków): ")
        if len(new_password) < 8:
            print("Podane hasło jest za krótkie")
        else:
            user.hashed_password = new_password
            print("Ustawiono nowe hasło")
    else:
        print("Niepoprawne hasło")

def list_users():
    users = User.load_all_users()
    for user in users:
        print(user.username)
    print()

def delete_user():
    user_name_input = input("Podaj nazwę użytkownika: ")
    password_input = input("Podaj hasło: ")
    user = User.load_user_by_username(user_name_input)
    if not user:
        print("Podany użytkownik nie istnieje")
    elif check_password(password_input, user.hashed_password) == True:
        user.delete()
        print('Usunięto użytkownika')
    else:
        print("Niepoprawne hasło")

def main():
    while True:
        try:
            user_choice = int(input("""Wybierz polecenie:
            1 - tworzenie użytkownika,
            2 - edycja hasła użytkownika,
            3 - usuwanie użytkownika,
            4 - listowanie użytkowników,
            5 - zakończ program.
            """))

            if user_choice == 1:
                create_user()
            elif user_choice == 2:
                change_password()
            elif user_choice == 3:
                delete_user()
            elif user_choice ==4:
                list_users()
            elif user_choice == 5:
                break
            else:
                print('Nieprawidłowe polecenie')
        except ValueError:
            print('Nieprawidłowa wartość')

if __name__ == '__main__':
    main()