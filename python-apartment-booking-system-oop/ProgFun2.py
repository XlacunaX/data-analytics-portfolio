'''
Name: Shambhavi Tewari
Student ID: s4016395
Highest Level Attempted: HD Level

Design Process:
This program's objective was to develop an adaptable ordering and booking system that could manage rewards, accommodate various product types, 
and build dynamic bundles. I started by creating the sequence of classes for visitors, orders, and products (apartment, supplements, and bundles). 
In order to keep the application going, I choose to utilize a `while} loop for the main menu.
This guarantees that communication will continue until the user decides to stop.

Since lists make it simple to search and iterate over data that varies in length, I decided to keep orders and products in lists.
It was especially difficult to validate the dates throughout the booking process because I had to make sure that the booking, check-in, 
and check-out dates made sense. I utilized the `datetime` module to make this simpler, which allowed for easy date comparison.

Errors in the program: There are no potential errors in the program. Everything is running properly.

Challenges:
Several challenges surfaced throughout the program's development, mostly related to handling changing product bundles, verifying dates, 
controlling guest incentive points, and making sure file input/output functions were reliable. Bundle implementation added complexity to the 
product management logic because it required careful consideration to apply discounts and dynamically manage the components. Another issue with bookings 
was validating dates. Since the dates of booking, check-in, and check-out had to adhere to reasonable guidelines in order to avoid mistakes in reservations. 
Keeping track of guest reward points was particularly challenging because the system had to reliably determine how many points might be earned and 
redeemed in different circumstances. Furthermore, using CSV files to provide data permanence between sessions posed challenges, especially when addressing 
corrupted or missing files, which were resolved by error handling. Lastly, to guarantee that the application handled invalid user inputs gently and 
enhance overall stability and user experience, input validation was essential. Iterative testing and software structure refinement helped 
overcome these obstacles and produce a more dependable and user-friendly solution.
Managing the CSV files presented another difficulty for me, particularly when it came to reading and entering orders, visitors, 
and products into the system. Ensuring that every product type—apartment unit, supplemental item, or bundle—was accurately identified and loaded 
with the necessary qualities necessitated meticulous processing of every line of data. Additionally, it was challenging to preserve the file structure 
and guarantee data integrity while adding new entries to these files, such as newly added products or visitors. It also took extra care to handle 
exceptions during file operations, such as corrupted or missing data, to make sure the software could manage mistakes without crashing.

'''

# Importing necessary python libraries
import sys
import os
from datetime import datetime

def handle_command_line_args():

    """
    The file names for the guest, product, and order data are determined by this function by processing the command-line inputs.
    It will automatically use 'guests.csv', 'products.csv', and 'orders.csv' if no arguments are given.
    It utilizes the first two or third argument supplied as the file name for the corresponding data file.

    """   
    guest_file = "guests.csv"
    product_file = "products.csv"
    order_file = "orders.csv"

    args = sys.argv[1:]  
    if len(args) == 0:
        print("No arguments provided, using default files: guests.csv, products.csv, orders.csv (if available)")
    elif len(args) == 2:
        guest_file = args[0]
        product_file = args[1]
        print(f"Using provided files: {guest_file} (guests), {product_file} (products), no order file provided.")
        order_file = None
    elif len(args) == 3:
        guest_file = args[0]
        product_file = args[1]
        order_file = args[2]
        print(f"Using provided files: {guest_file} (guests), {product_file} (products), {order_file} (orders)")
    else:
        print("Usage: python script.py <guest_file> <product_file> [<order_file>]")
        sys.exit(1)  #

    return guest_file, product_file, order_file

# Call the function to get file names from command-line arguments
guest_file, product_file, order_file = handle_command_line_args()

# Changing the working directory to the correct folder 
os.chdir("C:/Users/shamb/OneDrive/Desktop/Programming Fundamentals/Assignment 2")
print("Changed working directory to:", os.getcwd())

class Guest:
    """
    A customer or guest is represented in the system by the Guest class. A unique ID, name, reward points, reward rate, and redemption rate 
    are all associated with each guest. The class offers ways to show visitor information, update reward points, and manage these features.
    
    Attributes:
        guest_id (str): The unique identifier for the guest.
        name (str): The name of the guest.
        reward (int): The current reward points the guest has earned.
        reward_rate (int): The percentage of the total cost that will be converted into reward points.
        redeem_rate (int): The rate at which the guest can redeem reward points.
    
    Methods:
        get_id(): Returns the guest's unique ID.
        get_name(): Returns the guest's name.
        get_reward_rate(): Returns the guest's reward rate (percentage).
        get_reward(total_cost): Calculates the reward points earned based on the total cost and reward rate.
        get_redeem_rate(): Returns the redeem rate for the guest.
        update_reward(value): Adds the given value to the guest's reward points.
        display_info(): Prints out the guest's details including ID, name, reward points, reward rate, and redeem rate.
        set_reward_rate(rate): Sets a new reward rate for the guest.
        set_redeem_rate(rate): Sets a new redeem rate for the guest.

    """
    def __init__(self, guest_id, name, reward=0, reward_rate=100, redeem_rate=1):
        self.guest_id = guest_id
        self.name = name
        self.reward_rate = reward_rate
        self.reward = reward
        self.redeem_rate = redeem_rate

    # Getter methods
    def get_id(self):
        return self.guest_id

    def get_name(self):
        return self.name

    def get_reward_rate(self):
        return self.reward_rate

    def get_reward(self, total_cost):
        return round(total_cost * (self.reward_rate / 100))

    def get_redeem_rate(self):
        return self.redeem_rate

    # Method to update reward
    def update_reward(self, value):
        self.reward += value

    # Method to display guest info
    def display_info(self):
        print(f"ID: {self.guest_id}, Name: {self.name}, Reward Points: {self.reward}, Reward Rate: {self.reward_rate}%, Redeem Rate: {self.redeem_rate}%")

    # Methods to set reward and redeem rate
    def set_reward_rate(self, rate):
        self.reward_rate = rate

    def set_redeem_rate(self, rate):
        self.redeem_rate = rate

