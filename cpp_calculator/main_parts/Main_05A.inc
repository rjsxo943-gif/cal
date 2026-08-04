            const std::string expression = calculator_.history().at(static_cast<std::size_t>(selection - 1)).expression;
            std::cout << expression << " = " << calculator_.calculate(expression) << "\n";
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

void ConsoleApplication::printStatistics() const {
    const auto summary = statistics_.summary();
    std::cout << "Data:";
    if (statistics_.values().empty()) {
        std::cout << " (empty)\n";
    } else {
        std::cout << "\n";
        for (std::size_t i = 0; i < statistics_.values().size(); ++i) {
            std::cout << "  " << (i + 1) << ". " << calculator_.formatValue(statistics_.values()[i]) << "\n";
        }
    }

    const auto show = [this](const char* label, const std::optional<double>& value) {
        std::cout << std::left << std::setw(7) << label << " "
                  << (value.has_value() ? calculator_.formatValue(*value) : "-") << "\n";
    };
    std::cout << "n       " << summary.count << "\n"
              << "Sum     " << calculator_.formatValue(summary.total) << "\n";
    show("Mean", summary.mean);
    show("Min", summary.minimum);
    show("Max", summary.maximum);
    show("PopVar", summary.populationVariance);
    show("PopSD", summary.populationStandardDeviation);
    show("SampVar", summary.sampleVariance);
    show("SampSD", summary.sampleStandardDeviation);
}

void ConsoleApplication::printHistory() const {
    std::cout << "\n[History]\n";
    if (calculator_.history().empty()) {
        std::cout << "No calculations yet.\n";
        return;
    }
    const auto& entries = calculator_.history().entries();
    for (std::size_t i = 0; i < entries.size(); ++i) {
        std::cout << (i + 1) << ". " << entries[i].expression
                  << " = " << calculator_.formatValue(entries[i].value) << "\n";
    }
}

void ConsoleApplication::printCalculateHelp() const {
    std::cout << "Operators: + - * / ^ ! % and parentheses\n"
              << "Constants: pi, e, Ans\n"
              << "Functions: sqrt sin cos tan asin acos atan log ln abs recip\n"
              << "           npr ncr mod gcd lcm quot rem root random randint\n"
              << "Examples: 2+3*4, sin(30), root(3,-8), ncr(10,3)\n";
}

bool ConsoleApplication::isBackCommand(const std::string& input) {
    return ConsoleInput::trim(input) == ":back";
}

void ConsoleApplication::printError(const std::exception& error) {
    std::cout << error.what() << "\n";
}

}  // namespace calculator::app
