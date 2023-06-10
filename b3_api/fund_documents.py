from datetime import date, datetime, timedelta
from enum import IntEnum
from typing import Optional
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, parse_raw_as, validator

from b3_api.api_configs import APIConfigs
from b3_api.api_utils import encode_param


class DocumentType(IntEnum):
    monthly_report = 40
    income_report = 41


class Document(BaseModel):
    id: Optional[str]
    referenceDateFormat: str
    referenceDate: date
    urlFundosNet: str
    typeDocument: DocumentType
    documentSituation: str
    deliveryTypeCode: str
    version: int

    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self.id = parse_qs(urlparse(self.urlFundosNet).query)["id"][0]

    @validator("referenceDate", pre=True)
    def reference_date_str(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v.split("T")[0], "%Y-%m-%d").date()
        return v

    @validator("typeDocument", pre=True)
    def type_document_str(cls, v):
        if isinstance(v, dict) and "id" in v:
            if v["id"] == 40:
                return DocumentType.monthly_report
            elif v["id"] == 41:
                return DocumentType.income_report
            else:
                raise ValueError("typeDocument id must be 40 or 41")

        raise ValueError("typeDocument must be a dict")

    @validator("version", pre=True)
    def version_str(cls, v):
        if isinstance(v, str):
            return int(v)
        return v


def fund_documents(
    cnpj: str, document_type=40, year=2023, configs: APIConfigs = APIConfigs()
) -> list[Document]:
    """
    Get fund documents from B3

    curl 'https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/GetListedDocumentsTypeHistory/eyJjbnBqIjoiNDA4ODYyNDEwMDAxMDIiLCJkYXRlSW5pdGlhbCI6IjIwMjMtMDEtMDEiLCJkYXRlRmluYWwiOiIyMDIzLTEyLTMxIiwidHlwZSI6IjQwIn0=' \
      -H 'Accept: application/json'

    Parameters
    ----------
    cnpj: CNPJ of the fund
    document_type:
        40: Informe Mensal
        41: Rendimentos e Amortizações
    """
    params = {
        "cnpj": cnpj,
        "dateInitial": datetime(year, 1, 1).strftime("%Y-%m-%d"),
        "dateFinal": datetime(year, 12, 31).strftime("%Y-%m-%d"),
        "type": document_type,
    }

    params = encode_param(params)
    url = "{}/GetListedDocumentsTypeHistory/{}".format(
        configs.fund_calls_base_url, params
    )

    from b3_api.api_utils import request_session

    session = request_session("fund_documents", timedelta(days=1))
    response = session.get(url, headers=configs.default_headers)

    if response.status_code != 200:
        raise Exception("Error getting fund documents for {}".format(cnpj))

    all_docs = parse_raw_as(list[Document], response.text)
    # filter out inactive documents
    all_docs = [
        doc
        for doc in all_docs
        if doc.documentSituation != "(Inativo)"
        and doc.documentSituation != "(Cancelado)"
    ]
    # sorted by referenceDate and version
    all_docs.sort(key=lambda x: (x.referenceDate, x.version))
    # eliminate duplicated referenceDate and keep only the latest version
    all_docs = {doc.referenceDate: doc for doc in all_docs}.values()
    # globally sorted by referenceDate
    all_docs = sorted(all_docs, key=lambda doc: doc.referenceDate)

    return all_docs
