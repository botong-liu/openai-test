"""简单的 CSV 创建、写入和读取示例。"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Callable, Iterable


DEFAULT_HEADERS = ["id", "name", "score"]
RowFilter = Callable[[list[object]], bool]
RecordFilter = Callable[[dict[str, str]], bool]


def create_csv(file_path: str | Path, headers: Iterable[str] = DEFAULT_HEADERS) -> Path:
    """创建一个 CSV 文件并写入表头。"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list(headers))

    return path


def write_csv_rows(
    file_path: str | Path,
    rows: Iterable[Iterable[object]],
    row_filter: RowFilter | None = None,
) -> None:
    """向已有 CSV 文件追加多行数据，可选按条件过滤待写入行。"""
    path = Path(file_path)

    normalized_rows = [list(row) for row in rows]
    if row_filter is not None:
        normalized_rows = [row for row in normalized_rows if row_filter(row)]

    with path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(normalized_rows)


def read_csv(
    file_path: str | Path,
    record_filter: RecordFilter | None = None,
) -> list[dict[str, str]]:
    """读取 CSV 并以字典列表形式返回，可选按条件过滤读取结果。"""
    path = Path(file_path)

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        records = list(reader)

    if record_filter is not None:
        return [record for record in records if record_filter(record)]

    return records


if __name__ == "__main__":
    output_path = create_csv("data/students.csv")

    sample_rows = [
        [1, "Alice", 95],
        [2, "Bob", 88],
        [3, "Charlie", 91],
        [4, "David", 79],
    ]

    write_csv_rows(output_path, sample_rows, row_filter=lambda row: int(row[2]) >= 85)
    records = read_csv(output_path, record_filter=lambda row: int(row["score"]) >= 90)

    print(f"CSV 文件已生成: {output_path}")
    print("筛选后读取结果:")
    for row in records:
        print(row)
