#pragma once

#include <string>

namespace calculator {

enum class AngleMode {
    Degree,
    Radian,
    Gradian,
};

enum class DisplayMode {
    Normal,
    Fixed,
    Scientific,
};

class CalculatorState {
public:
    [[nodiscard]] AngleMode angleMode() const noexcept;
    [[nodiscard]] DisplayMode displayMode() const noexcept;
    [[nodiscard]] bool shiftActive() const noexcept;
    [[nodiscard]] int displayDigits() const noexcept;

    AngleMode cycleAngleMode() noexcept;
    DisplayMode cycleDisplayMode() noexcept;
    void setShiftActive(bool active) noexcept;

    [[nodiscard]] std::string angleModeName() const;
    [[nodiscard]] std::string displayModeName() const;

private:
    AngleMode angleMode_ = AngleMode::Degree;
    DisplayMode displayMode_ = DisplayMode::Normal;
    bool shiftActive_ = false;
    int displayDigits_ = 4;
};

}  // namespace calculator
