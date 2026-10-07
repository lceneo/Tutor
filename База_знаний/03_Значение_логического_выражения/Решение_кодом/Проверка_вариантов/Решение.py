# Проверяем каждый вариант: ложь от ИЛИ получается, когда обе части ложны.
city_names = ["Москва", "Омск", "Дубна", "Новокузнецк"]
for city_index in range(len(city_names)):
    city_name = city_names[city_index]
    has_even_letter_count = len(city_name) % 2 == 0
    ends_with_vowel = city_name[-1].lower() in "аеёиоуыэюя"
    expression_is_true = has_even_letter_count or ends_with_vowel
    if not expression_is_true:
        print(city_index + 1, city_name)
