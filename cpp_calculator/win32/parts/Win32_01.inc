    IdComplexLabelSecond,
    IdComplexSecond,
    IdComplexSolve,
    IdComplexResult
};

struct CalculatorButton {
    int id;
    const wchar_t* label;
    const char* insertion;
};

std::wstring utf8ToWide(const std::string& value) {
    if (value.empty()) {
        return {};
    }
    const int size = MultiByteToWideChar(
        CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
        static_cast<int>(value.size()), nullptr, 0);
    if (size <= 0) {
        return L"Invalid input";
    }
    std::wstring result(static_cast<std::size_t>(size), L'\0');
    MultiByteToWideChar(
        CP_UTF8, MB_ERR_INVALID_CHARS, value.data(),
        static_cast<int>(value.size()), result.data(), size);
    return result;
}

std::string wideToUtf8(const std::wstring& value) {
    if (value.empty()) {
        return {};
    }
    const int size = WideCharToMultiByte(
        CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
        static_cast<int>(value.size()), nullptr, 0, nullptr, nullptr);
    if (size <= 0) {
        throw InvalidInputError();
    }
    std::string result(static_cast<std::size_t>(size), '\0');
    WideCharToMultiByte(
        CP_UTF8, WC_ERR_INVALID_CHARS, value.data(),
        static_cast<int>(value.size()), result.data(), size, nullptr, nullptr);
    return result;
}

std::wstring getWindowTextString(HWND handle) {
    const int length = GetWindowTextLengthW(handle);
    if (length <= 0) {
        return {};
    }
    std::wstring text(static_cast<std::size_t>(length + 1), L'\0');
    GetWindowTextW(handle, text.data(), length + 1);
    text.resize(static_cast<std::size_t>(length));
    return text;
}

void setWindowTextUtf8(HWND handle, const std::string& value) {
    const std::wstring wide = utf8ToWide(value);
    SetWindowTextW(handle, wide.c_str());
}

double parseDouble(HWND edit) {
    const std::wstring text = getWindowTextString(edit);
    if (text.empty()) {
        throw InvalidInputError();
    }
    const std::string utf8 = wideToUtf8(text);
    std::size_t parsed = 0;
    double value = 0.0;
    try {
        value = std::stod(utf8, &parsed);
    } catch (...) {
        throw InvalidInputError();
    }
    if (parsed != utf8.size() || !std::isfinite(value)) {
        throw InvalidInputError();
    }
    return value;
}

class CalculatorWindow {
public:
    explicit CalculatorWindow(HINSTANCE instance) : instance_(instance) {}

    bool create(int showCommand) {
        WNDCLASSEXW windowClass{};
        windowClass.cbSize = sizeof(windowClass);
        windowClass.style = CS_HREDRAW | CS_VREDRAW;
        windowClass.lpfnWndProc = &CalculatorWindow::windowProcedure;
        windowClass.hInstance = instance_;
        windowClass.hCursor = LoadCursorW(nullptr, IDC_ARROW);
        windowClass.hIcon = LoadIconW(nullptr, IDI_APPLICATION);
        windowClass.hIconSm = windowClass.hIcon;
        windowClass.hbrBackground = reinterpret_cast<HBRUSH>(COLOR_WINDOW + 1);
        windowClass.lpszClassName = kWindowClass;

        if (!RegisterClassExW(&windowClass) && GetLastError() != ERROR_CLASS_ALREADY_EXISTS) {
            return false;
        }

        window_ = CreateWindowExW(
            0, kWindowClass, kWindowTitle,
            WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
            CW_USEDEFAULT, CW_USEDEFAULT, 1120, 800,
            nullptr, nullptr, instance_, this);
        if (!window_) {
            return false;
        }

        ShowWindow(window_, showCommand);
        UpdateWindow(window_);
        return true;
    }

    int run() {
        MSG message{};
        while (GetMessageW(&message, nullptr, 0, 0) > 0) {
            TranslateMessage(&message);
            DispatchMessageW(&message);
