'''
------------------------------------------------------------------------------------
Name: Shambhavi Tewari
Student ID: s4016395
Highest part attempted: All the parts are attempted and running in this code
Issues/errors: There are no errors in this program that might lead it to crashing.
-------------------------------------------------------------------------------------

DESIGN PROCESS OF THIS PROGRAM
Understanding the program's needs was the first step in the design process. 
The primary features needed were:
1. Taking care of bookings for guests, including managing the number of apartments and supplementary services.
2. Allowing improvements/updates to the apartments and supplementary items.
3. Maintaing the reward points of the guests.
4. offering a command-line menu interface that is easy to use and is interactive.

Based on the requirements, the core functions to be incorporated were: displaying a menu, booking functionality, data display and management.
For data structures dictionaries and lists were used.

* Function design
'display_menu()': Designed to give the user a simple text-based interface by displaying a menu of options.
'book_apartment()': is a feature-rich function designed to manage reservations. Input validation, processing guest selections for supplementary items,
cost calculation, and reward point management are all included in this function.
'validate_apartment_id()': This helper method makes sure that apartment IDs comply with a particular format to preserve data integrity.
'Add_update_apartment()' and 'add_update_supplementary_items()' are examples of data management functions that oversee the addition and 
updating of apartments and supplementary items, allowing for data modification as needed.
Display Functions: These functions help with transparency and user engagement by providing several ways to output stored data,
such as 'display_existing_guests()',' display_existing_apartments()', 'display_existing_supplementary_items()', and 'display_guest_history()'.

* While Loops were used to evaluate user input, making sure that when a user enters something incorrectly, the application asks them to try again rather than failing.
* Try-Except Blocks: These are used to handle potential errors and prevent crashes caused by erroneous data types, especially when dealing with numerical input.

WHY WHILE LOOP IS PREFERRED:
Since the while loop requires frequent user input validation and has unpredictable iteration counts, it is chosen over other loop types (such as for loops). 
The while loop's flexibility lies in its ability to carry on running after each iteration in response to a condition that is dynamically checked. 
While loops are ideal in scenarios where the number of repetitions is not preset, in contrast to for loops, which are usually employed when the number of iterations 
is known ahead of time.

* To oversee the hotel's supplementary items and reward point system, further logic was added:
Reward Points: Intended to allow users to earn points for their booking that can be exchanged for savings. To ensure accuracy and fairness, 
this function does careful point calculation and updating.
Supplementary Items: The logic permits visitors to request extra services, subject to restrictions (e.g., a maximum of two extra beds). 
This feature was included to improve the booking process and offer flexibility.

* Iterative Development and Testing
Initial Development: To make sure that essential elements like booking and data presentation operated as intended, the most basic functionality was put in place first.
Feature Expansion: New features were progressively added, like the ability to manage rewards and other items.
Testing and Debugging: To identify problems and make sure all features functioned as intended, regular running of the code was carried out. 
This procedure assisted in locating and resolving problems like inaccurate computations or inappropriate input handling.

* Challenges 
The most challenging part during this program was after defining the initial booking system. The updating of apartments and supplementary items hence these parts had to
be broken down into more smaller and manageable parts. Furthur on while make the exisiting guest history was challenging as initially in my code the guest history won't 
update, some logic revision was required for this part.

'''
# Dictionary consisting of existing guest in the hotel
existing_guests = {'Alyssa': 20, 'Luigi': 32}                        # "Python Dictionary," GeeksforGeeks, [Online]. Available: https://www.geeksforgeeks.org/python-dictionary/. 
                                                                     #  [Accessed: 9/08/2024].

# Dictionary for apartment ID, rate and capacity
apartments_hotel = {'U12swan': {'rate': 95.0, 'capacity': 2},
                    'U209duck': {'rate': 106.7, 'capacity': 3},
                    'U49goose': {'rate': 145.2, 'capacity': 4}}

# Dictionary of supplementary items and their rate
supplementary_items = {
    "car_park": {
        "price": 25,  # Price in AUD per night
    },
    "breakfast": {
        "price": 21,  # Price in AUD per person
    },
    "toothpaste": {
        "price": 5,  # Price in AUD per tube
    },
    "extra_bed": {
        "price": 50,  # Price in AUD per item
    }
}

# Dictionary to store the booking history for each guest
guest_order_history = {}

