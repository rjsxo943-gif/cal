#pragma once

#include <QWidget>

class QPushButton;

namespace calculator::gui {

class ControlPanel final : public QWidget {
    Q_OBJECT

public:
    explicit ControlPanel(QWidget* parent = nullptr);

    void setShiftActive(bool active);
    [[nodiscard]] QPushButton* modeButton() const noexcept;

signals:
    void shiftRequested();
    void modeRequested();
    void angleModeRequested();
    void displayModeRequested();
    void fractionToggleRequested();
    void cursorLeftRequested();
    void cursorRightRequested();
    void historyUpRequested();
    void historyDownRequested();
    void deleteRequested();
    void clearRequested();
    void historyToggleRequested();

private:
    QPushButton* shiftButton_ = nullptr;
    QPushButton* modeButton_ = nullptr;
};

}  // namespace calculator::gui
