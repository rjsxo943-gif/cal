        SetWindowTextW(buttonHandles_[IdShift], shiftActive_ ? L"SHIFT ON" : L"SHIFT");
        SetWindowTextW(buttonHandles_[IdSin], shiftActive_ ? L"asin" : L"sin");
        SetWindowTextW(buttonHandles_[IdCos], shiftActive_ ? L"acos" : L"cos");
        SetWindowTextW(buttonHandles_[IdTan], shiftActive_ ? L"atan" : L"tan");
        SetWindowTextW(buttonHandles_[IdLog], shiftActive_ ? L"10ˣ" : L"log");
        SetWindowTextW(buttonHandles_[IdLn], shiftActive_ ? L"eˣ" : L"ln");
        SetWindowTextW(buttonHandles_[IdSqrt], shiftActive_ ? L"ⁿ√" : L"√");
    }

    void insertExpression(const std::string& insertion) {
        const std::wstring wide = utf8ToWide(insertion);
        DWORD start = 0;
        DWORD end = 0;
        SendMessageW(
            expressionEdit_, EM_GETSEL,
            reinterpret_cast<WPARAM>(&start),
            reinterpret_cast<LPARAM>(&end));
        SendMessageW(
            expressionEdit_, EM_REPLACESEL, TRUE,
            reinterpret_cast<LPARAM>(wide.c_str()));
        const DWORD next = start + static_cast<DWORD>(wide.size());
        SendMessageW(expressionEdit_, EM_SETSEL, next, next);
        SetFocus(expressionEdit_);
    }

    void moveCursor(int direction) {
        DWORD start = 0;
        DWORD end = 0;
        SendMessageW(
            expressionEdit_, EM_GETSEL,
            reinterpret_cast<WPARAM>(&start),
            reinterpret_cast<LPARAM>(&end));
        const int length = GetWindowTextLengthW(expressionEdit_);
        int position = static_cast<int>(end);
        position = std::clamp(position + direction, 0, length);
        SendMessageW(expressionEdit_, EM_SETSEL, position, position);
        SetFocus(expressionEdit_);
    }

    void deleteAtCursor() {
        DWORD start = 0;
        DWORD end = 0;
        SendMessageW(
            expressionEdit_, EM_GETSEL,
            reinterpret_cast<WPARAM>(&start),
            reinterpret_cast<LPARAM>(&end));
        if (start == end && start > 0) {
            --start;
            SendMessageW(expressionEdit_, EM_SETSEL, start, end);
        }
        SendMessageW(
            expressionEdit_, EM_REPLACESEL, TRUE,
            reinterpret_cast<LPARAM>(L""));
        SetFocus(expressionEdit_);
    }

    void clearCalculator() {
        SetWindowTextW(expressionEdit_, L"");
        SetWindowTextW(resultEdit_, L"0");
        controller_.clearDisplayState();
        shiftActive_ = false;
        updateShiftButtons();
        updateStatus();
        SetFocus(expressionEdit_);
    }

    void calculateExpression() {
        try {
            const std::string expression = wideToUtf8(
                getWindowTextString(expressionEdit_));
            const std::string result = controller_.calculate(expression);
            setWindowTextUtf8(resultEdit_, result);
            refreshHistory();
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(resultEdit_, error.what());
        } catch (...) {
            SetWindowTextW(resultEdit_, L"Invalid input");
        }
    }

    void toggleFraction() {
        try {
            setWindowTextUtf8(resultEdit_, controller_.toggleFractionDisplay());
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(resultEdit_, error.what());
        }
    }

    void refreshFormattedResult() {
        if (!controller_.state().lastResult().has_value()) {
            return;
        }
        try {
            setWindowTextUtf8(resultEdit_, controller_.refreshLastResult());
        } catch (const CalculatorError& error) {
            setWindowTextUtf8(resultEdit_, error.what());
        }
    }

    void refreshHistory() {
        SendMessageW(historyList_, LB_RESETCONTENT, 0, 0);
        for (const auto& entry : controller_.history().entries()) {
            const std::string text =
                entry.expression + " = " + controller_.formatValue(entry.value);
            const std::wstring wide = utf8ToWide(text);
            SendMessageW(
                historyList_, LB_ADDSTRING, 0,
                reinterpret_cast<LPARAM>(wide.c_str()));
        }
        const auto count = controller_.history().size();
        if (count > 0) {
            SendMessageW(historyList_, LB_SETTOPINDEX, count - 1, 0);
        }
    }

    void addStatisticsValues() {
        try {
            statistics_.addValues(wideToUtf8(getWindowTextString(statInput_)));
            SetWindowTextW(statInput_, L"");
            refreshStatistics();
