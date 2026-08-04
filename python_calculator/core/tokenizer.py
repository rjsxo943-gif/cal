"""수식 문자열을 파서가 이해할 수 있는 Token 목록으로 변환한다."""

from dataclasses import dataclass
from enum import Enum, auto

from core.calculator_errors import InvalidInputError, SyntaxCalculatorError


class TokenType(Enum):
    """기본 연산과 공학 함수에서 사용하는 토큰의 종류."""

    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    FACTORIAL = auto()
    COMMA = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    END = auto()


@dataclass(frozen=True)
class Token:
    """수식에서 분리한 하나의 의미 단위."""

    token_type: TokenType
    value: float | str | None = None
    position: int = 0


class Tokenizer:
    """문자열을 왼쪽부터 읽어 Token 목록을 생성한다."""

    _SINGLE_CHARACTER_TOKENS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLY,
        "×": TokenType.MULTIPLY,
        "/": TokenType.DIVIDE,
        "÷": TokenType.DIVIDE,
        "^": TokenType.POWER,
        "!": TokenType.FACTORIAL,
        ",": TokenType.COMMA,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
    }

    def tokenize(self, expression: str) -> list[Token]:
        """수식 문자열을 Token 목록으로 변환한다."""
        if not expression or expression.isspace():
            raise InvalidInputError()

        tokens: list[Token] = []
        index = 0

        while index < len(expression):
            character = expression[index]

            if character.isspace():
                index += 1
                continue

            if character.isdigit() or character == ".":
                token, index = self._read_number(expression, index)
                tokens.append(token)
                continue

            if character == "π":
                tokens.append(
                    Token(
                        token_type=TokenType.IDENTIFIER,
                        value="pi",
                        position=index,
                    )
                )
                index += 1
                continue

            if character.isalpha() or character == "_":
                token, index = self._read_identifier(expression, index)
                tokens.append(token)
                continue

            if character == "√":
                tokens.append(
                    Token(
                        token_type=TokenType.IDENTIFIER,
                        value="sqrt",
                        position=index,
                    )
                )
                index += 1
                continue

            token_type = self._SINGLE_CHARACTER_TOKENS.get(character)
            if token_type is None:
                raise InvalidInputError()

            tokens.append(Token(token_type=token_type, position=index))
            index += 1

        tokens.append(Token(token_type=TokenType.END, position=len(expression)))
        return tokens

    @staticmethod
    def _read_number(expression: str, start: int) -> tuple[Token, int]:
        """start 위치부터 정수, 소수 또는 지수 표기 숫자를 읽는다."""
        index = start
        decimal_point_count = 0
        digit_count = 0

        while index < len(expression):
            character = expression[index]

            if character.isdigit():
                digit_count += 1
                index += 1
                continue

            if character == ".":
                decimal_point_count += 1
                if decimal_point_count > 1:
                    raise SyntaxCalculatorError()
                index += 1
                continue

            break

        if digit_count == 0:
            raise SyntaxCalculatorError()

        # 1E3, 2.5e-4와 같은 과학적 표기법을 하나의 NUMBER로 읽는다.
        if index < len(expression) and expression[index] in ("e", "E"):
            index += 1

            if index < len(expression) and expression[index] in ("+", "-"):
                index += 1

            exponent_start = index
            while index < len(expression) and expression[index].isdigit():
                index += 1

            if exponent_start == index:
                # 2e처럼 지수 숫자가 없는 입력은 완전한 숫자가 아니다.
                raise SyntaxCalculatorError()

        number_text = expression[start:index]

        try:
            value = float(number_text)
        except ValueError as error:
            raise SyntaxCalculatorError() from error

        return (
            Token(
                token_type=TokenType.NUMBER,
                value=value,
                position=start,
            ),
            index,
        )

    @staticmethod
    def _read_identifier(expression: str, start: int) -> tuple[Token, int]:
        """함수명이나 상수명을 하나의 IDENTIFIER 토큰으로 읽는다."""
        index = start

        while index < len(expression):
            character = expression[index]
            if not (character.isalpha() or character == "_"):
                break
            index += 1

        identifier = expression[start:index].lower()

        return (
            Token(
                token_type=TokenType.IDENTIFIER,
                value=identifier,
                position=start,
            ),
            index,
        )
