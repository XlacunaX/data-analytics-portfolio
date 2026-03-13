# Python Apartment Booking System

This project was completed as part of the **Programming Fundamentals (COSC2531)** course in the **Master of Analytics program at RMIT University**.

## Objective
Develop a command-line booking system for a serviced apartment company to manage guest reservations, supplementary services, and reward points.

## System Overview

The program simulates a **Point of Sale (POS) booking system** for a serviced apartment company called **Pythonia**.

The system allows booking managers to:

- Make apartment bookings
- Add supplementary services
- Manage apartment information
- Track guest reward points
- View guest booking history

## Tools Used

- Python
- Command-line interface
- Built-in data structures (lists and dictionaries)

## Key Features

### Booking Management
Users can book apartment units by entering:

- Guest name
- Number of guests
- Apartment ID
- Check-in and check-out dates
- Length of stay

The program calculates:

- Total booking cost
- Reward points earned

### Supplementary Services

Guests can add optional services such as:

- Car park
- Breakfast
- Toothpaste
- Extra bed

Multiple items can be added during the booking process.

### Reward Points System

Guests earn **1 reward point per dollar spent**.

Reward points can be redeemed:
- Every **100 points = $10 discount**.

### Menu-Driven Interface

The system includes a menu with options to:

1. Make a booking  
2. Add/update apartment information  
3. Add/update supplementary items  
4. Display existing guests  
5. Display existing apartment units  
6. Display existing supplementary items  
7. Display guest booking history  
8. Exit the program

### Input Validation

The system validates:

- Guest names
- Apartment IDs
- Length of stay
- Quantity of items
- Menu choices
