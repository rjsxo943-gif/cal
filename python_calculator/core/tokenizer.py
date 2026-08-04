"""수식 문자열을 파서가 이해할 수 있는 Token 목록으로 변환한다."""

from dataclasses import dataclass
from enum import Enum, auto

from core.calculator_errors import InvalidInputError, SyntaxCalculatorError


class TokenType(Enum):
    """Phase 2 기본 수식에서 사용하는 토큰의 종류."""

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    END = auto()


@dataclass(frozen=True)
class Token:
    """수식에서 분리한 하나의 의미 단위."""

    token_type: TokenType
    value: float | None = None
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

            # 공백은 계산 의미가 없으므로 건너뛴다.
            if character.isspace():
                index += 1
                continue

            if character.isdigit() or character == ".":
                token, index = self._read_number(expression, index)
                tokens.append(token)
                continue

            token_type = self._SINGLE_CHARACTER_TOKENS.get(character)
            if token_type is None:
                # 알파벳 함수와 상수는 Phase 3에서 추가한다.
                raise InvalidInputError()

            tokens.append(Token(token_type=token_type, position=index))
            index += 1

        # END는 Parser가 수식을 남김없이 읽었는지 확인할 때 사용한다.
        tokens.append(Token(token_type=TokenType.END, position=len(expression)))
        return tokens

    @staticmethod
    def _read_number(expression: str, start: int) -> tuple[Token, int]:
        """start 위치부터 하나의 정수 또는 소수를 읽는다."""
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

        # "."만 입력한 경우는 숫자가 아니다.
        if digit_count == 0:
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