# Function to display the menu consisting of all the options that a user can choose from 
def display_menu():

    '''
    This function displays the main menu to the user showing the options avaible for different actions
    related to hotel booking and management, such as making a booking, updating information about supplementary
    item or apartment units, displaying existing guest, apartment unit, supplementary item data, and to exit the program.

    This function does not take any parameters and either does return any value. It just
    prints the menu options for the user to choose from. 

    '''
    print("\nWelcome to Pythonia Service Apartments!")
    print("="*50)
    print("Please choose from the following options:")
    print("1) Make a booking")
    print("2) Add/update information of an apartment unit")
    print("3) Add/update information of a supplementary item")
    print("4) Display existing guests")
    print("5) Display existing apartment units")
    print("6) Display existing supplementary items")
    print("7) Display a guest booking and order history")
    print("0) Exit the program")
    print("="*50)

# Function to display booking receipt
def display_receipt(guest_name, number_of_guests, apartment_id, apartment_rate, checkin_date, checkout_date,
                    length_of_stay, booking_date, total_cost, reward_points, supplementary_orders):
    '''
    This function is to display the booking receipt.
    Parameters of this function are:
    guest_name (str): The name of the guest.
    number_of_guests (int): The number of guests for whom the booking is being made.
    apartment_id (str): The apartment ID of the booked apartment.
    apartment_rate (float): The rate per night of the booked apartment.
    checkin_date (str): The check-in date for the booking.
    checkout_date (str): The check-out date for the booking.
    length_of_stay (int): The duration of the stay.
    booking_date (str): The date of booking.
    total_cost (float): The total cost of the booking including supplementary items, if ordered.
    reward_points (int): The reward points earned from the booking.
    supplementary_orders (list): A list of supplementary items and their details.
    
    This function does not return any value.

    '''
    print("=" * 50)
    print("      Pythonia Serviced Apartments - Booking Receipt     ")
    print("=" * 50)
    print(f"Guest Name: {guest_name}")
    print(f"Number of guests: {number_of_guests}")
    print(f"Apartment id: {apartment_id}")
    print(f"Apartment rate: ${apartment_rate} (AUD)")
    print(f"Check-in date: {checkin_date}")
    print(f"Check-out date: {checkout_date}")
    print(f"Length of stay: {length_of_stay} nights")
    print(f"Booking date: {booking_date}")
    print("-" * 50)
    
    # If statement to display supplementary items (if any) ordered by the user. This if statement is the to display the list of 
    # supplementary items ordered by the user, it's quanity, price and then the total price of all the items 
    # ordered. It prints the price in AUD.

    if supplementary_orders:
        print("Supplementary items:")
        supplementary_total = 0
        for item in supplementary_orders:
            item_id = item['id']
            quantity = item['quantity']
            price = item['price']
            cost = item['cost']
            supplementary_total += cost
            print(f"Item id: {item_id} Quantity: {quantity} Price: ${price} Cost: ${cost}")

        print(f"Sub-total: ${supplementary_total:.2f}")
        print("-" * 50)

    print(f"Total cost: ${total_cost:.2f} (AUD)")
    print(f"Earned rewards: {reward_points} points")
    print("Thank you for your booking! We hope you will have an enjoyable stay.")
    print("=" * 50)

