import tkinter as tk
from tkinter import simpledialog, messagebox
from menu import MENU, ADD_ONS, resources, password
from management import is_resource_sufficient, is_transaction_successful, make_coffee, generate_report

class CoffeeMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Machine")
        self.selected_drink = tk.StringVar(value="espresso")
        self.selected_add_ons = {}
        self.custom_ingredients = {}
        self.total_cost = tk.DoubleVar(value=0.0)
        self.money_inserted = tk.DoubleVar(value=0.0)
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        tk.Label(self.main_frame, text="Select your drink:", font=("Arial", 14)).pack(pady=10)

        for drink in MENU.keys():
            tk.Radiobutton(self.main_frame, text=drink.capitalize(), variable=self.selected_drink, value=drink, command=self.update_selection).pack(anchor=tk.W)

        self.customize_var = tk.BooleanVar()
        self.customize_check = tk.Checkbutton(self.main_frame, text="Customize Ingredients", variable=self.customize_var, command=self.toggle_customize)
        self.customize_check.pack(pady=10)

        self.custom_ingredients_frame = tk.Frame(self.main_frame)
        self.custom_ingredients_frame.pack(pady=5)

        self.add_ons_frame = tk.LabelFrame(self.main_frame, text="Add-Ons")
        self.add_ons_frame.pack(pady=10)

        for add_on in ADD_ONS.keys():
            self.selected_add_ons[add_on] = tk.IntVar()
            tk.Checkbutton(self.add_ons_frame, text=f"{add_on.capitalize()} (${ADD_ONS[add_on]})", variable=self.selected_add_ons[add_on], command=self.update_total_cost).pack(anchor=tk.W)

        tk.Label(self.main_frame, text="Total Cost:").pack(pady=5)
        self.total_cost_label = tk.Label(self.main_frame, textvariable=self.total_cost, font=("Arial", 12))
        self.total_cost_label.pack(pady=5)

        self.money_frame = tk.Frame(self.main_frame)
        self.money_frame.pack(pady=10)

        tk.Label(self.money_frame, text="Enter Coins:").pack(pady=5)
        self.money_entries = {}
        for coin, value in [("Quarters ($0.25)", 0.25), ("Dimes ($0.10)", 0.10), ("Nickels ($0.05)", 0.05), ("Pennies ($0.01)", 0.01)]:
            frame = tk.Frame(self.money_frame)
            frame.pack(anchor=tk.W)
            tk.Label(frame, text=coin).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=5)
            entry.pack(side=tk.LEFT)
            self.money_entries[entry] = value
            entry.bind("<KeyRelease>", self.update_money_inserted)

        tk.Label(self.main_frame, text="Total Money Inserted:").pack(pady=5)
        self.money_inserted_label = tk.Label(self.main_frame, textvariable=self.money_inserted, font=("Arial", 12))
        self.money_inserted_label.pack(pady=5)

        self.order_button = tk.Button(self.main_frame, text="Order", command=self.order)
        self.order_button.pack(pady=10)

        self.report_button = tk.Button(self.main_frame, text="Report", command=self.report)
        self.report_button.pack(pady=10)

        self.update_selection()

    def toggle_customize(self):
        if self.customize_var.get():
            self.update_custom_ingredients()
        else:
            for widget in self.custom_ingredients_frame.winfo_children():
                widget.destroy()

    def update_selection(self):
        self.update_custom_ingredients()
        self.update_total_cost()

    def update_custom_ingredients(self):
        for widget in self.custom_ingredients_frame.winfo_children():
            widget.destroy()
        
        if self.customize_var.get():
            drink = MENU[self.selected_drink.get()]["ingredients"]
            for ingredient, amount in drink.items():
                self.custom_ingredients[ingredient] = tk.IntVar(value=amount)
                frame = tk.Frame(self.custom_ingredients_frame)
                frame.pack(anchor=tk.W)
                tk.Label(frame, text=f"{ingredient.capitalize()}:").pack(side=tk.LEFT)
                tk.Entry(frame, textvariable=self.custom_ingredients[ingredient], width=5).pack(side=tk.LEFT)

    def update_total_cost(self):
        drink_cost = MENU[self.selected_drink.get()]["cost"]
        add_ons_cost = sum(ADD_ONS[add_on] * self.selected_add_ons[add_on].get() for add_on in ADD_ONS)
        total = drink_cost + add_ons_cost
        self.total_cost.set(total)

    def update_money_inserted(self, event):
        total = 0
        for entry, value in self.money_entries.items():
            try:
                total += int(entry.get()) * value
            except ValueError:
                pass
        self.money_inserted.set(total)

    def order(self):
        drink = self.selected_drink.get()
        drink_ingredients = MENU[drink]["ingredients"].copy()
        
        if self.customize_var.get():
            for k, v in self.custom_ingredients.items():
                drink_ingredients[k] = v.get()

        if is_resource_sufficient(drink_ingredients):
            add_ons_cost = sum(ADD_ONS[add_on] * self.selected_add_ons[add_on].get() for add_on in ADD_ONS)
            total_cost = MENU[drink]["cost"] + add_ons_cost
            money_received = self.money_inserted.get()
            if is_transaction_successful(money_received, total_cost):
                make_coffee(drink, drink_ingredients)
                self.clear_selection()
        else:
            messagebox.showinfo("Insufficient Resources", "Sorry, there are insufficient resources to make your drink.")

    def report(self):
        password_in = simpledialog.askstring("Password", "Please enter the password to view the report: ")
        if password_in == password:
            report = generate_report()
            messagebox.showinfo("Report", report)
        else:
            messagebox.showinfo("Unauthorized", "Only Authorized Users can access the report")

    def clear_selection(self):
        self.selected_drink.set("espresso")
        for add_on in self.selected_add_ons:
            self.selected_add_ons[add_on].set(0)
        self.customize_var.set(0)
        self.money_inserted.set(0.0)
        for entry in self.money_entries:
            entry.delete(0, tk.END)
        for widget in self.custom_ingredients_frame.winfo_children():
            widget.destroy()
        self.update_selection()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeMachine(root)
    root.mainloop()
