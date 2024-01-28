import redis
import time
import os
from rich.console import Console
from rich.table import Table
from signal import signal, SIGINT
from sys import exit

# Initialize Redis (replace with your Redis configuration)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize product prices in Redis
absurd_product_names = {
    "Unicorn Tears": 1,
    "Invisible Toaster": 2,
    "Glow-in-the-Dark Socks": 3,
    "Banana Umbrella": 4,
    "Toothpaste Flavored Ice Cream": 5,
    "Flying Carpet": 6,
    "Bubble Wrap Suit": 7,
    "Singing Fish Slippers": 8,
    "Pizza-Flavored Toothpaste": 9,
    "Rainbow-Colored Bacon": 10,
}

for product, price in absurd_product_names.items():
    redis_key = f"{product}_price"
    redis_client.set(redis_key, float(price))

# Setup rich console
console = Console()

def handler(signal_received, frame):
    # Handle any cleanup here
    console.log("SIGINT or CTRL-C detected. Exiting gracefully")
    exit(0)

def display_prices():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Product", style="dim", width=28)
    table.add_column("Price", justify="right")

    for product in absurd_product_names.keys():
        redis_key = f"{product}_price"
        price = redis_client.get(redis_key).decode("utf-8")
        table.add_row(product, price)

    console.print(table)

# Handle SIGINT
signal(SIGINT, handler)

# Main loop
try:
    while True:
        display_prices()
        time.sleep(2)
except KeyboardInterrupt:
    # Handle any cleanup here
    console.log("Exiting gracefully")
