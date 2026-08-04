    }
    return {
        "Type: " + type,
        "Discriminant: " + formatter_.format(solution.discriminant, state.displayMode(), state.displayDigits()),
        "x1 = " + formatComplex(solution.root1, formatter_, state),
        "x2 = " + formatComplex(solution.root2, formatter_, state)};
}

std::string EquationController::formatComplex(
    const std::complex<double>& value,
    const core::ResultFormatter& formatter,
    const core::CalculatorState& state) {
    const double real = core::ResultFormatter::normalizeValue(value.real());
    const double imaginary = core::ResultFormatter::normalizeValue(value.imag());
    if (imaginary == 0.0) {
        return formatter.format(real, state.displayMode(), state.displayDigits());
    }
    const std::string realText = formatter.format(real, state.displayMode(), state.displayDigits());
    const std::string imaginaryText = formatter.format(std::abs(imaginary), state.displayMode(), state.displayDigits());
    return realText + (imaginary >= 0.0 ? " + " : " - ") + imaginaryText + "i";
}

}  // namespace calculator::modes


// ---- modes/ComplexCalculator.cpp ----
namespace calculator::modes {

ComplexSummary ComplexCalculator::fromRectangular(double real, double imaginary) const {
    ensureFinite(real, imaginary);
    return summarize({real, imaginary});
}

ComplexSummary ComplexCalculator::fromPolar(
    double magnitude,
    double phase,
    core::AngleMode mode) const {
    ensureFinite(magnitude, phase);
    if (magnitude < 0.0) {
        throw core::MathCalculatorError("Magnitude must not be negative");
    }
    const double radians = core::AngleConverter::toRadians(phase, mode);
    return summarize({magnitude * std::cos(radians), magnitude * std::sin(radians)});
}

ComplexSummary ComplexCalculator::summarize(const std::complex<double>& value) {
    ensureFinite(value.real(), value.imag());
    const double magnitude = std::abs(value);
    const double phase = magnitude == 0.0 ? 0.0 : std::atan2(value.imag(), value.real());
    if (!std::isfinite(magnitude) || !std::isfinite(phase)) {
        throw core::OverflowCalculatorError();
    }
    return {value, std::conj(value), magnitude, phase};
}

void ComplexCalculator::ensureFinite(double first, double second) {
    if (!std::isfinite(first) || !std::isfinite(second)) {
        throw core::InvalidInputError();
    }
}

}  // namespace calculator::modes


// ---- modes/ComplexController.cpp ----
namespace calculator::modes {

ComplexSummary ComplexController::fromRectangular(double real, double imaginary) const {
    return calculator_.fromRectangular(real, imaginary);
}
