"""이차방정식 화면과 계산 로직 사이를 연결한다."""

from dataclasses import dataclass
import math

from core.calculator_errors import CalculatorError, InvalidInputError
from core.calculator_state import CalculatorState
from core.quadratic_equation_solver import (
    QuadraticEquationSolver,
    QuadraticRootType,
    QuadraticSolution,
)
from core.result_formatter import ResultFormatter


@dataclass(frozen=True)
class EquationDisplayResult:
    """EquationPage가 바로 표시할 수 있는 형태의 결과."""

    is_success: bool
    classification: str = ""
    discriminant_text: str = ""
    root_lines: tuple[str, ...] = ()
    error_message: str = ""


class EquationController:
    """계수 해석, 근 계산, 표시 형식 적용을 담당한다."""

    def __init__(
        self,
        state: CalculatorState,
        solver: QuadraticEquationSolver | None = None,
        formatter: ResultFormatter | None = None,
    ) -> None:
        self.state = state
        self._solver = solver or QuadraticEquationSolver()
        self._formatter = formatter or ResultFormatter()
        self._last_solution: QuadraticSolution | None = None

    def solve(
        self,
        a_text: str,
        b_text: str,
        c_text: str,
    ) -> EquationDisplayResult:
        """입력 문자열을 계수로 변환하고 이차방정식을 계산한다."""
        try:
            a = self._parse_coefficient(a_text)
            b = self._parse_coefficient(b_text)
            c = self._parse_coefficient(c_text)
            solution = self._solver.solve(a, b, c)
        except CalculatorError as error:
            return EquationDisplayResult(
                is_success=False,
                error_message=str(error),
            )

        self._last_solution = solution
        return self._format_solution(solution)

    def redisplay_last_solution(self) -> EquationDisplayResult | None:
        """FMT 변경 후 최근 방정식 결과를 새 표시 형식으로 다시 만든다."""
        if self._last_solution is None:
            return None
        return self._format_solution(self._last_solution)

    @staticmethod
    def _parse_coefficient(text: str) -> float:
        """비어 있지 않은 유한 실수 계수를 읽는다."""
        stripped = text.strip()
        if not stripped:
            raise InvalidInputError()

        try:
            value = float(stripped)
        except ValueError as error:
            raise InvalidInputError() from error

        if not math.isfinite(value):
            raise InvalidInputError()
        return value

    def _format_solution(
        self,
        solution: QuadraticSolution,
    ) -> EquationDisplayResult:
        """QuadraticSolution을 현재 NORM/FIX/SCI 형식에 맞춰 변환한다."""
        discriminant_text = (
            f"Δ = {self._format_real(solution.discriminant)}"
        )

        if solution.root_type is QuadraticRootType.REPEATED_REAL:
            root_lines = (
                f"x = {self._format_real(solution.root1.real)}",
            )
        elif solution.root_type is QuadraticRootType.TWO_REAL:
            root_lines = (
                f"x₁ = {self._format_real(solution.root1.real)}",
                f"x₂ = {self._format_real(solution.root2.real)}",
            )
        else:
            root_lines = (
                f"x₁ = {self._format_complex(solution.root1)}",
                f"x₂ = {self._format_complex(solution.root2)}",
            )

        return EquationDisplayResult(
            is_success=True,
            classification=solution.root_type.value,
            discriminant_text=discriminant_text,
            root_lines=root_lines,
        )

    def _format_real(self, value: float) -> str:
        """공유 표시 상태를 사용해 실수를 문자열로 만든다."""
        return self._formatter.format(
            value,
            display_mode=self.state.display_mode,
            display_digits=self.state.display_digits,
        )

    def _format_complex(self, value: complex) -> str:
        """복소근을 a ± bi 형태로 표시한다."""
        real_part = 0.0 if abs(value.real) < 1e-15 else value.real
        imaginary_part = 0.0 if abs(value.imag) < 1e-15 else value.imag

        if imaginary_part == 0.0:
            return self._format_real(real_part)

        imaginary_magnitude = abs(imaginary_part)
        if abs(imaginary_magnitude - 1.0) < 1e-15:
            imaginary_text = "i"
        else:
            imaginary_text = f"{self._format_real(imaginary_magnitude)}i"

        if real_part == 0.0:
            return imaginary_text if imaginary_part > 0.0 else f"-{imaginary_text}"

        sign = "+" if imaginary_part > 0.0 else "-"
        return (
            f"{self._format_real(real_part)} "
            f"{sign} {imaginary_text}"
        )
