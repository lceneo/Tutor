# Считаем запуски, в которых исходное условие программы не выполняется.
input_pairs = [(12, 5), (5, 3), (-4, 1), (2, -5), (5, -7), (10, 3), (18, 6), (3, 0), (2, 5)]
not_output_count = 0
for s_value, t_value in input_pairs:
    yes_condition = s_value >= 2 and t_value < 5
    if not yes_condition:
        not_output_count = not_output_count + 1
print(not_output_count)
