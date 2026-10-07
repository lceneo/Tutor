# Переводим 100 в двоичную систему и считаем остатки, равные единице.
decimal_value = 100
binary_one_count = 0
while decimal_value > 0:
    binary_remainder = decimal_value % 2
    if binary_remainder == 1:
        binary_one_count = binary_one_count + 1
    decimal_value = decimal_value // 2
print(binary_one_count)
