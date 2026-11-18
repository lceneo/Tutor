"""Получение всех задач одной подзадачи: python parse_subtopic.py 24."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen

from parse_problem import BASE_URL, parse_problem


def get_constructor() -> list:
    request = Request(urljoin(BASE_URL, "newapi/general"), headers={
        "User-Agent": "Mozilla/5.0", "Accept": "application/json",
    })
    with urlopen(request, timeout=30) as response:
        data = json.load(response)
    constructor = data.get("constructor")
    if not isinstance(constructor, list):
        raise ValueError("Ответ сайта не содержит список constructor")
    return constructor


def walk_subtopics(subtopics):
    for subtopic in subtopics or []:
        yield subtopic
        yield from walk_subtopics(subtopic.get("subtopics"))


def find_subtopic(constructor, subtopic_id):
    matches = [subtopic for item in constructor for subtopic in walk_subtopics(item.get("subtopics"))
               if str(subtopic.get("id")) == str(subtopic_id)]
    if not matches:
        raise ValueError(f"Подзадача {subtopic_id} не найдена в каталоге")
    if len(matches) > 1:
        raise ValueError(f"Подзадача {subtopic_id} неоднозначна: найдено {len(matches)} записей")
    return matches[0]


class ProblemLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_numbers = False
        self.ids = []
        self.has_problem_list = False

    def handle_starttag(self, tag, attrs):
        classes = [value for name, value in attrs if name == "class" and value]
        if tag == "div" and any("prob_list" in value.split() for value in classes):
            self.has_problem_list = True
        if tag == "span" and any("prob_nums" in value.split() for value in classes):
            self.in_numbers = True
        if tag == "a" and self.in_numbers:
            href = next((value for name, value in attrs if name == "href"), None)
            if href:
                parsed = urlparse(urljoin(BASE_URL, href))
                values = parse_qs(parsed.query).get("id", [])
                if parsed.netloc == urlparse(BASE_URL).netloc and parsed.path == "/problem" and values:
                    if not re.fullmatch(r"[1-9]\d*", values[0]):
                        raise ValueError(f"Некорректный ID задачи в ссылке: {href}")
                    self.ids.append(int(values[0]))

    def handle_endtag(self, tag):
        if tag == "span" and self.in_numbers:
            self.in_numbers = False


def parse_subtopic(subtopic_id: int, *, subtopic: dict | None = None,
                   seen_ids: set | None = None) -> dict:
    """Возвращает подзадачу с метаданными и задачами из всех страниц подборки."""
    if isinstance(subtopic_id, bool) or not isinstance(subtopic_id, int) or subtopic_id <= 0:
        raise ValueError("ID подзадачи должен быть положительным целым числом")
    if subtopic is None:
        subtopic = find_subtopic(get_constructor(), subtopic_id)
    if subtopic.get("id") != subtopic_id:
        raise ValueError(f"Метаданные не соответствуют подзадаче {subtopic_id}")
    expected_amount = subtopic.get("amount")
    if expected_amount is not None and (isinstance(expected_amount, bool) or
                                        not isinstance(expected_amount, int) or expected_amount < 0):
        raise ValueError(f"Некорректное количество задач в подзадаче {subtopic_id}: {expected_amount}")
    if expected_amount == 0:
        return {"id": subtopic_id, "title": subtopic.get("title"), "amount": 0,
                "problem_count": 0, "problems": []}
    if seen_ids is None:
        seen_ids = set()

    ids = []
    skip = 0
    max_pages = max(20, (expected_amount + 4) // 5 + 10) if expected_amount is not None else 1000
    while True:
        if skip // 5 >= max_pages:
            raise ValueError(f"Сайт не завершил пагинацию подзадачи {subtopic_id} после {max_pages} страниц")
        url = urljoin(BASE_URL, f"test?theme={subtopic_id}")
        request = Request(url, data=f"ajax=1&skip={skip}".encode("ascii"), headers={
            "User-Agent": "Mozilla/5.0", "Accept": "text/html, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        })
        with urlopen(request, timeout=30) as response:
            source = response.read().decode(response.headers.get_content_charset() or "utf-8")
        page = ProblemLinks()
        page.feed(source)
        if not page.ids:
            if not page.has_problem_list and "В данной категории нет заданий" not in source:
                raise ValueError(f"Неожиданный ответ сайта для подзадачи {subtopic_id}")
            break
        ids.extend(page.ids)
        # Сервер возвращает страницы по пять позиций, но может скрыть задачу
        # на конкретной странице. Смещение всё равно сдвигается на пять.
        skip += 5

    if expected_amount is not None and len(ids) != expected_amount:
        print(f"Предупреждение: подзадача {subtopic_id}: в каталоге {expected_amount} задач, "
              f"в списке сайта получено {len(ids)}", file=sys.stderr)
    unique_ids = []
    duplicate_ids = []
    for problem_id in ids:
        if problem_id in seen_ids:
            if problem_id not in duplicate_ids:
                duplicate_ids.append(problem_id)
        else:
            seen_ids.add(problem_id)
            unique_ids.append(problem_id)
    print(f"Подзадача {subtopic_id}: получено ссылок {len(ids)}, новых задач {len(unique_ids)}; "
          "загружаю условия и решения", file=sys.stderr)
    result = {"id": subtopic_id, "title": subtopic.get("title"), "amount": expected_amount,
              "problem_count": len(set(ids)),
              "problems": [parse_problem(problem_id) for problem_id in unique_ids]}
    if duplicate_ids:
        result["duplicate_problem_ids"] = duplicate_ids
    return result


def write_json(result, output):
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if output is None:
        print(text)
    else:
        Path(output).write_text(text + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Получить все задачи подзадачи Решу ОГЭ")
    parser.add_argument("id", type=int, help="ID подзадачи")
    parser.add_argument("-o", "--output", help="сохранить JSON в файл UTF-8")
    args = parser.parse_args()
    try:
        if args.id <= 0:
            raise ValueError("ID подзадачи должен быть положительным целым числом")
        result = parse_subtopic(args.id)
        write_json(result, args.output)
    except (OSError, URLError, UnicodeError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
