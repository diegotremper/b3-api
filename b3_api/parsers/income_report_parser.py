import re

from bs4 import BeautifulSoup

from b3_api.parsers.models import IncomeReport, ReportType
from b3_api.parsers.utils import (
    ColumnDef,
    consume_table_by_pattern,
    find_columns,
    find_table_data,
)

WELL_KNOWN_INCOME_COLUMNS = [
    ColumnDef(title="Data da informação"),
    ColumnDef(
        title="Data-base (último dia de negociação “com” direito ao provento)",
        id="base_date",
    ),
    ColumnDef(title="Data do pagamento"),
    ColumnDef(
        title="Valor do provento por cota (R$)",
        id="dividend",
        also_known_as=["Valor do provento (R$/unidade)"],
    ),
    ColumnDef(title="Período de referência", id="reference_period"),
    ColumnDef(title="Ano", id="year"),
    ColumnDef(title="Rendimento isento de IR*"),
]

WELL_KNOWN_DATA_COLUMNS = [
    ColumnDef(title="Nome do Fundo"),
    ColumnDef(title="CNPJ do Fundo"),
    ColumnDef(title="Nome do Administrador"),
    ColumnDef(title="CNPJ do Administrador"),
    ColumnDef(title="Responsável pela Informação"),
    ColumnDef(title="Telefone Contato"),
    ColumnDef(title="Código ISIN da cota"),
    ColumnDef(title="Código de negociação da cota", id="ticker"),
    ColumnDef(title="Ano", id="year"),
]


def _month_to_number(month):
    if str(month).isnumeric():
        return int(month)

    month = str(month).lower()
    tries = {
        "janeiro": 1,
        "fevereiro": 2,
        "fevareiro": 2,
        "março": 3,
        "marco": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12,
    }

    if month in tries:
        return tries[month]


def _try_to_split(text, sep):
    if text is not None:
        month_and_year = [x.strip().lower() for x in text.split(sep)]
        if len(month_and_year) == 2:
            month = _month_to_number(month_and_year[0])
            year = month_and_year[1]
            if month is not None and year is not None:
                return f"{month}/{year}"

    return None


def _please_find_competence(fund_data_table, income_data_table):
    """This is a desperate attempt to find the competence of the report."""
    year = None
    reference_period = None
    base_date = None

    all_columns = find_table_data(
        fund_data_table,
        known_columns=WELL_KNOWN_DATA_COLUMNS,
        col_per_row=2,
    ) + find_table_data(
        income_data_table,
        known_columns=WELL_KNOWN_INCOME_COLUMNS,
    )

    for column in all_columns:
        if column.column_def.id == "reference_period":
            reference_period = column.value
        if column.column_def.id == "year":
            year = column.value
        if column.column_def.id == "base_date":
            base_date = column.value

    if str(year).isnumeric():
        year = int(year)
    else:
        year = None

    month = _month_to_number(reference_period)

    if month is not None and year is not None:
        return f"{month}/{year}"

    if reference_period is not None:
        if _try_to_split(reference_period, " "):
            return _try_to_split(reference_period, " ")

    if reference_period is not None:
        if _try_to_split(reference_period, "/"):
            return _try_to_split(reference_period, "/")

    if reference_period is not None:
        if _try_to_split(reference_period, "-"):
            return _try_to_split(reference_period, "-")

    if base_date is not None:
        return base_date


def income_report_parser(html: str):
    dividend = None
    ticker = None
    competence = None

    soup = BeautifulSoup(html, "html5lib")
    tables = soup.find_all("table")

    pattern = re.compile(r"\bCNPJ\b", re.MULTILINE | re.IGNORECASE)
    fund_data_table = consume_table_by_pattern(tables, pattern)
    fund_data = find_table_data(
        fund_data_table,
        known_columns=WELL_KNOWN_DATA_COLUMNS,
        col_per_row=2,
        debug=True,
    )
    for column in fund_data:
        if column.column_def.id == "ticker":
            ticker = column.value

    pattern = re.compile(r"\bRendimento\b", re.MULTILINE | re.IGNORECASE)
    income_data_table = consume_table_by_pattern(tables, pattern)
    income_data = find_table_data(
        income_data_table,
        known_columns=WELL_KNOWN_INCOME_COLUMNS,
        debug=True,
    )
    for column in income_data:
        if column.column_def.id == "dividend":
            dividend = column.value

    competence = _please_find_competence(fund_data_table, income_data_table)

    # here we go -> informe_rendimentos.html has a different layout
    if ticker is None:
        columns = find_columns(income_data_table, col_per_row=2)
        for column in columns:
            if (
                str(column[0]).strip().rstrip(":").lower()
                == "Código de negociação".strip().rstrip(":").lower()
            ):
                ticker = column[1]
                break

    return IncomeReport(
        type=ReportType.INCOME,
        name="Informações sobre Pagamento de Proventos",
        competence=competence,
        dividend=dividend,
        ticker=ticker,
    )
