import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QInputDialog
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
        username = self.username.text()
        password = self.password.text()
        print("Login attempt with username: ", username, " and password: ", password)
        client.send(client.LOGIN_MESSAGE)
        client.send(username)
        client.send(password)
        msg = client.receiveMessage()
        if msg == "!SUCCESS":
            print(f"Login was successful!")
            self.goToMainMenu()
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
    
    def goToMainMenu(self):
        mainMenu = MainMenu(self.username.text())
        widget.addWidget(mainMenu)
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
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()
        passwordConfirm = self.passwordConfirm.text()

        if not validLoginInfo.checkValidUsername(username):
            print("Error: Username not valid")
        if not validLoginInfo.checkValidEmail(email):
            print("Error: Email not valid")
        if not validLoginInfo.checkValidPassword(password):
            print("Error: Password not valid")
        elif password == passwordConfirm:
            print("Create Account Attempt with username: ", username, " email: ", email, " and password: ", password)
            client.send(client.REGISTER_MESSAGE)
            client.send(username)
            client.send(email)
            client.send(password)
            msg = client.receiveMessage()
            if msg == "!SUCCESS":
                print(f"Registration success!")
            elif msg == "!FAILURE":
                print(f"Error: Username or Email already in use.")
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
        self.browseButton.clicked.connect(self.browseFiles)
        self.uploadButton.clicked.connect(self.sendFile)

    def browseFiles(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', ".\localfiles")
        self.label_5.setText(file_name[0])

    def sendFile(self):
        client.sendFile(self.label_5.text())

class MainMenu(QDialog):
    def __init__(self, username):
        super(MainMenu, self).__init__()
        loadUi("mainMenu.ui", self)
        self.usernameLabel.setText(username)
        self.logoutButton.clicked.connect(self.logout)
        self.goToUploadButton.clicked.connect(self.goToUpload)
        self.goToDownloadButton.clicked.connect(self.goToDownload)

    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToUpload(self):
        uploadMenu = UploadMenu(self.usernameLabel.text())
        widget.addWidget(uploadMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToDownload(self):
        downloadMenu = DownloadMenu(self.usernameLabel.text())
        widget.addWidget(downloadMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class UploadMenu(QDialog):
    def __init__(self, username):
        super(UploadMenu, self).__init__()
        loadUi("uploadMenu.ui", self)
        self.usernameLabel.setText(username)
        self.logoutButton.clicked.connect(self.logout)
        self.browseButton.clicked.connect(self.browseFiles)
        self.uploadButton.clicked.connect(self.sendFile)
        self.mainMenuButton.clicked.connect(self.goToMainMenu)

    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def browseFiles(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', ".\localfiles")
        self.fileSelected.setText(file_name[0])

    def sendFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
        else:
            client.sendFile(self.fileSelected.text())

    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class DownloadMenu(QDialog):
    def __init__(self, username):
        super(DownloadMenu, self).__init__()
        loadUi("downloadMenu.ui", self)
        self.usernameLabel.setText(username)
        self.updateList()

    def updateList(self):
        client.send(client.FILE_LIST_MESSAGE)
        list = client.receiveList()
        self.fileList.addItems(list)
        self.logoutButton.clicked.connect(self.logout)
        self.selectFileButton.clicked.connect(self.selectFile)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.mainMenuButton.clicked.connect(self.goToMainMenu)

    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def selectFile(self):
        currentIndex = self.fileList.currentRow()
        item = self.fileList.item(currentIndex)
        self.fileSelected.setText(item.text())

    def downloadFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
        else:
            client.send(client.FILE_DOWNLOAD_MESSAGE)
            client.send(self.fileSelected.text())
            client.receiveFile()

    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)




app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
app.exec_()