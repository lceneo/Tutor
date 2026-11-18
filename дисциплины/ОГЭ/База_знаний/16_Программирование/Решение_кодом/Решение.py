# Читаем количество чисел, затем ищем наибольшее из кратных пяти.
number_count = int(input())
largest_multiple_of_five = 0
for _ in range(number_count):
    current_number = int(input())
    # Обновляем максимум только для подходящих чисел.
    if current_number % 5 == 0 and current_number > largest_multiple_of_five:
        largest_multiple_of_five = current_number
print(largest_multiple_of_five)
