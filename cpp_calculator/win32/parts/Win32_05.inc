        addPageControl(AppMode::Complex, complexLabelSecond_);
        complexSecond_ = createControl(
            L"EDIT", L"", WS_CHILD | WS_TABSTOP | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 220, 288, 300, 42, IdComplexSecond, displayFont_);
        addPageControl(AppMode::Complex, complexSecond_);

        addPageControl(AppMode::Complex, createControl(
            L"BUTTON", L"Convert",
            WS_CHILD | WS_TABSTOP | BS_DEFPUSHBUTTON,
            0, 20, 355, 250, 45, IdComplexSolve, boldFont_));

        complexResult_ = createControl(
            L"EDIT", L"",
            WS_CHILD | ES_MULTILINE | ES_READONLY | WS_VSCROLL,
            WS_EX_CLIENTEDGE, 20, 420, 790, 285, IdComplexResult, displayFont_);
        addPageControl(AppMode::Complex, complexResult_);
    }

    void handleCommand(int id, int notification, HWND control) {
        if (notification == BN_CLICKED) {
            switch (id) {
            case IdModeCalc: switchMode(AppMode::Calc); return;
            case IdModeStat: switchMode(AppMode::Statistics); return;
            case IdModeEqn: switchMode(AppMode::Equation); return;
            case IdModeComplex: switchMode(AppMode::Complex); return;
            case IdShift: toggleShift(); return;
            case IdDrg:
                controller_.state().cycleAngleMode();
                updateStatus();
                refreshFormattedResult();
                return;
            case IdFormat:
                controller_.state().cycleDisplayMode();
                updateStatus();
                refreshFormattedResult();
                return;
            case IdFraction: toggleFraction(); return;
            case IdCursorLeft: moveCursor(-1); return;
            case IdCursorRight: moveCursor(1); return;
            case IdDelete: deleteAtCursor(); return;
            case IdClear: clearCalculator(); return;
            case IdEquals: calculateExpression(); return;
            case IdHistoryClear:
                controller_.history().clear();
                refreshHistory();
                return;
            case IdStatAdd: addStatisticsValues(); return;
            case IdStatRemove: removeStatisticsValue(); return;
            case IdStatClear:
                statistics_.clear();
                refreshStatistics();
                return;
            case IdEqnSolve: solveEquation(); return;
            case IdComplexRect:
                complexPolarMode_ = false;
                updateComplexLabels();
                return;
            case IdComplexPolar:
                complexPolarMode_ = true;
                updateComplexLabels();
                return;
            case IdComplexSolve: solveComplex(); return;
            default:
                break;
            }

            const auto insertion = insertionById_.find(id);
            if (insertion != insertionById_.end()) {
                insertExpression(currentInsertion(id));
                if (shiftActive_ && isShiftable(id)) {
                    shiftActive_ = false;
                    updateShiftButtons();
                    updateStatus();
                }
                return;
            }
        }

        if (id == IdHistory && notification == LBN_DBLCLK) {
            const int selected = static_cast<int>(
                SendMessageW(historyList_, LB_GETCURSEL, 0, 0));
            if (selected != LB_ERR &&
                static_cast<std::size_t>(selected) < controller_.history().size()) {
                const auto& entry = controller_.history().at(
                    static_cast<std::size_t>(selected));
                setWindowTextUtf8(expressionEdit_, entry.expression);
                switchMode(AppMode::Calc);
                SetFocus(expressionEdit_);
                SendMessageW(expressionEdit_, EM_SETSEL, -1, -1);
            }
        }
    }

    std::string currentInsertion(int id) const {
        if (!shiftActive_) {
            return insertionById_.at(id);
        }
        switch (id) {
        case IdSin: return "asin(";
        case IdCos: return "acos(";
        case IdTan: return "atan(";
        case IdLog: return "10^(";
        case IdLn: return "e^(";
        case IdSqrt: return "root(";
        default: return insertionById_.at(id);
        }
    }

    static bool isShiftable(int id) {
        return id == IdSin || id == IdCos || id == IdTan ||
               id == IdLog || id == IdLn || id == IdSqrt;
    }

    void toggleShift() {
        shiftActive_ = !shiftActive_;
        updateShiftButtons();
        updateStatus();
    }

    void updateShiftButtons() {
