#include "core/CalculatorState.h"

namespace calculator {

AngleMode CalculatorState::angleMode() const noexcept {
    return angleMode_;
}

DisplayMode CalculatorState::displayMode() const noexcept {
    return displayMode_;
}

bool CalculatorState::shiftActive() const noexcept {
    return shiftActive_;
}

int CalculatorState::displayDigits() const noexcept {
    return displayDigits_;
}

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

    return displayMode_;
}

void CalculatorState::setShiftActive(const bool active) noexcept {
    shiftActive_ = active;
}

std::string CalculatorState::angleModeName() const {
    switch (angleMode_) {
    case AngleMode::Degree:
        return "DEG";
    case AngleMode::Radian:
        return "RAD";
    case AngleMode::Gradian:
        return "GRAD";
    }

    return "DEG";
}

std::string CalculatorState::displayModeName() const {
    switch (displayMode_) {
    case DisplayMode::Normal:
        return "NORM";
    case DisplayMode::Fixed:
        return "FIX" + std::to_string(displayDigits_);
    case DisplayMode::Scientific:
        return "SCI" + std::to_string(displayDigits_);
    }

    return "NORM";
}

}  // namespace calculator
