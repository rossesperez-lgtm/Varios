# Recorrer números del 1 al 100
# Número multiplo de 3 imprimir "Fizz"
# Número multiplo de 5 imprimir "Buzz"
# Número multiplo de 3 y 5 imprimir "FizzBuzz"

for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print(f"{i} FizzBuzz")
    elif i % 3 == 0:
        print(f"{i} Fizz")
    elif i % 5 == 0:
        print(f"{i} Buzz")
    else:
        print(f"{i}")


# While loop version
i = 1
while i <= 100:
    if i % 3 == 0 and i % 5 == 0:
        print(f"{i} FizzBuzz")
    elif i % 3 == 0:
        print(f"{i} Fizz")
    elif i % 5 == 0:
        print(f"{i} Buzz")
    else:
        print(f"{i}")
    i += 1


## Function version
def fizzbuzz(n):
    """Imprime los números del 1 a n aplicando las reglas de FizzBuzz."""
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print(f"{i} FizzBuzz")
        elif i % 3 == 0:
            print(f"{i} Fizz")
        elif i % 5 == 0:
            print(f"{i} Buzz")
        else:
            print(f"{i}")


fizzbuzz(100)
