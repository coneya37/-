import sys
from PyQt6 import QtWidgets
from database import register_client, register_worker, create_connection
from client import ClientWindow  # Импортируем окно клиента
from admin import AdminWindow    # Импортируем окно администратора

class AuthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 300)

        # Создание элементов интерфейса
        self.layout = QtWidgets.QVBoxLayout()

        self.fio_input = QtWidgets.QLineEdit(self)
        self.fio_input.setPlaceholderText("ФИО (для регистрации)")
        self.fio_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.fio_input)

        self.phone_input = QtWidgets.QLineEdit(self)
        self.phone_input.setPlaceholderText("Телефон (для регистрации)")
        self.phone_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.phone_input)

        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setPlaceholderText("Email (для регистрации)")
        self.email_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.email_input)

        self.login_input = QtWidgets.QLineEdit(self)
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.login_input)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.role_combobox = QtWidgets.QComboBox(self)
        self.role_combobox.addItems(["Клиент", "Администратор"])
        self.role_combobox.setStyleSheet("background-color: #cce4ff; font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.role_combobox)

        self.admin_code_input = QtWidgets.QLineEdit(self)
        self.admin_code_input.setPlaceholderText("Код администратора")
        self.admin_code_input.setStyleSheet("font-family: Roboto; font-size: 14px;")
        self.layout.addWidget(self.admin_code_input)

        self.register_button = QtWidgets.QPushButton("Регистрация", self)
        self.register_button.setStyleSheet("background-color: #a3cdff; font-family: Roboto; font-size: 14px;")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.login_button = QtWidgets.QPushButton("Войти", self)
        self.login_button.setStyleSheet("background-color: #a3cdff;font-family: Roboto; font-size: 14px;")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def register(self):
        fio = self.fio_input.text()
        phone_number = self.phone_input.text()
        email = self.email_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText()

        if len(password) < 8:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пароль должен содержать более 8 символов.")
            return

        if role == "Администратор":
            admin_code = self.admin_code_input.text()
            if admin_code != "2906":  # Пример кода
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный код администратора.")
                return

        if role == "Клиент":
            register_client(fio, phone_number, email, login, password)
        else:
            post = "Администратор"  # Должность для администратора
            register_worker(fio, post, phone_number, email, login, password)

        QtWidgets.QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
        self.clear_inputs()

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()

        role = self.check_credentials(login, password)
        if role is not None:
            QtWidgets.QMessageBox.information(self, "Успех", "Вход выполнен успешно!")
            self.close()
            if role == "Клиент":
                self.open_client_window()
            else:
                self.open_admin_window()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def check_credentials(self, login, password):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE login = ? AND password = ?", (login, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def open_client_window(self):
        self.client_window = ClientWindow()
        self.client_window.show()

    def open_admin_window(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()

    def clear_inputs(self):
        self.fio_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.admin_code_input.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())