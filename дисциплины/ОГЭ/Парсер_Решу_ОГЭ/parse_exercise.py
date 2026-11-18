"""Получение всех подзадач номера ОГЭ: python parse_exercise.py 5."""

import argparse
import sys
from urllib.error import URLError

from parse_subtopic import get_constructor, parse_subtopic, write_json


def find_exercise(constructor, exercise_number):
    # num повторяется у заданий с развёрнутым ответом; issue содержит номер ОГЭ.
    matches = [item for item in constructor if item.get("type") != "extra"
               and str(item.get("issue")) == str(exercise_number)]
    if len(matches) != 1:
        raise ValueError(f"Номер задания {exercise_number}: найдено записей в каталоге {len(matches)}")
    return matches[0]


def parse_exercise(exercise_number: int, constructor=None, seen_ids=None) -> dict:
    """Возвращает задание с метаданными, разделами и их задачами."""
    if isinstance(exercise_number, bool) or not isinstance(exercise_number, int) or exercise_number <= 0:
        raise ValueError("Номер задания должен быть положительным целым числом")
    if constructor is None:
        constructor = get_constructor()
    if seen_ids is None:
        seen_ids = set()
    item = find_exercise(constructor, exercise_number)
    subtopics = item.get("subtopics") or []
    if not subtopics and item.get("amount", 0):
        raise ValueError(f"Задание {exercise_number} содержит задачи, но не содержит подзадач")

    def parse_section(section):
        section_id = section.get("id")
        title = section.get("title")
        amount = section.get("amount")
        children = section.get("subtopics") or []
        if children:
            return {"id": section_id, "title": title, "amount": amount,
                    "subtopics": [parse_section(child) for child in children]}
        return parse_subtopic(section_id, subtopic=section, seen_ids=seen_ids)

    print(f"Задание {exercise_number}: {item.get('title')}", file=sys.stderr)
    return {"number": exercise_number, "issue": item.get("issue"), "type": item.get("type"),
            "title": item.get("title"), "amount": item.get("amount"),
            "subtopics": [parse_section(section) for section in subtopics]}


def main():
    parser = argparse.ArgumentParser(description="Получить все подзадачи номера ОГЭ")
    parser.add_argument("number", type=int, help="номер задания ОГЭ")
    parser.add_argument("-o", "--output", help="сохранить JSON в файл UTF-8")
    args = parser.parse_args()
    try:
        write_json(parse_exercise(args.number), args.output)
    except (OSError, URLError, UnicodeError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
