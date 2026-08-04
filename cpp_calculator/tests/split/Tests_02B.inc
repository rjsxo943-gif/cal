    EXPECT_EQ(controller.toggleFractionDisplay(), std::string("0.3333333333"));
    controller.state().cycleDisplayMode();
    EXPECT_EQ(controller.refreshLastResult(), std::string("0.3333"));
}

void statisticsTests() {
    calculator::modes::StatisticsController statistics;
    statistics.addValues("1, 2 3;4");
    const auto summary = statistics.summary();
    EXPECT_EQ(summary.count, static_cast<std::size_t>(4));
    EXPECT_NEAR(summary.total, 10.0, 1e-12);
    EXPECT_NEAR(*summary.mean, 2.5, 1e-12);
    EXPECT_NEAR(*summary.populationVariance, 1.25, 1e-12);
    EXPECT_NEAR(*summary.populationStandardDeviation, std::sqrt(1.25), 1e-12);
    EXPECT_NEAR(*summary.sampleVariance, 5.0 / 3.0, 1e-12);
    EXPECT_NEAR(*summary.sampleStandardDeviation, std::sqrt(5.0 / 3.0), 1e-12);
    const auto oldSize = statistics.values().size();
    EXPECT_THROWS_MESSAGE(CalculatorError, statistics.addValues("5, bad, 6"), "Invalid input");
    EXPECT_EQ(statistics.values().size(), oldSize);
    statistics.clear();
