from animals import Animal, Dog

def print_animal_info(animal: Animal) -> None:
    print(animal.describe())
    print("Speaks:", animal.speak())
    print("-" * 30)
    


def main() -> None:
    a = Animal("Unknown")
    d = Dog("Bello", "Labrador")

    print_animal_info(a)
    print_animal_info(d)


if __name__ == "__main__":
    main()