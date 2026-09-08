menu = '''Welcome to Coffee Shop 146!

Menu:
Drink: Latte
Price: ₱ 180

Drink: Cappuccino
Price: ₱ 150

Drink: Americano
Price: ₱ 120

Add whipped cream to your drink for ₱80 only!
'''

# Parent
class Customer:

    def __init__(self, name, payment):
        self.__name = name
        self.__payment = payment

    @property
    def name(self):
        return self.__name

    @property
    def payment(self):
        return self.__payment

# ADDED (QA): get_membership() added to parent so SeniorCitizen can override it
# with a proper display name. All other subclasses inherit this default behavior
# which returns the class name automatically.
    def get_membership(self): # Returns class name by default; overridden in SeniorCitizen for proper display
        return self.__class__.__name__

    def get_discount(self):
        return 0

    def get_final_total(self, coffee): # Added coffee parameter based on call
        subtotal = coffee.get_total()
        discount = subtotal * self.get_discount() # Polymorphism: child classes have their own method and produce different results
        total = subtotal - discount

        if self.payment.strip().lower() == "card":
            total *= 1.03 # multiply total amount to 1.03; 100% of the drink price and a 3% card fee

        return total

    def order(self, coffee): # f-strings are used to embed variables from both classes

# CHANGED (QA): was self.__class__.__name__ — changed to self.get_membership()
# so SeniorCitizen displays as "Senior Citizen" with a space instead of "SeniorCitizen"
        membership = self.get_membership() # Uses get_membership() so SeniorCitizen displays correctly

        print(f"\nCustomer: {self.name}")
        print(f"Membership: {membership}")

        coffee.display_drink()
        
        subtotal = coffee.get_total()
        discount = subtotal * self.get_discount()
        after_discount = subtotal - discount

        print(f"\nSubtotal: ₱{subtotal:.2f}") # displays the number with 2 decimal places
        print(f"{membership} Discount: {self.get_discount()* 100:.0f}%") # multiplies decimal percentage discount by 100; .0f means to show zero decimal places
        print(f"Discount Amount: - ₱{discount:.2f}")
        print(f"After discount: ₱{after_discount:.2f} ")
        print(f"\nPayment: {self.payment}")

        if self.payment.strip().lower() == "card":
            card_fee = after_discount * 0.03
            print(f"Card Fee: + ₱{card_fee:.2f}")
        else:
            print("Service fee: N/A")

        print(f"\nTotal: ₱{self.get_final_total(coffee):.2f}") # Abstraction: hides how total price was computed
        print()

print(menu) # calls the menu string

# Child
# Inheritance
class Regular(Customer):
    def get_discount(self):
        return 0

class Gold(Customer):
    def get_discount(self):
        return 0.05

class PWD(Customer):
    def get_discount(self):
        return 0.20

class SeniorCitizen(Customer):
# ADDED (QA): get_membership() overridden here to return "Senior Citizen" with a space
# because self.__class__.__name__ returns "SeniorCitizen" without a space
    def get_membership(self): # Overrides parent to return proper display name with space
        return "Senior Citizen"

    def get_discount(self):
        return 0.20


class Coffee:
    
    def __init__(self, drink, price, add_on=False):

        self.__drink = drink
        self.__price = price
        self.__add_on = add_on
        self.__add_on_price = 0

        self.add_add_on()

    @property
    def drink(self):
        return self.__drink

    @property
    def price(self):
        return self.__price

    @property
    def add_on(self):
        return self.__add_on

    def add_add_on(self): # precaution since False does not have .strip()
        if self.add_on and self.add_on.strip().lower() == "whipped cream":
            self.__add_on_price = 80

    def get_price(self):
        return self.price

    def get_add_on_price(self):
        return self.__add_on_price

    def get_total(self):
        return self.price + self.__add_on_price

    def display_drink(self):
        print(f"\nDrink: {self.drink}")
        print(f"Drink Price: ₱{self.get_price():.2f}")

        if self.add_on and self.add_on.strip().lower() == "whipped cream":
            print(f"Add-on: {self.add_on}")
            print(f"Add-on Price: ₱{self.get_add_on_price():.2f}")
        else:
            print("Add-on: None")
        

name = input("Enter your name: ")

print("\nMembership:")
print("1. Regular")
print("2. Gold")
print("3. Person with Disability (PWD)")
print("4. Senior Citizen")

membership = input("Choose your membership type (1-4): ")

# ADDED (QA): Early validation — stops program immediately if invalid choice is entered
# instead of waiting until after all inputs are collected
if membership not in ["1", "2", "3", "4"]:
    print("Invalid membership choice.")
    exit()

print("\nDrinks:")
print("1. Latte")
print("2. Cappuccino")
print("3. Americano")

drink_choice = input("Choose your drink (1-3): ")

# ADDED (QA): Early validation — stops program immediately if invalid drink is entered
if drink_choice not in ["1", "2", "3"]:
    print("Invalid drink choice.")
    exit()

print("\nAdd-on:")
print("1. Whipped Cream - ₱80")
print("2. None")

add_on_choice = input("Choose your add-on (1-2): ")

# ADDED (QA): Early validation — stops program immediately if invalid add-on is entered
if add_on_choice not in ["1", "2"]:
    print("Invalid add-on choice.")
    exit()

payment = input("\nPayment methods accepted (Cash/Card/GCash/Maya): ")

if payment.strip().lower() not in ["cash", "card", "gcash", "maya"]:
    print("Invalid payment method.")
    exit()


if drink_choice == "1":
    drink = "Latte"
    price = 180
elif drink_choice == "2":
    drink = "Cappuccino"
    price = 150
elif drink_choice == "3":
    drink = "Americano"
    price = 120
else:
    print("Invalid drink choice.")
    exit()

if add_on_choice == "1":
    add_on = "Whipped Cream"
elif add_on_choice == "2":
    add_on = "None"
else:
    print("Invalid add-on choice.")
    exit()

coffee = Coffee(drink, price, add_on)

if membership == "1":
    customer = Regular(name, payment)
elif membership == "2":
    customer = Gold(name, payment)
elif membership == "3":
    customer = PWD(name, payment)
elif membership == "4":
    customer = SeniorCitizen(name, payment)
else:
    print("Invalid membership choice.")
    exit()

print("\nReceipt:")
customer.order(coffee)
