from functools import cache
from pathlib import Path
from typing import Any

import yaml

from obtuvi import visit
from obtuvi.visitor.echo import EchoVisitor
from obtuvi.visitor.jsonpatch import JsonPatchVisitor


@cache
def load_data_file(name: str) -> Any:
    test_dir = Path(__file__).parent
    data_dir = test_dir / "data"
    data_path = data_dir / name
    data_text = data_path.read_text()
    data = yaml.safe_load(data_text)
    return data


def test_visit(old: str, new: str) -> None:
    a = load_data_file(old)
    b = load_data_file(new)
    print(f"{old} -> {new} (EchoVisitor)")
    visit(a, b, EchoVisitor())
    print("")

    print(f"{old} -> {new} (JsonPatchVisitor)")
    v1 = JsonPatchVisitor()
    visit(a, b, v1)
    print(v1.patch)
    print("")


def main():
    # value
    test_visit("value-base.yaml", "value-modified.yaml")
    test_visit("value-base.yaml", "value-type-mismatch.yaml")

    # list
    test_visit("list-base.yaml", "list-child-added.yaml")
    test_visit("list-base.yaml", "list-child-removed.yaml")
    test_visit("list-base.yaml", "list-child-modified.yaml")
    test_visit("list-base.yaml", "list-child-type-mismatch.yaml")
    test_visit("list-base.yaml", "list-rearranged.yaml")
    test_visit("list-base.yaml", "list-rearranged-added.yaml")

    # dict
    test_visit("dict-base.yaml", "dict-child-added.yaml")
    test_visit("dict-base.yaml", "dict-child-removed.yaml")
    test_visit("dict-base.yaml", "dict-child-modified.yaml")
    test_visit("dict-base.yaml", "dict-child-type-mismatch.yaml")


if __name__ == "__main__":
    main()
