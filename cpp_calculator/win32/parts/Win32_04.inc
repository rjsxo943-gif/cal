        const int gap = 8;

        for (std::size_t index = 0; index < buttons.size(); ++index) {
            const int row = static_cast<int>(index / 6);
            const int column = static_cast<int>(index % 6);
            HWND button = createControl(
                L"BUTTON", buttons[index].label,
                WS_CHILD | WS_VISIBLE | WS_TABSTOP |
                    (buttons[index].id == IdEquals ? BS_DEFPUSHBUTTON : BS_PUSHBUTTON),
                0,
                startX + column * (buttonWidth + gap),
                startY + row * (buttonHeight + gap),
                buttonWidth, buttonHeight, buttons[index].id,
                (buttons[index].id == IdEquals || buttons[index].id == IdClear)
                    ? boldFont_ : font_);
            addPageControl(AppMode::Calc, button);
            buttonHandles_[buttons[index].id] = button;
            if (buttons[index].insertion) {
                insertionById_[buttons[index].id] = buttons[index].insertion;
            }
        }
    }

    void createStatisticsPage() {
        addPageControl(AppMode::Statistics, createControl(
            L"STATIC", L"Enter numbers separated by spaces, commas, or semicolons.",
            WS_CHILD, 0, 20, 115, 790, 28, IdStatInstruction, boldFont_));

        statInput_ = createControl(
            L"EDIT", L"", WS_CHILD | WS_TABSTOP | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 20, 150, 500, 38, IdStatInput, font_);
        addPageControl(AppMode::Statistics, statInput_);

        addPageControl(AppMode::Statistics, createControl(
            L"BUTTON", L"Add", WS_CHILD | WS_TABSTOP | BS_PUSHBUTTON,
            0, 532, 150, 88, 38, IdStatAdd, boldFont_));
        addPageControl(AppMode::Statistics, createControl(
            L"BUTTON", L"Remove", WS_CHILD | WS_TABSTOP | BS_PUSHBUTTON,
            0, 630, 150, 88, 38, IdStatRemove, font_));
        addPageControl(AppMode::Statistics, createControl(
            L"BUTTON", L"Clear", WS_CHILD | WS_TABSTOP | BS_PUSHBUTTON,
            0, 728, 150, 82, 38, IdStatClear, font_));

        statList_ = createControl(
            L"LISTBOX", L"",
            WS_CHILD | WS_BORDER | WS_VSCROLL | LBS_NOTIFY | LBS_NOINTEGRALHEIGHT,
            WS_EX_CLIENTEDGE, 20, 205, 330, 500, IdStatList, font_);
        addPageControl(AppMode::Statistics, statList_);

        statSummary_ = createControl(
            L"EDIT", L"No data",
            WS_CHILD | ES_MULTILINE | ES_READONLY | WS_VSCROLL,
            WS_EX_CLIENTEDGE, 370, 205, 440, 500, IdStatSummary, displayFont_);
        addPageControl(AppMode::Statistics, statSummary_);
    }

    void createEquationPage() {
        addPageControl(AppMode::Equation, createControl(
            L"STATIC", L"Solve ax² + bx + c = 0",
            WS_CHILD, 0, 20, 120, 790, 34, IdEqnInstruction, titleFont_));

        createEquationInput(L"a", IdEqnLabelA, IdEqnA, 180);
        createEquationInput(L"b", IdEqnLabelB, IdEqnB, 235);
        createEquationInput(L"c", IdEqnLabelC, IdEqnC, 290);

        eqnA_ = GetDlgItem(window_, IdEqnA);
        eqnB_ = GetDlgItem(window_, IdEqnB);
        eqnC_ = GetDlgItem(window_, IdEqnC);

        addPageControl(AppMode::Equation, createControl(
            L"BUTTON", L"Solve equation",
            WS_CHILD | WS_TABSTOP | BS_DEFPUSHBUTTON,
            0, 20, 355, 250, 45, IdEqnSolve, boldFont_));

        eqnResult_ = createControl(
            L"EDIT", L"",
            WS_CHILD | ES_MULTILINE | ES_READONLY | WS_VSCROLL,
            WS_EX_CLIENTEDGE, 20, 420, 790, 285, IdEqnResult, displayFont_);
        addPageControl(AppMode::Equation, eqnResult_);
    }

    void createEquationInput(
        const wchar_t* label, int labelId, int editId, int y) {
        addPageControl(AppMode::Equation, createControl(
            L"STATIC", label, WS_CHILD | SS_CENTER,
            0, 20, y + 5, 50, 34, labelId, boldFont_));
        addPageControl(AppMode::Equation, createControl(
            L"EDIT", L"", WS_CHILD | WS_TABSTOP | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 78, y, 310, 40, editId, displayFont_));
    }

    void createComplexPage() {
        addPageControl(AppMode::Complex, createControl(
            L"STATIC", L"Complex number converter",
            WS_CHILD, 0, 20, 120, 790, 34, IdComplexInstruction, titleFont_));

        complexRect_ = createControl(
            L"BUTTON", L"Rectangular",
            WS_CHILD | WS_TABSTOP | BS_AUTORADIOBUTTON | WS_GROUP,
            0, 20, 175, 160, 36, IdComplexRect, font_);
        addPageControl(AppMode::Complex, complexRect_);
        complexPolar_ = createControl(
            L"BUTTON", L"Polar",
            WS_CHILD | WS_TABSTOP | BS_AUTORADIOBUTTON,
            0, 190, 175, 160, 36, IdComplexPolar, font_);
        addPageControl(AppMode::Complex, complexPolar_);
        SendMessageW(complexRect_, BM_SETCHECK, BST_CHECKED, 0);

        complexLabelFirst_ = createControl(
            L"STATIC", L"Real part", WS_CHILD,
            0, 20, 235, 190, 30, IdComplexLabelFirst, boldFont_);
        addPageControl(AppMode::Complex, complexLabelFirst_);
        complexFirst_ = createControl(
            L"EDIT", L"", WS_CHILD | WS_TABSTOP | ES_AUTOHSCROLL,
            WS_EX_CLIENTEDGE, 220, 228, 300, 42, IdComplexFirst, displayFont_);
        addPageControl(AppMode::Complex, complexFirst_);

        complexLabelSecond_ = createControl(
            L"STATIC", L"Imaginary part", WS_CHILD,
            0, 20, 295, 190, 30, IdComplexLabelSecond, boldFont_);
