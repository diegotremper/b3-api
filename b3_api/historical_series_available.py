from datetime import timedelta
from enum import IntEnum

from bs4 import BeautifulSoup
from pydantic import BaseModel

from b3_api.api_configs import APIConfigs


class SerieType(IntEnum):
    ANNUAL = 1
    MONTHLY = 2
    DAILY = 3


class DataSeries(BaseModel):
    name: str
    type: SerieType
    file_name: str


class AvailableSeries(BaseModel):
    annual_series: list[DataSeries] = []
    monthly_series: list[DataSeries] = []
    daily_series: list[DataSeries] = []


def historical_series_available(
    configs: APIConfigs = APIConfigs(),
) -> AvailableSeries:
    """
    Retrieves the available historical series from the B3 (Brazilian Stock Exchange) website.

    Args:
        configs (APIConfigs, optional): Configuration options for the API. Defaults to APIConfigs().

    Returns:
        AvailableSeries: An object containing the available historical series.

    Raises:
        Exception: If the response status code is unexpected or the resource is not found.

    """
    from b3_api.api_utils import request_session

    session = request_session("historical_series_available", timedelta(days=1))

    url = "https://bvmf.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricasArq.asp"
    response = session.get(
        url, headers={"User-Agent": configs.http_user_agent}
    )

    if response.status_code != 200:
        raise Exception(
            "Unexpected response code: url: {}, code: {}".format(
                url, response.status_code
            )
        )

    soup = BeautifulSoup(response.content, "html5lib")
    form = soup.find("form")

    annual_select = form.find("select", attrs={"name": "cboAno"})
    annual_series = [
        DataSeries(
            name=option.text, type=SerieType.ANNUAL, file_name=option["value"]
        )
        for option in annual_select.find_all("option")
        if "value" in option.attrs and option["value"] != ""
    ]

    monthly_select = form.find("select", attrs={"name": "cboMes"})
    monthly_series = [
        DataSeries(
            name=option.text, type=SerieType.MONTHLY, file_name=option["value"]
        )
        for option in monthly_select.find_all("option")
        if "value" in option.attrs and option["value"] != ""
    ]

    daily_daily_data = form.find("input", attrs={"name": "hdnDados"})
    daily_series = [
        DataSeries(
            name=f'{file_metadata.split("|")[1]}/{file_metadata.split("|")[0]}/{file_metadata.split("|")[2][-8:-4]}',
            type=SerieType.DAILY,
            file_name=file_metadata.split("|")[2],
        )
        for file_metadata in daily_daily_data["value"].split("_|_")
        if file_metadata != ""
    ]

    return AvailableSeries(
        annual_series=annual_series,
        monthly_series=monthly_series,
        daily_series=daily_series,
    )
