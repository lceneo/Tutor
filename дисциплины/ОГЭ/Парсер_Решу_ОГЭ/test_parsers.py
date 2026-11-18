"""Проверки форматов и дедупликации без запросов к сайту."""

import contextlib
import io
import json
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import parse_all
import parse_exercise
import parse_subtopic


CONSTRUCTOR = [
    {"num": 1, "issue": "1", "type": "short", "title": "Первое задание", "amount": 7,
     "subtopics": [{"id": 21, "title": "Первая подзадача", "amount": 5},
                   {"id": 22, "title": "Вторая подзадача", "amount": 2}]},
    {"num": 1, "issue": "13", "type": "detailed", "title": "Тринадцатое задание", "amount": 1,
     "subtopics": [{"id": 30, "title": "Ещё одна подзадача", "amount": 1},
                   {"id": 31, "title": "Пустая подзадача", "amount": 0}]},
    {"num": "extra", "issue": "Д1", "type": "extra", "title": "Дополнительное", "amount": 0},
]

PAGES = {
    (21, 0): [101, 102, 101],
    (21, 5): [102, 103],
    (22, 0): [103, 104],
    (30, 0): [104],
}


class FakeResponse:
    def __init__(self, text):
        self.text = text
        self.headers = self

    def get_content_charset(self):
        return "utf-8"

    def read(self):
        return self.text.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def fake_urlopen(request, timeout):
    theme = int(parse_qs(urlparse(request.full_url).query)["theme"][0])
    skip = int(parse_qs(request.data.decode("ascii"))["skip"][0])
    ids = PAGES.get((theme, skip), [])
    links = "".join(f'<span class="prob_nums"><a href="/problem?id={i}">{i}</a></span>' for i in ids)
    return FakeResponse(f'<div class="prob_list">{links}</div>')


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(parse_subtopic, "get_constructor", return_value=CONSTRUCTOR))
        self.stack.enter_context(patch.object(parse_exercise, "get_constructor", return_value=CONSTRUCTOR))
        self.stack.enter_context(patch.object(parse_all, "get_constructor", return_value=CONSTRUCTOR))
        self.stack.enter_context(patch.object(parse_subtopic, "urlopen", side_effect=fake_urlopen))
        self.stack.enter_context(patch.object(parse_subtopic, "parse_problem", side_effect=lambda i: {"id": i}))
        self.stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def test_subtopic_cli_includes_metadata_and_unique_count(self):
        output = io.StringIO()
        with patch.object(sys, "argv", ["parse_subtopic.py", "21"]), contextlib.redirect_stdout(output):
            self.assertEqual(parse_subtopic.main(), 0)
        result = json.loads(output.getvalue())
        self.assertEqual((result["id"], result["title"], result["amount"], result["problem_count"]),
                         (21, "Первая подзадача", 5, 3))
        self.assertEqual([p["id"] for p in result["problems"]], [101, 102, 103])

    def test_exercise_contains_metadata_and_preserves_cross_section_references(self):
        result = parse_exercise.parse_exercise(1)
        self.assertEqual((result["number"], result["title"]), (1, "Первое задание"))
        first, second = result["subtopics"]
        self.assertEqual(first["problem_count"], 3)
        self.assertEqual(second["problem_count"], 2)
        self.assertEqual([p["id"] for p in second["problems"]], [104])
        self.assertEqual(second["duplicate_problem_ids"], [103])

    def test_catalog_reuses_exercise_shape_and_excludes_extra(self):
        result = parse_all.parse_all()
        self.assertEqual([item["number"] for item in result], [1, 13])
        self.assertEqual(result[1]["title"], "Тринадцатое задание")
        self.assertEqual(result[1]["subtopics"][0]["duplicate_problem_ids"], [104])
        self.assertEqual(result[1]["subtopics"][1]["problem_count"], 0)
        self.assertEqual(result[1]["subtopics"][1]["problems"], [])
        ids = [p["id"] for item in result for section in item["subtopics"] for p in section["problems"]]
        self.assertEqual(ids, [101, 102, 103, 104])


if __name__ == "__main__":
    unittest.main()
