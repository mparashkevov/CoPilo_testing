import math

def calculator():
    print("Advanced Calculator")
    print("Select operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Power (^)")
    print("6. Modulus (%)")
    print("7. Square Root (sqrt)")
    print("8. Evaluate Expression (e.g., 2*(3+4))")
    print("9. Show History")
    print("0. Exit")

    history = []
    last_result = None

    def format_result(expr, result):
        return f"{expr} = {result}"

    while True:
        choice = input("\nEnter choice (0-9): ")
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '9':
            print("\n--- Calculation History ---")
            if not history:
                print("No history yet.")
            else:
                for h in history:
                    print(h)
            continue
        elif choice == '8':
            expr = input("Enter expression: ")
            try:
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                allowed_names['abs'] = abs
                result = eval(expr, {"__builtins__": None}, allowed_names)
                print(format_result(expr, result))
                history.append(format_result(expr, result))
                last_result = result
            except Exception as e:
                print(f"Error evaluating expression: {e}")
            continue

        if choice in ('1', '2', '3', '4', '5', '6'):
            try:
                num1 = input("Enter first number (or 'ans' for last result): ")
                num1 = last_result if num1.lower() == 'ans' and last_result is not None else float(num1)
                num2 = input("Enter second number (or 'ans' for last result): ")
                num2 = last_result if num2.lower() == 'ans' and last_result is not None else float(num2)
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue

            if choice == '1':
                res = num1 + num2
                expr = f"{num1} + {num2}"
            elif choice == '2':
                res = num1 - num2
                expr = f"{num1} - {num2}"
            elif choice == '3':
                res = num1 * num2
                expr = f"{num1} * {num2}"
            elif choice == '4':
                if num2 == 0:
                    print("Error: Division by zero.")
                    continue
                res = num1 / num2
                expr = f"{num1} / {num2}"
            elif choice == '5':
                res = num1 ** num2
                expr = f"{num1} ^ {num2}"
            elif choice == '6':
                res = num1 % num2
                expr = f"{num1} % {num2}"

            print(format_result(expr, res))
            history.append(format_result(expr, res))
            last_result = res

        elif choice == '7':
            try:
                num = input("Enter number for square root (or 'ans' for last result): ")
                num = last_result if num.lower() == 'ans' and last_result is not None else float(num)
                if num < 0:
                    print("Error: Cannot take square root of negative number.")
                    continue
                res = math.sqrt(num)
                expr = f"sqrt({num})"
                print(format_result(expr, res))
                history.append(format_result(expr, res))
                last_result = res
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    calculator()