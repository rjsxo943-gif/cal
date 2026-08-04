
ComplexSummary ComplexController::fromPolar(
    double magnitude,
    double phase,
    core::AngleMode mode) const {
    return calculator_.fromPolar(magnitude, phase, mode);
}

std::vector<std::string> ComplexController::formatSummary(
    const ComplexSummary& summary,
    const core::CalculatorState& state) const {
    const double phase = core::AngleConverter::fromRadians(summary.phaseRadians, state.angleMode());
    const std::string magnitude = formatter_.format(
        summary.magnitude, state.displayMode(), state.displayDigits());
    const std::string phaseText = formatter_.format(
        phase, state.displayMode(), state.displayDigits());
    return {
        "Rectangular: " + formatComplex(summary.value, state),
        "Polar: " + magnitude + " < " + phaseText + " " + state.angleModeName(),
        "Magnitude: " + magnitude,
        "Phase: " + phaseText + " " + state.angleModeName(),
        "Conjugate: " + formatComplex(summary.conjugate, state)};
}

std::string ComplexController::formatComplex(
    const std::complex<double>& value,
    const core::CalculatorState& state) const {
    const double real = core::ResultFormatter::normalizeValue(value.real());
    const double imaginary = core::ResultFormatter::normalizeValue(value.imag());
    const std::string realText = formatter_.format(real, state.displayMode(), state.displayDigits());
    if (imaginary == 0.0) {
        return realText;
    }

    const double magnitude = std::abs(imaginary);
    std::string imaginaryMagnitude;
    if (std::abs(magnitude - 1.0) < 1e-15) {
        imaginaryMagnitude.clear();
    } else {
        imaginaryMagnitude = formatter_.format(magnitude, state.displayMode(), state.displayDigits());
    }

    if (real == 0.0) {
        return std::string(imaginary < 0.0 ? "-" : "") + imaginaryMagnitude + "j";
    }
    return realText + (imaginary >= 0.0 ? " + " : " - ") + imaginaryMagnitude + "j";
}

}  // namespace calculator::modes
