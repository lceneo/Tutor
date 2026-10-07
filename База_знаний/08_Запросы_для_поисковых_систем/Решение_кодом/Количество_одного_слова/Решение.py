# Восстанавливаем размер второго запроса из объединения и пересечения.
union_page_count_thousands = 780
known_word_page_count_thousands = 260
shared_page_count_thousands = 50
other_word_page_count_thousands = union_page_count_thousands - known_word_page_count_thousands + shared_page_count_thousands
print(other_word_page_count_thousands)