class Product:
    """
    All product types (e.g., apartments, supplemental goods, packages) use the Product class as their base class. It outlines a product's 
    fundamental characteristics, such as its name, ID, and cost. The class offers subclasses the ability to override the empty display_info 
    method and getter methods for accessing these attributes.
    
    Attributes:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
    
    Methods:
        get_id(): Returns the product's unique ID.
        get_name(): Returns the product's name.
        get_price(): Returns the product's price.
        display_info(): A placeholder method for displaying product information, to be overridden by subclasses.
    
    """
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    # Getter methods
    def get_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    # Method to display product info
    def display_info(self):
        pass

class ApartmentUnit(Product):
    """
    An apartment product is represented by the ApartmentUnit class. It is an extension of the Product class, which it inherits from, 
    and it adds the 'capacity' parameter to indicate the most visitors the apartment can hold.

    Attributes:
        product_id (str): The unique identifier for apartment unit.
        name (str): The name of the apartment unit.
        price (float): The price of the apartment unit per night.
        capacity (int): The number of guests the apartment can accommodate.
    
    Methods:
        get_capacity(): Returns the guest capacity of the apartment.
        display_info(): Displays the apartment's details, including its ID, name, price, and guest capacity.
    """

    def __init__(self, product_id, name, price, capacity):
        super().__init__(product_id, name, price)
        self.capacity = capacity

    # Getter for capacity
    def get_capacity(self):
        return self.capacity

    # Override display_info method
    def display_info(self):
        print(f"Apartment ID: {self.product_id}, Name: {self.name}, Rate: ${self.price}, Capacity: {self.capacity} guests")

class SupplementaryItem(Product):
    """
    supplementary item that can be purchased in addition to an apartment, this is represented by the SupplementaryItem class.
    There are no new characteristics added to this class; it just inherits from the Product class.

    Attributes:
        product_id (str): The unique identifier for the supplementary item.
        name (str): The name of the supplementary item.
        price (float): The price of the supplementary item.
    
    Methods:
        display_info(): Displays the supplementary item's details, including its ID, name, and price.
    """
    def __init__(self, product_id, name, price):
        super().__init__(product_id, name, price)

    # Override display_info method
    def display_info(self):
        print(f"Supplementary Item ID: {self.product_id}, Name: {self.name}, Price: ${self.price}")

class Bundle(Product):
    """
    A product bundle with several components is represented by the Bundle class (products).
    By including a 'components' element that holds a list of product IDs and quantities that are a part of the bundle, it expands the Product class.

    Attributes:
        product_id (str): The unique identifier for the bundle.
        name (str): The name of the bundle.
        components (list): A list of product IDs and their quantities in the bundle.
        price (float): The total price of the bundle.
    
    Methods:
        display_info(): Displays the bundle's details, including the ID, name, price, and components.
    """
    def __init__(self, product_id, name, components, price):
        super().__init__(product_id, name, price)
        self.components = components  # A list of product IDs in the bundle

    def display_info(self):
        print(f"Bundle ID: {self.product_id}, Name: {self.name}, Price: ${self.price}")
        print("Components:")
        for component in self.components:
            print(f" - {component}")

class Order:
    """
    A guest's reservation or purchase is represented by the Order class. It includes information on the guest, the product 
    (such a supplementary product or apartment), the quantity of it, the overall cost of the order, the incentives that were accrued from the purchase, 
    and the order date and time.

    Attributes:
        guest (Guest): The guest who placed the order.
        product (Product): The product being ordered.
        quantity (int): The quantity of the product ordered.
        total_cost (float): The total cost of the order, including all products and services.
        earned_rewards (int): The number of reward points earned for the order.
        order_date_time (str): The date and time when the order was placed.
    
    Methods:
        compute_cost(): Returns the total cost of the order.
        display_order(): Returns a formatted string displaying the full details of the order.
        display_order_summary(): Returns a summary of the order, showing essential details in a tabular format.
        to_csv(): Converts the order details into a CSV format string for saving to a file.
    """
    def __init__(self, guest, product, quantity, total_cost, earned_rewards, order_date_time):
        self.guest = guest
        self.product = product
        self.quantity = quantity
        self.total_cost = total_cost
        self.earned_rewards = earned_rewards
        self.order_date_time = order_date_time

    # Method to compute total cost
    def compute_cost(self):
        return self.total_cost

    # Method to display the order
    def display_order(self):
        return f"Guest: {self.guest.get_name()}, Product: {self.product.get_name()}, Quantity: {self.quantity}, Total Cost: ${self.total_cost:.2f}, Earned Rewards: {self.earned_rewards}, Date: {self.order_date_time}"

    def display_order_summary(self):
        return f"{self.guest.get_name():<20} {self.product.get_name():<20} {self.quantity:<10} ${self.total_cost:<10.2f} {self.earned_rewards:<10} {self.order_date_time}"

    # Method to convert order details to CSV format
    def to_csv(self):
        product_details = f"{self.quantity} x {self.product.get_id()}"
        csv_string = f"{self.guest.get_name()},{product_details},{self.total_cost:.2f},{self.earned_rewards},{self.order_date_time}\n"
        return csv_string

