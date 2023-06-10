import immutables
from pydantic import BaseModel, validator


class APIConfigs(BaseModel):
    http_cache_dir: str = "data/cache/b3/http_cache"
    http_user_agent: str = "Mozilla/5.0 (Free APIs Please) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    fund_calls_base_url: str = (
        "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall"
    )
    fnet_base_url: str = "https://fnet.bmfbovespa.com.br/fnet/publico"
    default_headers: immutables.Map = immutables.Map(
        {
            "User-Agent": http_user_agent,
            "Accept": "application/json",
        }
    )

    @validator("default_headers", pre=True)
    def default_headers_dict(cls, v):
        if isinstance(v, dict):
            return immutables.Map(v)
        raise ValueError("default_headers must be a dict")

    class Config:
        frozen = True
        arbitrary_types_allowed = True
