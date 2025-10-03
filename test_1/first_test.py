def calculator():
	print("Simple Calculator")
	print("Select operation:")
	print("1. Add")
	print("2. Subtract")
	print("3. Multiply")
	print("4. Divide")

	while True:
		choice = input("Enter choice (1/2/3/4): ")
		if choice in ('1', '2', '3', '4'):
			try:
				num1 = float(input("Enter first number: "))
				num2 = float(input("Enter second number: "))
			except ValueError:
				print("Invalid input. Please enter numbers.")
				continue

			def format_result(x, y, op, result):
				# Show as int if all are integers
				if x.is_integer() and y.is_integer() and float(result).is_integer():
					x = int(x)
					y = int(y)
					result = int(result)
				else:
					# For floats, format to 10 significant digits, strip trailing zeros
					def fmt(val):
						if isinstance(val, float) and not val.is_integer():
							return ('{0:.10g}'.format(val)).rstrip('0').rstrip('.') if '.' in '{0:.10g}'.format(val) else '{0:.10g}'.format(val)
						return int(val) if isinstance(val, float) and val.is_integer() else val
					x = fmt(x)
					y = fmt(y)
					result = fmt(result)
				return f"{x} {op} {y} = {result}"

			if choice == '1':
				res = num1 + num2
				print(format_result(num1, num2, '+', res))
			elif choice == '2':
				res = num1 - num2
				print(format_result(num1, num2, '-', res))
			elif choice == '3':
				res = num1 * num2
				print(format_result(num1, num2, '*', res))
			elif choice == '4':
				if num2 == 0:
					print("Error: Division by zero.")
				else:
					res = num1 / num2
					print(format_result(num1, num2, '/', res))
		else:
			print("Invalid choice. Please select 1, 2, 3, or 4.")
			continue

		next_calc = input("Do you want to perform another calculation? (yes/no): ")
		if next_calc.lower() not in ('yes', 'y'):
			print("Goodbye!")
			break

if __name__ == "__main__":
	calculator()