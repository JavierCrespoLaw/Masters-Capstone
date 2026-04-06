import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

import client
import validLoginInfo

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginButton.clicked.connect(self.loginFunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAccButton.clicked.connect(self.goToCreateAcc)

    def loginFunction(self):
        email = self.email.text()
        password = self.password.text()
        print("Login attempt with email: ", email, " and password: ", password)
        client.send(client.LOGIN_MESSAGE)
        client.send(email)
        client.send(password)
        msg = client.receiveMessage()
        if msg == "!SUCCESS":
            print(f"Login was successful!")
            self.goToLoginSuccess()
        elif msg == "!FAILURE":
            print(f"Login failed.")

    def goToCreateAcc(self):
        createAcc = CreateAcc()
        widget.addWidget(createAcc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToLoginSuccess(self):
        loginSuccess = LoginSuccess()
        widget.addWidget(loginSuccess)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def closeEvent(self, a0):
        print("Is this doing anything?")

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createAcc.ui", self)
        self.signUpButton.clicked.connect(self.createAccFunction)
        self.returnToLoginButton.clicked.connect(self.goToLogin)

    def createAccFunction(self):
        email = self.email.text()
        password = self.password.text()
        passwordConfirm = self.passwordConfirm.text()

        if not validLoginInfo.checkValidEmail(email) and not validLoginInfo.checkValidPassword(password):
            print("Error: Email or password not valid")
        elif password == passwordConfirm:
            print("Create Account Attempt with email: ", email, " and password: ", password)
            client.send(client.REGISTER_MESSAGE)
            client.send(email)
            client.send(password)
            msg = client.receiveMessage()
            if msg == "!SUCCESS":
                print(f"Registration success!")
            elif msg == "!FAILURE":
                print(f"Error: Email already in use.")
        else:
            print("Error: Passwords must match")

    def goToLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginSuccess(QDialog):
    def __init__(self):
        super(LoginSuccess, self).__init__()
        loadUi("loginSuccess.ui", self)



app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
app.exec_()