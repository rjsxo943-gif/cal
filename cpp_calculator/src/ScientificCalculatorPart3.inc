// ---- core/CalculatorEngine.cpp ----
namespace calculator::core {

CalculatorEngine::CalculatorEngine(CalculatorState& state)
    : state_(state), randomGenerator_(std::random_device{}()) {}

CalculatorEngine::CalculatorEngine(CalculatorState& state, std::uint64_t seed)
    : state_(state), randomGenerator_(seed) {}

double CalculatorEngine::evaluate(const std::string& expression) {
    const Tokenizer tokenizer;
    ExpressionParser parser(
        tokenizer.tokenize(expression),
        state_.angleMode(),
        state_.answer(),
        &randomGenerator_);
    return parser.parse();
}

}  // namespace calculator::core


// ---- core/ResultFormatter.cpp ----
namespace calculator::core {

std::string ResultFormatter::format(
    double value,
    DisplayMode mode,
    int displayDigits,
    bool asFraction) const {
    value = normalizeValue(value);

    if (asFraction) {
        const auto fraction = formatFraction(value);
        if (fraction.has_value()) {
            return *fraction;
        }
    }

    std::ostringstream output;
    output.imbue(std::locale::classic());
    if (mode == DisplayMode::Fixed) {
        output << std::fixed << std::setprecision(displayDigits) << value;
    } else if (mode == DisplayMode::Scientific) {
        output << std::uppercase << std::scientific << std::setprecision(displayDigits) << value;
    } else {
        output << std::defaultfloat << std::setprecision(SignificantDigits) << value;
    }
    return output.str();
}

std::optional<std::string> ResultFormatter::formatFraction(double value) const {
    value = normalizeValue(value);
    const auto [numerator, denominator] = limitDenominator(value, MaxFractionDenominator);
    const double approximation = static_cast<double>(numerator) / static_cast<double>(denominator);
    const double error = std::abs(approximation - value);
    const double allowed = std::max(FractionTolerance, std::abs(value) * FractionTolerance);
    if (error > allowed) {
        return std::nullopt;
    }
    if (denominator == 1) {
        return std::to_string(numerator);
    }
    return std::to_string(numerator) + "/" + std::to_string(denominator);
}

bool ResultFormatter::canFormatAsFraction(double value) const {
    return formatFraction(value).has_value();
}

double ResultFormatter::normalizeValue(double value) {
    if (!std::isfinite(value)) {
        throw OverflowCalculatorError();
    }
    return std::abs(value) < 1e-15 ? 0.0 : value;
}

std::pair<long long, long long> ResultFormatter::limitDenominator(
    double value,
    long long maxDenominator) {
    if (!std::isfinite(value)) {
        throw OverflowCalculatorError();
    }

    const bool negative = value < 0.0;
    long double target = std::abs(static_cast<long double>(value));

    if (target > static_cast<long double>(std::numeric_limits<long long>::max())) {
        return {negative ? std::numeric_limits<long long>::min() : std::numeric_limits<long long>::max(), 1};
    }

    long long p0 = 0;
    long long q0 = 1;
    long long p1 = 1;
    long long q1 = 0;
    long double x = target;

    while (true) {
        const long double floorValue = std::floor(x);
        if (floorValue > static_cast<long double>(std::numeric_limits<long long>::max())) {
            break;
        }
        const long long a = static_cast<long long>(floorValue);

        const long double q2Wide = static_cast<long double>(q0) + static_cast<long double>(a) * q1;
        const long double p2Wide = static_cast<long double>(p0) + static_cast<long double>(a) * p1;
        if (q2Wide > maxDenominator || p2Wide > static_cast<long double>(std::numeric_limits<long long>::max())) {
            break;
        }

        const long long p2 = p0 + a * p1;
        const long long q2 = q0 + a * q1;
        p0 = p1;
        q0 = q1;
        p1 = p2;
        q1 = q2;

        const long double remainder = x - floorValue;
        if (std::abs(remainder) < 1e-30L) {
            break;
        }
        x = 1.0L / remainder;
    }

    if (q1 == 0) {
        p1 = static_cast<long long>(std::llround(target));
        q1 = 1;
    }

    if (q1 < maxDenominator) {
        const long long k = (maxDenominator - q0) / q1;
        if (k > 0) {
            const long double bound1Numerator = static_cast<long double>(p0) + static_cast<long double>(k) * p1;
            const long double bound1Denominator = static_cast<long double>(q0) + static_cast<long double>(k) * q1;
            const long double bound2Numerator = p1;
            const long double bound2Denominator = q1;
            const long double error1 = std::abs(bound1Numerator / bound1Denominator - target);
            const long double error2 = std::abs(bound2Numerator / bound2Denominator - target);
            if (error1 < error2 && bound1Numerator <= static_cast<long double>(std::numeric_limits<long long>::max())) {
                p1 = static_cast<long long>(bound1Numerator);
                q1 = static_cast<long long>(bound1Denominator);
            }
        }
    }

    const long long divisor = std::gcd(p1, q1);
    p1 /= divisor;
    q1 /= divisor;
    if (negative) {
        p1 = -p1;
    }
    return {p1, q1};
}

}  // namespace calculator::core


// ---- core/CalculationHistory.cpp ----
namespace calculator::core {

void CalculationHistory::add(std::string expression, double value) {
    entries_.push_back(HistoryEntry{std::move(expression), value});
}

const HistoryEntry& CalculationHistory::at(std::size_t index) const {
    if (index >= entries_.size()) {
        throw std::out_of_range("history index");
    }
    return entries_[index];
}

}  // namespace calculator::core


