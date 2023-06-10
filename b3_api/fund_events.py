from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator

from b3_api.api_configs import APIConfigs
from b3_api.api_utils import encode_param


class StockEvent(BaseModel):
    assetIssued: str
    factor: float
    approvedOn: Optional[date]
    isinCode: str
    label: str
    lastDatePrior: Optional[date]
    remarks: str

    @validator("factor", pre=True)
    def factor_str(cls, v):
        if isinstance(v, str):
            return float(v.replace(",", "."))
        return v

    @validator("approvedOn", "lastDatePrior", pre=True)
    def approved_on_str(cls, v):
        if v and isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y").date()
        return None


class _Payload(BaseModel):
    stockDividends: list[StockEvent]


def fund_events(
    symbol: str, cnpj: str, configs: APIConfigs = APIConfigs()
) -> list[StockEvent]:
    """
    Get a list of stock events for a fund from B3

    curl 'https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedSupplementFunds/eyJjbnBqIjoiMTY3MDY5NTgwMDAxMzIiLCJpZGVudGlmaWVyRnVuZCI6IktOQ1IiLCJ0eXBlRnVuZCI6N30=' \
      -H 'Accept: application/json'
    """
    identifier = "".join([i for i in symbol if not i.isdigit()])
    params = encode_param(
        {"typeFund": 7, "identifierFund": identifier.upper(), "cnpj": cnpj}
    )

    url = "{}/GetListedSupplementFunds/{}".format(
        configs.fund_calls_base_url, params
    )

    from b3_api.api_utils import request_session

    session = request_session("fund_events", timedelta(days=10))
    response = session.get(url, headers=configs.default_headers)

    if response.status_code != 200:
        raise Exception("Error getting fund details for {}".format(symbol))

    try:
        payload = _Payload.parse_raw(response.json())
    except Exception as e:
        if session.cache:
            session.cache.delete(urls=[url])
        raise Exception(
            "Error parsing stock events for {}:\n{}".format(
                symbol, response.text
            )
        ) from e

    payload.stockDividends.sort(key=lambda e: e.lastDatePrior, reverse=True)

    return payload.stockDividends
