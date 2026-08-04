#pragma once

#include <complex>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <random>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

// ---- core/CalculatorError.h ----
namespace calculator::core {

class CalculatorError : public std::runtime_error {
public:
    explicit CalculatorError(const std::string& message = "Invalid input")
        : std::runtime_error(message) {}
};

class SyntaxCalculatorError final : public CalculatorError {
public:
    SyntaxCalculatorError() : CalculatorError("Syntax ERROR") {}
};

class InvalidInputError final : public CalculatorError {
public:
    InvalidInputError() : CalculatorError("Invalid input") {}
};

class DivisionByZeroCalculatorError final : public CalculatorError {
public:
    DivisionByZeroCalculatorError() : CalculatorError("Division by zero") {}
};

class MathCalculatorError final : public CalculatorError {
public:
    MathCalculatorError() : CalculatorError("Math ERROR") {}
    explicit MathCalculatorError(const std::string& message) : CalculatorError(message) {}
};

class OverflowCalculatorError final : public CalculatorError {
public:
    OverflowCalculatorError() : CalculatorError("Overflow") {}
};

}  // namespace calculator::core


// ---- core/CalculatorState.h ----
namespace calculator::core {

enum class AngleMode { Degree, Radian, Gradian };
enum class DisplayMode { Normal, Fixed, Scientific };

class CalculatorState {
public:
    AngleMode angleMode() const noexcept { return angleMode_; }
    DisplayMode displayMode() const noexcept { return displayMode_; }
    int displayDigits() const noexcept { return displayDigits_; }
    double answer() const noexcept { return answer_; }
    const std::optional<double>& lastResult() const noexcept { return lastResult_; }
    bool fractionDisplay() const noexcept { return fractionDisplay_; }

    void setAngleMode(AngleMode mode) noexcept { angleMode_ = mode; }
    AngleMode cycleAngleMode() noexcept;

    void setDisplayMode(DisplayMode mode) noexcept;
    DisplayMode cycleDisplayMode() noexcept;

    void setAnswer(double value) noexcept { answer_ = value; }
    void setLastResult(double value) noexcept { lastResult_ = value; }
    void clearLastResult() noexcept { lastResult_.reset(); fractionDisplay_ = false; }
    void setFractionDisplay(bool enabled) noexcept { fractionDisplay_ = enabled; }

    std::string angleModeName() const;
    std::string displayModeName() const;

private:
    AngleMode angleMode_{AngleMode::Degree};
    DisplayMode displayMode_{DisplayMode::Normal};
    int displayDigits_{4};
    double answer_{0.0};
    std::optional<double> lastResult_{};
    bool fractionDisplay_{false};
};

}  // namespace calculator::core


// ---- core/AngleConverter.h ----
namespace calculator::core {

class AngleConverter {
public:
    static double toRadians(double value, AngleMode mode) noexcept;
    static double fromRadians(double value, AngleMode mode) noexcept;
};

}  // namespace calculator::core


// ---- core/Token.h ----
namespace calculator::core {

enum class TokenType {
    Number,
    Identifier,
    Plus,
    Minus,
    Multiply,
    Divide,
    Power,
    Factorial,
    Percent,
    Comma,
    LeftParen,
    RightParen,
    End
};

struct Token {
    TokenType type{TokenType::End};
    std::variant<std::monostate, double, std::string> value{};
    std::size_t position{0};
};

}  // namespace calculator::core


// ---- core/Tokenizer.h ----
namespace calculator::core {

class Tokenizer {
public:
    std::vector<Token> tokenize(const std::string& expression) const;
};

}  // namespace calculator::core


// ---- core/ExpressionParser.h ----
namespace calculator::core {

class ExpressionParser {
public:
    ExpressionParser(
        std::vector<Token> tokens,
        AngleMode angleMode = AngleMode::Degree,
        double answer = 0.0,
        std::mt19937_64* randomGenerator = nullptr);

    double parse();

private:
    double parseExpression();
    double parseTerm();
    double parseUnary();
    double parsePower();
    double parsePostfix();
    double parsePrimary();
    double parseIdentifier();
    std::vector<double> parseFunctionArguments();
    double evaluateFunction(const std::string& name, const std::vector<double>& arguments);

    double factorial(double value) const;
    static long long integer(double value);
    static long long nonnegativeInteger(double value);
    static void requireArgumentCount(const std::vector<double>& arguments, std::size_t count);
    static void ensureFinite(double value);

    const Token& current() const;
    Token advance();
    void consume(TokenType type);

    std::vector<Token> tokens_;
    std::size_t currentIndex_{0};
    AngleMode angleMode_{AngleMode::Degree};
    double answer_{0.0};
    std::mt19937_64 ownedRandomGenerator_;
    std::mt19937_64* randomGenerator_{nullptr};
};

}  // namespace calculator::core


// ---- core/CalculatorEngine.h ----
namespace calculator::core {

class CalculatorEngine {
public:
    explicit CalculatorEngine(CalculatorState& state);
    CalculatorEngine(CalculatorState& state, std::uint64_t seed);

    double evaluate(const std::string& expression);

private:
    CalculatorState& state_;
    std::mt19937_64 randomGenerator_;
};

}  // namespace calculator::core


// ---- core/ResultFormatter.h ----
namespace calculator::core {

class ResultFormatter {
public:
    static constexpr int SignificantDigits = 10;
    static constexpr long long MaxFractionDenominator = 10'000;
    static constexpr double FractionTolerance = 1e-12;