# Function for booking the apartment    
def book_apartment():
    '''
    This function handles the process of booking for the guest, it includes the input such as the guest name,
    number of guests, apartment ID etc. and there after calculating the total cost of booking, 
    and also managing the supplementary items and reward points.
    There are no parameters in this function and returns no value.

    This function is used to facilitate the main booking flow. Gathering guest information is the first step, 
    followed by confirming that the apartment of choice can hold the amount of guests and, if necessary, 
    adding extra beds. In addition, it handles reward point management, computes the final cost,
    and processes any additional items the guest requests. The function shows a thorough receipt after 
    updating the necessary dictionaries for guests and their order histories.

    '''

    while True:
        guest_name = input("Enter the main guest's name (e.g., Luigi): ").strip()
        if guest_name.isalpha():
            break
        else:
            print("Invalid name. Please enter a name containing only alphabetic characters.")

    while True:
        try:
            number_of_guests = int(input("Enter the number of guests: "))
            if number_of_guests <= 0:
                print("Please enter a positive number for guests.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for guests.")

    while True:
        apartment_id = input("Enter the apartment ID (e.g., U12swan, U209duck, U49goose): ")
        if apartment_id in apartments_hotel:
            apartment_rate = apartments_hotel[apartment_id]['rate']
            apartment_capacity = apartments_hotel[apartment_id]['capacity']
            print(f"Apartment rate for {apartment_id}: ${apartment_rate} per night")
            
            # Check if the number of guests exceeds the apartment's capacity
            if number_of_guests > apartment_capacity:
                print("Warning: The number of guests exceeds the apartment's capacity.")
                print("Please consider ordering an extra bed.")
                
                extra_beds_ordered = 0
                while number_of_guests > apartment_capacity and extra_beds_ordered < 2:
                    order_extra_bed = input("Would you like to order an extra bed? (y/n): ").strip().lower()
                    if order_extra_bed == 'y':
                        while True:
                            try:
                                quantity = int(input("Enter the quantity of extra beds (maximum 2): "))
                                if quantity < 1 or quantity > 2:
                                    print("You can only order up to 2 extra beds.")
                                    continue
                                break
                            except ValueError:
                                print("Please enter a valid number for quantity.")

                        if quantity + extra_beds_ordered > 2:
                            print("You can only order up to 2 extra beds in total.")
                            continue

                        item_id = 'extra_bed'
                        item_price = supplementary_items[item_id]['price']
                        item_cost = item_price * quantity
                        print(f"Item: {item_id}, Price per unit: ${item_price}, Quantity: {quantity}, Total Cost: ${item_cost}")

                        confirm = input("Do you want to confirm this order? (y/n): ").strip().lower()
                        if confirm == 'y':
                            extra_beds_ordered += quantity
                            apartment_capacity += quantity * 2  # Each extra bed allows for 2 more people
                            print(f"Order confirmed. {quantity} extra bed(s) added, increasing capacity to {apartment_capacity}.")
                        else:
                            print("Extra bed order cancelled.")
                    elif order_extra_bed == 'n':
                        break
                    else:
                        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

                if number_of_guests > apartment_capacity:
                    print("The number of guests still exceeds the maximum capacity even after ordering extra beds.")
                    print("Booking cannot proceed. Returning to main menu.")
                    return
            break
        else:
            print("Invalid apartment ID. Please try again.")

    checkin_date = input("Enter the check-in date (d/m/yyyy): ")
    checkout_date = input("Enter the check-out date (d/m/yyyy): ")

    while True:
        try:
            length_of_stay = int(input("Enter the length of stay (nights): "))
            if length_of_stay <= 0:
                print("Length of stay must be a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the length of stay.")

    booking_date = input("Enter the booking date (d/m/yyyy): ")

    total_cost = apartment_rate * length_of_stay
    reward_points = round(total_cost)  # Earned reward points before deduction

    # Initializing current_points to 0
    current_points = 0
    
    # Checking if the guest already has any reward points
    if guest_name in existing_guests:
        current_points = existing_guests[guest_name]

    
    total_supplementary_cost = 0
    supplementary_orders = []

    while True:
        order_more = input("Do you want to order a supplementary item? (y/n): ").strip().lower()
        if order_more == 'n':
            break
        elif order_more == 'y':
            print("\nAvailable Supplementary Items:")
            for item, details in supplementary_items.items():
                print(f"{item}: ${details['price']} each")

            while True:
                item_id = input("Enter Supplementary Item ID (e.g., car_park, breakfast, toothpaste, extra_bed): ").strip().lower()
                if item_id in supplementary_items:
                    item_price = supplementary_items[item_id]['price']
                    print(f"Price for {item_id}: ${item_price} each")
                    break
                else:
                    print("Invalid item ID. Please try again.")

            while True:
                try:
                    quantity = int(input(f"Enter quantity for {item_id}: "))
                    if quantity > 0:
                        break
                    else:
                        print("Please enter a positive quantity.")
                except ValueError:
                    print("Please enter a valid number for quantity.")

            item_cost = item_price * quantity
            print(f"Item: {item_id}, Price per unit: ${item_price}, Quantity: {quantity}, Total Cost: ${item_cost}")

            confirm = input("Do you want to confirm this order? (y/n): ").strip().lower()
            if confirm == 'y':
                total_supplementary_cost += item_cost
                supplementary_orders.append({'id': item_id, 'quantity': quantity, 'price': item_price, 'cost': item_cost})
                print(f"Order confirmed. Supplementary cost so far: ${total_supplementary_cost:.2f}")
            else:
                print("Item cancelled.")
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    total_cost += total_supplementary_cost

    # Check for reward points usage
    if current_points >= 100:
        print(f"You have {current_points} reward points.")
        use_points = input("Would you like to use your reward points to reduce the total cost? (y/n): ").strip().lower()
        if use_points == 'y':
            points_to_use = (current_points // 100) * 100  # Calculate points to use in multiples of 100
            discount = (points_to_use // 100) * 10  # Each 100 points gives $10 discount
            total_cost -= discount
            current_points -= points_to_use
            print(f"{points_to_use} points were used, reducing the total cost by ${discount:.2f}. New total cost: ${total_cost:.2f}")
        else:
            print("No reward points were used.")

    # Update guest's reward points after the booking
    if guest_name in existing_guests:
        existing_guests[guest_name] = current_points + reward_points
    else:
        existing_guests[guest_name] = reward_points

    # Store the order history
    order_details = {
        'apartment_id': apartment_id,
        'supplementary_orders': supplementary_orders,
        'total_cost': total_cost,
        'earned_rewards': reward_points
    }

    if guest_name in guest_order_history:
        guest_order_history[guest_name].append(order_details)
    else:
        guest_order_history[guest_name] = [order_details]    

    # Display final receipt, ensuring supplementary_orders is passed correctly
    display_receipt(guest_name, number_of_guests, apartment_id, apartment_rate, checkin_date, checkout_date,
                    length_of_stay, booking_date, total_cost, reward_points, supplementary_orders)

# Function to validate apartment ID format
def validate_apartment_id(apartment_id):
    '''
    This fucntion is used to validate the format of the entered apartment ID to ensure that it in the correct 
    format i.e starting with 'U' followed by numbers and ending with alphabetic characters representing the apartment name.
    Parameters of this function includes:
    apartment_id (str): This the apartment ID that needs to be validated.

    It returns a bool value, true if the apartment ID is valid i.e in the correct format, otherwise false.

    '''
    if len(apartment_id) < 3:
        return False
    if apartment_id[0] != 'U':
        return False
    i = 1
    while i < len(apartment_id) and apartment_id[i].isdigit():
        i += 1
    if i == len(apartment_id):  # No building name found
        return False
    building_name = apartment_id[i:]
    if not building_name.isalpha():
        return False
    return True

# Function to add or update apartment unit
def add_update_apartment():
    '''
    This function adds a new apartment in the dictionary or updates an existing apartment's information 
    such as capacity or rate. It first validates the apartment 
    ID format using the `validate_apartment_id()` function.
    
    '''
    input_str = input("Enter apartment_id rate capacity: ").strip()
    try:
        apartment_id, rate, capacity = input_str.split()
        if not validate_apartment_id(apartment_id):
            print("Invalid apartment ID format. Please use the format 'U12swan'.")
            return
        rate = float(rate)
        capacity = int(capacity)
        apartments_hotel[apartment_id] = {'rate': rate, 'capacity': capacity}
        print(f"Apartment {apartment_id} updated: Rate = {rate}, Capacity = {capacity} beds.")
    except ValueError:
        print("Invalid input. Please enter the data in the format: apartment_id rate capacity.")


def add_update_supplementary_items():
    '''
    This function makes it easier for users to handle more items by letting them add new ones or change their prices. 
    It verifies that the prices are valid numeric numbers and are greater than zero and also that the input is formatted correctly.

    '''
    while True:
        input_data = input("Enter supplementary item info (e.g., toothpaste 5.2, shampoo 8.2): ").strip()
        # Split the input by commas to handle multiple items
        items = [item.strip() for item in input_data.split(",")]

        valid_input = True
        updates = {}

        for item in items:
            parts = item.split()
            if len(parts) != 2:
                print("Invalid format. Please enter the data in the format: item_1 price_1, item_2 price_2, ...")
                valid_input = False
                break
            
            item_id, price = parts
            item_id = item_id.strip()
            price = price.strip()

            try:
                price = float(price)
                if price <= 0:
                    print(f"Price for {item_id} must be positive.")
                    valid_input = False
                    break
            except ValueError:
                print(f"Invalid price for {item_id}. Please enter a numeric value.")
                valid_input = False
                break
            
            updates[item_id] = price
        
        if valid_input:
            for item_id, price in updates.items():
                supplementary_items[item_id] = {"price": price}
                print(f"Supplementary item {item_id} updated with price ${price:.2f}.")
            break
        else:
            print("Please enter a valid list of supplementary items and prices.")

def display_existing_guests():
    '''
    This function offers a concise summary of every visitor who has made an apartment reservation in the past, 
    and their earned reward points. It facilitates monitoring the consumer rewards and engagement.
    '''
    print("Existing guests and their reward points:")
    for guest, points in existing_guests.items():
        print(f"{guest}: {points} points")

def display_existing_apartments():
    '''
    This function allows customers to see every apartment currently available in the hotel, 
    along with information about their per night price and the maximum number of guests that can accomodate
    in that apartment.
    '''
    print("Existing apartment units:")
    for apartment_id, info in apartments_hotel.items():
        print(f"{apartment_id}: ${info['rate']} per night, Capacity: {info['capacity']} beds")

def display_existing_supplementary_items():
    '''
    The function provides a list of all the supplementary items that are available to guests, along with their current costs. 
    This helps give guests the chance to personalize their stay by adding extra services or goods.

    '''
    print("Existing supplementary items:")
    for item, details in supplementary_items.items():
        print(f"{item}: ${details['price']} each")    

def display_guest_history():
    '''
    This function displays the the booking and order history of a specific guest based on their name. 
    It shows the apartments booked, supplementary items ordered, total costs, and earned rewards for each booking.

    '''
    while True:
        guest_name = input("Enter the guest's name to view their booking and order history: ").strip()
        if guest_name.isalpha() and guest_name in guest_order_history:
            break
        else:
            print("Invalid guest name or no booking history found. Please enter a valid guest name.")

    print(f"\nThis is the booking and order history for {guest_name}.")
    print("=" * 50)
    for i, order in enumerate(guest_order_history[guest_name], start=1):
        print(f"Order {i}")
        print(f"1 x {order['apartment_id']}")
        for supplementary in order['supplementary_orders']:
            print(f"{supplementary['quantity']} x {supplementary['id']}")
        print(f"Total Cost: ${order['total_cost']:.2f}")
        print(f"Earned Rewards: {order['earned_rewards']}")
        print("-" * 50)

# Function for menu
def menu():
    '''
    This function displays the main menu and handles user input for going 
    through different options and then calls the appropriate functions 
    based on user selection. This function has no paramteres and returns no value.
    
    ''' 
    while True:
        display_menu()
        choice = input("Enter a number to choose an option: ").strip()
        if choice == '1':
            book_apartment()
        elif choice == '2':
            add_update_apartment()
        elif choice == '3':
            add_update_supplementary_items()
        elif choice == '4':
            display_existing_guests()
        elif choice == '5':
            display_existing_apartments()
        elif choice == '6':
            display_existing_supplementary_items()
        elif choice == '7':  
            display_guest_history()    
        elif choice == '0':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")  

# Main function to start the booking process
def main():
    '''
    This is the entry point of the program. Calls the `menu()` function 
    to start the booking session with the user.

    '''
    menu()

if __name__ == "__main__":
    main()


'''
Course References
[1] Dipto Pratyaksa, "Week 1," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6546724. 

[2] Dipto Pratyaksa, "Week 2," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6563481. 

[3] Dipto Pratyaksa, "Week 3," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6575286. 

[4] Dipto Pratyaksa, "Week 4," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6592271. 

[5] Dipto Pratyaksa, "Week 5," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6600677. 

[6] Dipto Pratyaksa, "Week 6," RMIT Canvas. Available: https://rmit.instructure.com/courses/124829/modules/items/6609115. 

Other References
[1] P. S. "Hotel Management System Project in Python with Free Source Code," Medium, Jun. 22, 2023. [Online]. 
Available: https://medium.com/@pies052022/hotel-management-system-project-in-python-with-free-source-code-d77a475d8321. [Accessed:10/08/2024].

[2] "Hotel Management Project in Python," GeeksforGeeks, [Online]. Available: https://www.geeksforgeeks.org/hotel-management-project-in-python/. [Accessed: 10/08/2024].

'''

