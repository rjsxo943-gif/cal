#pragma once

#include "core/CalculatorState.h"

#include <QMainWindow>

class QSplitter;

namespace calculator::gui {

class CalculatorWidget;
class HistoryPanel;

class MainWindow final : public QMainWindow {
public:
    explicit MainWindow(QWidget* parent = nullptr);

private:
    void toggleHistoryPanel();
    void cycleAngleMode();
    void cycleDisplayMode();
    void handleCalculationRequest(const QString& expression);

    calculator::CalculatorState state_;
    CalculatorWidget* calculatorWidget_ = nullptr;
    HistoryPanel* historyPanel_ = nullptr;
    QSplitter* mainSplitter_ = nullptr;
};

}  // namespace calculator::gui
