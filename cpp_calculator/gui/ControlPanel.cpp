#include "gui/ControlPanel.h"

#include <QGridLayout>
#include <QPushButton>
#include <QStyle>

namespace calculator::gui {
namespace {

QPushButton* addButton(
    QGridLayout* layout,
    const QString& text,
    const int row,
    const int column,
    const int rowSpan = 1,
    const int columnSpan = 1) {
    auto* button = new QPushButton(text);
    layout->addWidget(button, row, column, rowSpan, columnSpan);
    return button;
}

}  // namespace

ControlPanel::ControlPanel(QWidget* parent)
    : QWidget(parent) {
    auto* layout = new QGridLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(6);

    shiftButton_ = addButton(layout, QStringLiteral("SHIFT"), 0, 0);
    shiftButton_->setObjectName(QStringLiteral("shiftButton"));
    shiftButton_->setProperty("active", false);

    modeButton_ = addButton(layout, QStringLiteral("MODE"), 0, 1);
    auto* angleButton = addButton(layout, QStringLiteral("DRG"), 0, 2);
    auto* leftButton = addButton(layout, QStringLiteral("◀"), 0, 3);
    auto* upButton = addButton(layout, QStringLiteral("▲"), 0, 4);
    auto* downButton = addButton(layout, QStringLiteral("▼"), 0, 5);
    auto* rightButton = addButton(layout, QStringLiteral("▶"), 0, 6);

    auto* historyButton = addButton(layout, QStringLiteral("HISTORY"), 1, 0, 1, 2);
    auto* formatButton = addButton(layout, QStringLiteral("FMT"), 1, 2);
    auto* fractionButton = addButton(layout, QStringLiteral("S⇔D"), 1, 3);
    auto* deleteButton = addButton(layout, QStringLiteral("DEL"), 1, 4);
    auto* clearButton = addButton(layout, QStringLiteral("AC"), 1, 5, 1, 2);

    connect(shiftButton_, &QPushButton::clicked, this, &ControlPanel::shiftRequested);
    connect(modeButton_, &QPushButton::clicked, this, &ControlPanel::modeRequested);
    connect(angleButton, &QPushButton::clicked, this, &ControlPanel::angleModeRequested);
    connect(formatButton, &QPushButton::clicked, this, &ControlPanel::displayModeRequested);
    connect(fractionButton, &QPushButton::clicked, this, &ControlPanel::fractionToggleRequested);
    connect(leftButton, &QPushButton::clicked, this, &ControlPanel::cursorLeftRequested);
    connect(rightButton, &QPushButton::clicked, this, &ControlPanel::cursorRightRequested);
    connect(upButton, &QPushButton::clicked, this, &ControlPanel::historyUpRequested);
    connect(downButton, &QPushButton::clicked, this, &ControlPanel::historyDownRequested);
    connect(deleteButton, &QPushButton::clicked, this, &ControlPanel::deleteRequested);
    connect(clearButton, &QPushButton::clicked, this, &ControlPanel::clearRequested);
    connect(historyButton, &QPushButton::clicked, this, &ControlPanel::historyToggleRequested);
}

void ControlPanel::setShiftActive(const bool active) {
    shiftButton_->setProperty("active", active);
    shiftButton_->style()->unpolish(shiftButton_);
    shiftButton_->style()->polish(shiftButton_);
}

QPushButton* ControlPanel::modeButton() const noexcept {
    return modeButton_;
}

}  // namespace calculator::gui
