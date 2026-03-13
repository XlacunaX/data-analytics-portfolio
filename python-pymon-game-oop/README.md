# Python Pymon Adventure Game (Object-Oriented Programming)

This project was completed as part of the **Programming Fundamentals (COSC2531)** course in the **Master of Analytics program at RMIT University**.

## Objective
Develop a fully object-oriented Python game where a player controls a creature called **Pymon** to explore locations, collect items, and battle other creatures.

## Tools Used
- Python
- Object-Oriented Programming (OOP)
- CSV file handling
- Command-line interface

## Key Concepts Implemented

- Object-Oriented programming with multiple classes
- Inheritance (`Pymon` extends `Creature`)
- Exception handling
- File I/O using CSV files
- Game state management
- Inventory and item usage
- Statistics tracking

## Game Features

### Map Navigation
Players move through interconnected locations using directions:

- North
- South
- East
- West

Each location contains creatures and items.

### Inventory System
Players can collect and use items such as:

- Apple (restores energy)
- Magic Potion (temporary battle immunity)
- Binoculars (inspect nearby locations)

### Battle System
The game includes a **rock–paper–scissors battle system** against other Pymon creatures.

- Best-of-three encounters
- Energy decreases after losing rounds
- Winning captures the opponent Pymon.

### Energy Management
- Energy decreases after movement and battles
- Items can restore energy
- If energy reaches zero, the Pymon escapes to another location.

### Statistics Tracking
The game records:

- Battles won
- Battles lost
- Battle history with timestamps

### File-Based Data
Game data is loaded from external files:

- `locations.csv`
- `creatures.csv`
- `items.csv`

This allows the game world to be dynamically generated.
