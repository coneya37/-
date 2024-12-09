import sys
from PyQt6 import QtWidgets, QtGui
from database import get_products, place_order, create_connection

class ClientWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Магазин бытовой техники")
        self.setFixedSize(700, 500)

        self.layout = QtWidgets.QVBoxLayout()

        # Создаем горизонтальный макет для кнопок
        self.top_buttons_layout = QtWidgets.QHBoxLayout()

        # Добавляем кнопку "Каталог"
        self.catalog_button = QtWidgets.QPushButton("Каталог", self)
        self.catalog_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")

        self.top_buttons_layout.addWidget(self.catalog_button)

        # Добавляем кнопку "Мои заказы"
        self.my_orders_button = QtWidgets.QPushButton("Мои заказы", self)
        self.my_orders_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.my_orders_button.clicked.connect(self.show_my_orders)
        self.top_buttons_layout.addWidget(self.my_orders_button)

        # Добавляем кнопку "Выход"
        self.exit_button = QtWidgets.QPushButton("Выход", self)
        self.exit_button.setStyleSheet("background-color: #ffa3a3; font-family: Roboto; font-size: 14px;")
        self.exit_button.clicked.connect(self.exit_application)
        self.top_buttons_layout.addWidget(self.exit_button)

        # Добавляем горизонтальный макет с кнопками в основной вертикальный макет
        self.layout.addLayout(self.top_buttons_layout)

        self.products_table = QtWidgets.QTableWidget(self)
        self.products_table.setColumnCount(7)  # Количество колонок
        self.products_table.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Описание", "Производитель", "Цена", "Количество"])
        self.layout.addWidget(self.products_table)

        self.load_products_button = QtWidgets.QPushButton("Загрузить товары", self)
        self.load_products_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.load_products_button.clicked.connect(self.load_products)
        self.layout.addWidget(self.load_products_button)

        self.payment_method_combobox = QtWidgets.QComboBox(self)
        self.payment_method_combobox.addItems(["Наличные", "Карта"])
        self.payment_method_combobox.setStyleSheet("background-color: #cce4ff; font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.payment_method_combobox)

        self.buy_button = QtWidgets.QPushButton("Купить", self)
        self.buy_button.setStyleSheet("background-color: #aeffa8; font-family: Roboto; font-size: 14px;")
        self.buy_button.clicked.connect(self.buy_product)
        self.layout.addWidget(self.buy_button)

        self.setLayout(self.layout)

    def load_products(self):
        products = get_products()
        self.products_table.setRowCount(len(products))
        for row_idx, row_data in enumerate(products):
            for col_idx, item in enumerate(row_data):
                self.products_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

    def buy_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row >= 0:
            product_id = self.products_table.item(selected_row, 0).text()
            payment_method = self.payment_method_combobox.currentText()
            client_id = 1
            place_order(client_id, product_id, payment_method)
            QtWidgets.QMessageBox.information(self, "Успех", "Товар успешно куплен!")

    def show_my_orders(self):
        conn = create_connection()
        cur = conn.cursor()
        client_id = 1
        cur.execute("SELECT p.* FROM orders o JOIN products p ON o.product_id = p.id WHERE o.client_id = ?",
                    (client_id,))
        orders = cur.fetchall()

        order_info = ""
        for order in orders:
            order_info += f"Название: {order[1]}, Категория: {order[2]}, Цена: {order[5]}\n"
        QtWidgets.QMessageBox.information(self, "Мои заказы", order_info)

    def exit_application(self):
        QtWidgets.QApplication.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec())