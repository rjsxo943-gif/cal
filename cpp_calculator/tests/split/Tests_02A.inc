    EXPECT_NEAR(engine.evaluate("cos(60)"), 0.5, 1e-12);
    EXPECT_NEAR(engine.evaluate("tan(45)"), 1.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("asin(0.5)"), 30.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("acos(0.5)"), 60.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("atan(1)"), 45.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("log(100)"), 2.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("ln(e)"), 1.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("abs(-4)"), 4.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("recip(4)"), 0.25, 1e-12);
    EXPECT_NEAR(engine.evaluate("root(3,-8)"), -2.0, 1e-10);
    EXPECT_NEAR(engine.evaluate("npr(10,3)"), 720.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("ncr(10,3)"), 120.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("gcd(12,18)"), 6.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("lcm(12,18)"), 36.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("quot(-10,3)"), -3.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("rem(-10,3)"), -1.0, 1e-12);
    EXPECT_NEAR(engine.evaluate("mod(-10,3)"), -1.0, 1e-12);
    const double randomValue = engine.evaluate("random()");
    EXPECT_TRUE(randomValue >= 0.0 && randomValue < 1.0);
    const double randomInteger = engine.evaluate("randint(5,5)");
    EXPECT_NEAR(randomInteger, 5.0, 0.0);
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("randint(5,2)"), "Math ERROR");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("sin()"), "Syntax ERROR");
    EXPECT_THROWS_MESSAGE(CalculatorError, engine.evaluate("tan(90)"), "Math ERROR");

    state.setAngleMode(AngleMode::Radian);
    EXPECT_NEAR(engine.evaluate("sin(pi/2)"), 1.0, 1e-12);
    state.setAngleMode(AngleMode::Gradian);
    EXPECT_NEAR(engine.evaluate("sin(100)"), 1.0, 1e-12);
}

void formatterAndControllerTests() {
    ResultFormatter formatter;
    EXPECT_EQ(formatter.format(1.0 / 3.0), std::string("0.3333333333"));
    EXPECT_EQ(formatter.format(1.0 / 3.0, DisplayMode::Fixed, 4), std::string("0.3333"));
    EXPECT_EQ(formatter.format(1.0 / 3.0, DisplayMode::Scientific, 4), std::string("3.3333E-01"));
    EXPECT_EQ(formatter.format(-0.0), std::string("0"));
    EXPECT_EQ(formatter.format(1.0 / 3.0, DisplayMode::Normal, 4, true), std::string("1/3"));
    EXPECT_TRUE(!formatter.formatFraction(pi).has_value());

    CalculatorController controller(7);
    EXPECT_EQ(controller.calculate("2+3"), std::string("5"));
    EXPECT_NEAR(controller.state().answer(), 5.0, 1e-12);
    EXPECT_EQ(controller.calculate("Ans*4"), std::string("20"));
    EXPECT_EQ(controller.history().size(), static_cast<std::size_t>(2));
    try { controller.calculate("1/0"); } catch (const CalculatorError&) {}
    EXPECT_NEAR(controller.state().answer(), 20.0, 1e-12);
    EXPECT_EQ(controller.history().size(), static_cast<std::size_t>(2));
    EXPECT_EQ(controller.calculate("1/3"), std::string("0.3333333333"));
    EXPECT_EQ(controller.toggleFractionDisplay(), std::string("1/3"));
