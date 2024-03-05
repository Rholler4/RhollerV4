def percentage_of_hex(percentage):
    hex_value = int('FFFF', 16)  # Convert 'FFFF' to integer using base 16 (hexadecimal)
    percentage_value = hex_value * (percentage / 100)
    return hex(round(percentage_value))

if __name__ == "__main__":
    try:
        percentage_input = float(input("Enter the requested percentage value: "))
        if 0 <= percentage_input <= 100:
            result_hex = percentage_of_hex(percentage_input)
            print(f"{percentage_input}% of FFFF in hex is: {result_hex}")
        else:
            print("Please enter a percentage value between 0 and 100.")
    except ValueError:
        print("Invalid input. Please enter a valid percentage value.")
