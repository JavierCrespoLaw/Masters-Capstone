import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QInputDialog, QLabel, QVBoxLayout, QDialogButtonBox
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
            self.goToAuthenticate()
        elif msg == "!FAILURE":
            print(f"Login failed.")
            dlg = CustomDialog("Login Failed", "Login Failed. Username or password is incorrect.")
            dlg.exec()

    def goToCreateAcc(self):
        createAcc = CreateAcc()
        widget.addWidget(createAcc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToLoginSuccess(self):
        loginSuccess = LoginSuccess()
        widget.addWidget(loginSuccess)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAuthenticate(self):
        authenticate = Authenticate(self.username.text())
        widget.addWidget(authenticate)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def closeEvent(self, a0):
        print("Is this doing anything?")

class Authenticate(QDialog):
    def __init__(self, username):
        super(Authenticate, self).__init__()
        loadUi("authenticate.ui", self)
        self.usernameLabel.setText(username)
        self.authenticateButton.clicked.connect(self.authenticate)

    def authenticate(self):
        authenticationCode = self.authenticationCode.text()
        authenticationCode = authenticationCode.replace(" ", "")
        print(f"Authentication attempt with code {authenticationCode}")
        client.send("!AUTH")
        client.send(authenticationCode)

        msg = client.receiveMessage()
        if msg == "!SUCCESS":
            print("Authentication successful!")
            self.goToMainMenu()
        elif msg == "!FAILURE":
            print("Authentication failed!")
            dlg = CustomDialog("Authentication Failed", "Authentication Failed. Code is incorrect.")
            dlg.exec()
        elif msg == "!HONEYTOKEN":
            print("Honeytoken triggered!")
            dlg = CustomDialog("Honeytoken triggered", "Honeytoken has been triggered. ")
            dlg.exec()

    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    

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
        authenticationNumber = self.selection2FA.currentText()

        if not validLoginInfo.checkValidUsername(username):
            print("Error: Username not valid")
        elif not validLoginInfo.checkValidEmail(email):
            print("Error: Email not valid")
        elif not validLoginInfo.checkValidPassword(password):
            print("Error: Password not valid")
        elif not authenticationNumber.isdigit():
            print("Error: Must select an Authentication Number")
        elif not password == passwordConfirm:
            print("Error: Passwords must match")
        else:
            print("Create Account Attempt with username: ", username, " email: ", email, " and password: ", password)
            client.send(client.REGISTER_MESSAGE)
            client.send(username)
            client.send(email)
            client.send(password)
            client.send(authenticationNumber)
            msg = client.receiveMessage()
            if msg == "!SUCCESS":
                print(f"Registration success!")
            elif msg == "!FAILURE":
                print(f"Error: Username or Email already in use.")

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
        self.goToDeleteButton.clicked.connect(self.goToDelete)

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

    def goToDelete(self):
        deleteMenu = DeleteMenu(self.usernameLabel.text())
        widget.addWidget(deleteMenu)
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


class DeleteMenu(QDialog):
    def __init__(self, username):
        super(DeleteMenu, self).__init__()
        loadUi("deleteMenu.ui", self)
        self.usernameLabel.setText(username)
        self.updateList()

    def updateList(self):
        client.send(client.FILE_LIST_MESSAGE)
        list = client.receiveList()
        self.fileList.clear()
        self.fileList.addItems(list)
        self.logoutButton.clicked.connect(self.logout)
        self.selectFileButton.clicked.connect(self.selectFile)
        self.deleteButton.clicked.connect(self.deleteFile)
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

    def deleteFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
        else:
            client.send(client.FILE_DELETE_MESSAGE)
            client.send(self.fileSelected.text())
            self.updateList()
            dlg = CustomDialog("File Deleted", "File has been deleted.")
            dlg.exec()

    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CustomDialog(QDialog):
    def __init__(self, windowMessage, dialogMessage):
        super().__init__()

        self.setWindowTitle(windowMessage)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        #self.buttonBox = QDialogButtonBox(QBtn)
        #self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(dialogMessage)
        layout.addWidget(message)
        #layout.addWidget(self.buttonBox)
        self.setLayout(layout)




app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
app.exec_()