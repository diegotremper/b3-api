from datetime import date

import tests.utils as utils
from b3_api.fund_get_document import fund_get_document


def test_fund_get_document_rendimento(request, mocker, requests_mock):
    utils.patch_request_session(mocker)
    income_response = utils.open_test_file(request, "informe_rendimentos.html")

    url = "https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=3"
    requests_mock.get(url, text=income_response)

    data = fund_get_document(3, 41)
    assert data.dividend == 1.0
    assert data.competence == date(2023, 4, 1)
    assert data.name == "Informações sobre Pagamento de Proventos"
    assert data.type == 41
