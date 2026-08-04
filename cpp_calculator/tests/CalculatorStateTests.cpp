#include "core/CalculatorState.h"

#include <cassert>
#include <iostream>

int main() {
    calculator::CalculatorState state;

    assert(state.angleModeName() == "DEG");
    assert(state.cycleAngleMode() == calculator::AngleMode::Radian);
    assert(state.angleModeName() == "RAD");
    assert(state.cycleAngleMode() == calculator::AngleMode::Gradian);
    assert(state.angleModeName() == "GRAD");
    assert(state.cycleAngleMode() == calculator::AngleMode::Degree);

    assert(state.displayModeName() == "NORM");
    assert(state.cycleDisplayMode() == calculator::DisplayMode::Fixed);
    assert(state.displayModeName() == "FIX4");
    assert(state.cycleDisplayMode() == calculator::DisplayMode::Scientific);
    assert(state.displayModeName() == "SCI4");
    assert(state.cycleDisplayMode() == calculator::DisplayMode::Normal);

    assert(!state.shiftActive());
    state.setShiftActive(true);
    assert(state.shiftActive());

    std::cout << "CalculatorState tests passed\n";
    return 0;
}
