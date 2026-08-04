#include "gui/HistoryPanel.h"

#include <QColor>
#include <QLabel>
#include <QListWidget>
#include <QListWidgetItem>
#include <QVBoxLayout>

namespace calculator::gui {

HistoryPanel::HistoryPanel(QWidget* parent)
    : QFrame(parent) {
    setObjectName(QStringLiteral("historyFrame"));
    setMinimumWidth(220);

    auto* layout = new QVBoxLayout(this);
    layout->setContentsMargins(14, 12, 14, 12);
    layout->setSpacing(8);

    auto* titleLabel = new QLabel(QStringLiteral("Calculation History"), this);
    titleLabel->setAlignment(Qt::AlignCenter);

    historyList_ = new QListWidget(this);
    auto* emptyItem = new QListWidgetItem(QStringLiteral("No calculations yet"), historyList_);
    emptyItem->setFlags(Qt::NoItemFlags);
    emptyItem->setForeground(QColor(QStringLiteral("#6b7280")));

    layout->addWidget(titleLabel);
    layout->addWidget(historyList_, 1);

    connect(historyList_, &QListWidget::itemDoubleClicked, this, [this](QListWidgetItem* item) {
        const QString expression = item->data(Qt::UserRole).toString();
        if (!expression.isEmpty()) {
            emit expressionSelected(expression);
        }
    });
}

void HistoryPanel::addEntry(const QString& expression, const QString& result) {
    if (historyList_->count() == 1 &&
        historyList_->item(0)->flags() == Qt::NoItemFlags) {
        delete historyList_->takeItem(0);
    }

    auto* item = new QListWidgetItem(expression + QStringLiteral(" = ") + result);
    item->setData(Qt::UserRole, expression);
    historyList_->insertItem(0, item);
}

}  // namespace calculator::gui
