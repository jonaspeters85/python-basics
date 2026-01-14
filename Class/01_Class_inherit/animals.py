class Animal:
    def __init__(self, name: str):
        self.name = name
        
    def speak(self) -> str:
        return "Some sound"
    
    def describe(self) -> str:
        return f"This is an animal named {self.name}."
    
class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed
        
    def speak(self) -> str:
        return "Woof!"
    
    def describe(self) -> str:
        return f"This is a {self.breed} dog named {self.name}."