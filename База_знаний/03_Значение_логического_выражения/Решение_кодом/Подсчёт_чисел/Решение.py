# Считаем двузначные числа, которые нечётные и не кратны пяти.
matching_number_count = 0
for candidate_number in range(10, 100):
    is_odd = candidate_number % 2 != 0
    is_not_multiple_of_five = candidate_number % 5 != 0
    if is_odd and is_not_multiple_of_five:
        matching_number_count = matching_number_count + 1
print(matching_number_count)
