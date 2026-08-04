#include "gui/MainWindow.h"

#include "gui/AppStyle.h"
#include "gui/CalculatorWidget.h"
#include "gui/HistoryPanel.h"

#include <QSplitter>

namespace calculator::gui {

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent) {
    setWindowTitle(QStringLiteral("Scientific Calculator - C++ Qt"));
    resize(1050, 720);
    setMinimumSize(780, 600);
    setStyleSheet(appStyleSheet());

    calculatorWidget_ = new CalculatorWidget(this);
    historyPanel_ = new HistoryPanel(this);

    mainSplitter_ = new QSplitter(Qt::Horizontal, this);
    mainSplitter_->addWidget(calculatorWidget_);
    mainSplitter_->addWidget(historyPanel_);
    mainSplitter_->setStretchFactor(0, 4);
    mainSplitter_->setStretchFactor(1, 1);
    mainSplitter_->setCollapsible(0, false);
    mainSplitter_->setSizes({800, 250});
    setCentralWidget(mainSplitter_);

    calculatorWidget_->setAngleMode(QString::fromStdString(state_.angleModeName()));
    calculatorWidget_->setDisplayMode(QString::fromStdString(state_.displayModeName()));

    connect(calculatorWidget_, &CalculatorWidget::historyToggleRequested, this, &MainWindow::toggleHistoryPanel);
    connect(calculatorWidget_, &CalculatorWidget::angleModeRequested, this, &MainWindow::cycleAngleMode);
    connect(calculatorWidget_, &CalculatorWidget::displayModeRequested, this, &MainWindow::cycleDisplayMode);
    connect(calculatorWidget_, &CalculatorWidget::fractionToggleRequested, this, [this] {
        calculatorWidget_->setResult(QStringLiteral("S⇔D: ENGINE NOT CONNECTED"));
    });
    connect(calculatorWidget_, &CalculatorWidget::calculateRequested, this, &MainWindow::handleCalculationRequest);
    connect(historyPanel_, &HistoryPanel::expressionSelected, calculatorWidget_, &CalculatorWidget::setExpression);
}

void MainWindow::toggleHistoryPanel() {
    if (historyPanel_->isVisible()) {
        historyPanel_->hide();
        return;
    }

    historyPanel_->show();
    mainSplitter_->setSizes({800, 250});
}

void MainWindow::cycleAngleMode() {
    state_.cycleAngleMode();
    calculatorWidget_->setAngleMode(QString::fromStdString(state_.angleModeName()));
}

void MainWindow::cycleDisplayMode() {
    state_.cycleDisplayMode();
    calculatorWidget_->setDisplayMode(QString::fromStdString(state_.displayModeName()));
}

void MainWindow::handleCalculationRequest(const QString& expression) {
    Q_UNUSED(expression);
    calculatorWidget_->setResult(QStringLiteral("ENGINE NOT CONNECTED"));
}

}  // namespace calculator::gui
