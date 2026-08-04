        }
        return static_cast<int>(message.wParam);
    }

private:
    static LRESULT CALLBACK windowProcedure(
        HWND window, UINT message, WPARAM wParam, LPARAM lParam) {
        CalculatorWindow* self = reinterpret_cast<CalculatorWindow*>(
            GetWindowLongPtrW(window, GWLP_USERDATA));

        if (message == WM_NCCREATE) {
            const auto* create = reinterpret_cast<CREATESTRUCTW*>(lParam);
            self = static_cast<CalculatorWindow*>(create->lpCreateParams);
            self->window_ = window;
            SetWindowLongPtrW(window, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(self));
        }

        if (self) {
            return self->handleMessage(message, wParam, lParam);
        }
        return DefWindowProcW(window, message, wParam, lParam);
    }

    static LRESULT CALLBACK expressionProcedure(
        HWND edit, UINT message, WPARAM wParam, LPARAM lParam,
        UINT_PTR, DWORD_PTR reference) {
        auto* self = reinterpret_cast<CalculatorWindow*>(reference);
        if (message == WM_KEYDOWN) {
            if (wParam == VK_RETURN) {
                self->calculateExpression();
                return 0;
            }
            if (wParam == VK_ESCAPE) {
                self->clearCalculator();
                return 0;
            }
        }
        return DefSubclassProc(edit, message, wParam, lParam);
    }

    LRESULT handleMessage(UINT message, WPARAM wParam, LPARAM lParam) {
        switch (message) {
        case WM_CREATE:
            createInterface();
            return 0;
        case WM_COMMAND:
            handleCommand(LOWORD(wParam), HIWORD(wParam), reinterpret_cast<HWND>(lParam));
            return 0;
        case WM_ERASEBKGND: {
            RECT area{};
            GetClientRect(window_, &area);
            HBRUSH brush = backgroundBrush_
                ? backgroundBrush_
                : reinterpret_cast<HBRUSH>(COLOR_WINDOW + 1);
            FillRect(reinterpret_cast<HDC>(wParam), &area, brush);
            return 1;
        }
        case WM_CTLCOLORSTATIC:
            return colorStatic(reinterpret_cast<HDC>(wParam), reinterpret_cast<HWND>(lParam));
        case WM_CTLCOLOREDIT:
            return colorEdit(reinterpret_cast<HDC>(wParam), reinterpret_cast<HWND>(lParam));
        case WM_DESTROY:
            destroyResources();
            PostQuitMessage(0);
            return 0;
        default:
            return DefWindowProcW(window_, message, wParam, lParam);
        }
    }

    void createInterface() {
        backgroundBrush_ = CreateSolidBrush(RGB(244, 247, 250));
        displayBrush_ = CreateSolidBrush(RGB(25, 32, 43));
        panelBrush_ = CreateSolidBrush(RGB(255, 255, 255));

        font_ = CreateFontW(
            -17, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");
        boldFont_ = CreateFontW(
            -18, 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");
        titleFont_ = CreateFontW(
            -27, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");
        displayFont_ = CreateFontW(
            -24, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, FIXED_PITCH | FF_MODERN, L"Cascadia Mono");
        resultFont_ = CreateFontW(
            -30, 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE,
            DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
            CLEARTYPE_QUALITY, FIXED_PITCH | FF_MODERN, L"Cascadia Mono");

        title_ = createControl(
            L"STATIC", L"Scientific Calculator", WS_CHILD | WS_VISIBLE,
            0, 20, 14, 430, 38, IdTitle, titleFont_);
        status_ = createControl(
            L"STATIC", L"", WS_CHILD | WS_VISIBLE | SS_RIGHT,
            0, 510, 22, 315, 30, IdStatus, boldFont_);

        createModeButton(IdModeCalc, L"CALC", 20);
        createModeButton(IdModeStat, L"STAT", 120);
        createModeButton(IdModeEqn, L"EQN", 220);
        createModeButton(IdModeComplex, L"CMPLX", 320);

        createHistoryPanel();
        createCalculatorPage();
        createStatisticsPage();
        createEquationPage();
        createComplexPage();

        switchMode(AppMode::Calc);
        updateStatus();
    }

    HWND createControl(
        const wchar_t* className, const wchar_t* text, DWORD style,
