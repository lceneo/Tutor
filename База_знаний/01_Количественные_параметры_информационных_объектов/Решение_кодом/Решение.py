# Размер уменьшения в байтах и число бит на один символ.
size_reduction_bytes = 8
bits_per_symbol = 8

# Находим число удалённых символов, затем убираем запятую и пробел.
bytes_per_symbol = bits_per_symbol // 8
target_name_length = size_reduction_bytes // bytes_per_symbol - 2

# Ищем название нужной длины среди вариантов из условия.
candidate_names = ["Обь", "Лена", "Волга", "Москва", "Макензи", "Амазонка"]
for candidate_name in candidate_names:
    if len(candidate_name) == target_name_length:
        print(candidate_name)
