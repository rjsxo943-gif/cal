#include "ScientificCalculator.h"

#include <cerrno>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <vector>

// ---- app/ConsoleInput.h ----
namespace calculator::app {

class ConsoleInput {
public:
    static std::optional<std::string> readLine(const std::string& prompt);
    static double parseDouble(const std::string& text);
    static int parseInt(const std::string& text);
    static std::string trim(const std::string& text);
};

}  // namespace calculator::app


// ---- app/ConsoleApplication.h ----
namespace calculator::app {

class ConsoleApplication {
public:
    int run();

private:
    void printHeader() const;
    void printMainMenu() const;
    void calculateMode();
    void statisticsMode();
    void equationMode();
    void complexMode();
    void settingsMode();
    void historyMode();

    void printStatistics() const;
    void printHistory() const;
    void printCalculateHelp() const;
    static bool isBackCommand(const std::string& input);
    static void printError(const std::exception& error);

    core::CalculatorController calculator_;
    modes::StatisticsController statistics_;
    modes::EquationController equation_;
    modes::ComplexController complex_;
};

}  // namespace calculator::app


// ---- app/ConsoleInput.cpp ----
namespace calculator::app {

std::optional<std::string> ConsoleInput::readLine(const std::string& prompt) {
    std::cout << prompt;
    std::string line;
    if (!std::getline(std::cin, line)) {
        return std::nullopt;
    }
    return line;
}