    std::string format(
        double value,
        DisplayMode mode = DisplayMode::Normal,
        int displayDigits = 4,
        bool asFraction = false) const;

    std::optional<std::string> formatFraction(double value) const;
    bool canFormatAsFraction(double value) const;
    static double normalizeValue(double value);

private:
    static std::pair<long long, long long> limitDenominator(
        double value,
        long long maxDenominator);
};

}  // namespace calculator::core


// ---- core/CalculationHistory.h ----
namespace calculator::core {

struct HistoryEntry {
    std::string expression;
    double value{0.0};
};

class CalculationHistory {
public:
    void add(std::string expression, double value);
    const std::vector<HistoryEntry>& entries() const noexcept { return entries_; }
    const HistoryEntry& at(std::size_t index) const;
    bool empty() const noexcept { return entries_.empty(); }
    std::size_t size() const noexcept { return entries_.size(); }
    void clear() noexcept { entries_.clear(); }

private:
    std::vector<HistoryEntry> entries_;
};

}  // namespace calculator::core


// ---- core/CalculatorController.h ----
namespace calculator::core {

class CalculatorController {
public:
    CalculatorController();
    explicit CalculatorController(std::uint64_t randomSeed);

    std::string calculate(const std::string& expression);
    std::string formatValue(double value, bool allowFraction = false) const;
    std::string toggleFractionDisplay();
    std::string refreshLastResult() const;
    void clearDisplayState() noexcept;

    CalculatorState& state() noexcept { return state_; }
    const CalculatorState& state() const noexcept { return state_; }
    CalculationHistory& history() noexcept { return history_; }
    const CalculationHistory& history() const noexcept { return history_; }

private:
    CalculatorState state_;
    CalculatorEngine engine_;
    ResultFormatter formatter_;
    CalculationHistory history_;
};

}  // namespace calculator::core


// ---- modes/StatisticsCalculator.h ----
namespace calculator::modes {

struct StatisticsSummary {
    std::size_t count{0};
    double total{0.0};
    std::optional<double> mean;
    std::optional<double> minimum;
    std::optional<double> maximum;
    std::optional<double> populationVariance;
    std::optional<double> populationStandardDeviation;
    std::optional<double> sampleVariance;
    std::optional<double> sampleStandardDeviation;
};

class StatisticsCalculator {
public:
    StatisticsSummary summarize(const std::vector<double>& values) const;
};

}  // namespace calculator::modes


// ---- modes/StatisticsController.h ----
namespace calculator::modes {

class StatisticsController {
public:
    void addValues(const std::string& input);
    void addValues(const std::vector<double>& values);
    void removeAt(std::size_t index);
    void clear() noexcept { values_.clear(); }

    const std::vector<double>& values() const noexcept { return values_; }
    StatisticsSummary summary() const;

    static std::vector<double> parseValues(const std::string& input);

private:
    std::vector<double> values_;
    StatisticsCalculator calculator_;
};

}  // namespace calculator::modes


// ---- modes/QuadraticEquationSolver.h ----
namespace calculator::modes {

enum class QuadraticRootType { TwoReal, RepeatedReal, TwoComplex };

struct QuadraticSolution {
    QuadraticRootType rootType{QuadraticRootType::TwoReal};
    double discriminant{0.0};
    std::complex<double> root1{};
    std::complex<double> root2{};
};

class QuadraticEquationSolver {
public:
    static constexpr double DiscriminantTolerance = 1e-12;
    QuadraticSolution solve(double a, double b, double c) const;
};

}  // namespace calculator::modes


// ---- modes/EquationController.h ----
namespace calculator::modes {

class EquationController {
public:
    QuadraticSolution solve(double a, double b, double c);
    std::vector<std::string> formatSolution(
        const QuadraticSolution& solution,
        const core::CalculatorState& state) const;

private:
    static std::string formatComplex(
        const std::complex<double>& value,
        const core::ResultFormatter& formatter,
        const core::CalculatorState& state);

    QuadraticEquationSolver solver_;
    core::ResultFormatter formatter_;
};

}  // namespace calculator::modes


// ---- modes/ComplexCalculator.h ----
namespace calculator::modes {

struct ComplexSummary {
    std::complex<double> value{};
    std::complex<double> conjugate{};
    double magnitude{0.0};
    double phaseRadians{0.0};
};

class ComplexCalculator {
public:
    ComplexSummary fromRectangular(double real, double imaginary) const;
    ComplexSummary fromPolar(double magnitude, double phase, core::AngleMode mode) const;

private:
    static ComplexSummary summarize(const std::complex<double>& value);
    static void ensureFinite(double first, double second);
};

}  // namespace calculator::modes


// ---- modes/ComplexController.h ----
namespace calculator::modes {

class ComplexController {
public:
    ComplexSummary fromRectangular(double real, double imaginary) const;
    ComplexSummary fromPolar(double magnitude, double phase, core::AngleMode mode) const;
    std::vector<std::string> formatSummary(
        const ComplexSummary& summary,
        const core::CalculatorState& state) const;

private:
    std::string formatComplex(
        const std::complex<double>& value,
        const core::CalculatorState& state) const;

    ComplexCalculator calculator_;
    core::ResultFormatter formatter_;
};

}  // namespace calculator::modes
