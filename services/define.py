import pandas as pd
from helpers.helper import inventory_data_list

# Insert new items
def insert_item(role:str) -> None:
    print("\nYou are now at: ▶ Insert Items (Admin only) ◀")
    file_dir="inventory.csv"
    # Initialize
    product_info="" # This variable is to accept input
    datalist={
                'Code': [],
                'Description': [],
                'Category': [],
                'Unit': [], 
                'Price': [],
                'Quantity': [],
                'Minimum': []
            } # This list is to store data temporarily
    
    # Only the admin can access
    access_allowed=("admin",) # Only admin can access

    # While loop is used so user can bulk import items
    while True:   
        if role not in access_allowed: # Check permission
            print("REJECTED: You have no permission to access this, please login again!")
            break # Return to main menu
            
        try:
            # Collect the item codes into a list
            print('\nPlease enter all the information based on the format below\nFORMAT: <Code>,<Description>,<Category>,<Unit>,<Price>,<Quantity>,<Minimum>')
            print("EXAMPLE: 10000,Milk 1L,Dairy,box,7.00,30,35\n")
            print("Type 'q' to return back to main menu")
            product_info=input('Please enter all the information of this product: ').split(",")

            if len(product_info)==1 and "q" in product_info: # If user choose to exit
                break

            # Check if 7 details in the input
            if len(product_info) !=7:
                raise Exception ("Invalid input format! Please enter according to format.")

            # Check if item code is 5 digit number
            if not product_info[0].strip().isdecimal() or not len(product_info[0].strip())==5:
                raise Exception ("Please enter a 5 digit number for item code.")
            else:
                # Check if item code is unique
                test_df=inventory_data_list()
                test_df_Code=test_df[test_df['Code']==str(product_info[0])]
                if not test_df_Code.empty:
                    raise Exception ("The item code must be unique")
            
            if not product_info[1].strip(): # Check description if empty
                raise Exception ("Description is empty, please enter the description for this product.")
            
            if not product_info[2].strip(): # Check category if empty
                raise Exception ("Cateogry is empty, please enter the category for this product")
            
            if not product_info[3].strip(): # Check Unit if empty
                raise Exception ("Unit is empty, please enter the Unit of this product.")
            
            # Try convert Price to 2 decimal, or throw error
            try: 
                product_info[4]='%.2f' % float(product_info[4].strip())
            except:
                raise Exception ("Price must be number.")
                
            #Check if quanity is positive integer
            if not product_info[5].strip().isdecimal():
                raise Exception ("Quantity must be positive integer.")
            
            #Check if minimum is positive integer
            if not product_info[6].strip().isdecimal():
                raise Exception ("Minimum must be positive integer.")

            # Save temporarily in a list
            datalist["Code"].append(product_info[0])
            datalist['Description'].append(product_info[1])
            datalist['Category'].append(product_info[2])
            datalist["Unit"].append(product_info[3])
            datalist['Price'].append(product_info[4])
            datalist['Quantity'].append(product_info[5])
            datalist['Minimum'].append(product_info[6])
            
            if input("Type 'y' to continue adding new item, or any other character to submit: ") =='y': 
                continue # If user want to continue add other items, loop again
            else: # If user doesn't want to add other items
                new_df=pd.DataFrame(datalist)
                new_df.to_csv(file_dir, mode='a', index=False, header=False)
                print("Insert new items successfully! ")
                break # Return back to main menu after finish adding items

        except Exception as e:
            print("\nERROR:",e)

    print("\nEXIT insert item function")

# Update details of items
def update_item(role:str) -> None:
    # Initialization
    file_dir="inventory.csv" # Locate the txt file directory
    access_allowed=("admin",) # Only admin can add new user
    code=change=""
    d={
        "1": "Code",
        "2": "Description",
        "3": "Category",
        "4": "Unit",
        "5": "Price", 
        "6": "Quantity",
        "7": "Minimum"
    }
    
    print("\nYou are now at: ▶ Update Items (Admin only) ◀\n")

    # Below will be repeated until user requests to exit
    while True:
        data_ls=inventory_data_list()
        code_ls=list(data_ls['Code'])
        #check if user is admin
        if role not in access_allowed:
            print("REJECTED: You have no permission to access this, please login again!")
            break
        else:
            try:
                print(data_ls.to_string(index=False))
                print("\nAbove are the existing records\n\ntype 'q' to return back to main menu. ")

                #Request to input item code only when it's empty
                if not code:
                    code=input("Specify the item's code which you would like to update: ").strip()

                # If user choose to quit
                if code=="q":
                    break
                # Check if the input item code exist
                if str(code) not in code_ls:
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
                row = code_ls.index(code)
                column = d[change]

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
                    data_ls.loc[row, d[change]] =str(new_value)
                    
                    # Update the changes with the list
                    data_ls.to_csv(file_dir, mode='w', index=False)
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

# Delete items
def delete_item(role:str) -> None:
    # Initialization
    file_dir = "inventory.csv"
    access_allowed = ["admin"] #Only admins allowed to access this function
    code = ""

    while True:
        data_ls=inventory_data_list()
        code_ls=list(data_ls['Code'])

        # Access check
        if role not in access_allowed: 
            print("You do not have permissions to access this. Please login again.")
            break
        else:
            # Items display and formatting
            print("You are now at: ▶ Delete Item (Admin only) ◀\n")
            print(data_ls.to_string(index=False))
            
            try:
                # Displaying available actions
                print("\nAbove are existing records\n\nType 'q' to return back to main menu. ")
                
                code = input("Which item would you like to delete? (Input item code): ").strip()
                if code == "q":
                    break
                if code not in code_ls:
                    code = ""
                    raise Exception("This item is not found. ")
                
                # Confirmation for deletion and deletion process
                if input(f"\nType 'y' to confirm, or any other characters to discard\nDelete {code}?(y): ").lower().strip() == "y":
                    new_data_ls=data_ls[data_ls['Code']!=code]
                    new_data_ls.to_csv(file_dir, mode='w', index=False)
            
                    # Deletion completed
                    print("\nItem with code {} has been successfully deleted.\n".format(code))
                    code = ""
                    print("Type 'y' to delete another item, other characters to quit. ")
                    if input("Delete another item (y) or exit? ").lower().strip() =="y": 
                        print("\n\nYou are now at: ▶ Delete Item (Admin only) ◀")
                        continue
                    else: 
                        break
                else:
                    print("\nDISCARDED\n")
                    continue
            
            # Error handler
            except Exception as e:
                print("\n\nERROR:",e, "\n")
                continue
    print("\nEXIT delete item function")