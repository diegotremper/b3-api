from datetime import timedelta
from typing import Optional

from pydantic import BaseModel

from b3_api.api_configs import APIConfigs
from b3_api.api_utils import _get_and_parse, encode_param


class Fund(BaseModel):
    acronym: str
    tradingName: str
    tradingCode: str
    tradingCodeOthers: str
    cnpj: str
    classification: str
    webSite: str
    fundAddress: str
    fundPhoneNumberDDD: str
    fundPhoneNumber: str
    fundPhoneNumberFax: str
    positionManager: str
    managerName: str
    companyAddress: str
    companyPhoneNumberDDD: str
    companyPhoneNumber: str
    companyPhoneNumberFax: str
    companyEmail: str
    companyName: str
    quotaCount: str
    quotaDateApproved: str
    typeFNET: Optional[str] = None
    codes: list[str]
    codesOther: Optional[str] = None
    segment: Optional[str] = None


class _Payload(BaseModel):
    detailFund: Fund


def fund_detail(symbol: str, configs: APIConfigs = APIConfigs()) -> Fund:
    """
    Get fund details from B3.

    Example:
        curl 'https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetDetailFundSIG/eyJ0eXBlRnVuZCI6NywiaWRlbnRpZmllckZ1bmQiOiJKQVNDIn0=' \
        -H 'Accept: application/json'
    """
    identifier = "".join([i for i in symbol if not i.isdigit()])
    params = encode_param(
        {"typeFund": 7, "identifierFund": identifier.upper()}
    )

    url = "{}/GetDetailFundSIG/{}".format(configs.fund_calls_base_url, params)

    from b3_api.api_utils import request_session

    session = request_session("fund_detail", timedelta(days=30))
    payload: _Payload = _get_and_parse(session, url, _Payload, configs)

    return payload.detailFund
