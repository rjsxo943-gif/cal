#include "gui/DisplayPanel.h"

#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QVBoxLayout>

namespace calculator::gui {
namespace {

QLabel* createStatusLabel(const QString& text, QWidget* parent) {
    auto* label = new QLabel(text, parent);
    label->setObjectName(QStringLiteral("statusLabel"));
    return label;
}

}  // namespace

DisplayPanel::DisplayPanel(QWidget* parent)
    : QFrame(parent) {
    setObjectName(QStringLiteral("displayFrame"));

    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(14, 12, 14, 12);
    mainLayout->setSpacing(4);

    auto* statusLayout = new QHBoxLayout();
    angleLabel_ = createStatusLabel(QStringLiteral("DEG"), this);
    formatLabel_ = createStatusLabel(QStringLiteral("NORM"), this);
    modeLabel_ = createStatusLabel(QStringLiteral("CALC"), this);
    shiftLabel_ = createStatusLabel(QStringLiteral("SHIFT OFF"), this);

    statusLayout->addWidget(angleLabel_);
    statusLayout->addWidget(formatLabel_);
    statusLayout->addWidget(modeLabel_);
    statusLayout->addStretch();
    statusLayout->addWidget(shiftLabel_);

    expressionEdit_ = new QLineEdit(this);
    expressionEdit_->setObjectName(QStringLiteral("expressionEdit"));
    expressionEdit_->setPlaceholderText(QStringLiteral("수식을 입력하세요"));
    expressionEdit_->setClearButtonEnabled(false);

    resultLabel_ = new QLabel(QStringLiteral("0"), this);
    resultLabel_->setObjectName(QStringLiteral("resultLabel"));
    resultLabel_->setAlignment(Qt::AlignRight | Qt::AlignVCenter);
    resultLabel_->setTextInteractionFlags(Qt::TextSelectableByMouse);

    mainLayout->addLayout(statusLayout);
    mainLayout->addWidget(expressionEdit_);
    mainLayout->addWidget(resultLabel_);
}

void DisplayPanel::insertText(const QString& text) {
    expressionEdit_->insert(text);
    expressionEdit_->setFocus();
}

void DisplayPanel::deletePreviousCharacter() {
    expressionEdit_->backspace();
    expressionEdit_->setFocus();
}

void DisplayPanel::clearDisplay() {
    expressionEdit_->clear();
    resultLabel_->setText(QStringLiteral("0"));
    expressionEdit_->setFocus();
}

void DisplayPanel::moveCursor(const int offset) {
    const int currentPosition = expressionEdit_->cursorPosition();
    const int textLength = static_cast<int>(expressionEdit_->text().size());
    const int newPosition = qBound(0, currentPosition + offset, textLength);
    expressionEdit_->setCursorPosition(newPosition);
    expressionEdit_->setFocus();
}

QString DisplayPanel::expression() const {
    return expressionEdit_->text();
}

void DisplayPanel::setResult(const QString& text) {
    resultLabel_->setText(text);
}

void DisplayPanel::setShiftActive(const bool active) {
    shiftLabel_->setText(active ? QStringLiteral("SHIFT ON") : QStringLiteral("SHIFT OFF"));
}

void DisplayPanel::setModeName(const QString& modeName) {
    modeLabel_->setText(modeName);
}

void DisplayPanel::setAngleMode(const QString& angleModeName) {
    angleLabel_->setText(angleModeName);
}

void DisplayPanel::setDisplayMode(const QString& displayModeName) {
    formatLabel_->setText(displayModeName);
}

QLineEdit* DisplayPanel::expressionEdit() const noexcept {
    return expressionEdit_;
}

}  // namespace calculator::gui
