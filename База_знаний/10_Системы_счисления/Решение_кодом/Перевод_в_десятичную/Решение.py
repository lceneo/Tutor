# Переводим двоичное число в десятичное разряд за разрядом.
binary_number_text = "1100110"
decimal_value = 0
for binary_digit in binary_number_text:
    decimal_value = decimal_value * 2 + int(binary_digit)
print(decimal_value)
