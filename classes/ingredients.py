class Ingredient:
    def __init__(self, name, effect, type ,taste, description , environment, rare):
        self.name = name
        self.effect = effect
        self.taste = taste
        self.description = description
        self.type = type
        self.environment = environment
        self.rare = rare

    def __str__(self):
        return f"{self.name}\n{self.rare}\n{self.type}\n{self.effect}\n{self.environment}\n{self.taste}\n{self.description}"

    def to_dict(self):
        # Convert the Ingredient instance to a dictionary
        return {
            "name": self.name,
            "rare" : self.rare,
            "effect": self.effect,
            "type": self.type,
            "taste": self.taste,
            "description": self.description,
            "environment": self.environment
        }