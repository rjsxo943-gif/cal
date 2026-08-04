    statistics.addValues("7");
    const auto one = statistics.summary();
    EXPECT_NEAR(*one.populationVariance, 0.0, 1e-12);
    EXPECT_TRUE(!one.sampleVariance.has_value());
    statistics.removeAt(0);
    EXPECT_TRUE(statistics.values().empty());
    EXPECT_THROWS_MESSAGE(CalculatorError, statistics.removeAt(0), "Select a data row");
}

void equationTests() {
    calculator::modes::QuadraticEquationSolver solver;
    auto solution = solver.solve(1.0, -5.0, 6.0);
    EXPECT_TRUE(solution.rootType == calculator::modes::QuadraticRootType::TwoReal);
    EXPECT_NEAR(solution.discriminant, 1.0, 1e-12);
    EXPECT_TRUE((std::abs(solution.root1.real() - 3.0) < 1e-12 && std::abs(solution.root2.real() - 2.0) < 1e-12) ||
                (std::abs(solution.root1.real() - 2.0) < 1e-12 && std::abs(solution.root2.real() - 3.0) < 1e-12));
    solution = solver.solve(1.0, 2.0, 1.0);
    EXPECT_TRUE(solution.rootType == calculator::modes::QuadraticRootType::RepeatedReal);
    EXPECT_NEAR(solution.root1.real(), -1.0, 1e-12);
    solution = solver.solve(1.0, 0.0, 1.0);
    EXPECT_TRUE(solution.rootType == calculator::modes::QuadraticRootType::TwoComplex);
    EXPECT_NEAR(std::abs(solution.root1.imag()), 1.0, 1e-12);
    EXPECT_THROWS_MESSAGE(CalculatorError, solver.solve(0.0, 1.0, 1.0), "Coefficient a must not be zero");
}

void complexTests() {
    calculator::modes::ComplexController controller;
    CalculatorState state;
    auto summary = controller.fromRectangular(3.0, 4.0);
    EXPECT_NEAR(summary.magnitude, 5.0, 1e-12);
    EXPECT_NEAR(calculator::core::AngleConverter::fromRadians(summary.phaseRadians, AngleMode::Degree),
                53.13010235415598, 1e-12);
    summary = controller.fromPolar(5.0, 53.13010235415598, AngleMode::Degree);
    EXPECT_NEAR(summary.value.real(), 3.0, 1e-10);
    EXPECT_NEAR(summary.value.imag(), 4.0, 1e-10);
    const auto lines = controller.formatSummary(controller.fromRectangular(0.0, 1.0), state);
    EXPECT_TRUE(lines[0].find("j") != std::string::npos);
    EXPECT_THROWS_MESSAGE(CalculatorError,
        controller.fromPolar(-1.0, 0.0, AngleMode::Degree),
        "Magnitude must not be negative");
}

}  // namespace

int main() {
    stateTests();
    tokenizerAndParserTests();
    scientificFunctionTests();
    formatterAndControllerTests();
    statisticsTests();
    equationTests();
    complexTests();
    return test::harness.finish();
}
