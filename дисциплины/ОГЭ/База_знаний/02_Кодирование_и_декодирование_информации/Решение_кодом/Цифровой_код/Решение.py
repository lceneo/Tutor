# Перебираем все варианты разбиения каждого сообщения на коды разной длины.
binary_codes = {"01": "А", "011": "В", "100": "Д", "111": "О", "010": "Р", "001": "У"}

def decode_from(encoded_message, current_position):
    # Конец строки означает, что найдено полное разбиение.
    if current_position == len(encoded_message):
        return [""]

    possible_decodings = []
    for code_fragment in binary_codes:
        if encoded_message[current_position:current_position + len(code_fragment)] == code_fragment:
            remaining_decodings = decode_from(encoded_message, current_position + len(code_fragment))
            for remaining_decoding in remaining_decodings:
                possible_decodings = possible_decodings + [binary_codes[code_fragment] + remaining_decoding]
    return possible_decodings

encoded_messages = ["01001001", "11101001", "10001010"]
for encoded_message in encoded_messages:
    possible_decodings = decode_from(encoded_message, 0)
    print(encoded_message, possible_decodings)
    print("Число разбиений:", len(possible_decodings))