// ---- core/CalculatorController.cpp ----
namespace calculator::core {

CalculatorController::CalculatorController()
    : state_(), engine_(state_) {}

CalculatorController::CalculatorController(std::uint64_t randomSeed)
    : state_(), engine_(state_, randomSeed) {}

std::string CalculatorController::calculate(const std::string& expression) {
    const double result = engine_.evaluate(expression);
    state_.setAnswer(result);
    state_.setLastResult(result);
    state_.setFractionDisplay(false);
    history_.add(expression, result);
    return formatValue(result);
}

std::string CalculatorController::formatValue(double value, bool allowFraction) const {
    return formatter_.format(
        value,
        state_.displayMode(),
        state_.displayDigits(),
        allowFraction && state_.fractionDisplay());
}

std::string CalculatorController::toggleFractionDisplay() {
    if (!state_.lastResult().has_value()) {
        throw InvalidInputError();
    }
    const double value = *state_.lastResult();
    if (!state_.fractionDisplay() && !formatter_.canFormatAsFraction(value)) {
        return formatter_.format(value, state_.displayMode(), state_.displayDigits(), false);
    }
    state_.setFractionDisplay(!state_.fractionDisplay());
    return formatter_.format(
        value,
        state_.displayMode(),
        state_.displayDigits(),
        state_.fractionDisplay());
}

std::string CalculatorController::refreshLastResult() const {
    if (!state_.lastResult().has_value()) {
        throw InvalidInputError();
    }
    return formatter_.format(
        *state_.lastResult(),
        state_.displayMode(),
        state_.displayDigits(),
        state_.fractionDisplay());
}

void CalculatorController::clearDisplayState() noexcept {
    state_.clearLastResult();
}

}  // namespace calculator::core


// ---- modes/StatisticsCalculator.cpp ----
namespace calculator::modes {

StatisticsSummary StatisticsCalculator::summarize(const std::vector<double>& values) const {
    for (double value : values) {
        if (!std::isfinite(value)) {
            throw core::InvalidInputError();
        }
    }

    StatisticsSummary summary;
    summary.count = values.size();
    if (values.empty()) {
        return summary;
    }

    long double sum = 0.0L;
    long double compensation = 0.0L;
    long double mean = 0.0L;
    long double m2 = 0.0L;
    std::size_t count = 0;

    for (double value : values) {
        const long double y = static_cast<long double>(value) - compensation;
        const long double next = sum + y;
        compensation = (next - sum) - y;
        sum = next;

        ++count;
        const long double delta = static_cast<long double>(value) - mean;
        mean += delta / static_cast<long double>(count);
        const long double delta2 = static_cast<long double>(value) - mean;
        m2 += delta * delta2;
    }

    const auto checkedDouble = [](long double value) {
        if (!std::isfinite(value) || std::abs(value) > static_cast<long double>(std::numeric_limits<double>::max())) {
            throw core::OverflowCalculatorError();
        }
        return static_cast<double>(value);
    };

    summary.total = checkedDouble(sum);
    summary.mean = checkedDouble(sum / static_cast<long double>(values.size()));
    summary.minimum = *std::min_element(values.begin(), values.end());
    summary.maximum = *std::max_element(values.begin(), values.end());

    const long double populationVariance = std::max(0.0L, m2 / static_cast<long double>(values.size()));
    summary.populationVariance = checkedDouble(populationVariance);
    summary.populationStandardDeviation = checkedDouble(std::sqrt(populationVariance));

    if (values.size() >= 2) {
        const long double sampleVariance = std::max(0.0L, m2 / static_cast<long double>(values.size() - 1));
        summary.sampleVariance = checkedDouble(sampleVariance);
        summary.sampleStandardDeviation = checkedDouble(std::sqrt(sampleVariance));
    }

    return summary;
}

}  // namespace calculator::modes


// ---- modes/StatisticsController.cpp ----
namespace calculator::modes {

void StatisticsController::addValues(const std::string& input) {
    const std::vector<double> parsed = parseValues(input);
    addValues(parsed);
}

void StatisticsController::addValues(const std::vector<double>& values) {
    for (double value : values) {
        if (!std::isfinite(value)) {
            throw core::InvalidInputError();
        }
    }
    values_.insert(values_.end(), values.begin(), values.end());
}

void StatisticsController::removeAt(std::size_t index) {
    if (index >= values_.size()) {
        throw core::MathCalculatorError("Select a data row");
    }
    values_.erase(values_.begin() + static_cast<std::ptrdiff_t>(index));
}

StatisticsSummary StatisticsController::summary() const {
    return calculator_.summarize(values_);
}

std::vector<double> StatisticsController::parseValues(const std::string& input) {
    std::string normalized = input;
    for (char& character : normalized) {
        if (character == ',' || character == ';') {
            character = ' ';
        }
    }

    std::istringstream stream(normalized);
    stream.imbue(std::locale::classic());
    std::vector<double> values;
    std::string token;
    while (stream >> token) {
        char* end = nullptr;
        errno = 0;
        const double value = std::strtod(token.c_str(), &end);
        if (errno == ERANGE || end == nullptr || *end != '\0' || !std::isfinite(value)) {
            throw core::InvalidInputError();
        }
        values.push_back(value);
    }
    if (values.empty()) {
        throw core::InvalidInputError();
    }
    return values;
}

}  // namespace calculator::modes


