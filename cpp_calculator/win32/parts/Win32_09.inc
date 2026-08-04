
    CalculatorController controller_;
    StatisticsController statistics_;
    EquationController equation_;
    ComplexController complex_;

    AppMode mode_{AppMode::Calc};
    bool shiftActive_{false};
    bool complexPolarMode_{false};
};

}  // namespace

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int showCommand) {
    SetProcessDPIAware();

    INITCOMMONCONTROLSEX commonControls{};
    commonControls.dwSize = sizeof(commonControls);
    commonControls.dwICC = ICC_STANDARD_CLASSES;
    InitCommonControlsEx(&commonControls);

    CalculatorWindow application(instance);
    if (!application.create(showCommand)) {
        MessageBoxW(
            nullptr,
            L"Failed to create the calculator window.",
            L"Scientific Calculator",
            MB_OK | MB_ICONERROR);
        return 1;
    }
    return application.run();
}
