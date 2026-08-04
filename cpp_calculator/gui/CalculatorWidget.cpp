#include "gui/CalculatorWidget.h"

#include "gui/ControlPanel.h"
#include "gui/DisplayPanel.h"

#include <QAction>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QMenu>
#include <QPushButton>
#include <QStackedWidget>
#include <QStyle>
#include <QVBoxLayout>

#include <array>
#include <utility>

namespace calculator::gui {
namespace {

QString modeName(const int index) {
    switch (index) {
    case 0:
        return QStringLiteral("CALC");
    case 1:
        return QStringLiteral("STAT");
    case 2:
        return QStringLiteral("EQN");
    case 3:
        return QStringLiteral("CMPLX");
    default:
        return QStringLiteral("CALC");
    }
}

}  // namespace

CalculatorWidget::CalculatorWidget(QWidget* parent)
    : QWidget(parent),
      shiftInsertText_({
          {QStringLiteral("sin"), QStringLiteral("asin(")},
          {QStringLiteral("cos"), QStringLiteral("acos(")},
          {QStringLiteral("tan"), QStringLiteral("atan(")},
          {QStringLiteral("log"), QStringLiteral("10^(")},
          {QStringLiteral("ln"), QStringLiteral("e^(")},
          {QStringLiteral("Ran#"), QStringLiteral("randint(")},
      }),
      shiftButtonLabels_({
          {QStringLiteral("sin"), QStringLiteral("asin")},
          {QStringLiteral("cos"), QStringLiteral("acos")},
          {QStringLiteral("tan"), QStringLiteral("atan")},
          {QStringLiteral("log"), QStringLiteral("10ˣ")},
          {QStringLiteral("ln"), QStringLiteral("eˣ")},
          {QStringLiteral("Ran#"), QStringLiteral("RanInt")},
      }) {
    auto* layout = new QVBoxLayout(this);
    layout->setContentsMargins(12, 12, 12, 12);
    layout->setSpacing(10);

    displayPanel_ = new DisplayPanel(this);
    controlPanel_ = new ControlPanel(this);

    modeStack_ = new QStackedWidget(this);
    modeStack_->addWidget(createCalculatePage());
    modeStack_->addWidget(createPlaceholderPage(QStringLiteral("Statistics Mode")));
    modeStack_->addWidget(createPlaceholderPage(QStringLiteral("Equation Mode")));
    modeStack_->addWidget(createPlaceholderPage(QStringLiteral("Complex Mode")));

    modeMenu_ = createModeMenu();

    layout->addWidget(displayPanel_);
    layout->addWidget(controlPanel_);
    layout->addWidget(modeStack_, 1);

    connect(controlPanel_, &ControlPanel::shiftRequested, this, &CalculatorWidget::toggleShift);
    connect(controlPanel_, &ControlPanel::modeRequested, this, &CalculatorWidget::showModeMenu);
    connect(controlPanel_, &ControlPanel::angleModeRequested, this, &CalculatorWidget::angleModeRequested);
    connect(controlPanel_, &ControlPanel::displayModeRequested, this, &CalculatorWidget::displayModeRequested);
    connect(controlPanel_, &ControlPanel::fractionToggleRequested, this, &CalculatorWidget::fractionToggleRequested);
    connect(controlPanel_, &ControlPanel::cursorLeftRequested, this, [this] { displayPanel_->moveCursor(-1); });
    connect(controlPanel_, &ControlPanel::cursorRightRequested, this, [this] { displayPanel_->moveCursor(1); });
    connect(controlPanel_, &ControlPanel::deleteRequested, displayPanel_, &DisplayPanel::deletePreviousCharacter);
    connect(controlPanel_, &ControlPanel::clearRequested, displayPanel_, &DisplayPanel::clearDisplay);
    connect(controlPanel_, &ControlPanel::historyToggleRequested, this, &CalculatorWidget::historyToggleRequested);
    connect(displayPanel_->expressionEdit(), &QLineEdit::returnPressed, this, &CalculatorWidget::requestCalculation);

    displayPanel_->expressionEdit()->setFocus();
}

QWidget* CalculatorWidget::createCalculatePage() {
    auto* page = new QWidget(this);
    auto* layout = new QGridLayout(page);
    layout->setSpacing(7);

    const std::array<std::pair<QString, QString>, 44> buttons = {{
        {QStringLiteral("sin"), QStringLiteral("sin(")},
        {QStringLiteral("cos"), QStringLiteral("cos(")},
        {QStringLiteral("tan"), QStringLiteral("tan(")},
        {QStringLiteral("log"), QStringLiteral("log(")},
        {QStringLiteral("ln"), QStringLiteral("ln(")},
        {QStringLiteral("x²"), QStringLiteral("^2")},
        {QStringLiteral("xʸ"), QStringLiteral("^")},
        {QStringLiteral("√"), QStringLiteral("sqrt(")},
        {QStringLiteral("π"), QStringLiteral("pi")},
        {QStringLiteral("e"), QStringLiteral("e")},
        {QStringLiteral("abs"), QStringLiteral("abs(")},
        {QStringLiteral("1/x"), QStringLiteral("recip(")},
        {QStringLiteral("x!"), QStringLiteral("!")},
        {QStringLiteral("nPr"), QStringLiteral("npr(")},
        {QStringLiteral("nCr"), QStringLiteral("ncr(")},
        {QStringLiteral("mod"), QStringLiteral("mod(")},
        {QStringLiteral("GCD"), QStringLiteral("gcd(")},
        {QStringLiteral("LCM"), QStringLiteral("lcm(")},
        {QStringLiteral(","), QStringLiteral(",")},
        {QStringLiteral("("), QStringLiteral("(")},
        {QStringLiteral("quot"), QStringLiteral("quot(")},
        {QStringLiteral("rem"), QStringLiteral("rem(")},
        {QStringLiteral("%"), QStringLiteral("%")},
        {QStringLiteral("root"), QStringLiteral("root(")},
        {QStringLiteral("Ran#"), QStringLiteral("random()")},
        {QStringLiteral("7"), QStringLiteral("7")},
        {QStringLiteral("8"), QStringLiteral("8")},
        {QStringLiteral("9"), QStringLiteral("9")},
        {QStringLiteral("÷"), QStringLiteral("/")},
        {QStringLiteral(")"), QStringLiteral(")")},
        {QStringLiteral("4"), QStringLiteral("4")},
        {QStringLiteral("5"), QStringLiteral("5")},
        {QStringLiteral("6"), QStringLiteral("6")},
        {QStringLiteral("×"), QStringLiteral("*")},
        {QStringLiteral("Ans"), QStringLiteral("Ans")},
        {QStringLiteral("1"), QStringLiteral("1")},
        {QStringLiteral("2"), QStringLiteral("2")},
        {QStringLiteral("3"), QStringLiteral("3")},
        {QStringLiteral("-"), QStringLiteral("-")},
        {QStringLiteral("EXP"), QStringLiteral("E")},
        {QStringLiteral("0"), QStringLiteral("0")},
        {QStringLiteral("."), QStringLiteral(".")},
        {QStringLiteral("+"), QStringLiteral("+")},
        {QStringLiteral("="), QString()},
    }};

    for (int index = 0; index < static_cast<int>(buttons.size()); ++index) {
        const auto& [label, insertedText] = buttons.at(index);
        const int row = index / 5;
        const int column = index % 5;
        auto* button = new QPushButton(label, page);

        if (label == QStringLiteral("=")) {
            button->setObjectName(QStringLiteral("equalsButton"));
            connect(button, &QPushButton::clicked, this, &CalculatorWidget::requestCalculation);
            layout->addWidget(button, row, column, 1, 2);
            continue;
        }

        calculateButtons_.insert(label, button);
        button->setProperty("shifted", false);
        connect(button, &QPushButton::clicked, this, [this, label, insertedText] {
            insertFromButton(label, insertedText);
        });
        layout->addWidget(button, row, column);
    }

    return page;
}

QWidget* CalculatorWidget::createPlaceholderPage(const QString& title) {
    auto* page = new QWidget(this);
    auto* layout = new QVBoxLayout(page);
    auto* label = new QLabel(title + QStringLiteral("\nUI will be added after the C++ core is ported."), page);
    label->setAlignment(Qt::AlignCenter);
    label->setStyleSheet(QStringLiteral("font-size: 20px; color: #6b7280;"));
    layout->addStretch();
    layout->addWidget(label);
    layout->addStretch();
    return page;
}

QMenu* CalculatorWidget::createModeMenu() {
    auto* menu = new QMenu(this);
    const std::array<std::pair<QString, int>, 4> modes = {{
        {QStringLiteral("Calculate"), 0},
        {QStringLiteral("Statistics"), 1},
        {QStringLiteral("Equation"), 2},
        {QStringLiteral("Complex"), 3},
    }};

    for (const auto& [text, index] : modes) {
        auto* action = menu->addAction(text);
        connect(action, &QAction::triggered, this, [this, index] { setMode(index); });
    }

    return menu;
}

void CalculatorWidget::showModeMenu() {
    auto* button = controlPanel_->modeButton();
    modeMenu_->popup(button->mapToGlobal(button->rect().bottomLeft()));
}

void CalculatorWidget::setMode(const int pageIndex) {
    modeStack_->setCurrentIndex(pageIndex);
    displayPanel_->setModeName(modeName(pageIndex));
    displayPanel_->expressionEdit()->setFocus();
}

void CalculatorWidget::toggleShift() {
    setShiftActive(!shiftActive_);
}

void CalculatorWidget::setShiftActive(const bool active) {
    shiftActive_ = active;
    displayPanel_->setShiftActive(active);
    controlPanel_->setShiftActive(active);
    updateShiftButtonLabels();
}

void CalculatorWidget::updateShiftButtonLabels() {
    for (auto iterator = shiftButtonLabels_.constBegin(); iterator != shiftButtonLabels_.constEnd(); ++iterator) {
        auto* button = calculateButtons_.value(iterator.key(), nullptr);
        if (button == nullptr) {
            continue;
        }

        button->setText(shiftActive_ ? iterator.value() : iterator.key());
        button->setProperty("shifted", shiftActive_);
        button->style()->unpolish(button);
        button->style()->polish(button);
    }
}

void CalculatorWidget::requestCalculation() {
    const QString expressionText = displayPanel_->expression().trimmed();
    if (expressionText.isEmpty()) {
        displayPanel_->setResult(QStringLiteral("Invalid input"));
        return;
    }

    emit calculateRequested(expressionText);
}

void CalculatorWidget::insertFromButton(const QString& buttonLabel, const QString& normalText) {
    const QString shiftedText = shiftInsertText_.value(buttonLabel);

    if (shiftActive_ && !shiftedText.isEmpty()) {
        displayPanel_->insertText(shiftedText);
        setShiftActive(false);
        return;
    }

    displayPanel_->insertText(normalText);
}

void CalculatorWidget::setResult(const QString& text) {
    displayPanel_->setResult(text);
}

void CalculatorWidget::setExpression(const QString& expression) {
    displayPanel_->expressionEdit()->setText(expression);
    displayPanel_->expressionEdit()->setCursorPosition(static_cast<int>(expression.size()));
    displayPanel_->expressionEdit()->setFocus();
}

void CalculatorWidget::setAngleMode(const QString& angleModeName) {
    displayPanel_->setAngleMode(angleModeName);
}

void CalculatorWidget::setDisplayMode(const QString& displayModeName) {
    displayPanel_->setDisplayMode(displayModeName);
}

}  // namespace calculator::gui
