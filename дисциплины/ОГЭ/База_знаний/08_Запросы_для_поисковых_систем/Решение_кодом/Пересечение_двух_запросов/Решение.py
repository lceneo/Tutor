# Из суммы размеров запросов вычитаем размер объединения.
word_a_page_count_thousands = 60
word_b_page_count_thousands = 140
union_page_count_thousands = 180
intersection_page_count_thousands = word_a_page_count_thousands + word_b_page_count_thousands - union_page_count_thousands
print(intersection_page_count_thousands)
