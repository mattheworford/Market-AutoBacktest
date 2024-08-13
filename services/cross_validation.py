from typing import List, Optional
from models import QuandlData, TiingoData, AlphaVantageData


class CrossValidator:
    def __init__(
        self,
        quandl_data: List[QuandlData],
        tiingo_data: List[TiingoData],
        alpha_vantage_data: List[AlphaVantageData],
    ):
        self.quandl_data = quandl_data
        self.tiingo_data = tiingo_data
        self.alpha_vantage_data = alpha_vantage_data

    def _compare_values(
        self, date: str, label: str, q_value: float, t_value: float, a_value: float
    ) -> List[str]:
        mismatches = []
        if q_value != t_value or q_value != a_value:
            mismatches.append(
                f"{label} mismatch on {date}: Quandl {q_value}, Tiingo {t_value}, AlphaVantage {a_value}"
            )
        return mismatches

    def _compare_record(
        self, q: QuandlData, t: TiingoData, a: AlphaVantageData
    ) -> List[str]:
        mismatches = []
        mismatches.extend(
            self._compare_values(q.date, "Open price", q.open, t.open, a.open)
        )
        mismatches.extend(
            self._compare_values(q.date, "High price", q.high, t.high, a.high)
        )
        mismatches.extend(
            self._compare_values(q.date, "Low price", q.low, t.low, a.low)
        )
        mismatches.extend(
            self._compare_values(q.date, "Close price", q.close, t.close, a.close)
        )
        mismatches.extend(
            self._compare_values(q.date, "Volume", q.volume, t.volume, a.volume)
        )
        return mismatches

    def compare_financial_metrics(self) -> List[str]:
        mismatches = []
        for q, t, a in zip(self.quandl_data, self.tiingo_data, self.alpha_vantage_data):
            if q.date == t.date == a.date:
                mismatches.extend(self._compare_record(q, t, a))
            else:
                mismatches.append(
                    f"Date mismatch: Quandl {q.date}, Tiingo {t.date}, AlphaVantage {a.date}"
                )
        return mismatches

    def compare_all(self) -> dict:
        return {
            "financial_metric_mismatches": self.compare_financial_metrics(),
        }
