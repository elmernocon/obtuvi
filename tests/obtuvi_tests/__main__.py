from functools import cache
from pathlib import Path
from typing import Any

import yaml

from obtuvi import visit
from obtuvi import ObjectTuple, Visitor


class TestVisitor(Visitor):
    def visit_node(self, t: ObjectTuple):
        print(f"@ {t.path}")

    def visit_node_added(self, t: ObjectTuple):
        print(f"@ {t.path}-add: {t.b}")

    def visit_node_removed(self, t: ObjectTuple):
        print(f"@ {t.path}-rem: {t.a}")

    def visit_node_modified(self, t: ObjectTuple):
        print(f"@ {t.path}-mod: {t.a} -> {t.b}")

    def visit_node_unmodified(self, t: ObjectTuple):
        print(f"@ {t.path}-unm: {t.a} == {t.b}")

    def visit_node_length_mismatch(self, t: ObjectTuple):
        print(f"@ {t.path}-len: [{len(t.a)}] -> [{len(t.b)}]")

    def visit_node_type_mismatch(self, t: ObjectTuple):
        print(f"@ {t.path}-typ: {t.a} ({type(t.a)}) -> {t.b} ({type(t.b)})")

    def visit_dict_node(self, t: ObjectTuple):
        print(f"@ {t.path}-dic")

    def visit_list_node(self, t: ObjectTuple):
        print(f"@ {t.path}-lis")


@cache
def load_data_file(name: str) -> Any:
    test_dir = Path(__file__).parent
    data_dir = test_dir / "data"
    data_path = data_dir / name
    data_text = data_path.read_text()
    data = yaml.safe_load(data_text)
    return data


def test_visit(old: str, new: str, visitor: Visitor) -> None:
    a = load_data_file(old)
    b = load_data_file(new)
    print(f"{old} -> {new}")
    visit(a, b, visitor)
    print("")


def main():
    visitor = TestVisitor()

    # value
    test_visit("value-base.yaml", "value-modified.yaml", visitor)
    test_visit("value-base.yaml", "value-type-mismatch.yaml", visitor)

    # list
    test_visit("list-base.yaml", "list-child-added.yaml", visitor)
    test_visit("list-base.yaml", "list-child-removed.yaml", visitor)
    test_visit("list-base.yaml", "list-child-modified.yaml", visitor)
    test_visit("list-base.yaml", "list-child-type-mismatch.yaml", visitor)
    test_visit("list-base.yaml", "list-rearranged.yaml", visitor)
    test_visit("list-base.yaml", "list-rearranged-added.yaml", visitor)

    # dict
    test_visit("dict-base.yaml", "dict-child-added.yaml", visitor)
    test_visit("dict-base.yaml", "dict-child-removed.yaml", visitor)
    test_visit("dict-base.yaml", "dict-child-modified.yaml", visitor)
    test_visit("dict-base.yaml", "dict-child-type-mismatch.yaml", visitor)


if __name__ == "__main__":
    main()
