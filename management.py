from tkinter import messagebox
from menu import MENU, ADD_ONS, resources, profit

def is_resource_sufficient(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] > resources.get(item, 0):
            messagebox.showinfo("Resource Error", f"Sorry there is not enough {item}.")
            return False
    return True

def is_transaction_successful(money_received, drink_cost):
    global revenue
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        messagebox.showinfo("Transaction Successful", f"Here is ${change} in change.")
        revenue += drink_cost
        return True
    else:
        messagebox.showinfo("Transaction Failed", "Sorry that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    messagebox.showinfo("Enjoy", f"Here is your {drink_name} ☕️. Enjoy!")

def clear_resources():
    # This function can handle clearing or replenishing resources
    pass

def generate_report():
    return (
        f"Water: {resources['water']}ml\n"
        f"Milk: {resources['milk']}ml\n"
        f"Coffee: {resources['coffee']}g\n"
        f"Chocolate: {resources['chocolate']}g\n"
        f"Whipped Cream: {resources['whipped cream']}g\n"
        f"Caramel: {resources['caramel']}g\n"
        f"Extra Shot: {resources['extra shot']}g\n"
        f"Vanilla Syrup: {resources['vanilla syrup']}ml\n"
        f"Money: ${revenue}"
    )
