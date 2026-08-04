void ConsoleApplication::printHeader() const {
    std::cout << "\n==================================================\n"
              << "          Scientific Calculator C++\n"
              << "==================================================\n"
              << "Angle: " << calculator_.state().angleModeName()
              << "    Format: " << calculator_.state().displayModeName()
              << "    Ans: " << calculator_.formatValue(calculator_.state().answer()) << "\n\n";
}

void ConsoleApplication::printMainMenu() const {
    std::cout << "1. Calculate\n"
              << "2. Statistics\n"
              << "3. Quadratic Equation\n"
              << "4. Complex Number\n"
              << "5. Settings\n"
              << "6. History\n"
              << "0. Exit\n\n";
}

void ConsoleApplication::calculateMode() {
    while (true) {
        std::cout << "\n[Calculate | " << calculator_.state().angleModeName()
                  << " | " << calculator_.state().displayModeName() << "]\n";
        const auto input = ConsoleInput::readLine(
            "Expression (:back, :history, :help, :drg, :fmt, :sd, :clear): ");
        if (!input.has_value() || isBackCommand(*input)) {
            return;
        }
        const std::string command = ConsoleInput::trim(*input);
        try {
            if (command == ":history") {
                printHistory();
            } else if (command == ":help") {
                printCalculateHelp();
            } else if (command == ":drg") {
                calculator_.state().cycleAngleMode();
                std::cout << "Angle: " << calculator_.state().angleModeName() << "\n";
            } else if (command == ":fmt") {
                calculator_.state().cycleDisplayMode();
                std::cout << "Format: " << calculator_.state().displayModeName() << "\n";
                if (calculator_.state().lastResult().has_value()) {
                    std::cout << "Result: " << calculator_.refreshLastResult() << "\n";
                }
            } else if (command == ":sd") {
                std::cout << "Result: " << calculator_.toggleFractionDisplay() << "\n";
            } else if (command == ":clear") {
                calculator_.clearDisplayState();
                std::cout << "Display cleared. Ans is unchanged.\n";
            } else if (!command.empty() && command.front() == ':') {
                std::cout << "Invalid input\n";
            } else {
                std::cout << "Result: " << calculator_.calculate(command) << "\n";
            }
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

void ConsoleApplication::statisticsMode() {
    while (true) {
        std::cout << "\n[Statistics | n=" << statistics_.values().size() << "]\n"
                  << "1. Add data\n2. Show data and summary\n3. Delete row\n4. Clear all\n0. Back\n";
        const auto input = ConsoleInput::readLine("Select: ");
        if (!input.has_value()) {
            return;
        }
        try {
            const int selection = ConsoleInput::parseInt(*input);
            if (selection == 0) {
