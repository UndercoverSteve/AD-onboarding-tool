from adtool import licenses

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

def prompt_sku_choice(user_id: str) -> dict:
    skus = licenses.list_skus(False)

    assigned_licenses = licenses.get_user_licenses(user_id)
    
    print("Select which SKUs you would like enabled for this user.")

    skus_to_choose = []

    # is_sku_currently_assigned = if sku was enabled before function call
    # should_assign_sku = assign sku with this function
    for sku in skus:
        sku["should_assign_sku"] = False
        sku["is_sku_currently_assigned"] = False

    # Check if license is already assigned
    for sku in skus:
        for assigned_license in assigned_licenses:
            if sku["skuId"] == assigned_license["skuId"]:
                sku["is_sku_currently_assigned"] == True
                sku["should_assign_sku"] == True

    def display_all_skus():
        sku_index = 0
        for sku in skus:
            sku_index += 1
            part_number = sku["skuPartNumber"]
            units_enabled = sku["prepaidUnits"]["enabled"]
            units_consumed = sku["consumedUnits"]

            sku_enabled = sku["should_assign_sku"]
            
            sku_enabled_text = " "

            sku_seats_used_after = ""

            if sku_enabled == True:
                sku_enabled_text = "X"

                if sku["is_sku_currently_assigned"] is False:
                    sku_seats_used_after = f" ({units_consumed + 1}) "
            elif sku_enabled == False:
                sku_enabled_text = " "

                if sku["is_sku_currently_assigned"] is True:
                    sku_seats_used_after = f" ({units_consumed - 1}) "

            print(f"{sku_index}) [{sku_enabled_text}] {part_number}: {units_consumed}{sku_seats_used_after}/{units_enabled} seats used")

    def toggle_sku(usr_prmpt_index: int):
        sku_index = 0
        for sku in skus:
            sku_index = sku_index + 1

            if sku_index == usr_prmpt_index:
                # Found user chosen sku!

                # Check to make sure amount of skus isn't at max. If it's at max break fail
                if (sku["prepaidUnits"]["enabled"] - sku["consumedUnits"]) <= 0 and sku["should_assign_sku"] == False:
                    print(sku["prepaidUnits"]["enabled"] - sku["consumedUnits"])
                    print("Max limit of this SKU is reached. Free up a license to assign to this user.")
                    break

                # Toggle SKU
                sku["should_assign_sku"] = not sku["should_assign_sku"]

    display_all_skus()

    while True:
        usr_prmpt_index = prompt_nonempty("Select SKU to enable for user. Type 'EXIT' to stop. ")
        if usr_prmpt_index == "EXIT" or usr_prmpt_index == "exit":
            # Go to next menu.
            return skus
        
        elif usr_prmpt_index.isdigit():
            usr_prmpt_index = int(usr_prmpt_index)
            toggle_sku(usr_prmpt_index)
        display_all_skus(False)

