def find_first(start, stop, step, condition):
    """Возвращает первое подходящее целое число в заданном направлении."""
    for value in range(start, stop, step):
        if condition(value):
            return value
    return None


largest = find_first(100, -101, -1, lambda x: not (x <= 15) and x < 20)
smallest = find_first(-100, 101, 1, lambda x: not (x < 2) and x < 5)
any_value = find_first(-100, 101, 1, lambda x: x < 8 and not (x < 7))

print("Наибольшее: ", largest)
print("Наименьшее: ", smallest)
print("Подходящее число: ", any_value)
