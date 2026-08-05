def prompt_nonempty(label: str) -> str:
    user_input = input(label).strip()
    while user_input == "":
        print("Input cannot be nothing! Try again.")
        user_input = input(label).strip()
    return user_input

def prompt_upn(label: str) -> str:
    user_input = prompt_nonempty(label)
    while not ("@" in user_input and "." in user_input.split("@")[1]):
        print("Email address not formatted correctly. Try again.")
        user_input = prompt_nonempty(label)
    return user_input

def prompt_yn(label: str) -> bool:
    user_input = prompt_nonempty(label).lower()
    while not (user_input == "y" or user_input == "n"):
        print("Input must be y or n, try again")
        user_input = prompt_nonempty(label).lower()
    if user_input == "y":
        user_approval = True
    elif user_input == "n":
        user_approval = False
    return user_approval



def prompt_new_user() -> dict:
    first_name = prompt_nonempty("What is the user's first name? ")
    last_name = prompt_nonempty("What is the user's last name? ")
    department = prompt_nonempty("What is the user's department? ")
    job_title = prompt_nonempty("What is the user's job title? ")
    manager_upn = prompt_upn("What is the user's manager's email address? ")

    user_dict = {
        "first_name": first_name,
        "last_name": last_name,
        "department": department,
        "job_title": job_title,
        "manager_upn": manager_upn,
    }

    print("First name: " + first_name + "\nLast name: " + last_name + "\nDepartment: " + department + "\nJob title: " + job_title + "\nManager's email address: " + manager_upn)

    check_correct = prompt_yn("Does this look correct? Y/N: ")
    if check_correct:
        return user_dict
    else:
        if prompt_yn("Would you like to try again? Y/N: "):
            return prompt_new_user()
        else:
            return None