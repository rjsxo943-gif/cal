"""Token 목록을 재귀 하강 방식으로 해석해 실수 결과를 만든다."""

import math
import random
import sys

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
        "abs",
        "recip",
        "npr",
        "ncr",
        "mod",
        "gcd",
        "lcm",
        "quot",
        "rem",
        "root",
        "random",
        "randint",
    }

    def __init__(
        self,
        tokens: list[Token],
        angle_mode: AngleMode = AngleMode.DEG,
        answer: float = 0.0,
        random_generator: random.Random | None = None,
    ) -> None:
        if not tokens:
            raise SyntaxCalculatorError()

        self._tokens = tokens
        self._current_index = 0
        self._angle_mode = angle_mode
        self._answer = answer

        # 난수 생성기를 외부에서 주입할 수 있게 해두면 테스트에서는
        # 고정된 seed를 사용하고 실제 프로그램에서는 일반 난수를 사용한다.
        self._random_generator = (
            random_generator if random_generator is not None else random.Random()
        )

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
        base = self._parse_postfix()

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

    def _parse_postfix(self) -> float:
        """값 뒤에 붙는 팩토리얼과 백분율 연산자를 처리한다."""
        value = self._parse_primary()

        while self._current_token().token_type in (
            TokenType.FACTORIAL,
            TokenType.PERCENT,
        ):
            operator = self._advance().token_type

            if operator is TokenType.FACTORIAL:
                value = self._factorial(value)
            else:
                # 50%는 50 / 100, 즉 0.5로 해석한다.
                value /= 100.0

        return value

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
        """상수, Ans 또는 괄호 인자를 받는 함수를 처리한다."""
        token = self._advance()

        if not isinstance(token.value, str):
            raise SyntaxCalculatorError()

        name = token.value.lower()

        if name == "ans":
            return self._answer

        if name in self._CONSTANTS:
            return self._CONSTANTS[name]

        if name not in self._FUNCTION_NAMES:
            raise InvalidInputError()

        self._consume(TokenType.LEFT_PAREN)
        arguments = self._parse_function_arguments()
        self._consume(TokenType.RIGHT_PAREN)

        return self._evaluate_function(name, arguments)

    def _parse_function_arguments(self) -> list[float]:
        """쉼표로 구분된 함수 인자 목록을 읽는다."""
        arguments: list[float] = []

        if self._current_token().token_type is TokenType.RIGHT_PAREN:
            return arguments

        arguments.append(self._parse_expression())

        while self._current_token().token_type is TokenType.COMMA:
            self._advance()
            arguments.append(self._parse_expression())

        return arguments

    def _evaluate_function(self, name: str, arguments: list[float]) -> float:
        """함수명과 인자 목록을 실제 계산으로 연결한다."""
        try:
            if name == "random":
                self._zero_arguments(arguments)
                return self._random_generator.random()

            if name == "randint":
                first_value, second_value = self._two_arguments(arguments)
                first = self._integer(first_value)
                second = self._integer(second_value)

                if first > second:
                    raise MathCalculatorError()

                return float(self._random_generator.randint(first, second))

            if name == "sqrt":
                argument = self._one_argument(arguments)
                if argument < 0.0:
                    raise MathCalculatorError()
                return math.sqrt(argument)

            if name == "sin":
                argument = self._one_argument(arguments)
                radians = AngleConverter.to_radians(argument, self._angle_mode)
                return math.sin(radians)

            if name == "cos":
                argument = self._one_argument(arguments)
                radians = AngleConverter.to_radians(argument, self._angle_mode)
                return math.cos(radians)

            if name == "tan":
                argument = self._one_argument(arguments)
                radians = AngleConverter.to_radians(argument, self._angle_mode)

                if abs(math.cos(radians)) < 1e-12:
                    raise MathCalculatorError()

                return math.tan(radians)

            if name == "asin":
                argument = self._one_argument(arguments)
                if not -1.0 <= argument <= 1.0:
                    raise MathCalculatorError()
                radians = math.asin(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "acos":
                argument = self._one_argument(arguments)
                if not -1.0 <= argument <= 1.0:
                    raise MathCalculatorError()
                radians = math.acos(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "atan":
                argument = self._one_argument(arguments)
                radians = math.atan(argument)
                return AngleConverter.from_radians(radians, self._angle_mode)

            if name == "log":
                argument = self._one_argument(arguments)
                if argument <= 0.0:
                    raise MathCalculatorError()
                return math.log10(argument)

            if name == "ln":
                argument = self._one_argument(arguments)
                if argument <= 0.0:
                    raise MathCalculatorError()
                return math.log(argument)

            if name == "abs":
                return abs(self._one_argument(arguments))

            if name == "recip":
                argument = self._one_argument(arguments)
                if argument == 0.0:
                    raise DivisionByZeroCalculatorError()
                return 1.0 / argument

            if name == "npr":
                n_value, r_value = self._two_arguments(arguments)
                n = self._nonnegative_integer(n_value)
                r = self._nonnegative_integer(r_value)
                if r > n:
                    raise MathCalculatorError()
                self._ensure_permutation_fits_float(n, r)
                return self._integer_result_to_float(math.perm(n, r))

            if name == "ncr":
                n_value, r_value = self._two_arguments(arguments)
                n = self._nonnegative_integer(n_value)
                r = self._nonnegative_integer(r_value)
                if r > n:
                    raise MathCalculatorError()
                self._ensure_combination_fits_float(n, r)
                return self._integer_result_to_float(math.comb(n, r))

            if name in ("mod", "rem"):
                dividend, divisor = self._two_arguments(arguments)
                if divisor == 0.0:
                    raise DivisionByZeroCalculatorError()
                return math.fmod(dividend, divisor)

            if name == "quot":
                dividend, divisor = self._two_arguments(arguments)
                if divisor == 0.0:
                    raise DivisionByZeroCalculatorError()

                # Python의 //는 음수에서 아래쪽 정수로 내림한다.
                # C++ 정수 나눗셈과 맞추기 위해 0 방향으로 절삭한다.
                return float(math.trunc(dividend / divisor))

            if name == "root":
                degree_value, radicand = self._two_arguments(arguments)
                degree = self._nonnegative_integer(degree_value)

                if degree == 0:
                    raise MathCalculatorError()

                if radicand < 0.0:
                    if degree % 2 == 0:
                        raise MathCalculatorError()
                    return -((-radicand) ** (1.0 / degree))

                return radicand ** (1.0 / degree)

            if name == "gcd":
                first_value, second_value = self._two_arguments(arguments)
                first = self._integer(first_value)
                second = self._integer(second_value)
                return self._integer_result_to_float(math.gcd(first, second))

            if name == "lcm":
                first_value, second_value = self._two_arguments(arguments)
                first = self._integer(first_value)
                second = self._integer(second_value)
                return self._integer_result_to_float(math.lcm(first, second))

        except OverflowError as error:
            raise OverflowCalculatorError() from error
        except ValueError as error:
            raise MathCalculatorError() from error

        raise InvalidInputError()

    def _factorial(self, value: float) -> float:
        """0 이상의 정수에 팩토리얼을 적용한다."""
        integer_value = self._nonnegative_integer(value)

        if integer_value > 170:
            raise OverflowCalculatorError()

        return float(math.factorial(integer_value))

    @staticmethod
    def _zero_arguments(arguments: list[float]) -> None:
        """인자가 없어야 하는 함수인지 확인한다."""
        if arguments:
            raise SyntaxCalculatorError()

    @staticmethod
    def _one_argument(arguments: list[float]) -> float:
        """인자가 정확히 하나인지 확인한다."""
        if len(arguments) != 1:
            raise SyntaxCalculatorError()
        return arguments[0]

    @staticmethod
    def _two_arguments(arguments: list[float]) -> tuple[float, float]:
        """인자가 정확히 두 개인지 확인한다."""
        if len(arguments) != 2:
            raise SyntaxCalculatorError()
        return arguments[0], arguments[1]

    @staticmethod
    def _integer(value: float) -> int:
        """실수 값이 정확한 정수인지 확인하고 int로 변환한다."""
        if not math.isfinite(value) or not value.is_integer():
            raise MathCalculatorError()
        return int(value)

    def _nonnegative_integer(self, value: float) -> int:
        """0 이상의 정수인지 확인한다."""
        integer_value = self._integer(value)
        if integer_value < 0:
            raise MathCalculatorError()
        return integer_value

    @staticmethod
    def _ensure_permutation_fits_float(n: int, r: int) -> None:
        """nPr 결과가 double 범위를 넘는지 계산 전에 확인한다."""
        if r == 0:
            return

        logarithm = math.lgamma(n + 1) - math.lgamma(n - r + 1)
        if logarithm > math.log(sys.float_info.max):
            raise OverflowCalculatorError()

    @staticmethod
    def _ensure_combination_fits_float(n: int, r: int) -> None:
        """nCr 결과가 double 범위를 넘는지 계산 전에 확인한다."""
        if r == 0 or r == n:
            return

        logarithm = (
            math.lgamma(n + 1)
            - math.lgamma(r + 1)
            - math.lgamma(n - r + 1)
        )
        if logarithm > math.log(sys.float_info.max):
            raise OverflowCalculatorError()

    @staticmethod
    def _integer_result_to_float(value: int) -> float:
        """큰 정수 결과를 공통 실수 표현으로 안전하게 변환한다."""
        try:
            result = float(value)
        except OverflowError as error:
            raise OverflowCalculatorError() from error

        if not math.isfinite(result):
            raise OverflowCalculatorError()

        return result

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