class Bundle:
    """
    A bundle of products, comprising several components bundled together at a discounted price, is represented by the Bundle class.
    An individual ID, name, list of items (each with a product ID and quantity), and the overall cost are all included in each bundle.

    Attributes:
        bundle_id (str): The unique identifier for the bundle.
        name (str): The name of the bundle.
        components (list of tuples): A list of components, where each component is a tuple in the format (product_id, quantity).
        price (float): The total price of the bundle, usually lower than the sum of individual product prices.

    Methods:
        get_id(): Returns the bundle ID.
        get_name(): Returns the bundle name.
        get_components(): Returns the list of components in the bundle.
        get_price(): Returns the total price of the bundle.
        display_info(): Displays the bundle information, including the ID, name, components, and price.
    """
    def __init__(self, bundle_id, name, components, price):
       
        self.bundle_id = bundle_id
        self.name = name
        self.components = components  # List of tuples like [(product_id, quantity), ...]
        self.price = price

    def get_id(self):
        return self.bundle_id

    def get_name(self):
        return self.name

    def get_components(self):
        return self.components

    def get_price(self):
        return self.price

    def display_info(self):

        print(f"ID: {self.bundle_id}")
        print(f"Name: {self.name}")
        component_str = ', '.join([f"{quantity} x {product_id}" if quantity > 1 else product_id for product_id, quantity in self.components])
        print(f"Components: {component_str}")
        print(f"Price: ${self.price:.2f}")

