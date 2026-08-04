

// ---- main.cpp ----
#ifdef _WIN32
#include <windows.h>
#endif

namespace {

void configureUtf8Console() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void printHelp() {
    std::cout
        << "Scientific Calculator C++ 1.0\n\n"
        << "Interactive mode:\n"
        << "  scientific_calculator\n\n"
        << "Single expression mode:\n"
        << "  scientific_calculator --eval \"2+3*4\" [--angle DEG|RAD|GRAD]"
           " [--format NORM|FIX|FIX4|SCI|SCI4]\n\n"
        << "Other options:\n"
        << "  --help       Show this help\n"
        << "  --version    Show version\n";
}

calculator::core::AngleMode parseAngle(const std::string& value) {
    if (value == "DEG") return calculator::core::AngleMode::Degree;
    if (value == "RAD") return calculator::core::AngleMode::Radian;
    if (value == "GRAD") return calculator::core::AngleMode::Gradian;
    throw calculator::core::InvalidInputError();
}

calculator::core::DisplayMode parseFormat(const std::string& value) {
    if (value == "NORM") return calculator::core::DisplayMode::Normal;
    if (value == "FIX" || value == "FIX4") return calculator::core::DisplayMode::Fixed;
    if (value == "SCI" || value == "SCI4") return calculator::core::DisplayMode::Scientific;
    throw calculator::core::InvalidInputError();
}

int runCommandLine(const std::vector<std::string>& arguments) {
    if (arguments.size() == 1 && arguments[0] == "--help") {
        printHelp();
        return 0;
    }
    if (arguments.size() == 1 && arguments[0] == "--version") {
        std::cout << "Scientific Calculator C++ 1.0.0\n";
        return 0;
    }

    std::string expression;
    calculator::core::AngleMode angleMode = calculator::core::AngleMode::Degree;
    calculator::core::DisplayMode displayMode = calculator::core::DisplayMode::Normal;

    for (std::size_t index = 0; index < arguments.size(); ++index) {
        const std::string& option = arguments[index];
        if (option == "--eval") {
            if (++index >= arguments.size() || !expression.empty()) {
                std::cerr << "Invalid command-line options\n";
                return 2;
            }
            expression = arguments[index];
        } else if (option == "--angle") {
            if (++index >= arguments.size()) {
                std::cerr << "Invalid command-line options\n";
                return 2;
            }
            try {
                angleMode = parseAngle(arguments[index]);
            } catch (const calculator::core::CalculatorError&) {
                std::cerr << "Invalid command-line options\n";
                return 2;
