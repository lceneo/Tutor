# Ввод: число строк, затем для каждой записи четыре значения через пробел:
# округ, фамилия, предмет, балл. Значения не должны содержать пробелов.
import sys
input_fields = sys.stdin.read().split()
record_count = int(input_fields[0])
next_field_index = 1
informatics_exam_count = 0
informatics_score_sum = 0
informatics_score_over_600_count = 0
district_v_participant_count = 0
district_zel_participant_count = 0
district_z_participant_count = 0

for record_index in range(record_count):
    district_code = input_fields[next_field_index]
    student_surname = input_fields[next_field_index + 1]
    exam_subject = input_fields[next_field_index + 2]
    exam_score = int(input_fields[next_field_index + 3])
    next_field_index = next_field_index + 4

    # Для информатики считаем количество, сумму и результаты выше 600.
    if exam_subject == "информатика":
        informatics_exam_count = informatics_exam_count + 1
        informatics_score_sum = informatics_score_sum + exam_score
        if exam_score > 600:
            informatics_score_over_600_count = informatics_score_over_600_count + 1

    # Отдельно считаем участников трёх округов для диаграммы.
    if district_code == "В":
        district_v_participant_count = district_v_participant_count + 1
    if district_code == "Зел":
        district_zel_participant_count = district_zel_participant_count + 1
    if district_code == "З":
        district_z_participant_count = district_z_participant_count + 1

print("Информатика, больше 600:", informatics_score_over_600_count)
if informatics_exam_count > 0:
    average_informatics_score = informatics_score_sum / informatics_exam_count
    print("Средний балл по информатике:", average_informatics_score)
print("Участники по округам В, Зел, З:", district_v_participant_count, district_zel_participant_count, district_z_participant_count)
