"""1변수 데이터의 요약 통계량을 계산한다."""

from dataclasses import dataclass
import math

from core.calculator_errors import InvalidInputError, OverflowCalculatorError


@dataclass(frozen=True)
class StatisticsSummary:
    """1변수 통계 결과를 계산 로직과 화면에서 공통으로 사용하는 값 객체."""

    count: int
    total: float
    mean: float | None
    minimum: float | None
    maximum: float | None
    population_variance: float | None
    population_standard_deviation: float | None
    sample_variance: float | None
    sample_standard_deviation: float | None


class OneVariableStatisticsCalculator:
    """유한 실수 데이터의 기본 1변수 통계량을 계산한다."""

    def summarize(self, values: list[float] | tuple[float, ...]) -> StatisticsSummary:
        """개수, 합계, 평균, 범위, 모집단·표본 분산과 표준편차를 반환한다."""
        data = tuple(values)

        if any(not math.isfinite(value) for value in data):
            raise InvalidInputError()

        count = len(data)
        if count == 0:
            return StatisticsSummary(
                count=0,
                total=0.0,
                mean=None,
                minimum=None,
                maximum=None,
                population_variance=None,
                population_standard_deviation=None,
                sample_variance=None,
                sample_standard_deviation=None,
            )

        try:
            total = math.fsum(data)
            mean = total / count
            squared_deviation_sum = math.fsum(
                (value - mean) ** 2 for value in data
            )
        except OverflowError as error:
            raise OverflowCalculatorError() from error

        calculated_values = (total, mean, squared_deviation_sum)
        if any(not math.isfinite(value) for value in calculated_values):
            raise OverflowCalculatorError()

        population_variance = squared_deviation_sum / count
        population_standard_deviation = math.sqrt(population_variance)

        sample_variance: float | None = None
        sample_standard_deviation: float | None = None

        if count >= 2:
            sample_variance = squared_deviation_sum / (count - 1)
            sample_standard_deviation = math.sqrt(sample_variance)

        return StatisticsSummary(
            count=count,
            total=total,
            mean=mean,
            minimum=min(data),
            maximum=max(data),
            population_variance=population_variance,
            population_standard_deviation=population_standard_deviation,
            sample_variance=sample_variance,
            sample_standard_deviation=sample_standard_deviation,
        )
