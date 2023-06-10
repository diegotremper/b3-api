import os
from datetime import date

import pytest

from b3_api.parsers.income_report_parser import income_report_parser


def load_sample_html_data(request, name):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open("{}/{}.html".format(test_dir, name)) as f:
        return f.read()


@pytest.fixture
def html_informe_rendimentos(request):
    return load_sample_html_data(request, "informe_rendimentos")


@pytest.fixture
def html_informe_rendimentos_2(request):
    return load_sample_html_data(request, "informe_rendimentos_2")


@pytest.fixture
def html_informe_rendimentos_3(request):
    return load_sample_html_data(request, "informe_rendimentos_3")


@pytest.fixture
def html_informe_rendimentos_4(request):
    return load_sample_html_data(request, "informe_rendimentos_4")


@pytest.fixture
def html_informe_rendimentos_5(request):
    return load_sample_html_data(request, "informe_rendimentos_5")


@pytest.fixture
def html_informe_rendimentos_6(request):
    return load_sample_html_data(request, "informe_rendimentos_6")


@pytest.fixture
def html_informe_rendimentos_7(request):
    return load_sample_html_data(request, "informe_rendimentos_7")


@pytest.fixture
def html_informe_rendimentos_8(request):
    return load_sample_html_data(request, "informe_rendimentos_8")


@pytest.fixture
def html_informe_rendimentos_9(request):
    return load_sample_html_data(request, "informe_rendimentos_9")


@pytest.fixture
def html_informe_rendimentos_10(request):
    return load_sample_html_data(request, "informe_rendimentos_10")


@pytest.fixture
def html_informe_rendimentos_11(request):
    return load_sample_html_data(request, "informe_rendimentos_11")


def test_parse_informe_rendimentos(html_informe_rendimentos):
    data = income_report_parser(html_informe_rendimentos)
    assert data.dividend == 1.0
    assert data.competence == date(2023, 4, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_2(html_informe_rendimentos_2):
    data = income_report_parser(html_informe_rendimentos_2)
    assert data.dividend == 0.5024913685
    assert data.competence == date(2018, 12, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_3(html_informe_rendimentos_3):
    data = income_report_parser(html_informe_rendimentos_3)
    assert data.dividend == 1.393448898
    assert data.competence == date(2018, 8, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_4(html_informe_rendimentos_4):
    data = income_report_parser(html_informe_rendimentos_4)
    assert data.dividend == 0.27
    assert data.competence == date(2022, 11, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_5(html_informe_rendimentos_5):
    data = income_report_parser(html_informe_rendimentos_5)
    assert data.dividend == 0.27
    assert data.competence == date(2023, 3, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_6(html_informe_rendimentos_6):
    data = income_report_parser(html_informe_rendimentos_6)
    assert data.dividend == 0.57
    assert data.competence == date(2022, 11, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_7(html_informe_rendimentos_7):
    data = income_report_parser(html_informe_rendimentos_7)
    assert data.dividend == 0.51
    assert data.competence == date(2018, 12, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_8(html_informe_rendimentos_8):
    data = income_report_parser(html_informe_rendimentos_8)
    assert data.dividend == 0.55
    assert data.competence == date(2018, 2, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_9(html_informe_rendimentos_9):
    data = income_report_parser(html_informe_rendimentos_9)
    assert data.dividend == 0.9
    assert data.competence == date(2018, 3, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_10(html_informe_rendimentos_10):
    data = income_report_parser(html_informe_rendimentos_10)
    assert data.dividend == 0.2
    assert data.competence == date(2017, 12, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41


def test_parse_informe_rendimentos_11(html_informe_rendimentos_11):
    data = income_report_parser(html_informe_rendimentos_11)
    assert data.dividend == 0.63
    assert data.competence == date(2019, 12, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41