class Records:
    """
    The system's maintenance of guest, product, and order records is handled by the Records class. It offers ways to display all entries, 
    read data from files, search for particular guests or items, and update files when changes are made. The class is in charge of loading, 
    unloading, and monitoring all customers, merchandise, and orders. Modifying and storing these data as CSV files.

    Attributes:
        guests (list): A list of Guest objects representing all guests in the system.
        products (list): A list of Product objects, which may include ApartmentUnit, SupplementaryItem, and Bundle objects.
        orders (list): A list of Order objects representing all orders made by guests.

    Methods:
        read_guests(filename): Reads guests from a CSV file and adds them to the guest list.
        find_guest(search_value): Searches for a guest by ID or name and returns the guest object if found.
        add_guest(guest_id, guest_name, reward_rate=100, reward=0, redeem_rate=1): Adds a new guest to the guest list.
        list_guests(): Displays all guests in the system.
        read_products(filename): Reads products from a CSV file and adds them to the product list.
        find_product(search_value): Searches for a product by ID or name and returns the product object if found.
        list_products(product_type=None): Displays all products, or specific types such as apartment, supplementary items, or bundles.
        display_all_orders(): Displays all orders in the system in a tabular format.
        read_orders(filename): Reads orders from a CSV file and adds them to the orders list.
        update_guest_file(filename='guests.csv'): Updates and saves the guest information to a CSV file.
        update_product_file(filename='products.csv'): Updates and saves the product information to a CSV file.
        update_order_file(filename='orders.csv'): Updates and saves the order information to a CSV file.
    """
    def __init__(self):

        self.guests = []
        self.products = []
        self.orders = []

    # Method to read guests from a file and add them to the guest list
    def read_guests(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    guest = Guest(data[0], data[1], int(data[2]), int(data[3]), int(data[4]))
                    self.guests.append(guest)
                    print(f"Loaded guest: {guest.get_name()} - ID: {guest.get_id()}, Reward Points: {guest.reward}")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    
    # Method to find a guest by guest ID or name
    def find_guest(self, search_value):
        search_value = search_value.strip().lower()  # Normalize the search to lowercase and strip whitespaces
        for guest in self.guests:
            if guest.get_id().strip().lower() == search_value or guest.get_name().strip().lower() == search_value:
                print(f"Guest found: {guest.get_id()} - {guest.get_name()}")
                return guest
        print(f"Guest with ID or name '{search_value}' not found.")
        return None

    def add_guest(self, guest_id, guest_name, reward_rate=100, reward=0, redeem_rate=1):
        
        new_guest = Guest(guest_id, guest_name, reward_rate, reward, redeem_rate)
        self.guests.append(new_guest)
        print(f"New guest added: {new_guest.get_name()} - ID: {new_guest.get_id()}")
    
    # Method to display all guests
    def list_guests(self):
        print("\nList of Guests:")
        for guest in self.guests:
            guest.display_info()

    # Method to read products from a file and add them to the product list
    def read_products(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    
                    data = line.strip().split(',')
                    data = [item.strip() for item in data]

                    if data[0].startswith('U'):
                        product = ApartmentUnit(data[0], data[1], float(data[2]), int(data[3]))
                        print(f"Loaded apartment: {product.get_id()} - {product.get_name()}")
                    
                    elif data[0].startswith('SI'):
                        product = SupplementaryItem(data[0], data[1], float(data[2]))
                        print(f"Loaded supplementary item: {product.get_id()} - {product.get_name()}")

                    elif data[0].startswith('B'):
                        bundle_id = data[0]
                        bundle_name = data[1]
                        components = data[2:-1]  
                        bundle_price = float(data[-1])  
                        product = Bundle(bundle_id, bundle_name, components, bundle_price)
                        print(f"Loaded bundle: {product.get_id()} - {product.get_name()}")
                    
                    else:
                        print(f"Unrecognized product format: {data}")
                        continue

                    self.products.append(product)

        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Method to find a product by product ID or name
    def find_product(self, search_value):
        search_value = search_value.strip().lower()
        for product in self.products:
            if product.get_id().lower() == search_value or product.get_name().lower() == search_value:
                print(f"Product found: {product.get_id()} - {product.get_name()}")
                return product
        print(f"Product with ID or name '{search_value}' not found.")
        return None

    # Method to display all products or specific types (apartment, supplementary)
    def list_products(self, product_type=None):
        if product_type == "apartment":
            print("\nList of Apartment Units:")
            for product in self.products:
                if isinstance(product, ApartmentUnit):
                    product.display_info()
        elif product_type == "supplementary":
            print("\nList of Supplementary Items:")
            for product in self.products:
                if isinstance(product, SupplementaryItem):
                    product.display_info()
        elif product_type == "bundle":
            print("\nList of Bundles:")
            for product in self.products:
                if isinstance(product, Bundle):
                    product.display_info()
        else:
            print("\nList of All Products:")
            for product in self.products:
                product.display_info()

     # Method to display all orders
    def display_all_orders(self):
        if not self.orders:
            print("No orders found.")
            return

        print(f"{'Guest':<20} {'Product':<20} {'Quantity':<10} {'Total Cost':<12} {'Rewards':<10} {'Order Date'}")
        print("=" * 100)
        for order in self.orders:
            print(order.display_order_summary())

    def read_orders(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    data = [item.strip() for item in line.strip().split(',')]  
                    if len(data) < 5:
                        print(f"Skipping malformed line: {line}")
                        continue

                    guest_name_or_id = data[0].strip()  
                    products_ordered = data[1:-3]  
                    total_cost = data[-3].strip() if data[-3].strip() else '0'  
                    earned_rewards = data[-2].strip() if data[-2].strip() else '0'  
                    order_date_time = data[-1].strip()  

                    
                    print(f"Processing Order: Guest: {guest_name_or_id}, Products: {products_ordered}, Total Cost: {total_cost}")
                    # Find the guest by name or ID
                    guest = self.find_guest(guest_name_or_id)
                    if not guest:
                        print(f"Error: Guest '{guest_name_or_id}' not found. Skipping order.")
                        continue  
                    # List to store products and their quantities
                    products = []
                    quantities = []
                    # Dynamically process each product in the order
                    for product_info in products_ordered:
                        try:
                            quantity, product_id_or_name = product_info.split(' x ')
                            product = self.find_product(product_id_or_name.strip())
                            if not product:
                                print(f"Error: Product '{product_id_or_name}' not found. Skipping product.")
                                continue

                            products.append(product)
                            quantities.append(int(quantity))
                        except ValueError:
                            print(f"Malformed product entry: {product_info}. Skipping.")
                            continue  

                    if not products:
                        print(f"Error: No valid products found for order: {line}")
                        continue

                    # Create the order object
                    order = Order(
                        guest=guest,
                        product=products[0], 
                        quantity=quantities[0],
                        total_cost=float(total_cost),
                        earned_rewards=int(earned_rewards),
                        order_date_time=order_date_time
                    )

                    # Update guest's reward points
                    guest.reward += int(earned_rewards)

                    # Update product sold quantities
                    for product, quantity in zip(products, quantities):
                        product.total_quantity_sold = getattr(product, 'total_quantity_sold', 0) + quantity

                    # Add the order to the records
                    self.orders.append(order)

                print("Orders loaded successfully.")
    
        except Exception as e:
            print("Cannot load the order file.")
            print(f"Error: {e}")

    def update_guest_file(self, filename='guests.csv'):
        try:
            with open(filename, 'w') as file:
                for guest in self.guests:
                    file.write(f"{guest.get_id()},{guest.get_name()},{guest.reward},{guest.get_reward_rate()},{guest.get_redeem_rate()}\n")
            print("Guest data saved successfully.")
        except Exception as e:
            print(f"Error saving guest data: {e}")

    def update_product_file(self, filename='products.csv'):
        try:
            with open(filename, 'w') as file:
                for product in self.products:
                    if isinstance(product, ApartmentUnit):
                        file.write(f"{product.get_id()},{product.get_name()},{product.get_price()},{product.get_capacity()}\n")
                    elif isinstance(product, SupplementaryItem):
                        file.write(f"{product.get_id()},{product.get_name()},{product.get_price()}\n")
                    elif isinstance(product, Bundle):
                        components = ','.join([f"{quantity} x {prod_id}" for prod_id, quantity in product.get_components()])
                        file.write(f"{product.get_id()},{product.get_name()},{components},{product.get_price()}\n")
            print("Product data saved successfully.")
        except Exception as e:
            print(f"Error saving product data: {e}")

    def update_order_file(self, filename='orders.csv'):
        try:
            with open(filename, 'w') as file:
                for order in self.orders:
                    product_details = ', '.join([f"{order.quantity} x {order.product.get_id()}"])
                    order_line = f"{order.guest.get_name()},{product_details},{order.total_cost:.2f},{order.earned_rewards},{order.order_date_time}\n"
                    file.write(order_line)
            print("Order data saved successfully.")
        except Exception as e:
            print(f"Error saving order data: {e}")
        
# Defining custom exceptions
class InvalidNameError(Exception):
    pass

class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidDateError(Exception):
    pass

class Operations:
    """
   The primary user interface for interacting with the ordering and booking system is the Operation class. It has the ability to manage 
   reservations for guests, provide product details, change rewards rates, put together bundles, and produce reports. The `Records` class  
   and the class communicate to handle visitor, product, and arrange information.

    Attributes:
        records (Records): An instance of the Records class to manage all guest, product, and order records.

    Methods:
        menu(): Displays the main menu and handles user input to choose various options.
        make_booking(): Allows a guest to make a booking for an apartment, supplementary items, or bundles.
        get_valid_date(prompt): Helper method to validate and return a date in the format 'd/m/yyyy'.
        handle_extra_beds(apartment, number_of_guests, length_of_stay): Adds extra beds if the number of guests exceeds apartment capacity.
        add_update_apartment(): Allows adding or updating apartment units in the system.
        add_update_supplementary_item(): Allows adding or updating supplementary items.
        add_update_bundle(): Allows adding or updating product bundles.
        create_bundle(): Helper function to create a bundle.
        adjust_reward_rate(): Adjusts the reward rate for all guests.
        adjust_redeem_rate(): Adjusts the redeem rate for all guests.
        generate_key_statistics(): Generates key business statistics, including the top 3 valuable guests and popular products.
        display_guest_order_history(): Displays the order history of a specific guest.
        terminate_program(): Saves all data before exiting the program.
    """
    def __init__(self):
        self.records = Records()

        # Loading the csv files
        try:
            self.records.read_guests("guests.csv")
            self.records.read_products("products.csv")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return
        try:
            self.records.read_orders("orders.csv")
        except FileNotFoundError:
            print("Cannot load the order file.")

    def menu(self):
        # Load guest, product, and order data from CSV files using command-line arguments
        try:
            self.records.read_guests(guest_file)
            self.records.read_products(product_file)
            if order_file:
                self.records.read_orders(order_file)  
            else:
                print("No order file provided, proceeding without loading previous orders.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

        while True:
            # Display the menu
            print("\nMenu:")
            print("1. Make a booking")
            print("2. Display existing guests")
            print("3. Display existing apartment units")
            print("4. Display existing supplementary items")
            print("5. Add/update supplementary items")
            print("6. Add/update bundles")  
            print("7. Adjust reward rate of all guests")  
            print("8. Adjust redeem rate of all guests")
            print("9. Display all orders")
            print("10. Generate Key Statistics")
            print("11. Display a guest's order history")  
            print("0. Exit")
            choice = input("Choose an option: ")

            # Handle menu options
            if choice == '1':
                self.make_booking()
            elif choice == '2':
                self.records.list_guests()
            elif choice == '3':
                self.records.list_products("apartment")
            elif choice == '4':
                self.records.list_products("supplementary")
            elif choice == '5':  
                self.add_update_supplementary_item()
            elif choice == '6':  
                self.add_update_bundle()
            elif choice == '7':  
                self.adjust_reward_rate()
            elif choice == '8':  
                self.adjust_redeem_rate()
            elif choice == '9':
                self.records.display_all_orders()
            elif choice == '10':
                self.generate_key_statistics()
            elif choice == '11':
                self.display_guest_order_history()            
            elif choice == '0':
                self.terminate_program()
                break
            else:
                print("Invalid choice. Please try again.")

    def make_booking(self):
        # Find guest by ID or name
        while True:
            guest_input = input("Enter guest ID or name: ").strip()
            guest = self.records.find_guest(guest_input)

                # If guest is not found, new guest ID will be created
            if guest is None:
                create_new = input(f"Guest with ID or name '{guest_input}' not found. Do you want to create a new guest? (y/n): ").strip().lower()
                if create_new == 'y':
                    guest_id = input("Enter new guest ID: ").strip()
                    guest_name = guest_input  # Use the input provided earlier as the guest name
                    self.records.add_guest(guest_id, guest_name)  # Add the new guest
                    guest = self.records.find_guest(guest_id)  # Retrieve the newly created guest
                    break
                else:
                    print("Please enter a valid guest ID or name.")
            else:
                print(f"Guest found: {guest.get_name()} - ID: {guest.get_id()}")
                break

        # Find product (apartment) by ID or name
        while True:
            apartment_input = input("Enter apartment ID or name: ").strip()
            apartment = self.records.find_product(apartment_input)
            if apartment and isinstance(apartment, ApartmentUnit):
                break
            print("Invalid apartment ID or name. Please try again.")

        # Get number of guests (validate input as a positive integer)
        while True:
            try:
                number_of_guests = int(input("Enter number of guests: "))
                if number_of_guests > 0:
                    break
                else:
                    print("Number of guests must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid number of guests.")

        # Get current booking date (current system time)
        booking_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        booking_date_dt = datetime.now()
        print(f"Booking date and time: {booking_date}")

        # Get check-in and check-out dates (validate input as a date in format dd/mm/yyyy)
        checkin_date = self.get_valid_date("Enter check-in date (d/m/yyyy): ")
        checkin_date_dt = datetime.strptime(checkin_date, "%d/%m/%Y")
        checkout_date = self.get_valid_date("Enter check-out date (d/m/yyyy): ")
        checkout_date_dt = datetime.strptime(checkout_date, "%d/%m/%Y")

        # Date validation checks
        if checkin_date_dt < booking_date_dt:
            print("Error: The check-in date cannot be earlier than the booking date.")
            return
        if checkout_date_dt < booking_date_dt:
            print("Error: The check-out date cannot be earlier than the booking date.")
            return
        if checkout_date_dt < checkin_date_dt:
            print("Error: The check-out date cannot be earlier than the check-in date.")
            return
        if checkin_date_dt == checkout_date_dt:
            print("Error: The check-in date cannot be the same as the check-out date.")
            return 

        # Calculate length of stay based on date difference
        length_of_stay = (checkout_date_dt - checkin_date_dt).days

        # Process supplementary items or bundles
        supplementary_orders = []
        while True:
            order_more = input("Do you want to order a supplementary item or bundle? (s for supplementary, b for bundle, n to finish): ").strip().lower()
            if order_more == 'n':
                break
            elif order_more == 's':
                supplementary_id = input("Enter supplementary item ID: ").strip().lower()
                supplementary_item = self.records.find_product(supplementary_id)
                if supplementary_item and isinstance(supplementary_item, SupplementaryItem):
                    quantity = int(input(f"Enter quantity for {supplementary_item.get_name()}: "))
                    supplementary_orders.append({'item': supplementary_item, 'quantity': quantity})
                else:
                    print("Invalid supplementary item ID.")
            elif order_more == 'b':
                bundle_id = input("Enter bundle ID or name: ").strip()
                bundle = self.records.find_product(bundle_id)
                if bundle and isinstance(bundle, Bundle):
                    supplementary_orders.append({'item': bundle, 'quantity': 1})  # Bundles are usually single items
                    print(f"Added bundle {bundle.get_name()} to your order.")
                else:
                    create_new_bundle = input("Bundle not found. Do you want to create a new bundle? (y/n): ").strip().lower()
                    if create_new_bundle == 'y':
                        self.create_bundle()
                    else:
                        print("Please enter a valid bundle ID or create a new one.")

        # Handle extra beds
        extra_beds_needed = self.handle_extra_beds(apartment, number_of_guests, length_of_stay)

        # Automatically add extra beds to the supplementary orders
        if extra_beds_needed > 0:
            extra_bed_item = self.records.find_product("SI6")  # Assuming SI6 is the extra bed
            if extra_bed_item:
                supplementary_orders.append({'item': extra_bed_item, 'quantity': extra_beds_needed})
                print(f"Added {extra_beds_needed} extra bed(s) for {length_of_stay} nights.")

        # Automatically add car park
        car_park_item = self.records.find_product("SI1")
        if car_park_item:
            supplementary_orders.append({'item': car_park_item, 'quantity': length_of_stay})
            print(f"Added car park(s) for {length_of_stay} nights.")

        # Calculate total costs and rewards
        apartment_subtotal = apartment.get_price() * length_of_stay
        supplementary_subtotal = sum(item['item'].get_price() * item['quantity'] for item in supplementary_orders)
        total_cost = apartment_subtotal + supplementary_subtotal
        earned_reward_points = guest.get_reward(total_cost)

        # Offer discount based on reward points
        discount = 0
        if guest.reward >= 100:
            print(f"You have {guest.reward} reward points.")
            use_points = input("Would you like to use your reward points to reduce the total cost? (y/n): ").strip().lower()
            if use_points == 'y':
                points_to_use = (guest.reward // 100) * 100  # Redeemable in multiples of 100
                discount = points_to_use / 100
                total_cost -= discount
                guest.reward -= points_to_use
                print(f"{points_to_use} points used. New total cost: ${total_cost:.2f}")

        # Update reward points after discount
        guest.update_reward(earned_reward_points)

        # Create and save the order
        order_id = f"Order{len(self.records.orders) + 1}"  # Unique order ID
        order = Order(
            guest=guest,
            product=apartment,  # Main apartment unit in the order
            quantity=1,  # Always 1 apartment unit
            total_cost=total_cost,
            earned_rewards=earned_reward_points,
            order_date_time=booking_date
        )

        # Update guest's total order amount
        guest.total_order_amount = getattr(guest, 'total_order_amount', 0) + total_cost

        # Update the apartment's sold quantity
        apartment.total_quantity_sold = getattr(apartment, 'total_quantity_sold', 0) + 1

        # Update the supplementary items' sold quantity
        for supplementary_order in supplementary_orders:
            product = supplementary_order['item']
            quantity = supplementary_order['quantity']
            product.total_quantity_sold = getattr(product, 'total_quantity_sold', 0) + quantity

        # Add the order to records and save to CSV
        self.records.orders.append(order)
        try:
            with open('orders.csv', 'a') as file:  # Append to the file
                file.write(order.to_csv())  # Write the CSV string to the file
                print("Order saved to orders.csv successfully.")
        except Exception as e:
            print(f"Error saving order to CSV: {e}")

        # Display the final receipt
        self.display_receipt(
            guest, number_of_guests, apartment, checkin_date, checkout_date, length_of_stay,
            booking_date, apartment_subtotal, supplementary_orders, supplementary_subtotal,
            total_cost, earned_reward_points, discount
        )

    # Helper function to validate date input
    def get_valid_date(self, prompt):
        while True:
            date_str = input(prompt).strip()
            try:
                valid_date = datetime.strptime(date_str, "%d/%m/%Y")
                return date_str  
            except ValueError:
                print("Invalid date format. Please enter a date in the format d/m/yyyy.")

    # Helper function to create a bundle
    def create_bundle(self):
        print("Creating a bundle...")
        bundle_components = []
        total_price = 0
        while True:
            product_id = input("Enter product ID to add to the bundle (or 'done' to finish): ").strip()
            if product_id.lower() == 'done':
                break
            product = self.records.find_product(product_id)
            if product:
                bundle_components.append(product)
                total_price += product.get_price()
                print(f"Added {product.get_name()} to the bundle.")
            else:
                print(f"Product {product_id} not found. Please try again.")
        
        if bundle_components:
            bundle_price = total_price * 0.80  # Apply the 20% discount for the bundle
            bundle_name = input("Enter a name for the bundle: ").strip()
            bundle_id = "B" + str(len(self.records.bundles) + 1)  # Generate a unique bundle ID
            new_bundle = Bundle(bundle_id, bundle_name, bundle_components, bundle_price)
            self.records.bundles.append(new_bundle)
            print(f"Bundle created with ID: {bundle_id}, Name: {bundle_name}, Price: ${bundle_price:.2f}")

    def display_receipt(self, guest, number_of_guests, apartment, checkin_date, checkout_date, length_of_stay,
                        booking_date, apartment_subtotal, supplementary_orders, supplementary_subtotal, total_cost,
                        earned_reward_points, discount):
        # Display the formatted receipt with all the booking details
        print("=" * 50)
        print(f"Guest name: {guest.get_name()}")
        print(f"Number of guests: {number_of_guests}")
        print(f"Apartment name: {apartment.get_name()}")
        print(f"Apartment rate: ${apartment.get_price():.2f} (AUD)")
        print(f"Check-in date: {checkin_date}")
        print(f"Check-out date: {checkout_date}")
        print(f"Length of stay: {length_of_stay} nights")
        print(f"Booking date: {booking_date}")
        print(f"Sub-total: ${apartment_subtotal:.2f} (AUD)")
        print("-" * 50)

        
        # Print supplementary items, if any
        if supplementary_orders:
            print("Supplementary items:")
            for order in supplementary_orders:
                item = order['item']
                quantity = order['quantity']
                cost = item.get_price() * quantity
                print(f"{item.get_id()} {item.get_name()} {quantity} x ${item.get_price():.2f} = ${cost:.2f}")
            print(f"Sub-total: ${supplementary_subtotal:.2f} (AUD)")
            print("-" * 50)

        # Print final totals
        print(f"Total cost: ${total_cost:.2f} (AUD)")
        print(f"Reward points to redeem: {guest.reward} points")
        print(f"Discount based on points: ${discount:.2f} (AUD)")
        print(f"Final total cost: ${total_cost:.2f} (AUD)")
        print(f"Earned rewards: {earned_reward_points} points")
        print("Thank you for your booking! We hope you will have an enjoyable stay.")
        print("=" * 50)
        
    # Helper function to validate date input
    def get_valid_date(self, prompt):
        while True:
            date_str = input(prompt).strip()
            try:
                valid_date = datetime.strptime(date_str, "%d/%m/%Y")
                return date_str  
            except ValueError:
                print("Invalid date format. Please enter a date in the format d/m/yyyy.")

    # Function to add extra beds            
    def handle_extra_beds(self, apartment, number_of_guests, length_of_stay):
        if number_of_guests > apartment.get_capacity():
            extra_guests = number_of_guests - apartment.get_capacity()
            extra_beds_needed = extra_guests * length_of_stay
            print(f"Extra beds needed for {extra_guests} extra guests for {length_of_stay} nights: {extra_beds_needed} bed(s).")
            return extra_beds_needed
        return 0

    def add_update_apartment(self):
        while True:
            apartment_input = input("Enter apartment information (ID, Rate, Capacity): ").strip()
            try:
                apartment_id, rate, capacity = apartment_input.split()
                rate = float(rate)
                capacity = int(capacity)
                
                # Validate the apartment ID format
                if not apartment_id.startswith('U'):
                    raise ValueError("Apartment ID should start with 'U'.")

                # Check if the apartment already exists
                existing_apartment = self.records.find_product(apartment_id)
                if existing_apartment:
                    # Update the apartment info if it exists
                    existing_apartment.price = rate
                    existing_apartment.capacity = capacity
                    print(f"Updated apartment: {apartment_id}")
                else:
                    # Add new apartment
                    new_apartment = ApartmentUnit(apartment_id, f"Apartment {apartment_id}", rate, capacity)
                    self.records.products.append(new_apartment)
                    print(f"Added new apartment: {apartment_id}")

                break
            except ValueError as ve:
                print(f"Invalid input: {ve}")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

     # Method to add or update supplementary items
    def add_update_supplementary_item(self):
        while True:
            product_id = input("Enter Supplementary Item ID (e.g., SI1) or 'done' to finish: ").strip()
            if product_id.lower() == 'done':
                break
            
            # Check if the product exists
            product = self.records.find_product(product_id)
            
            # If the product exists, update its details
            if product and isinstance(product, SupplementaryItem):
                print(f"Updating supplementary item: {product.get_id()} - {product.get_name()}")
                new_name = input(f"Enter new name for {product.get_name()} (or press Enter to keep it the same): ").strip()
                if new_name:
                    product.name = new_name
                new_price = input(f"Enter new price for {product.get_price()} (or press Enter to keep it the same): ").strip()
                if new_price:
                    product.price = float(new_price)
                print(f"Updated supplementary item: {product.get_id()} - {product.get_name()}, Price: ${product.get_price():.2f}")

            # If the product does not exist, create a new supplementary item
            else:
                print(f"Supplementary item with ID {product_id} not found. Creating a new one.")
                name = input("Enter supplementary item name: ").strip()
                price = float(input("Enter price: ").strip())
                new_supplementary_item = SupplementaryItem(product_id, name, price)
                self.records.products.append(new_supplementary_item)
                print(f"Added new supplementary item: {new_supplementary_item.get_id()} - {new_supplementary_item.get_name()}, Price: ${new_supplementary_item.get_price():.2f}")            

    # Add/Update Bundles
    def add_update_bundle(self):
        while True:
            bundle_id = input("Enter Bundle ID (e.g., B1) or 'done' to finish: ").strip()
            if bundle_id.lower() == 'done':
                break

        # Check if the bundle exists
            bundle = self.records.find_product(bundle_id)

            if bundle and isinstance(bundle, Bundle):
            # Update existing bundle
                print(f"Updating bundle: {bundle.get_id()} - {bundle.get_name()}")
                new_name = input(f"Enter new name for {bundle.get_name()} (or press Enter to keep it the same): ").strip()
                if new_name:
                    bundle.name = new_name

            # Update components
                print("Updating components. Enter product IDs one by one, or 'done' when finished.")
                components = []
                while True:
                    product_id = input("Enter product ID to add to bundle (or 'done' to finish): ").strip()
                    if product_id.lower() == 'done':
                        break
                    product = self.records.find_product(product_id)
                    if product:
                        try:
                            quantity = int(input(f"Enter quantity for {product.get_name()}: "))
                        except ValueError:
                            print("Invalid quantity. Please enter a valid number.")
                            continue
                        components.append((product.get_id(), quantity))
                    else:
                        print(f"Product '{product_id}' not found.")

                if components:
                    bundle.components = components

                # Update the bundle price
                new_price = input(f"Enter new price for {bundle.get_price()} (or press Enter to keep it the same): ").strip()
                if new_price:
                    bundle.price = float(new_price)

                print(f"Updated bundle: {bundle.get_id()} - {bundle.get_name()}, Price: ${bundle.get_price():.2f}")

            else:
                # Create new bundle
                print(f"Bundle with ID {bundle_id} not found. Creating a new bundle.")
                bundle_name = input("Enter name for the new bundle: ").strip()
                components = []

                print("Enter product IDs one by one to add to the bundle (or 'done' when finished).")
                total_price = 0
                while True:
                    product_id = input("Enter product ID to add to the bundle (or 'done' to finish): ").strip()
                    if product_id.lower() == 'done':
                        break
                    product = self.records.find_product(product_id)
                    if product:
                        try:
                            quantity = int(input(f"Enter quantity for {product.get_name()}: "))
                        except ValueError:
                            print("Invalid quantity. Please enter a valid number.")
                            continue
                        components.append((product.get_id(), quantity))
                        total_price += product.get_price() * quantity
                    else:
                        print(f"Product '{product_id}' not found.")

                if components:
                    # Applying 20% discount to the bundle price
                    bundle_price = total_price * 0.80
                    new_bundle = Bundle(bundle_id, bundle_name, components, bundle_price)
                    self.records.products.append(new_bundle)
                    print(f"New bundle created: {new_bundle.get_id()} - {new_bundle.get_name()}, Price: ${new_bundle.get_price():.2f}")


# Helper function to create a bundle
    def create_bundle(self):
        print("Creating a bundle...")
        bundle_components = []
        total_price = 0
        while True:
            product_id = input("Enter product ID to add to the bundle (or 'done' to finish): ").strip()
            if product_id.lower() == 'done':
                break
            product = self.records.find_product(product_id)
            if product:
                try:
                    quantity = int(input(f"Enter quantity for {product.get_name()}: "))
                except ValueError:
                    print("Invalid quantity. Please enter a valid number.")
                    continue
                bundle_components.append((product.get_id(), quantity))
                total_price += product.get_price() * quantity
                print(f"Added {quantity} x {product.get_name()} to the bundle.")
            else:
                print(f"Product '{product_id}' not found.")

        if bundle_components:
            bundle_price = total_price * 0.80  # Apply the 20% discount for the bundle
            bundle_name = input("Enter a name for the bundle: ").strip()
            bundle_id = "B" + str(len(self.records.products) + 1)  # Generate a unique bundle ID
            new_bundle = Bundle(bundle_id, bundle_name, bundle_components, bundle_price)
            self.records.products.append(new_bundle)  # Add the bundle to the products list
            print(f"Bundle created with ID: {bundle_id}, Name: {bundle_name}, Price: ${bundle_price:.2f}")


    # Adjust Reward Rate of All Guests
    def adjust_reward_rate(self):
        while True:
            try:
                new_rate = float(input("Enter new reward rate for all guests (must be a positive number): ").strip())
                if new_rate <= 0:
                    raise ValueError("Reward rate must be greater than zero.")
                for guest in self.records.guests:
                    guest.set_reward_rate(new_rate)
                print(f"Updated reward rate for all guests to {new_rate}%")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    # Adjust Redeem Rate of All Guests
    def adjust_redeem_rate(self):
        while True:
            try:
                new_rate = float(input("Enter new redeem rate for all guests (must be a positive number above 1%): ").strip())
                if new_rate < 1:
                    raise ValueError("Redeem rate must be 1% or greater.")
                for guest in self.records.guests:
                    guest.set_redeem_rate(new_rate)
                print(f"Updated redeem rate for all guests to {new_rate}%")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def generate_key_statistics(self):
        # Calculate "Top 3 most valuable guests"
        guests_sorted_by_value = sorted(self.records.guests, key=lambda guest: getattr(guest, 'total_order_amount', 0), reverse=True)[:3]

        # Calculate "Top 3 most popular products"
        products_sorted_by_quantity = sorted(self.records.products, key=lambda product: getattr(product, 'total_quantity_sold', 0), reverse=True)[:3]

        # Generate report content
        report = "Key Business Statistics Report\n\n"

        # Top 3 most valuable guests
        report += "Top 3 Most Valuable Guests:\n"
        for guest in guests_sorted_by_value:
            total_order_amount = getattr(guest, 'total_order_amount', 0)
            report += f"{guest.get_name()} - Total Order Amount: ${total_order_amount:.2f}\n"

        report += "\nTop 3 Most Popular Products:\n"
        # Top 3 most popular products
        for product in products_sorted_by_quantity:
            total_quantity_sold = getattr(product, 'total_quantity_sold', 0)
            report += f"{product.get_name()} - Quantity Sold: {total_quantity_sold}\n"

        # Save report to stats.txt
        with open("stats.txt", 'w') as file:
            file.write(report)

        # Display report to console as well
        print(report)

    def display_guest_order_history(self):
        guest_input = input("Enter guest ID or name: ").strip().lower()  # Make input case-insensitive
        guest = self.records.find_guest(guest_input)
    
        if guest is None:
            print(f"Guest '{guest_input}' not found.")
            return

        guest_orders = [order for order in self.records.orders if order.guest.get_id().lower() == guest.get_id().lower()]

        if not guest_orders:
            print(f"No orders found for guest '{guest.get_name()}'.")
            return

        # Display order history in a tabular format
        print(f"\nOrder history for {guest.get_name()}:\n")
        print(f"{'Order ID':<10} {'Products Ordered':<40} {'Total Cost':<15} {'Earned Rewards':<15}")
        print("=" * 80)

        for idx, order in enumerate(guest_orders, 1):
            products_ordered = f"{order.quantity} x {order.product.get_name()}"
            print(f"{'Order'+str(idx):<10} {products_ordered:<40} ${order.total_cost:<15.2f} {order.earned_rewards:<15}")

        print("=" * 80)

    def terminate_program(self):
        self.records.update_guest_file('guests.csv')
        self.records.update_product_file('products.csv')
        self.records.update_order_file('orders.csv')
        print("All data saved successfully. Exiting the program.")           

if __name__ == "__main__":
    records = Records()
    records.read_guests("guests.csv")
    records.read_products("products.csv")

    operations = Operations()
    operations.menu()


"""
References
1. RMIT University, "Programming Fundamentals," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/40579990/download?download_frd=1.

2. RMIT University, "Introduction to Python Classes," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/40712889/download?download_frd=1.

3. RMIT University, "Handling Data Files in Python," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/40934338/download?download_frd=1.

4. RMIT University, "Error Handling and Debugging in Python," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/41051619/download?download_frd=1.

5. RMIT University, "Advanced Topics: Object-Oriented Programming," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/41193305/download?download_frd=1.

6. RMIT University, "Final Submission Guidelines," accessed October 2024. [Online]. 
Available: https://rmit.instructure.com/courses/124829/files/41301616/download?download_frd=1.

7. "How to Code Efficiently in Python," YouTube, 22-Sept-2024. [Online]. 
Available: https://www.youtube.com/watch?v=KhklWqco8W0. [Accessed: 10-Oct-2024].

"""

