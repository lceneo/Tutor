"""Получение условия и решения одной задачи с inf-oge.sdamgia.ru.

Запуск: python parse_problem.py 10383
Сохранение JSON: python parse_problem.py 10383 --output задача_10383.json
Чтобы также сохранить HTML-файлы: python parse_problem.py 10383 --html-dir папка
Функцию parse_problem можно импортировать в скрипт разбора подзадачи.
"""

import argparse
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE_URL = "https://inf-oge.sdamgia.ru/"


def html_document(fragment: str, title: str, page_url: str) -> str:
    """Оборачивает фрагмент страницы в самостоятельный HTML-документ."""
    return (
        '<!DOCTYPE html>\n<html lang="ru">\n<head>\n'
        '<meta charset="utf-8">\n'
        f'<title>{escape(title)}</title>\n'
        f'<base href="{escape(page_url, quote=True)}">\n'
        '<style>.source_code p { white-space: pre-wrap; margin: 0; } '
        'table { border-collapse: collapse; } '
        'td, th { border: 1px solid #aaa; padding: 0.25em; }</style>\n'
        f'</head>\n<body>\n{fragment}\n</body>\n</html>'
    )


def document_body(document: str) -> str:
    """Извлекает фрагмент из документа, созданного html_document."""
    _, marker, body = document.partition("\n<body>\n")
    fragment, end, _ = body.rpartition("\n</body>\n</html>")
    if not marker or not end:
        raise ValueError("Не удалось извлечь содержимое HTML-документа")
    return fragment


class ProblemBlocks(HTMLParser):
    """Находит блоки и возвращает их исходное внутреннее HTML-содержимое."""

    def __init__(self, source: str, problem_id: int):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.solution_id = f"sol{problem_id}"
        self.line_offsets = [0]
        for match in re.finditer("\n", source):
            self.line_offsets.append(match.end())
        self.blocks = {"condition": [], "solution": []}
        self.active = None
        self.depth = 0
        self.start = 0

    def source_offset(self) -> int:
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            return
        if self.active is not None:
            self.depth += 1
            return
        element_id = next((value for name, value in attrs if name == "id"), "")
        if element_id and re.fullmatch(r"body\d+", element_id):
            self.active = "condition"
        elif element_id == self.solution_id:
            self.active = "solution"
        else:
            return
        self.depth = 1
        self.start = self.source_offset() + len(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag != "div" or self.active is None:
            return
        self.depth -= 1
        if self.depth == 0:
            self.blocks[self.active].append(self.source[self.start:self.source_offset()])
            self.active = None


class BlockContent(HTMLParser):
    """Извлекает читаемый текст, сохраняя ссылки на изображения на их местах."""

    def __init__(self, page_url: str):
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.parts = []
        self.ignored = 0
        self.table_depth = 0
        self.row = None
        self.cell = None

    def append_text(self, text):
        if self.cell is not None:
            self.cell.append(text)
        else:
            self.parts.append(text)

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.ignored += 1
            return
        if self.ignored:
            return
        if tag == "table":
            self.table_depth += 1
            if self.table_depth == 1:
                self.parts.append("\n")
            return
        if self.table_depth:
            if tag == "tr" and self.table_depth == 1:
                self.row = []
            elif tag in {"td", "th"} and self.row is not None and self.table_depth == 1:
                self.cell = []
            elif tag == "br" and self.cell is not None:
                self.cell.append(" ")
            elif tag == "img":
                src = next((value for name, value in attrs if name == "src"), None)
                if src:
                    self.append_text(f"[Изображение: {urljoin(self.page_url, src)}]")
            return
        if tag in {"p", "br", "div", "li", "tr"}:
            self.parts.append("\n")
        if tag == "img":
            src = next((value for name, value in attrs if name == "src"), None)
            if src:
                url = urljoin(self.page_url, src)
                self.parts.append(f"[Изображение: {url}]")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.ignored:
            self.ignored -= 1
        elif self.ignored:
            return
        elif self.table_depth:
            if tag in {"td", "th"} and self.cell is not None and self.table_depth == 1:
                self.row.append(" ".join("".join(self.cell).split()))
                self.cell = None
            elif tag == "tr" and self.row is not None and self.table_depth == 1:
                self.parts.append(" | ".join(self.row) + "\n")
                self.row = None
            elif tag == "table":
                self.table_depth -= 1
                if self.table_depth == 0:
                    self.parts.append("\n")
        elif tag in {"p", "div", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.ignored:
            if self.table_depth and self.cell is None:
                if data.strip():
                    self.parts.append(data)
            else:
                self.append_text(data)

    def result(self, fragment: str, title: str) -> dict:
        self.feed(fragment)
        text = "".join(self.parts).replace("\u00ad", "").replace("\xa0", " ").replace("\u202f", " ")
        lines = [line.rstrip() for line in text.splitlines()]
        text = "\n".join(line for line in lines if line.strip()).strip()
        html = html_document(fragment, title, self.page_url)
        return {"text": text, "html": html}


def parse_problem(problem_id: int) -> dict:
    """Возвращает данные одной задачи; при ошибке выбрасывает исключение."""
    if isinstance(problem_id, bool) or not isinstance(problem_id, int) or problem_id <= 0:
        raise ValueError("ID задачи должен быть положительным целым числом")
    url = urljoin(BASE_URL, f"problem?id={problem_id}")
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    with urlopen(request, timeout=30) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        source = response.read().decode(encoding)

    parser = ProblemBlocks(source, problem_id)
    parser.feed(source)
    for name, blocks in parser.blocks.items():
        if len(blocks) != 1:
            raise ValueError(f"Ожидался один блок {name}, найдено: {len(blocks)} (задача {problem_id})")

    return {
        "id": problem_id,
        "url": url,
        "condition": BlockContent(url).result(parser.blocks["condition"][0], f"Задача {problem_id}: условие"),
        "solution": BlockContent(url).result(parser.blocks["solution"][0], f"Задача {problem_id}: решение"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Получить условие и решение задачи Решу ОГЭ в JSON")
    parser.add_argument("id", type=int, help="положительный ID задачи")
    parser.add_argument("-o", "--output", type=Path, help="сохранить JSON в файл UTF-8")
    parser.add_argument("--html-dir", type=Path, help="папка для сохранения HTML-файлов условия и решения")
    args = parser.parse_args()
    try:
        result = parse_problem(args.id)
        if args.html_dir is not None:
            args.html_dir.mkdir(parents=True, exist_ok=True)
            for name in ("condition", "solution"):
                (args.html_dir / f"{args.id}_{name}.html").write_text(result[name]["html"], encoding="utf-8")
            condition = document_body(result["condition"]["html"])
            solution = document_body(result["solution"]["html"])
            combined = html_document(f"{condition}\n<hr>\n{solution}", f"Задача {args.id}", result["url"])
            (args.html_dir / f"{args.id}_combined.html").write_text(combined, encoding="utf-8")
        json_text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output is None:
            print(json_text)
        else:
            args.output.write_text(json_text + "\n", encoding="utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeError, ValueError, OSError) as error:
        print(f"Не удалось получить задачу: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
