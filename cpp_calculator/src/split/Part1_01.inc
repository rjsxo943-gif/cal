}  // namespace calculator::core


// ---- core/Tokenizer.cpp ----
namespace calculator::core {

namespace {

bool startsWith(const std::string& text, std::size_t position, std::string_view prefix) {
    return text.compare(position, prefix.size(), prefix) == 0;
}

bool isIdentifierStart(unsigned char character) {
    return std::isalpha(character) != 0 || character == '_';
}

bool isIdentifierPart(unsigned char character) {
    return std::isalpha(character) != 0 || character == '_';
}

Token makeSimple(TokenType type, std::size_t position) {
    return Token{type, std::monostate{}, position};
}

}  // namespace

std::vector<Token> Tokenizer::tokenize(const std::string& expression) const {
    if (expression.empty()) {
        throw InvalidInputError();
    }

    bool hasNonSpace = false;
    for (unsigned char character : expression) {
        if (std::isspace(character) == 0) {
            hasNonSpace = true;
            break;
        }
    }
    if (!hasNonSpace) {
        throw InvalidInputError();
    }

    std::vector<Token> tokens;
    std::size_t index = 0;

    while (index < expression.size()) {
        const unsigned char character = static_cast<unsigned char>(expression[index]);
        if (std::isspace(character) != 0) {
            ++index;
            continue;
        }

        if (startsWith(expression, index, u8"π")) {
            tokens.push_back(Token{TokenType::Identifier, std::string("pi"), index});
            index += std::string_view(u8"π").size();
            continue;
        }
        if (startsWith(expression, index, u8"√")) {
            tokens.push_back(Token{TokenType::Identifier, std::string("sqrt"), index});
            index += std::string_view(u8"√").size();
            continue;
        }
        if (startsWith(expression, index, u8"×")) {
            tokens.push_back(makeSimple(TokenType::Multiply, index));
            index += std::string_view(u8"×").size();
            continue;
        }
        if (startsWith(expression, index, u8"÷")) {
            tokens.push_back(makeSimple(TokenType::Divide, index));
            index += std::string_view(u8"÷").size();
            continue;
        }

        if (std::isdigit(character) != 0 || character == '.') {
            const std::size_t start = index;
            int decimalPoints = 0;
            int digits = 0;
            while (index < expression.size()) {
                const unsigned char current = static_cast<unsigned char>(expression[index]);
                if (std::isdigit(current) != 0) {
                    ++digits;
                    ++index;
                    continue;
                }
                if (current == '.') {
