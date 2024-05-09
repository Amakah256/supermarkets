import time
import tkinter as tk
from tkinter import simpledialog
from collections import defaultdict
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

# Define the products and their prices
products = {
    "Bar of soap": 4000,
  
   
}

# Create a dictionary to store daily purchase data
daily_purchases = defaultdict(lambda: defaultdict(int))

# Create a dictionary to store user credentials (email: password)
user_credentials = {}

# Create a dictionary to store password reset tokens (email: token)
password_reset_tokens = {}

# Track the number of login attempts
login_attempts = 0

# Create a variable to store the daily total
daily_total = 0

# Declare background_photo as a global variable
background_photo = None

# Define Employee Data Structure
employees = {
    "EMP001": {
        "name": "John Doe",
        "position": "Cashier",
        "contact": "john@example.com",
        "salary": 30000
    },
    "EMP002": {
        "name": "Jane Smith",
        "position": "Store Manager",
        "contact": "jane@example.com",
        "salary": 50000
    },
    # Add more employees as needed
}

# Employee Management Functions
def add_employee(employee_id, name, position, contact, salary):
    employees[employee_id] = {
        "name": name,
        "position": position,
        "contact": contact,
        "salary": salary
    }

def update_employee(employee_id, **kwargs):
    if employee_id in employees:
        for key, value in kwargs.items():
            employees[employee_id][key] = value
    else:
        print("Employee ID not found.")

def get_employee_info(employee_id):
    return employees.get(employee_id, "Employee not found.")

def remove_employee(employee_id):
    if employee_id in employees:
        del employees[employee_id]
        print("Employee removed successfully.")
    else:
        print("Employee ID not found.")

# Function to handle password validation before accessing the main system
def authenticate_user():
    email = email_entry.get()
    password = simpledialog.askstring("Password", "Enter your password:", show='*')

    # Check if the entered password matches the registered password for the email
    if email in user_credentials and user_credentials[email] == password:
        window.deiconify()  # Show the main window
        login_frame.withdraw()  # Hide the login frame
        show_product_prices()
    else:
        status_label.config(text="Incorrect password. Please try again.")

# Function to display the product prices after login
def show_product_prices():
    if product_frame.winfo_ismapped():
        products_text = "Available Products:\n"
        for product, price in products.items():
            products_text += f"{product}: {price} ugx\n"
        products_label.config(text=products_text)

# Function to display the price in the GUI and handle purchase data
def show_price():
    product_name = entry.get()
    if product_name in products:
        price = products[product_name]
        price_label.config(text=f"The price of {product_name} is {price} ugx")
    else:
        price_label.config(text="Product not found")

# Function to manually add a product to the daily purchase data
def add_product():
    product_name = entry.get()
    if product_name in products:
        # Add the product to the daily purchase list
        daily_purchases[time.strftime("%Y-%m-%d")][product_name] += 1

        # Update the daily total amount
        global daily_total
        daily_total += products[product_name]
        total_label.config(text=f"Daily Total: {daily_total} ugx")

        # Analyze the most bought product
        most_bought_product = max(
            daily_purchases[time.strftime("%Y-%m-%d")],
            key=daily_purchases[time.strftime("%Y-%m-%d")].get,
        )
        analysis_label.config(text=f"Most Bought Product: {most_bought_product}")

        # Update the product histogram
        update_histogram()

        # Print the receipt
        print_receipt()

    else:
        price_label.config(text="Product not found")

# Function to update the receipt label
def update_receipt_label(receipt_content):
    receipt_label.config(text=receipt_content)

# Function to print the receipt and save it as a file
def print_receipt():
    current_date = time.strftime("%Y-%m-%d")
    purchase_data = daily_purchases[current_date]
    total_amount = sum(
        products[p] * purchase_data[p] for p in purchase_data
    )

    receipt_content = f"DH Super Market Receipt\n"
    receipt_content += f"Date: {current_date}\n\n"
    receipt_content += "Products Purchased:\n"
    for product, quantity in purchase_data.items():
        receipt_content += f"{product} x{quantity}\n"
    receipt_content += f"\nTotal Amount: {total_amount} ugx\n"
    receipt_content += "Thank you for shopping with us! We are Glad."

    # Display the receipt content in the label
    update_receipt_label(receipt_content)

    # Save the receipt as a file in the user's documents folder
    save_receipt()

