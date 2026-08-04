"""이차방정식 ax² + bx + c = 0의 근을 계산한다."""

from dataclasses import dataclass
from enum import Enum
import math

from core.calculator_errors import (
    InvalidInputError,
    MathCalculatorError,
    OverflowCalculatorError,
)


class QuadraticRootType(str, Enum):
    """이차방정식 근의 분류."""

    TWO_REAL = "Two real roots"
    REPEATED_REAL = "Repeated real root"
    TWO_COMPLEX = "Two complex roots"


@dataclass(frozen=True)
class QuadraticSolution:
    """판별식과 두 근을 함께 보관하는 계산 결과."""

    root_type: QuadraticRootType
    discriminant: float
    root1: complex
    root2: complex


class QuadraticEquationSolver:
    """실수 계수를 갖는 이차방정식을 안정적으로 계산한다."""

    DISCRIMINANT_TOLERANCE = 1e-12

    def solve(self, a: float, b: float, c: float) -> QuadraticSolution:
        """계수 a, b, c를 받아 두 근과 근의 종류를 반환한다."""
        if not all(math.isfinite(value) for value in (a, b, c)):
            raise InvalidInputError()

        if a == 0.0:
            raise MathCalculatorError("Coefficient a must not be zero")

        discriminant = b * b - 4.0 * a * c
        if not math.isfinite(discriminant):
            raise OverflowCalculatorError()

        # 거의 0인 판별식은 부동소수점 오차로 양수·음수가 되지 않도록
        # 계수 크기를 고려한 허용 오차 안에서 정확한 0으로 정규화한다.
        comparison_scale = max(abs(b * b), abs(4.0 * a * c), 1.0)
        if abs(discriminant) <= self.DISCRIMINANT_TOLERANCE * comparison_scale:
            discriminant = 0.0

        if discriminant > 0.0:
            return self._solve_two_real(a, b, c, discriminant)

        if discriminant == 0.0:
            root = -b / (2.0 * a)
            self._ensure_finite(root)
            complex_root = complex(root, 0.0)
            return QuadraticSolution(
                root_type=QuadraticRootType.REPEATED_REAL,
                discriminant=0.0,
                root1=complex_root,
                root2=complex_root,
            )

        real_part = -b / (2.0 * a)
        imaginary_part = math.sqrt(-discriminant) / (2.0 * abs(a))
        self._ensure_finite(real_part)
        self._ensure_finite(imaginary_part)

        return QuadraticSolution(
            root_type=QuadraticRootType.TWO_COMPLEX,
            discriminant=discriminant,
            root1=complex(real_part, imaginary_part),
            root2=complex(real_part, -imaginary_part),
        )

    def _solve_two_real(
        self,
        a: float,
        b: float,
        c: float,
        discriminant: float,
    ) -> QuadraticSolution:
        """서로 다른 두 실근을 상쇄 오차가 적은 공식으로 계산한다."""
        square_root = math.sqrt(discriminant)

        # 일반 근의 공식은 b와 sqrt(Δ)가 비슷할 때 유효 숫자를 잃을 수 있다.
        # q를 먼저 계산한 뒤 두 번째 근을 c/q로 구하면 그 오차를 줄일 수 있다.
        q = -0.5 * (b + math.copysign(square_root, b))

        if q == 0.0:
            root1 = -b / (2.0 * a)
            root2 = root1
        else:
            root1 = q / a
            root2 = c / q

        self._ensure_finite(root1)
        self._ensure_finite(root2)

        return QuadraticSolution(
            root_type=QuadraticRootType.TWO_REAL,
            discriminant=discriminant,
            root1=complex(root1, 0.0),
            root2=complex(root2, 0.0),
        )

    @staticmethod
    def _ensure_finite(value: float) -> None:
        """근 계산 결과가 공통 double 범위 안인지 확인한다."""
        if not math.isfinite(value):
            raise OverflowCalculatorError()
