"""简单的 CSV 创建、写入和读取示例。"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


DEFAULT_HEADERS = ["id", "name", "score"]


def create_csv(file_path: str | Path, headers: Iterable[str] = DEFAULT_HEADERS) -> Path:
    """创建一个 CSV 文件并写入表头。"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list(headers))

    return path


def write_csv_rows(file_path: str | Path, rows: Iterable[Iterable[object]]) -> None:
    """向已有 CSV 文件追加多行数据。"""
    path = Path(file_path)

    with path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """读取 CSV 并以字典列表形式返回。"""
    path = Path(file_path)

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


if __name__ == "__main__":
    output_path = create_csv("data/students.csv")

    sample_rows = [
        [1, "Alice", 95],
        [2, "Bob", 88],
        [3, "Charlie", 91],
    ]

    write_csv_rows(output_path, sample_rows)
    records = read_csv(output_path)

    print(f"CSV 文件已生成: {output_path}")
    print("读取结果:")
    for row in records:
        print(row)
