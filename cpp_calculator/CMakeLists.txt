cmake_minimum_required(VERSION 3.21)

project(ScientificCalculatorCpp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

add_executable(scientific_calculator
    main.cpp
    core/CalculatorState.cpp
    core/CalculatorState.h
    gui/AppStyle.h
    gui/CalculatorWidget.cpp
    gui/CalculatorWidget.h
    gui/ControlPanel.cpp
    gui/ControlPanel.h
    gui/DisplayPanel.cpp
    gui/DisplayPanel.h
    gui/HistoryPanel.cpp
    gui/HistoryPanel.h
    gui/MainWindow.cpp
    gui/MainWindow.h
)

target_include_directories(scientific_calculator PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(scientific_calculator PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

if(MSVC)
    target_compile_options(scientific_calculator PRIVATE /utf-8 /W4 /permissive-)
else()
    target_compile_options(scientific_calculator PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(WIN32)
    set_target_properties(scientific_calculator PROPERTIES WIN32_EXECUTABLE TRUE)
endif()

include(CTest)
if(BUILD_TESTING)
    add_executable(calculator_state_tests
        tests/CalculatorStateTests.cpp
        core/CalculatorState.cpp
        core/CalculatorState.h
    )
    target_include_directories(calculator_state_tests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    add_test(NAME calculator_state_tests COMMAND calculator_state_tests)
endif()
