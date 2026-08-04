        DWORD extendedStyle, int x, int y, int width, int height, int id,
        HFONT font = nullptr) {
        HWND control = CreateWindowExW(
            extendedStyle, className, text, style,
            x, y, width, height, window_,
            reinterpret_cast<HMENU>(static_cast<INT_PTR>(id)),
            instance_, nullptr);
        SendMessageW(control, WM_SETFONT, reinterpret_cast<WPARAM>(font ? font : font_), TRUE);
        return control;
    }

    void createModeButton(int id, const wchar_t* label, int x) {
        createControl(
            L"BUTTON", label,
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON,
            0, x, 58, 90, 34, id, boldFont_);
    }

    void createHistoryPanel() {
        createControl(
            L"STATIC", L"History",
            WS_CHILD | WS_VISIBLE, 0, 835, 20, 235, 28, 700, boldFont_);
        historyList_ = createControl(
            L"LISTBOX", L"",
            WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL |
                LBS_NOTIFY | LBS_NOINTEGRALHEIGHT,
            WS_EX_CLIENTEDGE, 835, 52, 235, 650, IdHistory, font_);
        createControl(
            L"BUTTON", L"Clear history",
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON,
            0, 835, 712, 235, 36, IdHistoryClear, font_);
    }

    void addPageControl(AppMode mode, HWND control) {
        switch (mode) {
        case AppMode::Calc: calcControls_.push_back(control); break;
        case AppMode::Statistics: statControls_.push_back(control); break;
        case AppMode::Equation: equationControls_.push_back(control); break;
        case AppMode::Complex: complexControls_.push_back(control); break;
        }
    }

    void createCalculatorPage() {
        expressionEdit_ = createControl(
            L"EDIT", L"",
            WS_CHILD | WS_VISIBLE | WS_TABSTOP | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 20, 105, 790, 44, IdExpression, displayFont_);
        addPageControl(AppMode::Calc, expressionEdit_);
        SetWindowSubclass(
            expressionEdit_, expressionProcedure, 1,
            reinterpret_cast<DWORD_PTR>(this));

        resultEdit_ = createControl(
            L"EDIT", L"0",
            WS_CHILD | WS_VISIBLE | ES_RIGHT | ES_READONLY | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 20, 154, 790, 58, IdResult, resultFont_);
        addPageControl(AppMode::Calc, resultEdit_);

        const std::array<CalculatorButton, 48> buttons{{
            {IdShift, L"SHIFT", nullptr},
            {IdDrg, L"DRG", nullptr},
            {IdFormat, L"FMT", nullptr},
            {IdFraction, L"S⇔D", nullptr},
            {IdCursorLeft, L"◀", nullptr},
            {IdDelete, L"DEL", nullptr},

            {IdSin, L"sin", "sin("},
            {IdCos, L"cos", "cos("},
            {IdTan, L"tan", "tan("},
            {IdLog, L"log", "log("},
            {IdLn, L"ln", "ln("},
            {IdSqrt, L"√", "sqrt("},

            {IdNpr, L"nPr", "npr("},
            {IdNcr, L"nCr", "ncr("},
            {IdGcd, L"GCD", "gcd("},
            {IdLcm, L"LCM", "lcm("},
            {IdMod, L"MOD", "mod("},
            {IdAbs, L"ABS", "abs("},

            {Id7, L"7", "7"},
            {Id8, L"8", "8"},
            {Id9, L"9", "9"},
            {IdLeftParen, L"(", "("},
            {IdRightParen, L")", ")"},
            {IdDivide, L"÷", "/"},

            {Id4, L"4", "4"},
            {Id5, L"5", "5"},
            {Id6, L"6", "6"},
            {IdMultiply, L"×", "*"},
            {IdPercent, L"%", "%"},
            {IdFactorial, L"x!", "!"},

            {Id1, L"1", "1"},
            {Id2, L"2", "2"},
            {Id3, L"3", "3"},
            {IdMinus, L"−", "-"},
            {IdPi, L"π", "pi"},
            {IdE, L"e", "e"},

            {Id0, L"0", "0"},
            {IdDecimal, L".", "."},
            {IdAns, L"Ans", "Ans"},
            {IdPlus, L"+", "+"},
            {IdClear, L"AC", nullptr},
            {IdEquals, L"=", nullptr},

            {IdReciprocal, L"1/x", "recip("},
            {IdQuot, L"QUOT", "quot("},
            {IdRem, L"REM", "rem("},
            {IdRandom, L"Ran#", "random()"},
            {IdRandInt, L"RanInt", "randint("},
            {IdCursorRight, L"▶", nullptr}
        }};

        const int startX = 20;
        const int startY = 222;
        const int buttonWidth = 126;
        const int buttonHeight = 51;
