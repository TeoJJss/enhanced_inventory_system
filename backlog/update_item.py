"""
Script to update items
"""

def update_item(role: str) -> None:
    # Assume item code's format is 5-digit numbers and unique
    # Assume that "inventory.txt" is placed in the same directory as this file
    # Assume that price must be in 2 decimal format
    # Assume that the data entered accurately reflects the actual situation
    # Validation on the format of the data only, not the reliability

    # Initialization
    file_dir="inventory.txt" # Locate the txt file directory
    access_allowed=("admin",) # Only admin can add new user
    code=change=""
    d={
        "1": "Item code (MUST be 5 digits)",
        "2": "Description",
        "3": "Category",
        "4": "Unit",
        "5": "Price", 
        "6": "Quantity",
        "7": "Minimum (Threshold)"
    }
    
    print("\nYou are now at: ▶ Update Items (Admin only) ◀\n")

    # Below will be repeated until user requests to exit
    while True:
        data_ls=[]
        code_ls=[]
        #check if user is admin
        if role not in access_allowed:
            print("REJECTED: You have no permission to access this, please login again!")
            break
        else:
            # Get all records out from txt file
            with open(file_dir, "r") as inventory_file:
                # Display records from txt file in a neat format
                print("{:10} {:20} {:15} {:10} {:10} {:10} {:10}".format(*["Code", "Description", "Category", "Unit", "Price", "Quantity", "Minimum (Threshold)"]))
                print("---"*35)
                for line in inventory_file:
                    print("{:10} {:20} {:15} {:10} {:10}\t{:10}\t{:10}".format(*(line.strip().split("\t")))) # Specify field size for each column
                
                # Save each line into a list
                inventory_file.seek(0)
                data_ls=inventory_file.readlines()

            # Convert to 2D list
            for ind, data in enumerate(data_ls):
                data_ls[ind]=data.rstrip().split("\t")
            # Save item code into a new list
            for line in data_ls:
                code_ls.append(line[0])

            try:
                print("\nAbove are the existing records\n\ntype 'q' to return back to main menu. ")

                #Request to input item code only when it's empty
                if not code:
                    code=input("Specify the item's code which you would like to update: ").strip()

                # If user choose to quit
                if code=="q":
                    break
                # Check if the input item code exist
                if code not in code_ls:
                    code=""
                    raise Exception("The item code is not found! ")

                # Request user to choose what to update for the item code's row
                print("\nWhat do you wish to update?")
                for key, col in d.items():
                    print(f"\t\tType {key} for {col}")
                print("""
                Type b to go back item list
                Type q to go back main menu\n
                """)
                print(f"You're now updating - {code}")
                change=input("Your option: ").strip()

                # Check if user want to quit or go back to main menu
                if not change.isdecimal():
                    if change=="b":
                        code="" # Reset item code to empty
                        print("\nBACK to item list\n")
                        continue
                    elif change=="q":
                        break
                    else:
                        raise Exception("Invalid Option!\n")

                # Check if option is valid
                elif int(change) not in range(1,8):
                    raise Exception("Invalid option!\n")
                
                # Locate the element to change
                row=code_ls.index(code)
                column=int(change)

                print(f"\n\nYou're now changing the item code: {code}, for its {d[change]}")
                print("[Enter 'b' to go back item list]")
                new_value=input("New value: ").strip()
                
                if new_value != "b":
                    # Data validation
                    if change=="1": # If request to change item code
                        if new_value in code_ls: # Code must be unique
                            raise Exception("Item code must be unique!\nThe new Code is either the same with the previous, or conflicts with other items' code.\n")
                        elif len(new_value) != 5 or not new_value.isdecimal(): # Code must contain 5 digits
                            raise Exception("Item code must be 5 digits!\n")
                        code=new_value
                    elif change in ["2", "3", "4"]: # If request to change description/category/unit
                        if not new_value.strip(): # Description cannot be changed to empty
                            raise Exception(f"{d[change]} cannot be empty!\n")
                    elif change in ["5", "6", "7"]: # If request to change Price/Quantity/Minimum
                        # Price/Quantity/Minimum must be number
                        try:
                            float(new_value)
                        except:
                            raise Exception(f"{d[change]} must be a number! \n")
                        
                        # Price will be converted to 2 decimal automatically
                        if change=="5":
                            new_value="%.2f" % float(new_value)
                        # Quantity and Minimum must be integer
                        else:
                            try:
                                new_value=int(new_value)
                            except: # Error if user input decimal
                                raise Exception(f"{d[change]} must be integer! \n")

                        
                    # If pass all check, change the value in the list        
                    data_ls[row][column-1]=str(new_value)
                    
                    # Update the changes with the list
                    with open(file_dir, "w") as inventory_file:
                        for row in data_ls:
                            if data_ls.index(row) != 0: # After writing each row, break line
                                inventory_file.write("\n")
                            for column in row: # Use TAB to separate columns
                                inventory_file.write(str(column)+"\t")
                        print("\nUPDATED SUCESSFULLY\n")
                    
                    # Ask if user want to continue updating the same item code or new item code
                    if input(f"Type 'y' to continue updating other details for {code},\nor any other characters to switch: ").strip().lower()=='y':
                        print("\nYou are now at: ▶ Update Items (Admin only) ◀\n")
                        continue
                    else:
                        print("\nYou are now at: ▶ Update Items (Admin only) ◀\n")
                        code="" # Reset item code to empty
                        continue
                else:
                    print("\nBACK to item list\n")

            # Error handler
            except Exception as e:
                print("\n\nERROR:",e, "\n") # Display error message
                continue
    print("\nEXIT update item function")

update_item(role="admin")