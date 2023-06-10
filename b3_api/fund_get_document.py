from loguru import logger

from b3_api.api_configs import APIConfigs
from b3_api.parsers.income_report_parser import income_report_parser
from b3_api.parsers.models import Report, ReportType
from b3_api.parsers.monthly_report_parser import monthly_report_parser


def fund_get_document(
    id, type=40, configs: APIConfigs = APIConfigs()
) -> Report:
    """
    Get fund document from B3
    """
    url = "{}/exibirDocumento?id={}".format(configs.fnet_base_url, id)
    logger.debug("Getting document from {}", url)

    from b3_api.api_utils import request_session

    session = request_session("fund_get_document")

    response = session.get(
        url,
        headers={
            "User-Agent": configs.http_user_agent,
            "Accept": "text/html,application/xhtml+xml",
        },
    )

    if response.status_code != 200:
        raise Exception(
            "Error getting fund document for {}, body=[{}]".format(
                url, response.text
            )
        )

    html = response.text

    with logger.contextualize(url=url, id=id, type=type):
        if type == ReportType.MONTHLY:
            return monthly_report_parser(html)
        elif type == ReportType.INCOME:
            return income_report_parser(html)
        else:
            raise Exception("Unknown doc type {}".format(type))
