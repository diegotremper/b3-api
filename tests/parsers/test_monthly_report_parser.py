import os
from datetime import date

import pytest

from b3_api.parsers.monthly_report_parser import monthly_report_parser


def load_sample_html_data(request, name):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open("{}/{}.html".format(test_dir, name)) as f:
        return f.read()


@pytest.fixture
def monthly_report_html(request):
    return load_sample_html_data(request, "monthly_report")


def test_monthly_report_parser(monthly_report_html):
    data = monthly_report_parser(monthly_report_html)
    assert data.equityValuePerShare == 105.032292
    assert data.competence == date(2023, 3, 1)
    assert data.name == "Informe Mensal"
    assert data.type == 40
