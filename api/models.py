class UserModel:
    """Representing a User object."""
    def __init__(self, email: str, first_name: str, last_name: str) -> None:
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
    
    def __str__(self) -> str:
        return f"User<{self.email}>"


class Product:
    pass