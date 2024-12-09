import sys
from PyQt6 import QtWidgets, QtGui
from database import create_connection, get_products, add_product, delete_product, get_clients, get_orders, register_client, delete_client

class AdminWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Магазин бытовой техники. Администратор")
        self.setFixedSize(700, 500)

        # Основной вертикальный layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Создание верхнего горизонтального layout для кнопок
        self.button_layout = QtWidgets.QHBoxLayout()

        # Кнопки
        self.catalog_button = QtWidgets.QPushButton("Каталог", self)
        self.catalog_button.clicked.connect(self.show_catalog)
        self.catalog_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.button_layout.addWidget(self.catalog_button)

        self.orders_button = QtWidgets.QPushButton("Заказы", self)
        self.orders_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.orders_button.clicked.connect(self.show_orders)
        self.button_layout.addWidget(self.orders_button)

        self.clients_button = QtWidgets.QPushButton("Клиенты", self)
        self.clients_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.clients_button.clicked.connect(self.show_clients)
        self.button_layout.addWidget(self.clients_button)

        self.exit_button = QtWidgets.QPushButton("Выход", self)
        self.exit_button.setStyleSheet("background-color: #ffa3a3; font-family: Roboto; font-size: 14px;")
        self.exit_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.exit_button)

        # Добавляем кнопки в основной layout
        self.main_layout.addLayout(self.button_layout)

        self.products_table = QtWidgets.QTableWidget(self)
        self.products_table.setColumnCount(7)
        self.products_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Категория", "Описание", "Производитель", "Цена", "Количество"])
        self.main_layout.addWidget(self.products_table)

        self.orders_table = QtWidgets.QTableWidget(self)
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels(
            ["ID", "ФИО Клиента", "Название", "Категория", "Описание", "Производитель", "Цена"])
        self.orders_table.setVisible(False)
        self.main_layout.addWidget(self.orders_table)

        self.clients_table = QtWidgets.QTableWidget(self)
        self.clients_table.setColumnCount(6)
        self.clients_table.setHorizontalHeaderLabels(
            ["ID", "Логин", "ФИО", "Телефон", "Email", "Пароль"])
        self.clients_table.setVisible(False)
        self.main_layout.addWidget(self.clients_table)

        self.load_products_button = QtWidgets.QPushButton("Обновить каталог", self)
        self.load_products_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.load_products_button.clicked.connect(self.load_products)
        self.main_layout.addWidget(self.load_products_button)

        self.add_product_button = QtWidgets.QPushButton("Добавить товар", self)
        self.add_product_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.add_product_button.clicked.connect(self.add_product)
        self.add_product_button.setVisible(False)  # Скрываем по умолчанию
        self.main_layout.addWidget(self.add_product_button)

        self.edit_product_button = QtWidgets.QPushButton("Изменить товар", self)
        self.edit_product_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.edit_product_button.clicked.connect(self.edit_product)
        self.edit_product_button.setVisible(False)  # Скрываем по умолчанию
        self.main_layout.addWidget(self.edit_product_button)

        self.delete_product_button = QtWidgets.QPushButton("Удалить товар", self)
        self.delete_product_button.setStyleSheet("background-color: #ffa3a3; font-family: Roboto; font-size: 14px;")
        self.delete_product_button.clicked.connect(self.delete_product)
        self.delete_product_button.setVisible(False)  # Скрываем по умолчанию
        self.main_layout.addWidget(self.delete_product_button)

        self.edit_client_button = QtWidgets.QPushButton("Изменить клиента", self)
        self.edit_client_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.edit_client_button.clicked.connect(self.edit_client)
        self.edit_client_button.setVisible(False)  # Скрываем по умолчанию
        self.main_layout.addWidget(self.edit_client_button)

        self.delete_client_button = QtWidgets.QPushButton("Удалить клиента", self)
        self.delete_client_button.setStyleSheet("background-color: #ffa3a3; font-family: Roboto; font-size: 14px;")
        self.delete_client_button.clicked.connect(self.delete_client)
        self.delete_client_button.setVisible(False)  # Скрываем по умолчанию
        self.main_layout.addWidget(self.delete_client_button)

        self.setLayout(self.main_layout)

    def load_products(self):
        products = get_products()
        self.products_table.setRowCount(len(products))
        for row_idx, row_data in enumerate(products):
            for col_idx, item in enumerate(row_data):
                self.products_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

    def add_product(self):
        name, ok1 = QtWidgets.QInputDialog.getText(self, "Добавить товар", "Название:")
        if not ok1: return
        category, ok2 = QtWidgets.QInputDialog.getText(self, "Добавить товар", "Категория:")
        if not ok2: return
        description, ok3 = QtWidgets.QInputDialog.getText(self, "Добавить товар", "Описание:")
        if not ok3: return
        manufacturer, ok4 = QtWidgets.QInputDialog.getText(self, "Добавить товар", "Производитель:")
        if not ok4: return
        price, ok5 = QtWidgets.QInputDialog.getDouble(self, "Добавить товар", "Цена:")
        if not ok5: return
        quantity, ok6 = QtWidgets.QInputDialog.getInt(self, "Добавить товар", "Количество:")
        if not ok6: return

        add_product(name, category, description, manufacturer, price, quantity)
        self.load_products()

    def edit_product(self):
        product_id = self.product_id_input.text()
        name = self.name_input.text()
        category = self.category_input.text()
        description = self.description_input.text()
        manufacturer = self.manufacturer_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, category = ?, description = ?, manufacturer = ?, price = ?, quantity_in_stock = ?
            WHERE id = ?
        """, (name, category, description, manufacturer, price, quantity, product_id))
        conn.commit()
        conn.close()

        self.product_id_input.clear()
        self.name_input.clear()
        self.category_input.clear()
        self.description_input.clear()
        self.manufacturer_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()

        QtWidgets.QMessageBox.information(self, "Успех", "Данные товара успешно обновлены!")

    def edit_client(self):
        client_id = self.client_id_input.text()
        login = self.login_input.text()
        fio = self.fio_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clients
            SET login = ?, fio = ?, phone_number = ?, email = ?, password = ?
            WHERE id = ?
        """, (login, fio, phone_number, email, password, client_id))
        conn.commit()
        conn.close()

        self.client_id_input.clear()
        self.login_input.clear()
        self.fio_input.clear()
        self.phone_number_input.clear()
        self.email_input.clear()
        self.password_input.clear()

        QtWidgets.QMessageBox.information(self, "Успех", "Данные клиента успешно обновлены!")

    def delete_product(self):
        selected_row = self.products_table.currentRow()
        if selected_row >= 0:
            product_id = self.products_table.item(selected_row, 0).text()  # Предполагаем, что ID товара в первой колонке
            try:
                delete_product(product_id)
                self.load_products()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар для удаления.")

    def show_catalog(self):
        self.load_products_button.setVisible(True)
        self.products_table.setVisible(True)  # Показываем таблицу товаров
        self.add_product_button.setVisible(True)  # Показываем кнопку добавления товара
        self.delete_product_button.setVisible(True)  # Показываем кнопку удаления товара
        self.edit_product_button.setVisible(True)  # Показываем кнопку изменения товара
        self.orders_table.setVisible(False)    # Скрываем таблицу заказов
        self.clients_table.setVisible(False)   # Скрываем таблицу клиентов
        self.delete_client_button .setVisible(False)  # Скрываем кнопку удаления клиента
        self.edit_client_button.setVisible(False)    # Скрываем кнопку изменения клиента

    def show_orders(self):
        self.load_orders()  # Загружаем заказы
        self.orders_table.setVisible(True)  # Показываем таблицу заказов
        self.products_table.setVisible(False)  # Скрываем таблицу товаров
        self.clients_table.setVisible(False)  # Скрываем таблицу клиентов
        self.delete_client_button.setVisible(False)  # Скрываем кнопку удаления клиента
        self.edit_client_button.setVisible(False)    # Скрываем кнопку изменения клиента
        self.load_products_button.setVisible(False)
        self.add_product_button.setVisible(False)
        self.edit_product_button.setVisible(False)
        self.delete_product_button.setVisible(False)

    def load_orders(self):
        orders = get_orders()  # Получаем заказы из базы данных
        self.orders_table.setRowCount(len(orders))
        for row_idx, row_data in enumerate(orders):
            for col_idx, item in enumerate(row_data):
                self.orders_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

    def show_clients(self):
        self.load_clients()  # Загружаем клиентов
        self.clients_table.setVisible(True)    # Показываем таблицу клиентов
        self.delete_client_button.setVisible(True)  # Показываем кнопку удаления клиента
        self.edit_client_button.setVisible(True)    # Показываем кнопку изменения клиента
        self.products_table.setVisible(False)  # Скрываем таблицу товаров
        self.orders_table.setVisible(False)    # Скрываем таблицу заказов
        self.add_product_button.setVisible(False)
        self.edit_product_button.setVisible(False)
        self.delete_product_button.setVisible(False)
        self.load_products_button.setVisible(False)

    def load_clients(self):
        clients = get_clients()  # Получаем клиентов из базы данных
        self.clients_table.setRowCount(len(clients))
        for row_idx, row_data in enumerate(clients):
            for col_idx, item in enumerate(row_data):
                self.clients_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(item)))

    def delete_client(self):
        selected_row = self.clients_table.currentRow()
        if selected_row >= 0:
            client_id = self.clients_table.item(selected_row, 0).text()  # Предполагаем, что ID клиента в первой колонке
            try:
                delete_client(client_id)  # Удаляем клиента из базы данных
                self.load_clients()  # Обновляем таблицу клиентов
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось удалить клиента: {str(e)}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())