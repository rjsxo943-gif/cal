                    ++decimalPoints;
                    if (decimalPoints > 1) {
                        throw SyntaxCalculatorError();
                    }
                    ++index;
                    continue;
                }
                break;
            }
            if (digits == 0) {
                throw SyntaxCalculatorError();
            }

            if (index < expression.size() && (expression[index] == 'e' || expression[index] == 'E')) {
                ++index;
                if (index < expression.size() && (expression[index] == '+' || expression[index] == '-')) {
                    ++index;
                }
                const std::size_t exponentStart = index;
                while (index < expression.size() &&
                       std::isdigit(static_cast<unsigned char>(expression[index])) != 0) {
                    ++index;
                }
                if (exponentStart == index) {
                    throw SyntaxCalculatorError();
                }
            }

            const std::string numberText = expression.substr(start, index - start);
            char* end = nullptr;
            errno = 0;
            const double value = std::strtod(numberText.c_str(), &end);
            if (errno == ERANGE || end == nullptr || *end != '\0') {
                throw SyntaxCalculatorError();
            }
            tokens.push_back(Token{TokenType::Number, value, start});
            continue;
        }

        if (isIdentifierStart(character)) {
            const std::size_t start = index;
            while (index < expression.size() &&
                   isIdentifierPart(static_cast<unsigned char>(expression[index]))) {
                ++index;
            }
            std::string name = expression.substr(start, index - start);
            for (char& letter : name) {
                letter = static_cast<char>(std::tolower(static_cast<unsigned char>(letter)));
            }
            tokens.push_back(Token{TokenType::Identifier, std::move(name), start});
            continue;
        }

        TokenType type;
        switch (character) {
        case '+': type = TokenType::Plus; break;
        case '-': type = TokenType::Minus; break;
        case '*': type = TokenType::Multiply; break;
        case '/': type = TokenType::Divide; break;
        case '^': type = TokenType::Power; break;
        case '!': type = TokenType::Factorial; break;
        case '%': type = TokenType::Percent; break;
        case ',': type = TokenType::Comma; break;
        case '(': type = TokenType::LeftParen; break;
        case ')': type = TokenType::RightParen; break;
        default: throw InvalidInputError();
        }
        tokens.push_back(makeSimple(type, index));
        ++index;
    }

    tokens.push_back(makeSimple(TokenType::End, expression.size()));
    return tokens;
}

}  // namespace calculator::core


