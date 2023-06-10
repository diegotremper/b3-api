import tests.utils as utils
from b3_api.fund_documents import fund_documents


def test_fund_documents_incomes(request, mocker, requests_mock):
    incomes = utils.open_test_file(request, "incomes.json")
    utils.patch_request_session(mocker)

    requests_mock.get(
        "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedDocumentsTypeHistory/eyJjbnBqIjogIjIxNDA4MDYzMDAwMTUxIiwgImRhdGVJbml0aWFsIjogIjIwMjAtMDEtMDEiLCAiZGF0ZUZpbmFsIjogIjIwMjAtMTItMzEiLCAidHlwZSI6IDQxfQ==",
        text=incomes,
        headers={"Content-Type": "application/json"},
    )

    docs = fund_documents("21408063000151", year=2020, document_type=41)
    assert len(docs) == 12
