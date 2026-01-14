# Type Hints. Just for the user not the interpreter

def add(a: int, b: int) -> int:         # gets two integers and returns their sum as an integer
    return a + b

def add2(a: float, b: int) -> int:     
    return a + b                        # returns a sum as an float!
#
def myFunc(x:int = 5) -> str:         
    return str(x)


print(add(2, 3))                      # Correct usage: both arguments are integers
print(add2(2.5, 3))                   # Correct usage: first argument is
print(myFunc())                       # if no argument is passed, default value 5 is used
print(myFunc(45))
