import re

from bs4 import BeautifulSoup

from b3_api.parsers.models import MonthlyReport, ReportType
from b3_api.parsers.utils import ColumnDef, consume_table_by_pattern
from b3_api.parsers.utils import find_table_data as find_table_data

WELL_KNOWN_NET_WORTH_COLUMNS = [
    ColumnDef(title="Ativo – R$"),
    ColumnDef(title="Patrimônio Líquido – R$"),
    ColumnDef(title="Número de Cotas Emitidas"),
    ColumnDef(
        title="Valor Patrimonial das Cotas – R$", id="equityValuePerShare"
    ),
]

WELL_KNOWN_SHAREHOLDERS_COLUMNS = [
    ColumnDef(
        title="Data da Informação sobre detalhamento do número de cotistas¹"
    ),
    ColumnDef(title="Número de cotistas"),
    ColumnDef(title="Pessoa física"),
    ColumnDef(title="Pessoa jurídica não financeira"),
    ColumnDef(title="Banco comercial"),
    ColumnDef(title="Corretora ou distribuidora"),
    ColumnDef(title="Outras pessoas jurídicas financeiras"),
    ColumnDef(title="Investidores não residentes"),
    ColumnDef(title="Entidade aberta de previdência complementar"),
    ColumnDef(title="Entidade fechada de previdência complementar"),
    ColumnDef(title="Regime próprio de previdência dos servidores públicos"),
    ColumnDef(title="Sociedade seguradora ou resseguradora"),
    ColumnDef(title="Sociedade de capitalização e de arrendamento mercantil"),
    ColumnDef(title="Fundos de investimento imobiliário"),
    ColumnDef(title="Outros fundos de investimento"),
    ColumnDef(
        title="Cotistas de distribuidores do fundo (distribuição por conta e ordem)"
    ),
    ColumnDef(title="Outros tipos de cotistas não relacionados"),
]

WELL_KNOWN_DATA_COLUMNS = [
    ColumnDef(title="Nome do Fundo"),
    ColumnDef(title="CNPJ do Fundo"),
    ColumnDef(title="Data de Funcionamento"),
    ColumnDef(title="Público Alvo"),
    ColumnDef(title="Código ISIN"),
    ColumnDef(title="Quantidade de cotas emitidas"),
    ColumnDef(title="Fundo Exclusivo?"),
    ColumnDef(
        title="Cotistas possuem vínculo familiar ou societário familiar?"
    ),
    ColumnDef(title="Classificação autorregulação"),
    ColumnDef(title="Prazo de Duração"),
    ColumnDef(title="Data do Prazo de Duração"),
    ColumnDef(title="Encerramento do exercício social"),
    ColumnDef(title="Mercado de negociação das cotas"),
    ColumnDef(title="Entidade administradora de mercado organizado"),
    ColumnDef(title="Nome do Administrador"),
    ColumnDef(title="CNPJ do Administrador"),
    ColumnDef(title="Endereço"),
    ColumnDef(title="Telefones"),
    ColumnDef(title="Site"),
    ColumnDef(title="E-mail"),
    ColumnDef(title="Competência", id="competence"),
]


def monthly_report_parser(html: str):
    equityValuePerShare = None
    competence = None

    soup = BeautifulSoup(html, "html5lib")
    tables = soup.find_all("table")

    pattern = re.compile(
        r"\bNome\s+do\s+Fundo\b", re.MULTILINE | re.IGNORECASE
    )
    fund_data_table = consume_table_by_pattern(tables, pattern)
    fund_data = find_table_data(
        fund_data_table,
        known_columns=WELL_KNOWN_DATA_COLUMNS,
        col_per_row=2,
    )
    for column in fund_data:
        if column.column_def.id == "competence":
            competence = column.value

    pattern = re.compile(
        r"mero\s+de\s+Cotas\s+Emitidas", re.MULTILINE | re.IGNORECASE
    )
    net_worth_table = consume_table_by_pattern(tables, pattern)
    net_worth_data = find_table_data(
        net_worth_table,
        known_columns=WELL_KNOWN_NET_WORTH_COLUMNS,
        skip_first_column=True,
    )
    for column in net_worth_data:
        if column.column_def.id == "equityValuePerShare":
            equityValuePerShare = column.value

    return MonthlyReport(
        equityValuePerShare=equityValuePerShare,
        competence=competence,
        name="Informe Mensal",
        type=ReportType.MONTHLY,
    )
