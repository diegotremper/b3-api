import base64
import functools
import json

from requests_cache import NEVER_EXPIRE, CachedSession

from b3_api.api_configs import APIConfigs


@functools.cache
def request_session(
    name, expire_after=NEVER_EXPIRE, configs=APIConfigs()
) -> CachedSession:
    """
    Create a persistent session with requests_cache.
    Used to not overload B3 servers until they decide to block us.
    """
    return CachedSession(
        "{}/{}.sqlite".format(configs.http_cache_dir, name),
        expire_after=expire_after,
    )


def encode_param(params: dict) -> str:
    """
    Encode a dict as json-encoded-base64 string.
    A lovely pattern for API parameters by the way 🤌.
    Congratulations to the B3 API team. 👏
    """
    json_string = json.dumps(params).encode("utf-8")
    return base64.b64encode(json_string).decode("utf-8")