# Function to save the receipt as a file in the user's documents folder
def save_receipt():
    current_date = time.strftime("%Y-%m-%d")
    purchase_data = daily_purchases[current_date]
    total_amount = sum(
        products[p] * purchase_data[p] for p in purchase_data
    )

    receipt_content = f"DH Super Market Receipt\n"
    receipt_content += f"Date: {current_date}\n\n"
    receipt_content += "Products Purchased:\n"
    for product, quantity in purchase_data.items():
        receipt_content += f"{product} x{quantity}\n"
    receipt_content += f"\nTotal Amount: {total_amount} ugx\n"
    receipt_content += "Thank you for shopping with us! We are Glad."

    # Get the user's documents directory in a platform-independent way
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    if not os.path.exists(documents_path):
        documents_path = os.path.join(
            os.path.expanduser("~"), "My Documents"
        )  # For Windows users, might vary by system language

    # Save the receipt as a file in the documents folder
    receipt_filename = f"Receipt_{current_date}.txt"
    receipt_path = os.path.join(documents_path, receipt_filename)

    try:
        with open(receipt_path, "w") as receipt_file:
            receipt_file.write(receipt_content)

        # Display a message to the user
        receipt_saved_label.config(
            text=f"Receipt saved in documents folder as {receipt_filename}"
        )
    except Exception as e:
        # Display an error message if there was an issue saving the receipt
        receipt_saved_label.config(text=f"Error saving receipt: {str(e)}")

# Function to reset the program (clear data and interface)
def reset_program():
    global daily_purchases, daily_total
    daily_purchases = defaultdict(lambda: defaultdict(int))
    daily_total = 0
    entry.delete(0, tk.END)  # Clear the product entry field
    price_label.config(text="")  # Clear the price label
    total_label.config(text="")  # Clear the total label
    analysis_label.config(text="")  # Clear the analysis label
    receipt_label.config(text="")  # Clear the receipt label
    receipt_saved_label.config(text="")  # Clear the saved receipt label

# Function to update the product histogram
def update_histogram():
    # Get the purchase data for the current day
    purchase_data = daily_purchases[time.strftime("%Y-%m-%d")]

    # Get the product names and their respective counts
    products = list(purchase_data.keys())
    counts = list(purchase_data.values())

    # Plot the histogram
    plt.bar(products, counts)
    plt.xlabel("Products")
    plt.ylabel("Count")
    plt.title("Daily Product Purchase")
    plt.xticks(rotation=45)
    plt.show()

# Function to update the time label
def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=f"Current Time: {current_time}")
    time_label.after(1000, update_time)  # Update time every second

# Function to handle login process
def login():
    global login_attempts
    email = email_entry.get()
    password = password_entry.get()

    if email in user_credentials and user_credentials[email] == password:
        login_attempts = 0
        authenticate_user()  # Call the authentication function
    else:
        login_attempts += 1
        if login_attempts == 3:
            window.quit()
        else:
            status_label.config(
                text="Invalid email or password. Please try again."
            )

# Function to handle registration process
def register():
    email = email_entry.get()
    password = password_entry.get()

    if email and password:
        if email not in user_credentials:
            user_credentials[email] = password
            status_label.config(
                text="Registration successful. Please log in."
            )
        else:
            status_label.config(
                text="Email already registered. Please log in."
            )
    else:
        status_label.config(text="Please enter email and password.")

# Function to handle password reset process
def reset_password():
    email = email_entry.get()

    if email in user_credentials:
        # Generate a random token for password reset
        token = "MfKs0774653303."  # Replace with actual token generation logic

        # Store the password reset token
        password_reset_tokens[email] = token

        # Send the password reset token to the user (e.g., via email)
        # Update the status label
        status_label.config(
            text="Password reset token sent. Check your email."
        )
    else:
        status_label.config(text="Email not registered.")

# Function to add a new item to the existing products
def add_new_item():
    new_item_name = new_item_name_entry.get()
    new_item_price = new_item_price_entry.get()
    
    if new_item_name and new_item_price:
        try:
            # Convert the price to an integer
            new_item_price = int(new_item_price)
            # Add the new item to the products dictionary
            products[new_item_name] = new_item_price
            # Update the products display label
            show_product_prices()
            # Clear the entry fields
            new_item_name_entry.delete(0, tk.END)
            new_item_price_entry.delete(0, tk.END)
            status_label.config(text="New item added successfully.")
        except ValueError:
            status_label.config(text="Please enter a valid price.")
    else:
        status_label.config(text="Please enter both item name and price.")

