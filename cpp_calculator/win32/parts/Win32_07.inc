        } catch (const CalculatorError& error) {
            setWindowTextUtf8(statSummary_, error.what());
        }
    }

    void removeStatisticsValue() {
        try {
            const int selected = static_cast<int>(
                SendMessageW(statList_, LB_GETCURSEL, 0, 0));
            if (selected == LB_ERR) {
                throw calculator::core::MathCalculatorError("Select a data row");
            }
            statistics_.removeAt(static_cast<std::size_t>(selected));
            refreshStatistics();
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(statSummary_, error.what());
        }
    }

    void refreshStatistics() {
        SendMessageW(statList_, LB_RESETCONTENT, 0, 0);
        for (double value : statistics_.values()) {
            const std::wstring text = utf8ToWide(controller_.formatValue(value));
            SendMessageW(
                statList_, LB_ADDSTRING, 0,
                reinterpret_cast<LPARAM>(text.c_str()));
        }

        const auto summary = statistics_.summary();
        if (summary.count == 0) {
            SetWindowTextW(statSummary_, L"No data");
            return;
        }

        const auto valueText = [this](const std::optional<double>& value) {
            return value.has_value() ? controller_.formatValue(*value) : std::string("N/A");
        };

        std::ostringstream output;
        output
            << "n = " << summary.count << "\r\n"
            << "sum = " << controller_.formatValue(summary.total) << "\r\n"
            << "mean = " << valueText(summary.mean) << "\r\n"
            << "min = " << valueText(summary.minimum) << "\r\n"
            << "max = " << valueText(summary.maximum) << "\r\n\r\n"
            << "population variance = " << valueText(summary.populationVariance) << "\r\n"
            << "population std dev = " << valueText(summary.populationStandardDeviation) << "\r\n"
            << "sample variance = " << valueText(summary.sampleVariance) << "\r\n"
            << "sample std dev = " << valueText(summary.sampleStandardDeviation);
        setWindowTextUtf8(statSummary_, output.str());
    }

    void solveEquation() {
        try {
            const auto solution = equation_.solve(
                parseDouble(eqnA_), parseDouble(eqnB_), parseDouble(eqnC_));
            const auto lines = equation_.formatSolution(
                solution, controller_.state());
            std::string result;
            for (const auto& line : lines) {
                if (!result.empty()) {
                    result += "\r\n";
                }
                result += line;
            }
            setWindowTextUtf8(eqnResult_, result);
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(eqnResult_, error.what());
        }
    }

    void updateComplexLabels() {
        if (complexPolarMode_) {
            SetWindowTextW(complexLabelFirst_, L"Magnitude");
            SetWindowTextW(complexLabelSecond_, L"Phase");
        } else {
            SetWindowTextW(complexLabelFirst_, L"Real part");
            SetWindowTextW(complexLabelSecond_, L"Imaginary part");
        }
    }

    void solveComplex() {
        try {
            const double first = parseDouble(complexFirst_);
            const double second = parseDouble(complexSecond_);
            const auto summary = complexPolarMode_
                ? complex_.fromPolar(first, second, controller_.state().angleMode())
                : complex_.fromRectangular(first, second);
            const auto lines = complex_.formatSummary(
                summary, controller_.state());
            std::string result;
            for (const auto& line : lines) {
                if (!result.empty()) {
                    result += "\r\n";
                }
                result += line;
            }
            setWindowTextUtf8(complexResult_, result);
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(complexResult_, error.what());
        }
    }

    void switchMode(AppMode mode) {
        mode_ = mode;
        showPage(calcControls_, mode == AppMode::Calc);
        showPage(statControls_, mode == AppMode::Statistics);
        showPage(equationControls_, mode == AppMode::Equation);
        showPage(complexControls_, mode == AppMode::Complex);

        if (mode == AppMode::Calc) {
            SetFocus(expressionEdit_);
        } else if (mode == AppMode::Statistics) {
            SetFocus(statInput_);
        } else if (mode == AppMode::Equation) {
            SetFocus(eqnA_);
        } else {
            SetFocus(complexFirst_);
        }
        updateStatus();
