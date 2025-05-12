from abc import ABC, abstractmethod
import json
from datetime import datetime

class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def to_dict(self):
        pass

    def __str__(self):
        return f"{self.name} (ID: {self.product_id}) - ${self.price} x {self.quantity}"


class Electronics(Product):
    def __init__(self, product_id, name, price, quantity, brand, warranty_years):
        super().__init__(product_id, name, price, quantity)
        self.brand = brand
        self.warranty_years = warranty_years

    def to_dict(self):
        return {
            "type": "Electronics",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "brand": self.brand,
            "warranty_years": self.warranty_years
        }


class Grocery(Product):
    def __init__(self, product_id, name, price, quantity, expiry_date):
        super().__init__(product_id, name, price, quantity)
        self.expiry_date = expiry_date

    def to_dict(self):
        return {
            "type": "Grocery",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date
        }


class Clothing(Product):
    def __init__(self, product_id, name, price, quantity, size, material):
        super().__init__(product_id, name, price, quantity)
        self.size = size
        self.material = material

    def to_dict(self):
        return {
            "type": "Clothing",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "size": self.size,
            "material": self.material
        }


# Custom Exceptions
class DuplicateProductIDError(Exception):
    pass

class InsufficientStockError(Exception):
    pass


# Inventory Class
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            raise DuplicateProductIDError("Product ID already exists.")
        self.products[product.product_id] = product

    def update_quantity(self, product_id, quantity):
        if product_id not in self.products:
            raise KeyError("Product not found.")
        if quantity < 0 and abs(quantity) > self.products[product_id].quantity:
            raise InsufficientStockError("Insufficient stock to remove.")
        self.products[product_id].quantity += quantity

    def search_product(self, keyword):
        return [
            product for product in self.products.values()
            if keyword.lower() in product.name.lower()
        ]

    def list_all_products(self):
        return list(self.products.values())

    def remove_expired_products(self):
        to_remove = []
        today = datetime.now().date()
        for pid, product in self.products.items():
            if isinstance(product, Grocery):
                expiry_date = datetime.strptime(product.expiry_date, "%Y-%m-%d").date()
                if expiry_date < today:
                    to_remove.append(pid)
        for pid in to_remove:
            del self.products[pid]

    def total_inventory_value(self):
        return sum(p.price * p.quantity for p in self.products.values())

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump({pid: p.to_dict() for pid, p in self.products.items()}, f, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data.values():
                ptype = item.get("type")
                if ptype == "Electronics":
                    product = Electronics(**item)
                elif ptype == "Grocery":
                    product = Grocery(**item)
                elif ptype == "Clothing":
                    product = Clothing(**item)
                else:
                    continue
                self.products[product.product_id] = product
