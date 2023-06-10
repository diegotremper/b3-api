import tests.utils as utils
from b3_api.fund_events import fund_events


def test_fund_events(request, mocker, requests_mock):
    sample = utils.open_test_file(request, "sample.json")
    utils.patch_request_session(mocker)

    requests_mock.get(
        "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedSupplementFunds/eyJ0eXBlRnVuZCI6IDcsICJpZGVudGlmaWVyRnVuZCI6ICJLTkNSIiwgImNucGoiOiAiMTY3MDY5NTgwMDAxMzIifQ==",
        json=sample,
        headers={"Content-Type": "application/json"},
    )

    events = fund_events("kncr11", "16706958000132")
    assert len(events) == 1
