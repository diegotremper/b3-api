import tests.utils as utils
from b3_api.historical_series_available import historical_series_available


def _find_by_name(series, name):
    return next((s for s in series if s.name == name), None)


def test_historical_series_available(request, mocker, requests_mock):
    utils.patch_request_session(mocker)

    requests_mock.get(
        "https://bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricasArq.asp",
        text=utils.open_test_file(request, "sample.html"),
    )

    available_series = historical_series_available()

    assert len(available_series.annual_series) == 37
    assert len(available_series.monthly_series) == 12
    assert len(available_series.daily_series) == 108

    serie = _find_by_name(available_series.annual_series, "2010")
    assert serie is not None
    assert serie.type == 1
    assert serie.file_name == "COTAHIST_A2010.ZIP"

    serie = _find_by_name(available_series.monthly_series, "Mai/2023")
    assert serie is not None
    assert serie.type == 2
    assert serie.file_name == "COTAHIST_M052023.ZIP"

    serie = _find_by_name(available_series.daily_series, "15/03/2023")
    assert serie is not None
    assert serie.type == 3
    assert serie.file_name == "COTAHIST_D15032023.ZIP"
