import tests.utils as utils
from b3_api.fund_detail import fund_detail


def test_fund_detail(request, mocker, requests_mock):
    http_200 = utils.open_test_file(request, "http_200.json")
    utils.patch_request_session(mocker)

    requests_mock.get(
        "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetDetailFundSIG/eyJ0eXBlRnVuZCI6IDcsICJpZGVudGlmaWVyRnVuZCI6ICJQVkJJIn0=",
        json=http_200,
        headers={"Content-Type": "application/json"},
    )

    fund = fund_detail("pvbi11")
    assert fund.acronym == "PVBI"
    assert fund.tradingName == "FII VBI PRI "
    assert fund.tradingCode == "PVBI11 "
    assert fund.tradingCodeOthers == ""
    assert fund.cnpj == "35652102000176"
    assert (
        fund.classification
        == "Financeiro e Outros/Fundos/Fundos Imobiliários                                  "
    )
    assert fund.webSite == "www.btgpactual.com"
    assert (
        fund.fundAddress
        == "PRAIA DO BOTAFOGO, 501 - 5 ANDAR - CEP: 22250911 CIDADE: RIO DE JANEIRO UF: RJ"
    )
    assert fund.fundPhoneNumberDDD == "11"
    assert fund.fundPhoneNumber == "33832513"
    assert fund.fundPhoneNumberFax == "0"
    assert fund.positionManager == "DIRETOR RESPONSAVEL                     "
    assert (
        fund.managerName
        == "ALLAN HADID                                                 "
    )
    assert (
        fund.companyAddress
        == "PRAIA DO BOTAFOGO, 501 - 5 ANDAR - CEP: 22250911 CIDADE: RIO DE JANEIRO UF: RJ"
    )
    assert fund.companyPhoneNumberDDD == "11"
    assert fund.companyPhoneNumberDDD == "11"
    assert fund.companyPhoneNumber == "33832513"
    assert fund.companyPhoneNumberFax == "0"
    assert fund.companyEmail == "sh-contato-fundoimobiliario@btgpactual.com"
    assert (
        fund.companyName
        == "FDO. INV. IMOB. VBI PRIME PROPERTIES              "
    )
    assert fund.quotaCount == "12142208"
    assert fund.quotaDateApproved == "07/11/2022"
    assert fund.typeFNET is None
    assert fund.codes == ["PVBI11"]
    assert fund.codesOther is None
    assert fund.segment is None
