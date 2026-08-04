"""Token 목록을 재귀 하강 방식으로 해석해 실수 결과를 만든다."""

import math

from core.calculator_errors import (
    DivisionByZeroCalculatorError,
    MathCalculatorError,
    OverflowCalculatorError,
    SyntaxCalculatorError,
)
from core.tokenizer import Token, TokenType


class ExpressionParser:
    """연산자 우선순위를 함수 계층으로 표현하는 재귀 하강 파서."""

    def __init__(self, tokens: list[Token]) -> None:
        if not tokens:
            raise SyntaxCalculatorError()

        self._tokens = tokens
        self._current_index = 0

    def parse(self) -> float:
        """전체 수식을 계산하고 남은 토큰이 없는지 확인한다."""
        result = self._parse_expression()

        if self._current_token().token_type is not TokenType.END:
            raise SyntaxCalculatorError()

        if not math.isfinite(result):
            raise OverflowCalculatorError()

        return result

    def _parse_expression(self) -> float:
        """덧셈과 뺄셈을 처리한다."""
        value = self._parse_term()

        while self._current_token().token_type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self._advance().token_type
            right_value = self._parse_term()

            if operator is TokenType.PLUS:
                value += right_value
            else:
                value -= right_value

        return value

    def _parse_term(self) -> float:
        """곱셈과 나눗셈을 처리한다."""
        value = self._parse_unary()

        while self._current_token().token_type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            operator = self._advance().token_type
            right_value = self._parse_unary()

            if operator is TokenType.MULTIPLY:
                value *= right_value
                continue

            if right_value == 0.0:
                raise DivisionByZeroCalculatorError()

            value /= right_value

        return value

    def _parse_unary(self) -> float:
        """숫자 앞에 붙는 단항 +와 단항 -를 처리한다."""
        token_type = self._current_token().token_type

        if token_type is TokenType.PLUS:
            self._advance()
            return self._parse_unary()

        if token_type is TokenType.MINUS:
            self._advance()
            return -self._parse_unary()

        return self._parse_power()

    def _parse_power(self) -> float:
        """
        거듭제곱을 오른쪽 결합으로 처리한다.

        오른쪽 피연산자를 _parse_unary()로 읽기 때문에
        2^-2와 2^3^2를 모두 자연스럽게 처리할 수 있다.
        """
        base = self._parse_primary()

        if self._current_token().token_type is not TokenType.POWER:
            return base

        self._advance()
        exponent = self._parse_unary()

        try:
            result = base**exponent
        except ZeroDivisionError as error:
            raise DivisionByZeroCalculatorError() from error
        except OverflowError as error:
            raise OverflowCalculatorError() from error

        # 일반 계산 모드에서는 복소수 결과를 허용하지 않는다.
        if isinstance(result, complex):
            raise MathCalculatorError()

        return float(result)

    def _parse_primary(self) -> float:
        """숫자 또는 괄호로 묶인 하위 수식을 처리한다."""
        token = self._current_token()

        if token.token_type is TokenType.NUMBER:
            self._advance()
            if token.value is None:
                raise SyntaxCalculatorError()
            return token.value

        if token.token_type is TokenType.LEFT_PAREN:
            self._advance()
            value = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN)
            return value

        raise SyntaxCalculatorError()

    def _current_token(self) -> Token:
        """현재 파서가 바라보는 토큰을 반환한다."""
        if self._current_index >= len(self._tokens):
            raise SyntaxCalculatorError()

        return self._tokens[self._current_index]

    def _advance(self) -> Token:
        """현재 토큰을 반환한 뒤 다음 토큰으로 이동한다."""
        token = self._current_token()
        self._current_index += 1
        return token

    def _consume(self, expected_type: TokenType) -> Token:
        """예상한 종류의 토큰이 있으면 소비하고, 아니면 오류를 낸다."""
        token = self._current_token()

        if token.token_type is not expected_type:
            raise SyntaxCalculatorError()

        self._current_index += 1
        return token
