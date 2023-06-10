from requests_cache import DO_NOT_CACHE

from b3_api.api_configs import APIConfigs


def historical_series_download(
    configs: APIConfigs = APIConfigs(), **kwargs
) -> bytes:
    r"""
    Download historical series from B3.

    Parameters
    ----------
    :param configs: (optional) APIConfigs object
    :param kwargs: Optional arguments that ``request`` takes.

    configs : optional, APIConfigs()
    **kwargs : optional
        year : int
            Year of the historical series.
        month : int
            Month of the historical series.
        day : int
            Day of the historical series.

    Returns
    -------
    The historical series file content.

    Examples
    --------
    >>> from b3_api.historical_series_download import historical_series_download
    >>> content = historical_series_download(year=2010)
    >>> content = historical_series_download(year=2010, month=1)
    >>> content = historical_series_download(year=2010, month=1, day=2)
    """
    file_name = None
    if "year" in kwargs:
        file_name = "COTAHIST_A{year}.ZIP".format(**kwargs)
    if "month" in kwargs:
        file_name = "COTAHIST_M{month:02d}{year}.ZIP".format(**kwargs)
    if "day" in kwargs:
        file_name = "COTAHIST_D{day:02d}{month:02d}{year}.ZIP".format(**kwargs)

    url = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/{}".format(
        file_name
    )

    from b3_api.api_utils import request_session

    session = request_session("historical_series_download", DO_NOT_CACHE)
    response = session.get(
        url, headers={"User-Agent": configs.http_user_agent}
    )

    if response.status_code != 200:
        raise Exception(
            "Error downloading file {}, code: {}".format(
                file_name, response.status_code
            )
        )

    return response.content
