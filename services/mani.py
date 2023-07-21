from helpers.helper import inventory_data_list

# Stock taking - confirm and change quantity of items
def stock_taking(role:str) -> None:
    #Initialize
    file_dir="inventory.csv" #Locates text file directory
    access_allowed=("admin","inventory-checker") # Only admin and inventory-checker can perform stock-taking
    data_ls=[]
    updated_data_ls=[]

    #Welcome message
    print("\nYou are now at: ▶ Stock Taking ◀\n")
    
    # Validate user type
    while True: 
        if role not in access_allowed: #check if user is admin
            print("REJECTED: You have no permission to access this, please login again!")
            break 
        try:
            # Get item 2D list
            data_ls=inventory_data_list()

            # Display existing inventory
            print("Below are the existing inventory:")
            print(data_ls[['Code', 'Description']].to_string(index=False))

            print("\nTo check the stock, first you need to enter an item code.")
            print("Type 'q' to go back to main menu.")

            ItemCode=input("\nPlease enter the item code: ").strip() #input 5 digit item code

            #If user wants to go back to main menu
            if ItemCode=="q":
                break #returns to main menu
            quantity=data_ls[data_ls['Code']==ItemCode]['Quantity']

            #checks for the specific row in the txt file
            for row in range(len(data_ls)): 
                if str(data_ls["Code"][row])==str(ItemCode): #check if input is in csv file 
                    print(f"Quantity for item code {ItemCode} is {data_ls['Quantity'][row]}") #prints the specific quantity for the item code that 
                    
                    #Ask user if quantity needs to be changed
                    QuantityChange = input("\nType 'y' to change the quantity: ").strip()
                    if QuantityChange == "y": #check if input is 'y' to change quantity
                        NewQuantity = input(f"Please enter new quantity for item code {ItemCode}: ").strip() 

                        #check if input is a positive integer
                        if not NewQuantity.isdecimal():
                            raise Exception("Quantity must be positive integer") 
                        data_ls.loc[row, 'Quantity'] = NewQuantity

                        # Updates the new quantity to the specific item code in the txt file
                        data_ls.to_csv(file_dir, index=False, mode='w')
                        print(f"\nSUCCESS: Quantity for item code {data_ls['Code'][row]} has been updated to {data_ls['Quantity'][row]}\n")
                        break #returns to item code selection after made changes to quantity in file
                    else:
                        print("No change")
                        break #returns back to item code selection
            else: # If can't find the input item code until the end of file
                raise Exception("Item code not exists") 
        except Exception as e:
            print("\nERROR:",e)

    print("EXIT Stock-taking")

# Stock replenishment - Add newly purchased items (increase quantity in stock)
def stock_replenishment(role:str) -> None:
    #Initialize
    file_dir="inventory.csv" #Locates text file directory
    access_allowed=("admin","purchaser") # Only admin and purchaser can perform stock-replenishment
    data_ls=[]
    updated_data_ls=[]

    #Welcome message
    print("\nYou are now at: ▶ Stock Replenishment ◀\n")
    
     # Validate user type
    while True: 
        if role not in access_allowed: #check if user is admin
            print("REJECTED: You have no permission to access this, please login again!")
            break 
        try:
            # Get item 2D list
            data_ls=inventory_data_list()

            # Display existing inventory
            print("Below are the existing inventory:")
            print(data_ls[['Code', 'Description']].to_string(index=False))

            print("\nTo add the stock, first you need to enter an item code.")
            print("Type 'q' to go back to main menu.")

            ItemCode=input("\nPlease enter the item code: ").strip() # input 5 digit item code

            #If user wants to go back to main menu
            if ItemCode=="q":
                break # returns to main menu
            
            quantity=data_ls[data_ls['Code']==ItemCode]['Quantity']

            #checks for the specific row in the txt file
            for row in range(len(data_ls)): 
                if str(data_ls["Code"][row])==str(ItemCode): #check if input is in txt file 
                    print(f"Quantity for item code {ItemCode} is {data_ls['Quantity'][row]}") #prints the specific quantity for the item code that 
                    
                    print("\nType 'b' to go back")
                    QuantityIncrease = input(f"Please enter quantity to add to current amount for item code {ItemCode}: ").strip() 

                    if QuantityIncrease=="b":
                        print("No change") 
                        break # return to item code selection
                    #check if input is a positive integer
                    if not QuantityIncrease.isdecimal():
                        raise Exception("Quantity must be positive integer") 
                    data_ls.loc[row, 'Quantity'] = str(int(data_ls['Quantity'][row])+int(QuantityIncrease))

                    data_ls.to_csv(file_dir, index=False, mode='w')
                    print(f"\nSUCCESS: Quantity for item code {data_ls['Code'][row]} has been updated to {data_ls['Quantity'][row]}\n")
                    break # return to item code selection after made changes to quantity in file
                    
            else: # If can't find the input item code until the end of file
                raise Exception("Item code not exists") 
        except Exception as e:
            print("\nERROR:",e)

    print("EXIT Stock-replenmishment")

