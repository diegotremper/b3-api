from typing import Optional

from pydantic import BaseModel


class ColumnDef(BaseModel):
    title: str
    id: Optional[str] = None
    also_known_as: Optional[list[str]] = None

    def match(self, title):
        match = (
            self.title.strip().rstrip(":").lower()
            == str(title).strip().rstrip(":").lower()
        )
        if not match and self.also_known_as:
            match = str(title).strip().rstrip(":").lower() in [
                str(t).strip().rstrip(":").lower() for t in self.also_known_as
            ]

        return match

    def handle_value(self, v):
        return str(v).strip()


class ColumnValue(BaseModel):
    column_def: ColumnDef
    title: str
    value: str


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def find_column_def(title: str, column_defs: list[ColumnDef]):
    for column_def in column_defs:
        if column_def.match(title):
            return column_def

    return None


def consume_table_by_pattern(tables, pattern, pop=True):
    for table in tables:
        found = table.find_all("span", string=pattern)
        if len(found) > 0:
            if pop:
                tables.remove(table)
            return table

    for table in tables:
        found = table.find_all("b", string=pattern)
        if len(found) > 0:
            if pop:
                tables.remove(table)
            return table

    raise Exception("Table not found for pattern: " + str(pattern))


def _clean(text):
    return text.strip()


def find_table_lines(table, skip_first_column=False):
    return [
        [
            _clean(cell.text)
            for cell in row("td")
            if not skip_first_column or cell != row("td")[0]
        ]
        for row in table("tr")
    ]


def find_columns(table, col_per_row=1, skip_first_column=False):
    lines = find_table_lines(table, skip_first_column)

    if col_per_row == 1:
        return lines

    found = []
    for line in lines:
        columns = list(chunks(line, col_per_row))
        found += columns

    return found


def find_table_data(table, **kwargs) -> list[ColumnValue]:
    col_per_row = kwargs.get("col_per_row", 1)
    debug = kwargs.get("debug", False)
    known_columns = kwargs.get("known_columns", [])
    skip_first_column = kwargs.get("skip_first_column", False)

    columns = find_columns(table, col_per_row, skip_first_column)

    if debug:
        import pprint

        print("Columns in table:")
        pprint.pprint(columns)

    found = []
    for column in columns:
        title = column[0]
        column_def = find_column_def(title, known_columns)
        if column_def:
            value = column_def.handle_value(column[1])
            found.append(
                ColumnValue(column_def=column_def, title=title, value=value)
            )

    if debug:
        print("Columns in FOUND in table:")
        for column in found:
            print(column.json())

    return found
