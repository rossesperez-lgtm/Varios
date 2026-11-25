# Solicitar al usuario una operación (suma, resta, multiplicación, división) y dos números
# Ejecutar la operación y mostrar el resultado
# Debe repetirse hassta que el usuario decida salir indicando "salir"

while True:
    operacion = input(
        "Ingrese operación (suma, resta, multiplicación, división) o 'salir' para terminar: "
    ).lower()

    if operacion == "salir":
        print("Saliendo de la calculadora. ¡Hasta luego!")
        break

    if operacion not in ["suma", "resta", "multiplicación", "división"]:
        print("Operación no válida. Intente nuevamente.")
        continue

    try:
        valor1 = float(input("Ingrese el primer número: "))
        valor2 = float(input("Ingrese el segundo número: "))
    except ValueError:
        print("Entrada no válida. Por favor, ingrese números válidos.")
        continue

    operacion_resultado = 0
    if operacion == "suma":
        operacion_resultado = valor1 + valor2
    elif operacion == "resta":
        operacion_resultado = valor1 - valor2
    elif operacion == "multiplicación":
        operacion_resultado = valor1 * valor2
    elif operacion == "división":
        if valor2 != 0:
            operacion_resultado = valor1 / valor2
        else:
            print("Error: No se puede dividir entre cero.")
            continue

    print(f"El resultado de la {operacion} es: {operacion_resultado}")
