# C++ Qt Scientific Calculator

Python/PySide6 계산기와 동일한 기능과 화면 흐름을 목표로 하는 C++/Qt Widgets 버전이다.

## Current stage

Phase 1 GUI skeleton:

- `QMainWindow` + horizontal `QSplitter`
- calculator panel and collapsible history panel
- expression input and result display
- scientific calculator button grid
- cursor movement, DEL, AC
- SHIFT state and shifted button labels
- DEG/RAD/GRAD status cycling
- NORM/FIX4/SCI4 status cycling
- MODE placeholder pages

The expression engine is intentionally not connected yet. Pressing `=` displays `ENGINE NOT CONNECTED`.

## Requirements

- Visual Studio 2022
- CMake 3.21+
- Qt 5 or Qt 6 Widgets development kit built for the selected MSVC compiler

## Build with Visual Studio CMake support

1. Open the `cpp_calculator` folder in Visual Studio.
2. Set the Qt installation prefix when CMake cannot find Qt.
3. Select an x64 Debug or Release configuration.
4. Build and run the `scientific_calculator` target.

Command-line example:

```powershell
cd C:\Users\user\cal\cpp_calculator
cmake -S . -B build -DCMAKE_PREFIX_PATH=C:\Qt\6.x.x\msvc2022_64
cmake --build build --config Debug
.\build\Debug\scientific_calculator.exe
```

Replace the example Qt path with the actual installed kit path.

## Architecture

```text
MainWindow
├─ CalculatorWidget
│  ├─ DisplayPanel
│  ├─ ControlPanel
│  └─ mode stack
├─ HistoryPanel
└─ CalculatorState
```

GUI classes do not perform expression calculation. The next stage adds the C++ tokenizer, parser, engine, formatter, and controller.
