    }

    int passed_{0};
    int failed_{0};
};

inline Harness harness;

}  // namespace test

#define EXPECT_TRUE(expression) test::harness.expectTrue((expression), #expression, __FILE__, __LINE__)
#define EXPECT_EQ(left, right) test::harness.expectEqual((left), (right), #left " == " #right, __FILE__, __LINE__)
#define EXPECT_NEAR(left, right, tolerance) test::harness.expectNear((left), (right), (tolerance), #left " ~= " #right, __FILE__, __LINE__)
#define EXPECT_THROWS_MESSAGE(exception_type, expression, message) \
    test::harness.expectThrowsMessage<exception_type>([&]() { static_cast<void>(expression); }, (message), #expression, __FILE__, __LINE__)


// ---- tests/CalculatorTests.cpp ----
using calculator::core::AngleMode;
using calculator::core::CalculatorController;
using calculator::core::CalculatorEngine;
using calculator::core::CalculatorError;
using calculator::core::CalculatorState;
using calculator::core::DisplayMode;
using calculator::core::MathCalculatorError;
using calculator::core::ResultFormatter;

namespace {
constexpr double pi = 3.141592653589793238462643383279502884;

void stateTests() {
    CalculatorState state;
    EXPECT_EQ(state.angleModeName(), std::string("DEG"));
    state.cycleAngleMode(); EXPECT_EQ(state.angleModeName(), std::string("RAD"));
    state.cycleAngleMode(); EXPECT_EQ(state.angleModeName(), std::string("GRAD"));
    state.cycleAngleMode(); EXPECT_EQ(state.angleModeName(), std::string("DEG"));
    EXPECT_EQ(state.displayModeName(), std::string("NORM"));
    state.cycleDisplayMode(); EXPECT_EQ(state.displayModeName(), std::string("FIX4"));
    state.cycleDisplayMode(); EXPECT_EQ(state.displayModeName(), std::string("SCI4"));
    state.cycleDisplayMode(); EXPECT_EQ(state.displayModeName(), std::string("NORM"));
}

void tokenizerAndParserTests() {
    CalculatorState state;
    CalculatorEngine engine(state, 1234);
    EXPECT_NEAR(engine.evaluate("2+3*4"), 14.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("(2+3)*4"), 20.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("-5+3"), -2.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("2^3^2"), 512.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("-2^2"), -4.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("(-2)^2"), 4.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("50%"), 0.5, 1e-12);
    EXPECT_NEAR(engine.evaluate("5!"), 120.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("1E3+2.5e-1"), 1000.25, 1e-12);
    EXPECT_NEAR(engine.evaluate(u8"π"), pi, 1e-15);
    EXPECT_NEAR(engine.evaluate(u8"√(16)"), 4.0, 1e-12);
    EXPECT_NEAR(engine.evaluate(u8"6÷2×3"), 9.0, 1e-12);

    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("1/0"), "Division by zero");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("sin("), "Syntax ERROR");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("unknown(1)"), "Invalid input");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("171!"), "Overflow");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("sqrt(-1)"), "Math ERROR");
}

void scientificFunctionTests() {
    CalculatorState state;
    CalculatorEngine engine(state, 42);
    EXPECT_NEAR(engine.evaluate("sqrt(16)"), 4.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("sin(30)"), 0.5, 1e-12);
