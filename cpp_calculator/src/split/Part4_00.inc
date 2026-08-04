// ---- modes/QuadraticEquationSolver.cpp ----
namespace calculator::modes {

QuadraticSolution QuadraticEquationSolver::solve(double a, double b, double c) const {
    if (!std::isfinite(a) || !std::isfinite(b) || !std::isfinite(c)) {
        throw core::InvalidInputError();
    }
    if (a == 0.0) {
        throw core::MathCalculatorError("Coefficient a must not be zero");
    }

    double discriminant = b * b - 4.0 * a * c;
    if (!std::isfinite(discriminant)) {
        throw core::OverflowCalculatorError();
    }

    const double scale = std::max({std::abs(b * b), std::abs(4.0 * a * c), 1.0});
    if (std::abs(discriminant) <= DiscriminantTolerance * scale) {
        discriminant = 0.0;
    }

    if (discriminant > 0.0) {
        const double squareRoot = std::sqrt(discriminant);
        const double q = -0.5 * (b + std::copysign(squareRoot, b));
        const double root1 = q == 0.0 ? -b / (2.0 * a) : q / a;
        const double root2 = q == 0.0 ? root1 : c / q;
        if (!std::isfinite(root1) || !std::isfinite(root2)) {
            throw core::OverflowCalculatorError();
        }
        return {QuadraticRootType::TwoReal, discriminant, {root1, 0.0}, {root2, 0.0}};
    }

    if (discriminant == 0.0) {
        const double root = -b / (2.0 * a);
        if (!std::isfinite(root)) {
            throw core::OverflowCalculatorError();
        }
        return {QuadraticRootType::RepeatedReal, 0.0, {root, 0.0}, {root, 0.0}};
    }

    const double realPart = -b / (2.0 * a);
    const double imaginaryPart = std::sqrt(-discriminant) / (2.0 * std::abs(a));
    if (!std::isfinite(realPart) || !std::isfinite(imaginaryPart)) {
        throw core::OverflowCalculatorError();
    }
    return {
        QuadraticRootType::TwoComplex,
        discriminant,
        {realPart, imaginaryPart},
        {realPart, -imaginaryPart}};
}

}  // namespace calculator::modes


// ---- modes/EquationController.cpp ----
namespace calculator::modes {

QuadraticSolution EquationController::solve(double a, double b, double c) {
    return solver_.solve(a, b, c);
}

std::vector<std::string> EquationController::formatSolution(
    const QuadraticSolution& solution,
    const core::CalculatorState& state) const {
    std::string type;
    switch (solution.rootType) {
    case QuadraticRootType::TwoReal: type = "Two real roots"; break;
    case QuadraticRootType::RepeatedReal: type = "Repeated real root"; break;
    case QuadraticRootType::TwoComplex: type = "Two complex roots"; break;
