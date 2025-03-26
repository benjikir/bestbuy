import store
import products


def start(store_obj):
    """Starts the Best Buy store user interface."""
    while True:
        print("\nWelcome to Best Buy Store!\n")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nAvailable Products:")
            for idx, product in enumerate(store_obj.get_all_products(), start=1):
                print(f"{idx}. {product.name} - ${product.price} - {product.quantity} in stock")

        elif choice == "2":
            print(f"Total quantity in store: {store_obj.get_total_quantity()}")

        elif choice == "3":
            shopping_list = []
            all_products = store_obj.get_all_products()

            while True:
                print("\nAvailable Products:")
                for idx, product in enumerate(all_products, start=1):
                    print(f"{idx}. {product.name} - ${product.price} - {product.quantity} in stock")

                product_choice = input("Enter product number or name (or 'done' to finish): ")
                if product_choice.lower() == "done":
                    break

                product = None

                if product_choice.isdigit():
                    product_index = int(product_choice) - 1
                    if 0 <= product_index < len(all_products):
                        product = all_products[product_index]
                else:
                    product = next((p for p in all_products if p.name.lower() == product_choice.lower()), None)

                if not product:
                    print("Invalid product selection. Please try again.")
                    continue

                try:
                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("Quantity must be greater than zero.")
                        continue
                    if product.quantity < quantity:
                        print(f"Not enough stock available. Only {product.quantity} left.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

                shopping_list.append((product, quantity))

            if shopping_list:
                total_price = store_obj.order(shopping_list)
                print(f"Total price of your order: ${total_price}")
            else:
                print("No valid items in your order.")

        elif choice == "4":
            print("Thank you for shopping with us!")
            break

        else:
            print("Invalid choice. Please try again.")


# Setup initial stock of inventory
product_inventory = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
    products.Product("Air Pods Pro2", price=199, quantity=50)
]

best_buy = store.Store(product_inventory)
start(best_buy)


# store.py
from typing import List, Tuple
import products


class Store:
    def __init__(self, product_list: List[products.Product]):
        if not isinstance(product_list, list):
            raise TypeError("product_list must be a list.")
        for product in product_list:
            if not isinstance(product, products.Product):
                raise TypeError("All elements in product_list must be Product objects.")
        self.product_list = product_list

    def add_product(self, product: products.Product):
        if not isinstance(product, products.Product):
            raise TypeError("product must be a Product object.")
        self.product_list.append(product)

    def remove_product(self, product: products.Product):
        if not isinstance(product, products.Product):
            raise TypeError("product must be a Product object.")
        if product not in self.product_list:
            raise ValueError("Product not found in the store.")
        self.product_list.remove(product)

    def get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.product_list)

    def get_all_products(self) -> List[products.Product]:
        return [product for product in self.product_list if product.quantity > 0]

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        total_price = 0.0
        for product, quantity in shopping_list:
            if product in self.product_list and product.quantity >= quantity:
                product.quantity -= quantity
                total_price += product.price * quantity
        return total_price