# View insufficient items
def view_replenish_list(role:str) -> None:
    # Initialization
    access_allowed=("admin", "purchaser") # Only admin and purchaser can acceess
    data_list = []

    print("You are now at ▶ View Replenish List ◀\n")
    print("Please replenish items below:\n")
    
    # Check user's role
    if role not in access_allowed:
        print("REJECTED: You have no permission to access this, please login again!")
    else:
        # Get items 2D List
        data_list=inventory_data_list()

        # Display items with quantity lower than minimum
        df_lower=data_list[data_list['Quantity'].astype(int) < data_list['Minimum'].astype(int)]
        print(df_lower.to_string(index=False))

        # Return to main menu after user finish reading
        input("Type any character to exit after finish reading: ")
    print("Exit view replenish list")

# Search for items in the record
def search_items(role:str) -> None:
    #Initialize
    access_allowed=("admin","inventory-checker", "purchaser") # Only admin and inventory checker can search items
    data_ls=[]

    #Welcome message
    print("\nYou are now at: ▶ Search Items ◀\n")
    
    # Validate user type
    while True: 
        if role not in access_allowed:
            print("REJECTED: You have no permission to access this, please login again!")
            break 
        try:
            # Get items 2D List
            data_ls=inventory_data_list()
 
            print("\nTo search items, please choose which method you want to use to search your required items \n 1.Description \n 2.Code range \n 3.Category \n 4.Price ")
            print("Type 'q' to go back to main menu.")

            # Let user to choose a method
            Method=input("\nPlease enter the method number: ")

            if Method.strip()=="q": # User requests to exit
                break #returns to main menu
            elif Method.isdecimal() and 0<int(Method)<=4: # If user enter a valid option
                found=False
                if Method.strip()=="1": # Search using description
                    Description = input("Please input the item's description: ").strip()

                    # Display item list
                    q_result=data_ls[data_ls['Description']==Description]
                    if q_result.empty:
                        raise Exception("Item not found! ")
                    print(q_result.to_string(index=False))

                elif Method.strip()=="2": # Search using item code range
                    print("Enter item code range separated by '~'")
                    print("Format: <initial>~<final>")
                    print("Example: 30000~39999")
                    CodeRange=input("Please enter item code range based on format: ").strip().split("~")
                    if len(CodeRange)!=2: # If wrong input format
                        raise Exception("Please enter input based on format!")
                    
                    # If item code is in invalid format
                    elif not CodeRange[0].isdecimal() or not CodeRange[1].isdecimal() or len(CodeRange[0])!=5 or len(CodeRange[1])!=5:
                        raise Exception("Please enter 5-digit item code for both initial and final!")
                        
                    elif int(CodeRange[0])>int(CodeRange[1]): # If initial smaller than final
                        raise Exception("Initial must be smaller than final!")
                    
                    # Display item list
                    min=int(CodeRange[0])
                    max=int(CodeRange[1])+1

                    q_result=data_ls[data_ls['Code'].astype(int).between(min, max, inclusive="both")]

                    if q_result.empty:
                        raise Exception("Item cannot be found")
                    print(q_result.to_string(index=False))

                elif Method.strip()=="3": # Search using item category
                    Category = input("Please input the item category: ").strip()

                    # Display item list
                    q_result=data_ls[data_ls['Category']==Category]

                    if q_result.empty:
                        raise Exception("Item cannot be found")
                    print(q_result.to_string(index=False))

                elif Method.strip()=="4": # Search using price range
                    print("Enter the item price range\nWARNING: All prices will be rounded to 2 decimal")
                    try:
                        min="%.2f" % (float(input("Price min: "))) # Convert to 2 decimal
                        max="%.2f" % (float(input("Price max: "))) # Convert to 2 decimal
                    except ValueError: # If entered values are not number
                        raise Exception("Price must be number!")
                    
                    # Display item list
                    print(f"Items with price range {min} and {max}\n")
                    q_result=data_ls[data_ls['Price'].astype(float).between(float(min), float(max), inclusive="both")]

                    if q_result.empty:
                        raise Exception("Item cannot be found")
                    print(q_result.to_string(index=False))
            else:
                raise Exception("Invalid option!")
        except Exception as e:
            print("\nERROR:",e)

    print("EXIT search item")