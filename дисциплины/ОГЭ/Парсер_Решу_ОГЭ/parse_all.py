"""Получение всех заданий ОГЭ, кроме дополнительных: python parse_all.py."""

import argparse
import sys
from urllib.error import URLError

from parse_exercise import parse_exercise
from parse_subtopic import get_constructor, write_json


def parse_all() -> list:
    """Возвращает каталог в порядке сайта, исключая type='extra'."""
    constructor = get_constructor()
    result = []
    seen_ids = set()
    for item in constructor:
        if item.get("type") == "extra":
            continue
        issue = item.get("issue")
        if not str(issue).isdigit() or int(issue) <= 0:
            raise ValueError(f"Не удалось определить номер задания: {issue!r}")
        number = int(issue)
        result.append(parse_exercise(number, constructor, seen_ids))
    return result


def main():
    parser = argparse.ArgumentParser(description="Получить весь каталог заданий ОГЭ, кроме дополнительных")
    parser.add_argument("-o", "--output", help="сохранить JSON в файл UTF-8")
    args = parser.parse_args()
    try:
        write_json(parse_all(), args.output)
    except (OSError, URLError, UnicodeError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
