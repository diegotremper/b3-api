from datetime import date, datetime
from enum import IntEnum

from pydantic import BaseModel, validator


class ReportType(IntEnum):
    MONTHLY = 40
    INCOME = 41


class Report(BaseModel):
    type: ReportType
    name: str
    competence: date

    @validator("competence", pre=True)
    def competence_str(cls, v):
        if isinstance(v, str):
            # check if date contains one slash only
            if v.count("/") == 1:
                v = "1/" + v
            v = datetime.strptime(v, "%d/%m/%Y").date()
            return v.replace(day=1)

        return v


class MonthlyReport(Report):
    equityValuePerShare: float

    @validator("equityValuePerShare", pre=True)
    def equity_value_per_share_str(cls, v):
        if isinstance(v, str):
            return float(v.replace(".", "").replace(",", "."))
        return v


class IncomeReport(Report):
    dividend: float
    ticker: str

    @validator("dividend", pre=True)
    def dividend_str(cls, v):
        if isinstance(v, str):
            return float(v.replace(".", "").replace(",", "."))
        return v
