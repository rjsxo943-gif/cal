"""Token 목록을 재귀 하강 방식으로 해석해 실수 결과를 만든다."""

import math

from core.angle_converter import AngleConverter
from core.calculator_errors import (
    DivisionByZeroCalculatorError,
    InvalidInputError,
    MathCalculatorError,
    OverflowCalculatorError,
    SyntaxCalculatorError,
)
from core.calculator_state import AngleMode
from core.tokenizer import Token, TokenType


class ExpressionParser:
    """연산자 우선순위를 함수 계층으로 표현하는 재귀 하강 파서."""

    _CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
    }

    _FUNCTION_NAMES = {
        "sqrt",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "log",
        "ln",
    }

    def __init__(
        self,
        tokens: list[Token],
        angle_mode: AngleMode = AngleMode.DEG,
        answer: float = 0.0,
    ) -> None:
        if not tokens:
            raise SyntaxCalculatorError()

        self._tokens = tokens
        self._current_index = 0
        self._angle_mode = angle_mode
        self._answer = answer

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
        """거듭제곱을 오른쪽 결합으로 처리한다."""
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

        if isinstance(result, complex):
            raise MathCalculatorError()

        return float(result)

    def _parse_primary(self) -> float:
        """숫자, 괄호, 상수, Ans 또는 함수 호출을 처리한다."""
        token = self._current_token()

        if token.token_type is TokenType.NUMBER:
            self._advance()
            if not isinstance(token.value, float):
                raise SyntaxCalculatorError()
            return token.value

        if token.token_type is TokenType.LEFT_PAREN:
            self._advance()
            value = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN)
            return value

        if token.token_type is TokenType.IDENTIFIER:
            return self._parse_identifier()

        raise SyntaxCalculatorError()

    def _parse_identifier(self) -> float:
        """상수, Ans 또는 괄호 하나를 인자로 받는 공학 함수를 처리한다."""
        token = self._advance()

        if not isinstance(token.value, str):
            raise SyntaxCalculatorError()

        name = token.value.lower()

        # Ans는 CalculatorState에 저장된 가장 최근 성공 결과를 사용한다.
        if name == "ans":
            return self._answer

        if name in self._CONSTANTS:
            return self._CONSTANTS[name]

        if name not in self._FUNCTION_NAMES:
            raise InvalidInputError()

        # 함수는 sin(30), sqrt(16)처럼 괄호를 필수로 사용한다.
        self._consume(TokenType.LEFT_PAREN)
        argument = self._parse_expression()
        self._consume(TokenType.RIGHT_PAREN)

        return self._evaluate_function(name, argument)

    def _evaluate_function(self, name: str, argument: float) -> float:
        """함수명과 인자를 실제 math 계산으로 연결한다."""
        try:
            if name == "sqrt":
                if argument < 0.0:
                    raise MathCalculatorError()
                return math.sqrt(argument)

            if name == "sin":
                radians = AngleConverter.to_radians(argument, self._angle_mode)
                return math.sin(radians)

            if name == "cos":
                radians = AngleConverter.to_radians(argument, self._angle_mode)
                return math.cos(radians)

            if name == "tan":
                radians = AngleConverter.to_radians(argument, self._angle_mode)

                # 90°, pi/2 rad, 100 grad처럼 탄젠트가 정의되지 않는
                # 위치를 부동소수점 오차 범위 안에서 Math ERROR로 처리한다.
                if abs(math.cos(radians)) < 1e-12:
                    raise MathCalculatorError()

                return math.tan(radians)

            if name == "asin":
                if not -1.0 <= argument <= 1.0:
                    raise MathCalculatorError()
                radians = math.asin(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "acos":
                if not -1.0 <= argument <= 1.0:
                    raise MathCalculatorError()
                radians = math.acos(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "atan":
                radians = math.atan(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "log":
                if argument <= 0.0:
                    raise MathCalculatorError()
                return math.log10(argument)

            if name == "ln":
                if argument <= 0.0:
                    raise MathCalculatorError()
                return math.log(argument)

        except OverflowError as error:
            raise OverflowCalculatorError() from error
        except ValueError as error:
            raise MathCalculatorError() from error

        raise InvalidInputError()

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
