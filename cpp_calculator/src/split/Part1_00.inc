// ---- core/CalculatorState.cpp ----
namespace calculator::core {

AngleMode CalculatorState::cycleAngleMode() noexcept {
    switch (angleMode_) {
    case AngleMode::Degree:
        angleMode_ = AngleMode::Radian;
        break;
    case AngleMode::Radian:
        angleMode_ = AngleMode::Gradian;
        break;
    case AngleMode::Gradian:
        angleMode_ = AngleMode::Degree;
        break;
    }
    return angleMode_;
}

void CalculatorState::setDisplayMode(DisplayMode mode) noexcept {
    displayMode_ = mode;
    fractionDisplay_ = false;
}

DisplayMode CalculatorState::cycleDisplayMode() noexcept {
    switch (displayMode_) {
    case DisplayMode::Normal:
        displayMode_ = DisplayMode::Fixed;
        break;
    case DisplayMode::Fixed:
        displayMode_ = DisplayMode::Scientific;
        break;
    case DisplayMode::Scientific:
        displayMode_ = DisplayMode::Normal;
        break;
    }
    fractionDisplay_ = false;
    return displayMode_;
}

std::string CalculatorState::angleModeName() const {
    switch (angleMode_) {
    case AngleMode::Degree: return "DEG";
    case AngleMode::Radian: return "RAD";
    case AngleMode::Gradian: return "GRAD";
    }
    return "DEG";
}

std::string CalculatorState::displayModeName() const {
    switch (displayMode_) {
    case DisplayMode::Normal: return "NORM";
    case DisplayMode::Fixed: return "FIX" + std::to_string(displayDigits_);
    case DisplayMode::Scientific: return "SCI" + std::to_string(displayDigits_);
    }
    return "NORM";
}

}  // namespace calculator::core


// ---- core/AngleConverter.cpp ----
namespace calculator::core {

namespace {
constexpr double anglePi = 3.141592653589793238462643383279502884;
}

double AngleConverter::toRadians(double value, AngleMode mode) noexcept {
    switch (mode) {
    case AngleMode::Degree: return value * anglePi / 180.0;
    case AngleMode::Radian: return value;
    case AngleMode::Gradian: return value * anglePi / 200.0;
    }
    return value;
}

double AngleConverter::fromRadians(double value, AngleMode mode) noexcept {
    switch (mode) {
    case AngleMode::Degree: return value * 180.0 / anglePi;
    case AngleMode::Radian: return value;
    case AngleMode::Gradian: return value * 200.0 / anglePi;
    }
    return value;
}

