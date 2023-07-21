import pandas as pd

# Register new user into the record
def add_user(role:str) -> None: 
    # Initialization
    file_dir="userdata.csv"
    user_info=""
    access_allowed=("admin",) # Only admin can add new user

    # Welcome message
    print("\nYou are now at: ▶ Add New User (Admin only) ◀\nTo add a new user, you need to specify username, password and user type. Please type these data separated by comma(,)\nMinimum 8 characters required for password.\nWARNING: username and password are both case-sensitive and space-sensitive!\n")
    # Validate user type
    if role not in access_allowed:
        print("REJECTED: You have no permission to access this, please login again!")

    # If user is admin
    else:
        user_type_allowed=("admin", "inventory-checker", "purchaser") # 3 types of user allowed to input

        # Repeat asking user to input new user's details until request to exit
        while True:
            errors=[]
            #Guide user to input
            print("Format: <username>,<password>,<user_type>\nExample input: Ali,1234A@bc,purchaser\nTo return back to main menu, type 'q'\n")

            # Get new user's info 
            user_info=(input("Please enter new user's info: ").rstrip()).split(",")

            try:
                # Data validation
                # If user choose to exit
                if len(user_info)==1 and "q" in user_info:
                    break

                # If not 2 commas in the input
                if len(user_info) !=3:
                    raise Exception("Please input username, password and user type!")
                
                # If username is empty
                if len(user_info[0].strip())<1:
                    errors.append("Username cannot be empty!")
                
                # If password length not exceed 8
                if len(user_info[1])<8 :
                    errors.append("Password length must more than or equal to 8!")
                
                # If user type is invalid
                if user_info[2].lower().strip() not in user_type_allowed:
                    errors.append("Invalid user type!")

                if errors:
                    raise Exception(errors)

                # After data validation pass
                # Confirm with user before adding the data into txt
                username, password, user_type=user_info
                print(f"\n\nNew user info\nusername: {username.strip()}\t|\tpassword: {password}\t|\tuser_type: {user_type.lower().strip()}")
                print("\nType 'y' to confirm, or any other characters to discard")

                # If user confirmed, add data
                if input("Confirm? (y): ").lower().strip() == "y":
                    # Open file and append userdata
                    df=pd.read_csv(file_dir).astype(str)
                    if not (df[df['Username']==str(username)]).empty:
                        raise Exception("Username already exists! ")
                    tmp_df=pd.DataFrame({
                        'Username': [username],
                        'Password': [password],
                        'Role': [user_type]
                    })
                    tmp_df.to_csv(file_dir, mode='a', index=False, header=False)

                    # Ask user if want to add new user or exit
                    print("Type 'y' to add another user, other characters to quit. ")
                    if input("Add another user or exit?(y)").lower().strip() =="y": # If user request to continue adding new user
                        print("\n\nYou are now at: ▶ Add New User (Admin only) ◀")
                        continue
                    else: # If user request to exit
                        break
                
                # If user choose to discard data
                else:
                    print("\nDISCARDED\n")
                    continue 

            # Error handler
            except Exception as e:
                user_info="" # user info reset if any error is found
                print("\n\nERROR:",e, "\n")
    
    # Code below will be run if user choose to exit and the loop breaks
    print("\nEXIT add user function\n")