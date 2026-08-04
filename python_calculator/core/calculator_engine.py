"""Tokenizer와 ExpressionParser를 연결하는 계산 엔진."""

import random

from core.calculator_state import CalculatorState
from core.expression_parser import ExpressionParser
from core.tokenizer import Tokenizer


class CalculatorEngine:
    """GUI와 무관하게 수식 문자열을 숫자 결과로 계산한다."""

    def __init__(
        self,
        state: CalculatorState | None = None,
        random_generator: random.Random | None = None,
    ) -> None:
        self._tokenizer = Tokenizer()
        self._state = state or CalculatorState()

        # 하나의 Engine이 같은 난수 생성기를 계속 사용한다.
        # 테스트에서는 seed가 고정된 random.Random을 주입할 수 있다.
        self._random_generator = (
            random_generator if random_generator is not None else random.Random()
        )

    def evaluate(self, expression: str) -> float:
        """문자열 수식을 현재 계산기 상태에 따라 계산한다."""
        tokens = self._tokenizer.tokenize(expression)
        parser = ExpressionParser(
            tokens,
            angle_mode=self._state.angle_mode,
            answer=self._state.answer,
            random_generator=self._random_generator,
        )
        return parser.parse()