# Create the GUI window
window = tk.Tk()
window.title("Product Price Display")
window.geometry("800x400")  # Adjust the window size as needed

# Create login frame
login_frame = tk.Toplevel(window)  # Use Toplevel for a separate window
login_frame.title("Login")

email_label = tk.Label(login_frame, text="Email:")
email_label.grid(row=0, column=0, padx=5, pady=5)

email_entry = tk.Entry(login_frame)
email_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)

password_entry = tk.Entry(login_frame, show="*")  # Use the 'show' option to hide the entered password
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

register_button = tk.Button(login_frame, text="Register", command=register)
register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

reset_button = tk.Button(login_frame, text="Forgot Password", command=reset_password)
reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(login_frame, text="")
status_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create main frame
main_frame = tk.Frame(window)
main_frame.pack(expand=True, fill="both")  # Expand the main frame to fill the window

# Create a label with the background image
background_label = tk.Label(main_frame, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for the product display
product_frame = tk.Frame(main_frame, bg="white")
product_frame.pack(side="left", padx=10, pady=10)

label = tk.Label(product_frame, text="Product Price Display")
label.pack()

entry = tk.Entry(product_frame)
entry.pack()

show_price_button = tk.Button(product_frame, text="Show Price", command=show_price)
show_price_button.pack()

add_button = tk.Button(product_frame, text="Add to Purchase", command=add_product)
add_button.pack()

# Add the "Print Receipt" button
print_button = tk.Button(product_frame, text="Print Receipt", command=print_receipt)
print_button.pack()

# Add the "Save Receipt" button
save_button = tk.Button(product_frame, text="Save Receipt", command=save_receipt)
save_button.pack()

price_label = tk.Label(product_frame, text="")
price_label.pack()

total_label = tk.Label(product_frame, text="")
total_label.pack()

analysis_label = tk.Label(product_frame, text="")
analysis_label.pack()

products_label = tk.Label(product_frame, text="")
products_label.pack()

# Display the product prices after creating the products label
show_product_prices()

# Create a label to display the receipt
receipt_label = tk.Label(product_frame, text="", justify="left")
receipt_label.pack()

# Create a label to display the saved receipt message
receipt_saved_label = tk.Label(product_frame, text="")
receipt_saved_label.pack()

# Create a button to reset the program
reset_button = tk.Button(product_frame, text="Reset Program", command=reset_program)
reset_button.pack()

# Create a button to update the product histogram
update_histogram_button = tk.Button(product_frame, text="Update Histogram", command=update_histogram)
update_histogram_button.pack()

# Create a label to display the current time
time_label = tk.Label(product_frame, text="")
time_label.pack()

# Update the time label initially
update_time()

# Create a frame for the employee management interface
employee_management_frame = tk.Frame(main_frame, bg="white")
employee_management_frame.pack(side="right", padx=10, pady=10)

# Function to display employee management interface
def show_employee_management():
    employee_management_frame.pack(side="right", padx=10, pady=10)

# Create a button to show employee management interface
show_employee_management_button = tk.Button(product_frame, text="Employee Management", command=show_employee_management)
show_employee_management_button.pack()

# Create a label for employee management
employee_management_label = tk.Label(employee_management_frame, text="Employee Management")
employee_management_label.pack()

# Create labels and entry fields for adding a new employee
new_employee_label = tk.Label(employee_management_frame, text="Add New Employee")
new_employee_label.pack()

new_employee_id_label = tk.Label(employee_management_frame, text="Employee ID:")
new_employee_id_label.pack()

new_employee_id_entry = tk.Entry(employee_management_frame)
new_employee_id_entry.pack()

new_employee_name_label = tk.Label(employee_management_frame, text="Name:")
new_employee_name_label.pack()

new_employee_name_entry = tk.Entry(employee_management_frame)
new_employee_name_entry.pack()

new_employee_position_label = tk.Label(employee_management_frame, text="Position:")
new_employee_position_label.pack()

new_employee_position_entry = tk.Entry(employee_management_frame)
new_employee_position_entry.pack()

new_employee_contact_label = tk.Label(employee_management_frame, text="Contact:")
new_employee_contact_label.pack()

new_employee_contact_entry = tk.Entry(employee_management_frame)
new_employee_contact_entry.pack()

new_employee_salary_label = tk.Label(employee_management_frame, text="Salary:")
new_employee_salary_label.pack()

new_employee_salary_entry = tk.Entry(employee_management_frame)
new_employee_salary_entry.pack()

add_employee_button = tk.Button(
    employee_management_frame,
    text="Add Employee",
    command=lambda: add_employee(
        new_employee_id_entry.get(),
        new_employee_name_entry.get(),
        new_employee_position_entry.get(),
        new_employee_contact_entry.get(),
        int(new_employee_salary_entry.get()),
    ),
)
add_employee_button.pack()

# Create labels and entry fields for updating an existing employee
update_employee_label = tk.Label(employee_management_frame, text="Update Employee")
update_employee_label.pack()

update_employee_id_label = tk.Label(employee_management_frame, text="Employee ID:")
update_employee_id_label.pack()

update_employee_id_entry = tk.Entry(employee_management_frame)
update_employee_id_entry.pack()

update_employee_name_label = tk.Label(employee_management_frame, text="Name:")
update_employee_name_label.pack()

update_employee_name_entry = tk.Entry(employee_management_frame)
update_employee_name_entry.pack()

update_employee_position_label = tk.Label(employee_management_frame, text="Position:")
update_employee_position_label.pack()

update_employee_position_entry = tk.Entry(employee_management_frame)
update_employee_position_entry.pack()

update_employee_contact_label = tk.Label(employee_management_frame, text="Contact:")
update_employee_contact_label.pack()

update_employee_contact_entry = tk.Entry(employee_management_frame)
update_employee_contact_entry.pack()

update_employee_salary_label = tk.Label(employee_management_frame, text="Salary:")
update_employee_salary_label.pack()

update_employee_salary_entry = tk.Entry(employee_management_frame)
update_employee_salary_entry.pack()

update_employee_button = tk.Button(
    employee_management_frame,
    text="Update Employee",
    command=lambda: update_employee(
        update_employee_id_entry.get(),
        name=update_employee_name_entry.get(),
        position=update_employee_position_entry.get(),
        contact=update_employee_contact_entry.get(),
        salary=int(update_employee_salary_entry.get()),
    ),
)
update_employee_button.pack()

# Create a label and entry field for removing an employee
remove_employee_label = tk.Label(employee_management_frame, text="Remove Employee")
remove_employee_label.pack()

remove_employee_id_label = tk.Label(employee_management_frame, text="Employee ID:")
remove_employee_id_label.pack()

remove_employee_id_entry = tk.Entry(employee_management_frame)
remove_employee_id_entry.pack()

remove_employee_button = tk.Button(
    employee_management_frame,
    text="Remove Employee",
    command=lambda: remove_employee(remove_employee_id_entry.get()),
)
remove_employee_button.pack()

# Function to withdraw the employee management frame
def hide_employee_management():
    employee_management_frame.pack_forget()

# Create a button to hide the employee management interface
hide_employee_management_button = tk.Button(
    employee_management_frame, text="Hide Employee Management", command=hide_employee_management
)
hide_employee_management_button.pack()

# Hide the employee management frame initially
hide_employee_management()

# Create the Add Item frame
add_item_frame = tk.Frame(main_frame, bg="white")
add_item_frame.pack(side="right", padx=10, pady=10)

# Create labels and entry fields for adding a new item
new_item_name_label = tk.Label(add_item_frame, text="Item Name:")
new_item_name_label.pack()

new_item_name_entry = tk.Entry(add_item_frame)
new_item_name_entry.pack()

new_item_price_label = tk.Label(add_item_frame, text="Item Price:")
new_item_price_label.pack()

new_item_price_entry = tk.Entry(add_item_frame)
new_item_price_entry.pack()

# Create a button to add the new item
add_item_button = tk.Button(add_item_frame, text="Add New Item", command=add_new_item)
add_item_button.pack()

# Hide the Add Item frame initially
add_item_frame.pack_forget()

# Function to show the Add Item frame
def show_add_item_frame():
    add_item_frame.pack(side="right", padx=10, pady=10)

# Create a button to show the Add Item frame
show_add_item_button = tk.Button(product_frame, text="Add New Item", command=show_add_item_frame)
show_add_item_button.pack()

# Run the main event loop
window.mainloop()
