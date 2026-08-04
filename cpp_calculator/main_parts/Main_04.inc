                const auto real = ConsoleInput::readLine("Real part: ");
                const auto imaginary = ConsoleInput::readLine("Imaginary part: ");
                if (!real.has_value() || !imaginary.has_value()) return;
                summary = complex_.fromRectangular(
                    ConsoleInput::parseDouble(*real),
                    ConsoleInput::parseDouble(*imaginary));
            } else if (selection == 2) {
                const auto magnitude = ConsoleInput::readLine("Magnitude: ");
                const auto phase = ConsoleInput::readLine(
                    "Phase (" + calculator_.state().angleModeName() + "): ");
                if (!magnitude.has_value() || !phase.has_value()) return;
                summary = complex_.fromPolar(
                    ConsoleInput::parseDouble(*magnitude),
                    ConsoleInput::parseDouble(*phase),
                    calculator_.state().angleMode());
            } else {
                std::cout << "Invalid input\n";
                continue;
            }
            for (const std::string& line : complex_.formatSummary(summary, calculator_.state())) {
                std::cout << line << "\n";
            }
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

void ConsoleApplication::settingsMode() {
    while (true) {
        std::cout << "\n[Settings]\n"
                  << "1. Cycle angle mode (current: " << calculator_.state().angleModeName() << ")\n"
                  << "2. Cycle display format (current: " << calculator_.state().displayModeName() << ")\n"
                  << "0. Back\n";
        const auto input = ConsoleInput::readLine("Select: ");
        if (!input.has_value()) return;
        try {
            const int selection = ConsoleInput::parseInt(*input);
            if (selection == 0) return;
            if (selection == 1) {
                calculator_.state().cycleAngleMode();
            } else if (selection == 2) {
                calculator_.state().cycleDisplayMode();
            } else {
                std::cout << "Invalid input\n";
            }
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

void ConsoleApplication::historyMode() {
    while (true) {
        printHistory();
        std::cout << "Enter a history number to calculate again, c to clear, or 0 to go back.\n";
        const auto input = ConsoleInput::readLine("Select: ");
        if (!input.has_value()) return;
        const std::string cleaned = ConsoleInput::trim(*input);
        if (cleaned == "0" || cleaned == ":back") return;
        if (cleaned == "c" || cleaned == "C") {
            calculator_.history().clear();
            std::cout << "History cleared.\n";
            continue;
        }
        try {
            const int selection = ConsoleInput::parseInt(cleaned);
            if (selection <= 0 || static_cast<std::size_t>(selection) > calculator_.history().size()) {
                throw core::InvalidInputError();
            }
