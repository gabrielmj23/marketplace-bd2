from dataclasses import dataclass

@dataclass
class Product:
    """Class for representing a single product"""
    title: str
    price: str
    rating: str
    seller_reputation: str
    brand: str
    cpu: str
    disk: str
    ram: str
    post_url: str
    img_url: str
    
    FIELD_NAMES = [ "title", "price", "rating", "seller_reputation", "brand", "cpu", "disk", "ram", "post_url", "img_url" ]

    def to_dict(self):
        """Returns dictionary representation of a product"""

        return {
            "title": self.title,
            "price": self.price,
            "rating": self.rating,
            "seller_reputation": self.seller_reputation,
            "brand": self.brand,
            "cpu": self.cpu,
            "disk": self.disk,
            "ram": self.ram,
            "post_url": self.post_url,
            "img_url": self.img_url,
        }
