// ---- core/ExpressionParser.cpp ----
namespace calculator::core {

namespace {
constexpr double pi = 3.141592653589793238462643383279502884;
constexpr double euler = 2.718281828459045235360287471352662498;

bool isKnownFunction(const std::string& name) {
    static const std::set<std::string> names{
        "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "log", "ln",
        "abs", "recip", "npr", "ncr", "mod", "gcd", "lcm", "quot", "rem",
        "root", "random", "randint"};
    return names.find(name) != names.end();
}

long double checkedProduct(long double left, long double right) {
    const long double result = left * right;
    if (!std::isfinite(result) || result > static_cast<long double>(std::numeric_limits<double>::max())) {
        throw OverflowCalculatorError();
    }
    return result;
}

}  // namespace

ExpressionParser::ExpressionParser(
    std::vector<Token> tokens,
    AngleMode angleMode,
    double answer,
    std::mt19937_64* randomGenerator)
    : tokens_(std::move(tokens)),
      angleMode_(angleMode),
      answer_(answer),
      ownedRandomGenerator_(std::random_device{}()),
      randomGenerator_(randomGenerator != nullptr ? randomGenerator : &ownedRandomGenerator_) {
    if (tokens_.empty()) {
        throw SyntaxCalculatorError();
    }
}

double ExpressionParser::parse() {
    const double result = parseExpression();
    if (current().type != TokenType::End) {
        throw SyntaxCalculatorError();
    }
    ensureFinite(result);
    return result;
}

double ExpressionParser::parseExpression() {
    double value = parseTerm();
    while (current().type == TokenType::Plus || current().type == TokenType::Minus) {
        const TokenType operation = advance().type;
        const double right = parseTerm();
        value = operation == TokenType::Plus ? value + right : value - right;
        ensureFinite(value);
    }
    return value;
}

double ExpressionParser::parseTerm() {
    double value = parseUnary();
    while (current().type == TokenType::Multiply || current().type == TokenType::Divide) {
        const TokenType operation = advance().type;
        const double right = parseUnary();
        if (operation == TokenType::Multiply) {
            value *= right;
        } else {
            if (right == 0.0) {
                throw DivisionByZeroCalculatorError();
            }
            value /= right;
        }
        ensureFinite(value);
    }
    return value;
}

double ExpressionParser::parseUnary() {
    if (current().type == TokenType::Plus) {
        advance();
        return parseUnary();
    }
    if (current().type == TokenType::Minus) {
        advance();
        return -parseUnary();
    }
    return parsePower();
}

double ExpressionParser::parsePower() {
    const double base = parsePostfix();
    if (current().type != TokenType::Power) {
        return base;
    }
    advance();
    const double exponent = parseUnary();
    if (base == 0.0 && exponent < 0.0) {
        throw DivisionByZeroCalculatorError();
    }
    errno = 0;
    const double result = std::pow(base, exponent);
    if (errno == EDOM || std::isnan(result)) {
        throw MathCalculatorError();
    }
    if (errno == ERANGE || !std::isfinite(result)) {
        throw OverflowCalculatorError();
    }
    return result;
}

double ExpressionParser::parsePostfix() {
    double value = parsePrimary();
    while (current().type == TokenType::Factorial || current().type == TokenType::Percent) {
        const TokenType operation = advance().type;
        value = operation == TokenType::Factorial ? factorial(value) : value / 100.0;
        ensureFinite(value);
    }
    return value;
}

double ExpressionParser::parsePrimary() {
    const Token token = current();
    if (token.type == TokenType::Number) {
        advance();
        if (!std::holds_alternative<double>(token.value)) {
            throw SyntaxCalculatorError();
        }
        return std::get<double>(token.value);
    }
    if (token.type == TokenType::LeftParen) {
        advance();
        const double value = parseExpression();
        consume(TokenType::RightParen);
        return value;
    }
    if (token.type == TokenType::Identifier) {
        return parseIdentifier();
    }
    throw SyntaxCalculatorError();
}

double ExpressionParser::parseIdentifier() {
    const Token token = advance();
    if (!std::holds_alternative<std::string>(token.value)) {
        throw SyntaxCalculatorError();
    }
    const std::string name = std::get<std::string>(token.value);
    if (name == "ans") {
        return answer_;
    }
    if (name == "pi") {
        return pi;
    }
    if (name == "e") {
        return euler;
    }
    if (!isKnownFunction(name)) {
        throw InvalidInputError();
    }
    consume(TokenType::LeftParen);
    const std::vector<double> arguments = parseFunctionArguments();
    consume(TokenType::RightParen);
    return evaluateFunction(name, arguments);
}

std::vector<double> ExpressionParser::parseFunctionArguments() {
    std::vector<double> arguments;
    if (current().type == TokenType::RightParen) {
        return arguments;
    }
    arguments.push_back(parseExpression());
    while (current().type == TokenType::Comma) {
        advance();
        arguments.push_back(parseExpression());
    }
    return arguments;
}

double ExpressionParser::evaluateFunction(
    const std::string& name,
    const std::vector<double>& arguments) {
    double result = 0.0;

    if (name == "random") {
        requireArgumentCount(arguments, 0);
        result = std::generate_canonical<double, std::numeric_limits<double>::digits>(*randomGenerator_);
    } else if (name == "randint") {
        requireArgumentCount(arguments, 2);
        const long long first = integer(arguments[0]);
        const long long second = integer(arguments[1]);
        if (first > second) {
            throw MathCalculatorError();
        }
        std::uniform_int_distribution<long long> distribution(first, second);
        result = static_cast<double>(distribution(*randomGenerator_));
    } else if (name == "sqrt") {
        requireArgumentCount(arguments, 1);
        if (arguments[0] < 0.0) {
            throw MathCalculatorError();
        }
        result = std::sqrt(arguments[0]);
    } else if (name == "sin" || name == "cos" || name == "tan") {
        requireArgumentCount(arguments, 1);
        const double radians = AngleConverter::toRadians(arguments[0], angleMode_);
        if (name == "sin") {
            result = std::sin(radians);
        } else if (name == "cos") {
            result = std::cos(radians);
        } else {
            if (std::abs(std::cos(radians)) < 1e-12) {
                throw MathCalculatorError();
            }
            result = std::tan(radians);
        }
    } else if (name == "asin" || name == "acos" || name == "atan") {
        requireArgumentCount(arguments, 1);
        const double value = arguments[0];
        double radians = 0.0;
        if (name == "asin") {
            if (value < -1.0 || value > 1.0) {
                throw MathCalculatorError();
            }
            radians = std::asin(value);
        } else if (name == "acos") {
            if (value < -1.0 || value > 1.0) {
                throw MathCalculatorError();
            }
            radians = std::acos(value);
        } else {
            radians = std::atan(value);
        }
        result = AngleConverter::fromRadians(radians, angleMode_);
    } else if (name == "log" || name == "ln") {
        requireArgumentCount(arguments, 1);
        if (arguments[0] <= 0.0) {
            throw MathCalculatorError();
        }
        result = name == "log" ? std::log10(arguments[0]) : std::log(arguments[0]);
    } else if (name == "abs") {
        requireArgumentCount(arguments, 1);
        result = std::abs(arguments[0]);
    } else if (name == "recip") {
        requireArgumentCount(arguments, 1);
        if (arguments[0] == 0.0) {
            throw DivisionByZeroCalculatorError();
        }
        result = 1.0 / arguments[0];
    } else if (name == "npr" || name == "ncr") {
        requireArgumentCount(arguments, 2);
        const long long n = nonnegativeInteger(arguments[0]);
        const long long r = nonnegativeInteger(arguments[1]);
        if (r > n) {
            throw MathCalculatorError();
        }
        long double value = 1.0L;
        if (name == "npr") {
            for (long long i = 0; i < r; ++i) {
                value = checkedProduct(value, static_cast<long double>(n - i));
            }
        } else {
            const long long effectiveR = std::min(r, n - r);
            for (long long i = 1; i <= effectiveR; ++i) {
                value *= static_cast<long double>(n - effectiveR + i);
                value /= static_cast<long double>(i);
                if (!std::isfinite(value) || value > static_cast<long double>(std::numeric_limits<double>::max())) {
                    throw OverflowCalculatorError();
                }
            }
        }
        result = static_cast<double>(value);
    } else if (name == "mod" || name == "rem") {
        requireArgumentCount(arguments, 2);
        if (arguments[1] == 0.0) {
            throw DivisionByZeroCalculatorError();
        }
        result = std::fmod(arguments[0], arguments[1]);
    } else if (name == "quot") {
        requireArgumentCount(arguments, 2);
        if (arguments[1] == 0.0) {
            throw DivisionByZeroCalculatorError();
        }
        result = std::trunc(arguments[0] / arguments[1]);
    } else if (name == "root") {
        requireArgumentCount(arguments, 2);
        const long long degree = nonnegativeInteger(arguments[0]);
        const double radicand = arguments[1];
        if (degree == 0) {
            throw MathCalculatorError();
        }
        if (radicand < 0.0) {
            if (degree % 2 == 0) {
                throw MathCalculatorError();
            }
            result = -std::pow(-radicand, 1.0 / static_cast<double>(degree));
        } else {
            result = std::pow(radicand, 1.0 / static_cast<double>(degree));
        }
    } else if (name == "gcd" || name == "lcm") {
        requireArgumentCount(arguments, 2);
        const long long first = integer(arguments[0]);
        const long long second = integer(arguments[1]);
        if (name == "gcd") {
            result = static_cast<double>(std::gcd(first, second));
        } else {
            if (first == 0 || second == 0) {
                result = 0.0;
            } else {
                const long long divisor = std::gcd(first, second);
                const long double candidate = std::abs(static_cast<long double>(first) / divisor * static_cast<long double>(second));
                if (!std::isfinite(candidate) || candidate > static_cast<long double>(std::numeric_limits<double>::max())) {
                    throw OverflowCalculatorError();
                }
                result = static_cast<double>(candidate);
            }
        }
    } else {
        throw InvalidInputError();
    }

    ensureFinite(result);
    return result;
}

double ExpressionParser::factorial(double value) const {
    const long long number = nonnegativeInteger(value);
    if (number > 170) {
        throw OverflowCalculatorError();
    }
    long double result = 1.0L;
    for (long long current = 2; current <= number; ++current) {
        result *= static_cast<long double>(current);
    }
    return static_cast<double>(result);
}

long long ExpressionParser::integer(double value) {
    if (!std::isfinite(value) || std::trunc(value) != value ||
        value < static_cast<double>(std::numeric_limits<long long>::min()) ||
        value > static_cast<double>(std::numeric_limits<long long>::max())) {
        throw MathCalculatorError();
    }
    return static_cast<long long>(value);
}

long long ExpressionParser::nonnegativeInteger(double value) {
    const long long number = integer(value);
    if (number < 0) {
        throw MathCalculatorError();
    }
    return number;
}

void ExpressionParser::requireArgumentCount(
    const std::vector<double>& arguments,
    std::size_t count) {
    if (arguments.size() != count) {
        throw SyntaxCalculatorError();
    }
}

void ExpressionParser::ensureFinite(double value) {
    if (!std::isfinite(value)) {
        throw OverflowCalculatorError();
    }
}

const Token& ExpressionParser::current() const {
    if (currentIndex_ >= tokens_.size()) {
        throw SyntaxCalculatorError();
    }
    return tokens_[currentIndex_];
}

Token ExpressionParser::advance() {
    const Token token = current();
    ++currentIndex_;
    return token;
}

void ExpressionParser::consume(TokenType type) {
    if (current().type != type) {
        throw SyntaxCalculatorError();
    }
    advance();
}

}  // namespace calculator::core


