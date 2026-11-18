# Разделяем строку на коды из разбора и заменяем каждый код буквой.
code_segments = ["#", "~#", "~", "#+", "+~#"]
symbol_to_letter = {"+#": "А", "#+": "Е", "~": "Л", "#": "П", "+~#": "Т", "~#": "О"}

decoded_message = ""
for code_segment in code_segments:
    decoded_message = decoded_message + symbol_to_letter[code_segment]
print(decoded_message)
