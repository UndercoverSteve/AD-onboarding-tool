from adtool.graph_client import get_client
from adtool.users import create_user
from adtool.users import get_people
from adtool.prompts import prompt_new_user

def menu():
    while True:
        print("M365 Onboarding CLI\n1) Onboard new user (no license yet)\n2) List first 10 users\nq) Quit")
        user_input = input("Choose: ")
        user_input = user_input.lower()
        if user_input == "1":
            user_dict = prompt_new_user()
            if user_dict is None:
                continue
            # Onboard new people.
            create_user(user_dict)
            # Loop back to menu.
        elif user_input == "2":
            get_people()
        elif user_input == "q":
            return None
        else:
            print("Wrong input, try again.")

menu()