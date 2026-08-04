    }

    static void showPage(const std::vector<HWND>& controls, bool visible) {
        for (HWND control : controls) {
            ShowWindow(control, visible ? SW_SHOW : SW_HIDE);
        }
    }

    void updateStatus() {
        std::wstring modeName;
        switch (mode_) {
        case AppMode::Calc: modeName = L"CALC"; break;
        case AppMode::Statistics: modeName = L"STAT"; break;
        case AppMode::Equation: modeName = L"EQN"; break;
        case AppMode::Complex: modeName = L"CMPLX"; break;
        }

        const std::wstring angle = utf8ToWide(controller_.state().angleModeName());
        const std::wstring format = utf8ToWide(controller_.state().displayModeName());
        std::wstring status = angle + L"   " + format + L"   " + modeName;
        if (shiftActive_) {
            status += L"   SHIFT";
        }
        SetWindowTextW(status_, status.c_str());
    }

    LRESULT colorStatic(HDC deviceContext, HWND control) {
        if (control == resultEdit_) {
            SetBkColor(deviceContext, RGB(25, 32, 43));
            SetTextColor(deviceContext, RGB(118, 240, 181));
            return reinterpret_cast<LRESULT>(displayBrush_);
        }
        if (control == statSummary_ || control == eqnResult_ ||
            control == complexResult_) {
            SetBkColor(deviceContext, RGB(255, 255, 255));
            SetTextColor(deviceContext, RGB(20, 28, 38));
            return reinterpret_cast<LRESULT>(panelBrush_);
        }
        if (control == status_ || control == title_) {
            SetBkMode(deviceContext, TRANSPARENT);
            SetTextColor(deviceContext, RGB(33, 45, 60));
            return reinterpret_cast<LRESULT>(backgroundBrush_);
        }
        SetBkMode(deviceContext, TRANSPARENT);
        SetTextColor(deviceContext, RGB(42, 53, 68));
        return reinterpret_cast<LRESULT>(backgroundBrush_);
    }

    LRESULT colorEdit(HDC deviceContext, HWND control) {
        if (control == resultEdit_) {
            SetBkColor(deviceContext, RGB(25, 32, 43));
            SetTextColor(deviceContext, RGB(118, 240, 181));
            return reinterpret_cast<LRESULT>(displayBrush_);
        }
        if (control == expressionEdit_) {
            SetBkColor(deviceContext, RGB(25, 32, 43));
            SetTextColor(deviceContext, RGB(244, 247, 250));
            return reinterpret_cast<LRESULT>(displayBrush_);
        }
        SetBkColor(deviceContext, RGB(255, 255, 255));
        SetTextColor(deviceContext, RGB(20, 28, 38));
        return reinterpret_cast<LRESULT>(panelBrush_);
    }

    void destroyResources() {
        if (expressionEdit_) {
            RemoveWindowSubclass(expressionEdit_, expressionProcedure, 1);
        }
        DeleteObject(font_);
        DeleteObject(boldFont_);
        DeleteObject(titleFont_);
        DeleteObject(displayFont_);
        DeleteObject(resultFont_);
        DeleteObject(backgroundBrush_);
        DeleteObject(displayBrush_);
        DeleteObject(panelBrush_);
    }

    HINSTANCE instance_{};
    HWND window_{};

    HFONT font_{};
    HFONT boldFont_{};
    HFONT titleFont_{};
    HFONT displayFont_{};
    HFONT resultFont_{};
    HBRUSH backgroundBrush_{};
    HBRUSH displayBrush_{};
    HBRUSH panelBrush_{};

    HWND title_{};
    HWND status_{};
    HWND historyList_{};

    HWND expressionEdit_{};
    HWND resultEdit_{};

    HWND statInput_{};
    HWND statList_{};
    HWND statSummary_{};

    HWND eqnA_{};
    HWND eqnB_{};
    HWND eqnC_{};
    HWND eqnResult_{};

    HWND complexRect_{};
    HWND complexPolar_{};
    HWND complexLabelFirst_{};
    HWND complexLabelSecond_{};
    HWND complexFirst_{};
    HWND complexSecond_{};
    HWND complexResult_{};

    std::vector<HWND> calcControls_;
    std::vector<HWND> statControls_;
    std::vector<HWND> equationControls_;
    std::vector<HWND> complexControls_;
    std::unordered_map<int, HWND> buttonHandles_;
    std::unordered_map<int, std::string> insertionById_;
