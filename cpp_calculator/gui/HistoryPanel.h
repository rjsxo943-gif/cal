#pragma once

#include <QFrame>

class QListWidget;

namespace calculator::gui {

class HistoryPanel final : public QFrame {
    Q_OBJECT

public:
    explicit HistoryPanel(QWidget* parent = nullptr);

    void addEntry(const QString& expression, const QString& result);

signals:
    void expressionSelected(const QString& expression);

private:
    QListWidget* historyList_ = nullptr;
};

}  // namespace calculator::gui
