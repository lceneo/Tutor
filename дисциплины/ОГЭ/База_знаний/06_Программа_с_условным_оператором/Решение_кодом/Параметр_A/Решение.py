# Перебираем целые A и считаем, сколько раз программа выдаёт YES.
input_s_values = [13, 11, -12, 2, -10, 6, 2, 9, 1]
input_t_values = [2, 12, 12, -2, -10, -5, 8, 10, 13]
matching_parameter_count = 0

# Все границы изменения результата лежат между -13 и 14.
for parameter_a in range(-20, 21):
    yes_output_count = 0
    for pair_index in range(len(input_s_values)):
        if input_s_values[pair_index] > parameter_a or input_t_values[pair_index] > 12:
            yes_output_count = yes_output_count + 1
    if yes_output_count == 5:
        matching_parameter_count = matching_parameter_count + 1
        print("Подходит A:", parameter_a)

print("Число значений A:", matching_parameter_count)
