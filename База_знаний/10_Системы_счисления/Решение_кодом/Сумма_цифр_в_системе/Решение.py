# Считаем суммы цифр в восьмеричных записях и выбираем наименьшую.
decimal_numbers = [55, 83, 91]
octal_base = 8
smallest_octal_digit_sum = None
for decimal_number in decimal_numbers:
    remaining_value = decimal_number
    octal_digit_sum = 0
    while remaining_value > 0:
        octal_digit = remaining_value % octal_base
        octal_digit_sum = octal_digit_sum + octal_digit
        remaining_value = remaining_value // octal_base
    print(decimal_number, "сумма цифр:", octal_digit_sum)
    if smallest_octal_digit_sum is None or octal_digit_sum < smallest_octal_digit_sum:
        smallest_octal_digit_sum = octal_digit_sum
print("Наименьшая сумма:", smallest_octal_digit_sum)
