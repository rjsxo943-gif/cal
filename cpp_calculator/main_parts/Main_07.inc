            }
        } else if (option == "--format") {
            if (++index >= arguments.size()) {
                std::cerr << "Invalid command-line options\n";
                return 2;
            }
            try {
                displayMode = parseFormat(arguments[index]);
            } catch (const calculator::core::CalculatorError&) {
                std::cerr << "Invalid command-line options\n";
                return 2;
            }
        } else {
            std::cerr << "Invalid command-line options\n";
            return 2;
        }
    }

    if (expression.empty()) {
        std::cerr << "Invalid command-line options\n";
        return 2;
    }

    calculator::core::CalculatorController calculator;
    calculator.state().setAngleMode(angleMode);
    calculator.state().setDisplayMode(displayMode);
    try {
        std::cout << calculator.calculate(expression) << '\n';
        return 0;
    } catch (const calculator::core::CalculatorError& error) {
        std::cout << error.what() << '\n';
        return 1;
    } catch (const std::exception&) {
        std::cout << "Invalid input\n";
        return 1;
    }
}

}  // namespace

int main(int argc, char* argv[]) {
    configureUtf8Console();
    if (argc > 1) {
        std::vector<std::string> arguments;
        arguments.reserve(static_cast<std::size_t>(argc - 1));
        for (int index = 1; index < argc; ++index) {
            arguments.emplace_back(argv[index]);
        }
        return runCommandLine(arguments);
    }

    calculator::app::ConsoleApplication application;
    return application.run();
}
