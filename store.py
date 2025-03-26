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

