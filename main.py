from datetime import datetime
from helpers.helper import *
from services.define import *
from services.mani import *
from services.users import *

# Main controller function
def main() -> None: 
    role=""
    auto=True
    # Access control
    option_ls={
            "admin": ["insert_item", "update_item", "delete_item", "stock_taking", 
                      "view_replenish_list", "stock_replenishment", "search_items", "add_user"],
            "inventory-checker": ["stock_taking", "search_items"],
            "purchaser": ["view_replenish_list", "stock_replenishment", "search_items"]
            }
    # Welcome message
    print("\nWelcome to ▶ GROCERY STORE INVENTORY SYSTEM ◀\n")
    while True:
        # Login
        if not role:
            role=user_authentication()
            auto=True
        
        if auto: # This should only do one time for each login
            # If user is inventory checker and the time is end of business day, execute stock taking automatically
            if role=="inventory-checker" and int(datetime.now().strftime("%H"))>=20:
                print("\nYou are inventory checker and now is the end of business day")
                print("ALERT: Please perform stock-taking")
                stock_taking(role)

            # If user is purchaser and the time is end of business day, execute stock taking automatically
            elif role=="purchaser" and int(datetime.now().strftime("%H"))>=20:
                print("\nYou are purchaser and now is the end of business day")
                print("ALERT: Please view replenish list")
                view_replenish_list(role)
            auto=False 

        try:
            # Display list options
            print("\nYou are now at: ▶ Main Menu ◀\n")
            if role in option_ls.keys():
                for ind in range(len(option_ls[role])):
                    option=option_ls[role][ind].split("(")[0].replace("_", " ").title()
                    print(f"Type {ind+1} to {option}")
            # Invalid role
            else:
                raise Exception("Invalid role!")

            # Display logout and exit options
            print("\nType 'e' to exit the system\nType 'l' to logout")
            # User input
            inp=input("\nPlease enter your option: ")

            # Exit
            if inp.strip()=="e":
                print("\nEXIT GROCERY STORE INVENTORY SYSTEM")
                exit()
            # Logout
            elif inp.strip()=="l":
                role=""
                print("\nLog Out")
                continue
            # Execute option's function
            elif inp.strip().isdecimal() and 0<int(inp)<=len(option_ls[role]):
                eval(option_ls[role][int(inp)-1]+"(role)")
            # Error
            else:
                raise Exception("Invalid option!")
            
        # Display error
        except Exception as e:
            print("ERROR:", e)

# This system will not run automatically if it's imported as module in another file
if __name__=='__main__':
    main()