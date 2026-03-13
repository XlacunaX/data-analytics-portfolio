"""
@author: Shambhavi Tewari
@student_id : s4016395
@highest_level_attempted (P/C/D/HD): HD

- Reflection:
Design Process:
The design process started by determining the fundamental elements needed for a game that included locations, creatures, items, 
and a Pymon that the player controlled. For clarity and reusability, I divided the game into modular classes called Location, Creature, 
Pymon (which inherits from Creature), Item, and Record. These classes represented different game entities. In order to facilitate interactions, 
key methods were then created. The Operation class served as the main controller for setup, input processing, and game state modifications, 
keeping a single duty for every class. Entities were kept in lists, and named data, such as player stats, could be accessed more easily 
using the dictionaries, which allowed for flexible and effective game management.

Challenges: 
Making links between locations was one of the main challenges especially making sure that every directional door 
connected to the appropriate Location. At first, I kept door connections as strings, which are location names, 
but this wasn't enough to retrieve attributes. I came up with a two-step method to fix this: first, I set doors by name, 
and then I resolved each door to point to a real Location object, enabling bidirectional travel. I used the 
verify_door_connections method to automate the tedious process of confirming that connections were legitimate.
Managing the pymon's energy while they were moving and fighting, was another challenge. Tracking moves to decrement energy 
and putting in place an escape mechanism when energy ran out were necessary for this. To ensure gameplay continuity, 
the Pymon's escape and respawn mechanism was designed using recursion-like handling, which places the pymon
in a new area and resets energy.

- Reference:
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

7. Computerphile, “Pathfinding for Beginners - A* Algorithm,” YouTube, Aug. 15, 2018. [Online]. 
Available: https://www.youtube.com/watch?v=waY3LfJhQLY

8. Brackeys, “How to make a Video Game in Unity - BEGINNER TUTORIAL,” YouTube, Feb. 15, 2020. [Online]. 
Available: https://www.youtube.com/watch?v=fo4e3njyGy0

"""

import random
import os 
from datetime import datetime
import sys

# Get file names from command-line arguments with defaults
location_file = "locations.csv"
creature_file = "creatures.csv"
item_file = "items.csv"

if len(sys.argv) > 1:
    location_file = sys.argv[1]
if len(sys.argv) > 2:
    creature_file = sys.argv[2]
if len(sys.argv) > 3:
    item_file = sys.argv[3]

# Setting the working directory 
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
print("Changed working directory to:", os.getcwd())

# Function for random generator
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 

class InvalidDirectionException(Exception):
    """Exception raised when an invalid direction is selected."""
    pass

class InvalidInputFileFormat(Exception):
    """Exception raised when a CSV file has invalid content or format."""
    pass

            
class Location:

    """
    This class represents a location in the Pymon world.

    Attributes:
    - name (str): The name of the location.
    - description (str): A brief description of the location.
    - doors (dict): Dictionary of doors connecting this location to others in four cardinal directions 
      (keys: "west", "north", "east", "south")
    - creatures (list): List of creatures present in the location.
    - items (list): List of items present in the location.

    Methods:
    - add_creature(creature): Adds a creature to the location.
    - add_item(item): Adds an item to the location.
    - connect_east(another_room): Connects this location's east door to another room's west door.
    - connect_west(another_room): Connects this location's west door to another room's east door.
    - connect_north(another_room): Connects this location's north door to another room's south door.
    - connect_south(another_room): Connects this location's south door to another room's north door.
    - get_name(): Returns the name of the location.
    - get_description(): Returns the description of the location.
    
    """

    def __init__(self, name="New room", description="A mysterious place", w=None, n=None, e=None, s=None):
        self.name = name
        self.description = description
        self.doors = {
            "west": w,
            "north": n,
            "east": e,
            "south": s
        }
        self.creatures = []
        self.items = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def add_item(self, item):
        self.items.append(item)

    def connect_east(self, another_room):
        self.doors["east"] = another_room
        another_room.doors["west"] = self

    def connect_west(self, another_room):
        self.doors["west"] = another_room
        another_room.doors["east"] = self

    def connect_north(self, another_room):
        self.doors["north"] = another_room
        another_room.doors["south"] = self

    def connect_south(self, another_room):
        self.doors["south"] = another_room
        another_room.doors["north"] = self

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class Creature:
    """
    This class provides the foundation for all of the game's creatures, enabling them to have distinct identifiers, 
    descriptions, and locations. Other classes (like Pymon) that might have more features or properties are intended to extend it.

    Attributes:
    - nickname (str): The unique name or nickname of the creature.
    - description (str): A brief description of the creature. Defaults to "A mysterious creature."
    - location (Location or None): The location where the creature is currently present. Initially set to None.

    Methods:
    - set_location(location): Sets the creature's location.
    - get_location(): Returns the creature's current location.
    - __str__(): Provides a string representation of the creature, displaying its nickname and description.

    """

    def __init__(self, nickname, description="A mysterious creature"):
        self.nickname = nickname
        self.description = description
        self.location = None  

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def __str__(self):
        return f"{self.nickname}: {self.description}"


