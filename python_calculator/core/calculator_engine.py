"""Tokenizer와 ExpressionParser를 연결하는 기본 계산 엔진."""

from core.expression_parser import ExpressionParser
from core.tokenizer import Tokenizer


class CalculatorEngine:
    """GUI와 무관하게 수식 문자열을 숫자 결과로 계산한다."""

    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def evaluate(self, expression: str) -> float:
        """문자열 수식을 토큰화하고 파싱해 실수 결과를 반환한다."""
        tokens = self._tokenizer.tokenize(expression)
        parser = ExpressionParser(tokens)
        return parser.parse()
