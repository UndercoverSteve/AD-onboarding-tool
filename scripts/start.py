from adtool.graph_client import get_client
from adtool import users
from adtool.prompts import prompt_new_user
from adtool.licenses import list_skus

def menu():
    while True:
        print("M365 Onboarding CLI\n1) Onboard new user \n2) List first 10 users\n3) List available SKUs\n4) User manager \nq) Quit")
        user_input = input("Choose: ")
        user_input = user_input.lower()
        if user_input == "1":
            users.onboard_user_flow()
            # Loop back to menu.
        elif user_input == "2":
            print(users.get_people())
        elif user_input == "3":
            list_skus()
        elif user_input == "4":
            users.people_manager()
        elif user_input == "q":
            return None
        else:
            print("Wrong input, try again.")

menu()