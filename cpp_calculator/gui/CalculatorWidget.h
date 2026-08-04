#pragma once

#include <QHash>
#include <QWidget>

class QMenu;
class QPushButton;
class QStackedWidget;

namespace calculator::gui {

class ControlPanel;
class DisplayPanel;

class CalculatorWidget final : public QWidget {
    Q_OBJECT

public:
    explicit CalculatorWidget(QWidget* parent = nullptr);

    void setResult(const QString& text);
    void setExpression(const QString& expression);
    void setAngleMode(const QString& angleModeName);
    void setDisplayMode(const QString& displayModeName);

signals:
    void calculateRequested(const QString& expression);
    void historyToggleRequested();
    void angleModeRequested();
    void displayModeRequested();
    void fractionToggleRequested();

private:
    QWidget* createCalculatePage();
    QWidget* createPlaceholderPage(const QString& title);
    QMenu* createModeMenu();

    void showModeMenu();
    void setMode(int pageIndex);
    void toggleShift();
    void setShiftActive(bool active);
    void updateShiftButtonLabels();
    void requestCalculation();
    void insertFromButton(const QString& buttonLabel, const QString& normalText);

    DisplayPanel* displayPanel_ = nullptr;
    ControlPanel* controlPanel_ = nullptr;
    QStackedWidget* modeStack_ = nullptr;
    QMenu* modeMenu_ = nullptr;
    bool shiftActive_ = false;
    QHash<QString, QPushButton*> calculateButtons_;
    QHash<QString, QString> shiftInsertText_;
    QHash<QString, QString> shiftButtonLabels_;
};

}  // namespace calculator::gui
