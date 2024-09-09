import os
from dotenv import load_dotenv

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    },
    "americano": {
        "ingredients": {
            "water": 300,
            "coffee": 18,
        },
        "cost": 2.0,
    },
    "mocha": {
        "ingredients": {
            "water": 100,
            "milk": 150,
            "coffee": 24,
            "chocolate": 20,
        },
        "cost": 3.5,
    }
}

ADD_ONS = {
    "whipped cream": 0.5,
    "caramel": 0.3,
    "extra shot": 0.7,
    "vanilla syrup": 0.4,
}

resources = {
    "water": 1000,
    "milk": 1000,
    "coffee": 500,
    "chocolate": 50,
    "whipped cream": 50,
    "caramel": 40,
    "extra shot": 50,
    "vanilla syrup": 30,
}

profit = 0
password = os.getenv("PASSWORD")