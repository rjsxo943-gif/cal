                return;
            }
            if (selection == 1) {
                const auto values = ConsoleInput::readLine("Values (comma/space/semicolon separated): ");
                if (!values.has_value()) return;
                statistics_.addValues(*values);
                printStatistics();
            } else if (selection == 2) {
                printStatistics();
            } else if (selection == 3) {
                if (statistics_.values().empty()) {
                    throw core::MathCalculatorError("Select a data row");
                }
                for (std::size_t i = 0; i < statistics_.values().size(); ++i) {
                    std::cout << (i + 1) << ". " << calculator_.formatValue(statistics_.values()[i]) << "\n";
                }
                const auto row = ConsoleInput::readLine("Row number: ");
                if (!row.has_value()) return;
                const int rowNumber = ConsoleInput::parseInt(*row);
                if (rowNumber <= 0) {
                    throw core::MathCalculatorError("Select a data row");
                }
                statistics_.removeAt(static_cast<std::size_t>(rowNumber - 1));
                printStatistics();
            } else if (selection == 4) {
                statistics_.clear();
                std::cout << "Data cleared.\n";
            } else {
                std::cout << "Invalid input\n";
            }
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

void ConsoleApplication::equationMode() {
    std::cout << "\n[Quadratic Equation | ax^2 + bx + c = 0]\n";
    try {
        const auto aText = ConsoleInput::readLine("a (:back): ");
        if (!aText.has_value() || isBackCommand(*aText)) return;
        const auto bText = ConsoleInput::readLine("b: ");
        if (!bText.has_value()) return;
        const auto cText = ConsoleInput::readLine("c: ");
        if (!cText.has_value()) return;
        const auto solution = equation_.solve(
            ConsoleInput::parseDouble(*aText),
            ConsoleInput::parseDouble(*bText),
            ConsoleInput::parseDouble(*cText));
        for (const std::string& line : equation_.formatSolution(solution, calculator_.state())) {
            std::cout << line << "\n";
        }
    } catch (const std::exception& error) {
        printError(error);
    }
}

void ConsoleApplication::complexMode() {
    while (true) {
        std::cout << "\n[Complex Number | " << calculator_.state().angleModeName() << "]\n"
                  << "1. Rectangular input (a + bj)\n"
                  << "2. Polar input (r < theta)\n"
                  << "0. Back\n";
        const auto input = ConsoleInput::readLine("Select: ");
        if (!input.has_value()) return;
        try {
            const int selection = ConsoleInput::parseInt(*input);
            if (selection == 0) return;
            modes::ComplexSummary summary;
            if (selection == 1) {