class Pymon(Creature):
    """
    The Pymon class is intended to be a player character that moves around different environments, interacts with objects, 
    and encounters other animals. Building upon the fundamental features of the Creature class, this class adds 
    features unique to the Pymon, like inventory management, energy management, and a rock-paper-scissors battle system.

    Attributes:
    - energy (int): The energy level of the Pymon, initialized to 3, which decreases with movement and challenges.
    - current_location (Location or None): The current location of the Pymon in the game world.
    - inventory (list): A list to store items collected by the Pymon.
    - immunity (bool): A flag to indicate temporary immunity in battle, activated when a magic potion is used.
    - has_binocular (bool): A flag to indicate if the Pymon has a binocular, used to inspect neighboring locations.
    - move_count (int): A counter to track moves made by the Pymon, influencing energy depletion.
    - battle_history (list): Stores records of battles the Pymon has participated in.

    Methods:
    - move(direction): Moves the Pymon in a specified direction if possible, depleting energy every two moves.
    - escape(locations): Handles the Pymon's escape to a random location when energy is depleted.
    - spawn(loc): Sets the Pymon's starting location.
    - get_location(): Returns the current location of the Pymon.
    - get_energy(): Returns the current energy level of the Pymon.
    - set_energy(energy): Sets the energy level of the Pymon within the valid range (0 to 3).
    - inspect(): Displays the Pymon's nickname, energy, and current location.
    - pick_item(item_name): Allows the Pymon to pick up an item in its current location if it is pickable.
    - view_inventory(): Displays the Pymon's inventory and allows selection of an item to use.
    - use_binocular(): Provides an option to inspect the Pymon's current and adjacent locations using a binocular.
    - use_item(item_name): Uses an item from the Pymon's inventory if it matches the specified name.
    - challenge(creature_name): Initiates a battle with a specified creature in the current location, playing a rock-paper-scissors game.

    """

    def __init__(self, nickname="The player"):
        super().__init__(nickname, "A loyal Pymon")
        self.energy = 3  # Starting with 3/3 energy points
        self.current_location = None
        self.inventory = []  # Initialize inventory as an empty list
        self.immunity = False
        self.has_binocular = False
        self.move_count = 0  # Track moves for energy reduction
        self.battle_history = []

    def move(self, direction=None):
        if self.current_location is not None and direction in self.current_location.doors:
            next_location = self.current_location.doors[direction]

            # Ensure that next_location is a Location object, not a string
            if isinstance(next_location, Location):
                print(f"\nMoving to which direction?: {direction}")
                print(f"You traveled {direction} and arrived at {next_location.get_name()}.")

                # Only remove self if it exists in the creatures list
                if self in self.current_location.creatures:
                    self.current_location.creatures.remove(self)
                else:
                    print(f"Warning: {self.nickname} not found in {self.current_location.get_name()} creatures list.")

                # Add self to the new location
                next_location.add_creature(self)
                self.current_location = next_location
                self.move_count += 1  # Increment move count

                # Decrease energy every 2 moves
                if self.move_count % 2 == 0:
                    self.energy -= 1
                    print(f"Pymon's energy decreased to {self.energy}")
                    if self.energy <= 0:
                        self.escape(Operation().record.locations)  # Pass locations to escape method
            else:
                print(f"There is no door to the {direction}. Pymon remains at its current location.")
        else:
            raise InvalidDirectionException(f"No location in the {direction} direction.")

    def escape(self, locations):
        # Handle escape when energy is depleted
        print("Pymon has no energy and is escaping into the wild!")
        if not locations:
            print("No locations available for escape. Game cannot continue.")
            exit()

        random_location = random.choice(locations)  # Move to a random location
        self.spawn(random_location)  # Move Pymon to random location
        if len(Operation.bench) == 0:
            print("This was your last Pymon. Game over!")
            exit()
        else:
            self.energy = 3  # Reset energy after escape
            print(f"Pymon escaped to {random_location.get_name()} and regained some energy.")

    def spawn(self, loc):
        if loc is not None:
            loc.add_creature(self)
            self.current_location = loc
            print(f"{self.nickname} spawned at {loc.get_name()}")  

    def get_location(self):
        return self.current_location

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        # Set energy, ensuring it remains within allowed range (e.g., 0 to 3)
        self.energy = max(0, min(3, energy))

    def inspect(self):
        # Display Pymon's biodata and energy
        print(f"Pymon {self.nickname} - Energy: {self.energy} - Location: {self.current_location.get_name() if self.current_location else 'None'}")

    def pick_item(self, item_name):
        # Attempt to pick up an item in the current location
        for item in self.current_location.items:
            if item.name.lower() == item_name.lower():
                if item.is_pickable:
                    print(f"{item.name} has been added to your inventory.")
                    self.inventory.append(item)
                    self.current_location.items.remove(item)
                else:
                    print(f"{item.name} cannot be picked up.")
                return
        print(f"No item named '{item_name}' found here.")

    def view_inventory(self):
        # Display all items in the inventory
        if not self.inventory:
            print("Your inventory is empty.")
            return

        print("\nYour inventory contains:")
        for idx, item in enumerate(self.inventory, 1):
            print(f"{idx}) {item}")

        # Sub-command to use an item
        choice = input("Enter the item number to use or press Enter to go back: ").strip()
        if choice:
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(self.inventory):
                    item = self.inventory[choice]
                    print(f"Using {item.name}...")
                    self.use_item(item.name)  
                else:
                    print("Invalid item selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")


    def use_binocular(self):
        option = input("Select binocular option ('current', 'west', 'north', 'east', 'south'): ").lower()

        if option == "current":
            creatures = ", ".join(c.nickname for c in self.current_location.creatures if c != self)
            items = ", ".join(i.name for i in self.current_location.items)
            details = f"In the current area, you see: "
            details += f"{creatures}" if creatures else "no creatures"
            details += f" and items like {items}." if items else " and no notable items."
            print(details)

        elif option in ["west", "north", "east", "south"]:
            connected_location = self.current_location.doors.get(option)
            if connected_location:
                creatures = ", ".join(c.nickname for c in connected_location.creatures)
                items = ", ".join(i.name for i in connected_location.items)
                print(f"In the {option}, there is {connected_location.get_name()}.")
                print(f"  Description: {connected_location.description}")
                print(f"  Creatures: {creatures}" if creatures else "  No creatures here.")
                print(f"  Items: {items}" if items else "  No items here.")
            else:
                print(f"This direction ({option}) leads nowhere.")
        else:
            print("Invalid option selected for binocular.")


    def use_item(self, item_name):
        item = next((i for i in self.inventory if i.name.lower() == item_name.lower()), None)
        if not item:
            print(f"No item named '{item_name}' in inventory.")
            return

        # Handle different item types
        if item_name.lower() == "apple":
            if self.energy < 3:
                self.energy += 1
                print(f"Pymon ate the apple. Energy increased to {self.energy}.")
            else:
                print("Pymon's energy is already at maximum.")
            self.inventory.remove(item)

        elif item_name.lower() == "magic potion":
            self.immunity = True
            print("Magic potion used. Pymon has temporary immunity in the next battle.")
            self.inventory.remove(item)

        elif item_name.lower() == "binocular":
            print("Using Binocular...")  
            self.use_binocular()  
            self.inventory.remove(item)

        else:
            print(f"The item '{item_name}' cannot be used.")


    def challenge(self, creature_name):
        opponent = next((c for c in self.current_location.creatures if c.nickname.lower() == creature_name.lower()), None)

        if not opponent:
            print(f"No creature named '{creature_name}' here to challenge.")
            return None  

        print(f"Challenging {opponent.nickname} to a battle!")
        outcomes = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
        win_count = 0
        lose_count = 0
        draw_count = 0  # Track draws

        while self.energy > 0 and win_count < 2 and lose_count < 2:
            player_choice = input("Choose (rock, paper, scissors): ").lower()
            if player_choice not in ['rock', 'paper', 'scissors']:
                print("Invalid choice. Please choose 'rock', 'paper', or 'scissors'. Try again.")
                continue

            opponent_choice = random.choice(['rock', 'paper', 'scissors'])
            print(f"Opponent chose {opponent_choice}")

            if player_choice == opponent_choice:
                print("It's a draw.")
                draw_count += 1
            elif outcomes[player_choice] == opponent_choice:
                print("You win this round!")
                win_count += 1
            else:
                print("You lose this round.")
                lose_count += 1
                if self.immunity:
                    print("Your magic potion protected you!")
                    self.immunity = False  
                else:
                    self.energy -= 1

        # Determine result and modify game state
        result = {
            "opponent": opponent.nickname,
            "win": win_count,
            "draw": draw_count,
            "loss": lose_count
        }

        if win_count == 2:
            print(f"You defeated {opponent.nickname} and captured it!")
            self.current_location.creatures.remove(opponent)
    
            # Convert the defeated creature to a Pymon and add to bench
            captured_pymon = Pymon(opponent.nickname)
            captured_pymon.description = opponent.description
            Operation.bench.append(captured_pymon)  
            print(f"{opponent.nickname} has been added to your bench.")
    
            Operation.stats["battles_won"] += 1
        elif lose_count == 2 or self.energy <= 0:
            print("You lost the battle. Pymon retreats!")
            Operation.stats["battles_lost"] += 1

        return result 
    
