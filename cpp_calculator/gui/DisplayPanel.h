#pragma once

#include <QFrame>

class QLabel;
class QLineEdit;

namespace calculator::gui {

class DisplayPanel final : public QFrame {
public:
    explicit DisplayPanel(QWidget* parent = nullptr);

    void insertText(const QString& text);
    void deletePreviousCharacter();
    void clearDisplay();
    void moveCursor(int offset);

    [[nodiscard]] QString expression() const;

    void setResult(const QString& text);
    void setShiftActive(bool active);
    void setModeName(const QString& modeName);
    void setAngleMode(const QString& angleModeName);
    void setDisplayMode(const QString& displayModeName);

    [[nodiscard]] QLineEdit* expressionEdit() const noexcept;

private:
    QLabel* angleLabel_ = nullptr;
    QLabel* formatLabel_ = nullptr;
    QLabel* modeLabel_ = nullptr;
    QLabel* shiftLabel_ = nullptr;
    QLineEdit* expressionEdit_ = nullptr;
    QLabel* resultLabel_ = nullptr;
};

}  // namespace calculator::gui
