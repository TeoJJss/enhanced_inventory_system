import pandas as pd

# Login authentication to user
def user_authentication() -> str:
    # Initialize
    filename="userdata.csv"
    credentials=username=password=""
    print("LOGIN AUTHENTICATION\nPlease login using your username and password.")
    print("WARNING: username and password are case-sensitive")
    while True:
        # Opening file and taking credentials from file
        credentials=pd.read_csv(filename).astype(str)

        # Asking for user input
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        q=credentials.loc[
            (credentials['Username']==username) & 
            (credentials['Password']==password)
            ]
        if not q.empty:
            role = q['Role'].to_string(index=False)
            print("Authentication successful. User is a(n)", role)
            return role
        else:
            print("Authentication failed! Incorrect password or username, please login again.")

# Read the records in the CSV
def inventory_data_list() -> list:
    df=pd.read_csv('inventory.csv').astype(str)

    return df