class Record:
    """
    The Record class manages data imports and initializes associations between places, creatures, and items in order 
    to act as a central repository for game entities. This makes it possible to maintain and access game elements 
    in an organized manner, which is necessary for effective game functionality.

    Attributes:
    - locations (list): Stores all Location objects created from the location data file.
    - creatures (list): Stores all Creature or Pymon objects created from the creature data file.
    - items (list): Stores all Item objects created from the item data file.

    Methods:
    - import_location(filename): Reads location data from a CSV file and creates Location objects. Also resolves door connections between locations.
    - get_locations(): Returns the list of all locations.
    - import_creatures(filename): Reads creature data from a CSV file, creates Creature or Pymon objects, and assigns them to random locations.
    - import_items(filename): Reads item data from a CSV file and creates Item objects, storing them in the items list.
    - find_location_by_name(name): Searches and returns a Location object by its name if found.

    """

    def __init__(self):
        self.locations = []
        self.creatures = []
        self.items = []  


    def import_location(self, filename="locations.csv"):
        try:
            with open(filename, mode="r") as file:
                next(file)
                for row in file:
                    if not row.strip():
                        continue 

                    # Split row by commas and unpack into variables
                    parts = row.strip().split(',')
                    if len(parts) < 6:
                        raise InvalidInputFileFormat("Location file has invalid format or missing columns.")
            
                    # Extract the name, description, and door names
                    name = parts[0].strip()
                    description = parts[1].strip()
                    west = parts[2].split('=')[1].strip() if '=' in parts[2] else parts[2].strip()
                    north = parts[3].split('=')[1].strip() if '=' in parts[3] else parts[3].strip()
                    east = parts[4].split('=')[1].strip() if '=' in parts[4] else parts[4].strip()
                    south = parts[5].split('=')[1].strip() if '=' in parts[5] else parts[5].strip()
            
                    # Create the location and temporarily store door names as strings
                    location = Location(name=name, description=description)
                    location.doors["west"] = west if west != "None" else None
                    location.doors["north"] = north if north != "None" else None
                    location.doors["east"] = east if east != "None" else None
                    location.doors["south"] = south if south != "None" else None
                    self.locations.append(location)

        # Resolve door connections
            for location in self.locations:
                for direction, target_name in location.doors.items():
                    if target_name:
                        target_location = self.find_location_by_name(target_name)
                        if target_location:
                            if direction == "west":
                                location.connect_west(target_location)
                            elif direction == "north":
                                location.connect_north(target_location)
                            elif direction == "east":
                                location.connect_east(target_location)
                            elif direction == "south":
                                location.connect_south(target_location)
                        else:
                            print(f"Warning: Target location '{target_name}' not found for {location.name}'s {direction} door.")

        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except InvalidInputFileFormat as e:
            print(f"Error in {filename}: {e}")


    def get_locations(self):
        return self.locations        

    def import_creatures(self, filename="creatures.csv"):
        try:
            with open(filename, mode="r") as file:
                next(file)  # Skip header row
                for line in file:
                    row = line.strip().split(',')
                    if len(row) < 3:
                        raise InvalidInputFileFormat("Creatures file has invalid format or missing columns.")
                
                    # Read only name, description, and adoptable status
                    nickname = row[0].strip()
                    description = row[1].strip()
                    adoptable = row[2].strip().lower() == "yes"

                    # Create the creature or Pymon based on the adoptable status
                    creature = Pymon(nickname) if adoptable else Creature(nickname, description)

                    # Instead of assigning a location from the file, assign randomly
                    random_location = random.choice(self.locations) if self.locations else None
                    if random_location:
                        random_location.add_creature(creature)
                    else:
                        print("Warning: No locations available to place creatures.")

                    # Append creature to the list for tracking
                    self.creatures.append(creature)
                    
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except InvalidInputFileFormat as e:
            print(f"Error in {filename}: {e}")

    def import_items(self, filename="items.csv"):
        try:
            with open(filename, mode="r") as file:
                next(file)
                for line in file:
                    row = line.strip().split(',')
                    if len(row) < 2:
                        raise InvalidInputFileFormat("Items file has invalid format or missing columns.")
                
                    name, description = row[0], row[1]
                    item = Item(name=name, description=description)
                    self.items.append(item)
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except InvalidInputFileFormat as e:
            print(f"Error in {filename}: {e}")


    def find_location_by_name(self, name):
        for location in self.locations:
            if location.get_name() == name:
                return location
        return None

