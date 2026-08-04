double ConsoleInput::parseDouble(const std::string& text) {
    const std::string cleaned = trim(text);
    if (cleaned.empty()) {
        throw core::InvalidInputError();
    }
    char* end = nullptr;
    errno = 0;
    const double value = std::strtod(cleaned.c_str(), &end);
    if (errno == ERANGE || end == nullptr || *end != '\0' || !std::isfinite(value)) {
        throw core::InvalidInputError();
    }
    return value;
}

int ConsoleInput::parseInt(const std::string& text) {
    const double value = parseDouble(text);
    if (std::trunc(value) != value || value < std::numeric_limits<int>::min() ||
        value > std::numeric_limits<int>::max()) {
        throw core::InvalidInputError();
    }
    return static_cast<int>(value);
}

std::string ConsoleInput::trim(const std::string& text) {
    const std::size_t first = text.find_first_not_of(" \t\r\n");
    if (first == std::string::npos) {
        return {};
    }
    const std::size_t last = text.find_last_not_of(" \t\r\n");
    return text.substr(first, last - first + 1);
}

}  // namespace calculator::app


// ---- app/ConsoleApplication.cpp ----
namespace calculator::app {

int ConsoleApplication::run() {
    while (true) {
        printHeader();
        printMainMenu();
        const auto input = ConsoleInput::readLine("Select: ");
        if (!input.has_value()) {
            std::cout << "\nGoodbye.\n";
            return 0;
        }

        try {
            const int selection = ConsoleInput::parseInt(*input);
            switch (selection) {
            case 1: calculateMode(); break;
            case 2: statisticsMode(); break;
            case 3: equationMode(); break;
            case 4: complexMode(); break;
            case 5: settingsMode(); break;
            case 6: historyMode(); break;
            case 0:
                std::cout << "Goodbye.\n";
                return 0;
            default:
                std::cout << "Invalid input\n";
                break;
            }
        } catch (const std::exception& error) {
            printError(error);
        }
    }
}