class Item:
    """
    In the game, different items are created and managed using the Item class. Each item can affect Pymon or the player 
    in a different way, giving the game more depth. The `use` technique improves interactivity by enabling items to 
    directly affect the Pymon's state based on their distinct effects.

    Attributes:
    - name (str): The name of the item.
    - description (str): A brief description of the item.
    - is_pickable (bool): Indicates if the item can be picked up and added to a player's inventory.
    - effect (function, optional): A function that defines any special effect the item has on the Pymon when used.

    Methods:
    - use(pymon): Applies the item's effect to the specified Pymon if an effect is defined.
    - __str__(): Provides a string representation of the item, combining its name and description.

    
    """

    def __init__(self, name, description, is_pickable=True, effect=None):
        self.name = name
        self.description = description
        self.is_pickable = is_pickable
        self.effect = effect

    def use(self, pymon):
        if self.effect:
            self.effect(pymon) 

    def __str__(self):
        return f"{self.name}: {self.description}"

    
class Operation:
    """
    As the primary controller of the game, the Operation class controls interactions, maintains the gaming environment, 
    and logs player progress. To produce a seamless game experience, it interfaces with other classes such as `Record`, 
    `Location`, and `Pymon`. In order to improve gameplay dynamics, this class also offers methods for custom 
    additions (locations and monsters).
    
    Attributes:
    - bench (list): A class attribute that stores Pymons captured and benched during gameplay.
    - record (Record): An instance of the Record class to manage the game's locations, creatures, and items.
    - current_pymon (Pymon): The currently active Pymon controlled by the player.
    - stats (dict): Tracks various game statistics such as battles won/lost, items collected, and battle history.

    Methods:
    - setup(): Initializes the game environment by loading locations, creatures, and items from files, randomly 
      assigning creatures and items to locations, and setting the starting position for the player's Pymon.
    - verify_door_connections(): Verifies that all door connections between locations are established correctly and reports any unresolved connections.
    - generate_stats(): Displays current game statistics, including battles won/lost, items collected, and energy level.
    - record_battle(): Records battle details with a timestamp for tracking battle history.
    - display_battle_history(): Displays a detailed history of all battles fought by the player, including wins, draws, and losses.
    - handle_menu(): Provides a menu interface for player actions such as moving, picking items, challenging creatures, and managing stats.
    - inspect_pymon(): Allows the player to inspect the currently active Pymon or select a Pymon from the bench.
    - select_benched_pymon(): Lists all benched Pymons and enables the player to swap the current Pymon with one from the bench.
    - inspect_location(): Displays information about the current location, including creatures and items present.
    - start_game(): Initiates the game with introductory text and calls the main menu.
    - save_game_state(): Saves the game's current state to a file, recording locations, creatures, and items.
    - load_game_state(): Loads the game state from a file, reinitializing locations, creatures, and items.
    - add_custom_location(): Adds a new custom location to the game environment based on player input and saves it to the file.
    - add_custom_creature(): Adds a new custom creature to the game environment and saves it to the file.

   """

    bench = []
    
    def __init__(self, location_file="locations.csv", creature_file="creatures.csv", item_file="items.csv"):
        self.record = Record()
        self.current_pymon = Pymon("Kimimon")

    def setup(self):
        # Load data from files
        self.record.import_location(location_file)
        self.record.import_creatures(creature_file)
        self.record.import_items(item_file)
    
        # Randomly assign creatures to locations
        for creature in self.record.creatures:
            random.choice(self.record.locations).add_creature(creature)

        # Randomly assign items to locations
        for item in self.record.items:
            random.choice(self.record.locations).add_item(item)

        # Set a random starting location for Pymon
        self.current_pymon.spawn(random.choice(self.record.locations))

        # Debug output to confirm setup
        print("Initial setup complete:")
        print("Locations:", [location.name for location in self.record.locations])
    
        for location in self.record.locations:
            creatures = [creature.nickname for creature in location.creatures]
            items = [item.name for item in location.items]
            print(f"{location.name} creatures: {creatures}")
            print(f"{location.name} items: {items}")

        
       # Confirm connections 
        for location in self.record.locations:
            for direction, connected_location in location.doors.items():
                if isinstance(connected_location, Location):
                # If connected_location is an actual Location object
                    print(f"{location.name} has a door to the {direction} leading to {connected_location.get_name()}.")
                elif isinstance(connected_location, str):
                    print(f"Warning: Door from {location.name} to the {direction} leads to an unresolved location name: {connected_location}.")
                else:
                    print(f"{location.name} has no door to the {direction}.")

      # Verify door connections once after setup
        self.verify_door_connections()

    def verify_door_connections(self):
        print("\n--- Verifying Door Connections ---")
        for location in self.record.locations:
            for direction, target_location in location.doors.items():
                if isinstance(target_location, Location):
                    print(f"{location.name} has a door to the {direction} leading to {target_location.name}")
                else:
                    print(f"Warning: {location.name} has an unresolved door to the {direction}.")                

    stats = {
        "battles_won": 0,
        "battles_lost": 0,
        "items_collected": 0,
        "battle_history": []  
    }

    def generate_stats(self):
        # Display current game statistics
        print("\n--- Game Statistics ---")
        print(f"Battles Won: {Operation.stats['battles_won']}")
        print(f"Battles Lost: {Operation.stats['battles_lost']}")
        print(f"Items Collected: {Operation.stats['items_collected']}")
        print(f"Current Energy Level: {self.current_pymon.energy}")
    
        # Call the separate method to display battle history
        self.display_battle_history()
        print("-----------------------")

    def record_battle(self, opponent_name, win_count, draw_count, loss_count):
        """Records a completed battle's statistics with a timestamp."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%d/%m/%Y %I:%M%p")
        battle_record = {
            "timestamp": timestamp,
            "opponent": opponent_name,
            "win": win_count,
            "draw": draw_count,
            "loss": loss_count
        }
        Operation.stats["battle_history"].append(battle_record)

    def display_battle_history(self):
        """Displays detailed history of all battles, including totals for wins, draws, and losses."""
        print("\n--- Battle History ---")
        if Operation.stats["battle_history"]:
            total_wins = total_draws = total_losses = 0
            for i, battle in enumerate(Operation.stats["battle_history"], 1):
                print(f"Battle {i}, {battle['timestamp']} Opponent: {battle['opponent']}, "
                    f"W: {battle['win']} D: {battle['draw']} L: {battle['loss']}")
                total_wins += battle['win']
                total_draws += battle['draw']
                total_losses += battle['loss']
            print(f"Total: W: {total_wins} D: {total_draws} L: {total_losses}")
        else:
            print("No battles have been recorded yet.")
        print("-----------------------")
    

    def handle_menu(self):
        while True:
            print("\n--- Pymon Game Menu ---")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an item")
            print("5) View inventory (a. Select item to use)")
            print("6) Challenge a creature")
            print("7) Generate stats")
            print("8) Add Custom Location")  
            print("9) Add Custom Creature")   
            print("10) Exit the program")
            choice = input("Choose an option: ")

            if choice == "1":
                self.inspect_pymon()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                direction = input("Enter direction (west, north, east, south): ").lower()
                try:
                    self.current_pymon.move(direction)
                except InvalidDirectionException as e:
                    print(e)
            elif choice == "4":
                item_name = input("Enter the name of the item to pick up: ")
                self.current_pymon.pick_item(item_name)
            elif choice == "5":
                self.current_pymon.view_inventory()
            elif choice == "6":
                creature_name = input("Enter the name of the creature to challenge: ")
                result = self.current_pymon.challenge(creature_name)
                if result:
                    self.record_battle(result["opponent"], result["win"], result["draw"], result["loss"])
            elif choice == "7":
                self.generate_stats()  
            elif choice == "8":
                self.add_custom_location()  
            elif choice == "9":
                self.add_custom_creature()  
            elif choice == "10":
                print("Exiting the game. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def inspect_pymon(self):
        print("\n1) Inspect current Pymon")
        print("2) List and select a benched Pymon")
        choice = input("Choose an option: ")
        if choice == "1":
            # Display current Pymon's details
            self.current_pymon.inspect()
        elif choice == "2":
            self.select_benched_pymon()
        else:
            print("Invalid choice. Returning to main menu.")

    def select_benched_pymon(self):
        # List all Pymons in the bench and allow selection
        if not Operation.bench:
            print("No additional Pymon in the bench for now.")
            return

        print("\nBenched Pymons:")
        for idx, pymon in enumerate(Operation.bench):
            print(f"{idx + 1}) {pymon.nickname} - {pymon.description}")

        choice = input("Select a Pymon by number to make it your current Pymon: ")
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(Operation.bench):
                # Temporarily store the current location
                current_location = self.current_pymon.current_location

                # Swap the current Pymon with the selected benched Pymon
                self.current_pymon, Operation.bench[choice] = Operation.bench[choice], self.current_pymon
            
                # Assign the current location to the new active Pymon
                self.current_pymon.current_location = current_location

                print(f"{self.current_pymon.nickname} is now your active Pymon.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

            
    def inspect_location(self):
        # Display details of the current location
        location = self.current_pymon.get_location()
        if location:
            print(f"\nYou are at {location.get_name()}, {location.get_description()}")
            print("Creatures here:")
            for creature in location.creatures:
                if creature != self.current_pymon:
                    print(f" - {creature.nickname}: {creature.description}")
            print("Items here:")
            for item in location.items:
                print(f" - {item}")
        else:
            print("Pymon is not in any location.")

    def start_game(self):
        print("Welcome to Pymon World!")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.")
        print(f"You started at {self.current_pymon.get_location().get_name()}")
        self.handle_menu()

    def save_game_state(self, filename="save2024.csv"):
        try:
            with open(filename, mode="w", newline="") as file:
                file.write("Location Name,Description\n")
                for location in self.record.locations:
                    file.write(f"{location.name},{location.description}\n")
                
                file.write("\n")  # Blank line between sections

                # Save creatures and their locations
                file.write("Creature Name,Description,Location\n")
                for creature in self.record.creatures:
                    location = creature.get_location().get_name() if creature.get_location() else "Unknown"
                    file.write(f"{creature.nickname},{creature.description},{location}\n")

                file.write("\n")  # Blank line between sections

                # Save items
                file.write("Item Name,Description\n")
                for item in self.record.items:
                    file.write(f"{item.name},{item.description}\n")

            print(f"Game state saved to {filename}")
        except IOError as e:
            print(f"An error occurred while saving the game state: {e}")

    def load_game_state(self, filename="save2024.csv"):
        try:
            with open(filename, mode="r") as file:
                section = None
                for line in file:
                    # Skip blank lines
                    line = line.strip()
                    if not line:
                        continue

                    # Detect section headers based on specific keywords
                    if line.startswith("Location Name"):
                        section = "location"
                        continue
                    elif line.startswith("Creature Name"):
                        section = "creature"
                        continue
                    elif line.startswith("Item Name"):
                        section = "item"
                        continue

                    # Process each section differently based on the header
                    data = line.split(",")  # Manually split by commas
                    if section == "location" and len(data) >= 2:
                        name, description = data[0], data[1]
                        location = Location(name=name, description=description)
                        self.record.locations.append(location)
                    elif section == "creature" and len(data) >= 3:
                        nickname, description, location_name = data[0], data[1], data[2]
                        creature = Creature(nickname, description)
                        location = self.record.find_location_by_name(location_name.strip())
                        if location:
                            location.add_creature(creature)
                        self.record.creatures.append(creature)
                    elif section == "item" and len(data) >= 2:
                        name, description = data[0], data[1]
                        item = Item(name=name, description=description)
                        self.record.items.append(item)

            print(f"Game state loaded from {filename}")
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
        except IOError as e:
            print(f"An error occurred while loading the game state: {e}")

    def add_custom_location(self):
        name = input("Enter location name: ")
        description = input("Enter description: ")
        doors = {
            "west": input("Enter west connection or 'None': "),
            "north": input("Enter north connection or 'None': "),
            "east": input("Enter east connection or 'None': "),
            "south": input("Enter south connection or 'None': ")
        }
        new_location = Location(name=name, description=description)
    
        # Set doors to other locations if they exist
        for direction, location_name in doors.items():
            if location_name != "None":
                existing_location = self.record.find_location_by_name(location_name)
                if existing_location:
                    if direction == "west":
                        new_location.connect_west(existing_location)
                    elif direction == "north":
                        new_location.connect_north(existing_location)
                    elif direction == "east":
                        new_location.connect_east(existing_location)
                    elif direction == "south":
                        new_location.connect_south(existing_location)
                else:
                    print(f"Location '{location_name}' not found. No connection made to the {direction}.")
    
        # Add new location to records and save to file
        self.record.locations.append(new_location)
        with open("locations.csv", "a") as file:
            file.write(f"{name},{description},{doors['west']},{doors['north']},{doors['east']},{doors['south']}\n")
        print(f"New location '{name}' added and saved.")


    def add_custom_creature(self):
        nickname = input("Enter creature name: ")
        description = input("Enter description: ")
        adoptable = input("Adoptable (yes/no): ").lower() == "yes"
        new_creature = Pymon(nickname) if adoptable else Creature(nickname, description)
        self.record.creatures.append(new_creature)
        with open("creatures.csv", "a") as file:
            file.write(f"{nickname},{description},{adoptable}\n")
    
if __name__ == '__main__':
    game = Operation(location_file, creature_file, item_file)
    game.setup()
    game.start_game()


