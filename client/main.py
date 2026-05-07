import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QInputDialog, QLabel, QVBoxLayout, QDialogButtonBox
from PyQt5.uic import loadUi

import client
import validLoginInfo

# Login Menu
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginButton.clicked.connect(self.loginFunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAccButton.clicked.connect(self.goToCreateAcc)
        self.resetPasswordButton.clicked.connect(self.goToResetPasswordStage1)

    # Attempts to log in to the server using the username and password
    # If it is successful, user will go to the 2FA stage
    # Otherwise, an alert will pop up telling the user it was unsuccessful
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
        elif msg == "!NOT_SECURE":
            print(f"Account not secure.")
            dlg = CustomDialog("Account not secure", "Account is currently not secure. Please reset your password.")
            dlg.exec()

    # Switches to the Create Account menu
    def goToCreateAcc(self):
        createAcc = CreateAcc()
        widget.addWidget(createAcc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login Success menu
    def goToLoginSuccess(self):
        loginSuccess = LoginSuccess()
        widget.addWidget(loginSuccess)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Two Factor Authentication menu
    def goToAuthenticate(self):
        authenticate = Authenticate(self.username.text())
        widget.addWidget(authenticate)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the first Reset Password menu
    def goToResetPasswordStage1(self):
        client.send(client.RESET_PASSWORD_MESSAGE)
        resetPasswordStage1 = ResetPasswordStage1()
        widget.addWidget(resetPasswordStage1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Authenticate Menu
class Authenticate(QDialog):
    def __init__(self, username):
        super(Authenticate, self).__init__()
        loadUi("authenticate.ui", self)
        self.usernameLabel.setText(username)
        self.authenticateButton.clicked.connect(self.authenticate)

    # Attempts to authenticate the user using the code they entered
    # If successful, they go to the main menu
    # If not, a popup will appear informing them that the code is incorrect
    # If a honeytoken is triggered, the user is sent back to the login menu
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
            self.goToLogin()

    # Switches to the Main Menu
    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login menu
    def goToLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Create Account Menu
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createAcc.ui", self)
        self.signUpButton.clicked.connect(self.createAccFunction)
        self.returnToLoginButton.clicked.connect(self.goToLogin)

    # Attempts to create an account using the provided information
    # Checks to make sure that the information is valid before sending it to the server
    # If it is valid, it is sent to the server where it checks to see if the username or email is taken
    # If they are available, an account is made and the user goes back to the login menu
    # If not, the user is informed the username or email is already being used
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
                dlg = CustomDialog("Registration Success", "Account has been created! Please check your email for your 2FA codes.")
                dlg.exec()
                self.goToLogin()
            elif msg == "!FAILURE":
                print(f"Error: Username or Email already in use.")

    # Switches to the Login menu
    def goToLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# First stage of the reset password menu
class ResetPasswordStage1(QDialog):
    def __init__(self):
        super(ResetPasswordStage1, self).__init__()
        loadUi("resetPasswordStage1.ui", self)
        self.confirmButton.clicked.connect(self.step1)
        self.loginButton.clicked.connect(self.goToLogin)

    # Step 1 of the password reset proccess
    # Sends the given email to the server to check if it is there
    # If it is, the server will send a code and the user will go to the next stage
    # If not, the user will be notified that the email is either invalid or not in the database
    def step1(self):
        email = self.email.text()
        print(f"Attempting to reset account password with email {email}")
        if(validLoginInfo.checkValidEmail(email)):
            client.send(email)
            response = client.receiveMessage()
            if response == "!SUCCESS":
                print(f"Email success!")
                self.goToResetPasswordStage2()
            else:
                dlg = CustomDialog("Email not found", "Email not found in database. Please check your spelling and try again.")
                dlg.exec()
        else:
            dlg = CustomDialog("Invalid email", "Email not valid. Please check your spelling and try again.")
            dlg.exec()

    # Switches to the Reset Password stage 2 menu
    def goToResetPasswordStage2(self):
        resetPasswordStage2 = ResetPasswordStage2(self.email.text())
        widget.addWidget(resetPasswordStage2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login menu
    def goToLogin(self):
        client.send("!CANCEL")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Second stage of the reset password menu
class ResetPasswordStage2(QDialog):
    def __init__(self, email):
        super(ResetPasswordStage2, self).__init__()
        loadUi("resetPasswordStage2.ui", self)
        self.email.setText(email)
        self.confirmButton.clicked.connect(self.step2)
        self.loginButton.clicked.connect(self.goToLogin)

    # Step 2 of the password reset proccess
    # Sends the code that the user entered in to the server to verify if it's the one that was emailed to them
    # If yes, goes to stage 3
    # If not, the user is informed that the code is not valid
    # If too many incorrect codes are used, the user is sent back to the login screen
    def step2(self):
        code = self.code.text()
        print(f"Sending verification code {code}")
        client.send(code)
        response = client.receiveMessage()
        if response == "!SUCCESS":
            self.goToResetPasswordStage3()
        elif response == "!FAILURE":
            dlg = CustomDialog("Incorrect code", "Code not valid. Please check your spelling and try again.")
            dlg.exec()
        elif response == "!STOP":
            dlg = CustomDialog("Too many incorrect codes", "Too many incorrect codes have been entered. Please try again later.")
            dlg.finished.connect(self.onPopupClosed)
            dlg.exec()

    # Switches to the Reset Password stage 3 menu
    def goToResetPasswordStage3(self):
        resetPasswordStage3 = ResetPasswordStage3(self.email.text())
        widget.addWidget(resetPasswordStage3)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login menu when the popup is closed
    def onPopupClosed(self, result):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login menu and informs the server to cancel the password reset proccess
    def goToLogin(self):
        client.send("!CANCEL")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Third stage of the reset password menu
class ResetPasswordStage3(QDialog):
    def __init__(self, email):
        super(ResetPasswordStage3, self).__init__()
        loadUi("resetPasswordStage3.ui", self)
        self.email.setText(email)
        self.confirmButton.clicked.connect(self.step3)
        self.loginButton.clicked.connect(self.goToLogin)

    # Step 3 of the reset password proccess
    # If the information entered is valid, the information is sent to the server
    # If the password is the same as the previous one, the user is informed to pick a different one
    # Otherwise, the password is successfully reset and the user is sent back to the Login screen
    def step3(self):
        password = self.password.text()
        passwordConfirm = self.passwordConfirm.text()
        authenticationNumber = self.selection2FA.currentText()
        if not validLoginInfo.checkValidPassword(password):
            dlg = CustomDialog("Invalid Password", "Password not valid. Must be 8-20 characters long, with at least 1 uppercase, 1 lowercase, 1 number, and 1 symbol (@$#%)")
            dlg.exec()
        elif not authenticationNumber.isdigit():
            dlg = CustomDialog("No Authentication Number", "Must select an authentication number")
            dlg.exec()
        elif not password == passwordConfirm:
            dlg = CustomDialog("Passwords don't match", "Passwords do not match. Please check your spelling and try again.")
            dlg.exec()
        
        else:
            client.send(password)
            client.send(authenticationNumber)
            response = client.receiveMessage()
            if response == "!SAME":
                dlg = CustomDialog("Same Password", "Password cannot be the same as the old password.")
                dlg.exec()
            if response == "!SUCCESS":
                dlg = CustomDialog("Success!", "Password has been reset! Please check your email for new 2FA codes.")
                dlg.finished.connect(self.onPopupClosed)
                dlg.exec()

    # Switches to the Login menu when the popup is closed
    def onPopupClosed(self, result):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Login menu and also informs the server to cancel the password reset proccess
    def goToLogin(self):
        client.send("!CANCEL")
        client.send("!CANCEL")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Login success menu (currently unused, mainly for testing)
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

# Main menu
class MainMenu(QDialog):
    def __init__(self, username):
        super(MainMenu, self).__init__()
        loadUi("mainMenu.ui", self)
        self.usernameLabel.setText(username)
        self.logoutButton.clicked.connect(self.logout)
        self.goToUploadButton.clicked.connect(self.goToUpload)
        self.goToDownloadButton.clicked.connect(self.goToDownload)
        self.goToDeleteButton.clicked.connect(self.goToDelete)

    # Logs the user out and sends them to the login screen
    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Upload File menu
    def goToUpload(self):
        uploadMenu = UploadMenu(self.usernameLabel.text())
        widget.addWidget(uploadMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Download File menu
    def goToDownload(self):
        downloadMenu = DownloadMenu(self.usernameLabel.text())
        widget.addWidget(downloadMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Switches to the Delete File menu
    def goToDelete(self):
        deleteMenu = DeleteMenu(self.usernameLabel.text())
        widget.addWidget(deleteMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Upload File menu
class UploadMenu(QDialog):
    def __init__(self, username):
        super(UploadMenu, self).__init__()
        loadUi("uploadMenu.ui", self)
        self.usernameLabel.setText(username)
        self.logoutButton.clicked.connect(self.logout)
        self.browseButton.clicked.connect(self.browseFiles)
        self.uploadButton.clicked.connect(self.sendFile)
        self.mainMenuButton.clicked.connect(self.goToMainMenu)

    # Logs the user out and sends them to the login screen
    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Allows the user to browse local files and select one to upload
    def browseFiles(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', ".\localfiles")
        self.fileSelected.setText(file_name[0])

    # If a file has been selected, send it to the server
    def sendFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
            dlg = CustomDialog("No File selected", "No file has been selected. Please select a file to upload.")
            dlg.exec()
        else:
            client.sendFile(self.fileSelected.text())
            dlg = CustomDialog("File Uploaded", "File has been uploaded.")
            dlg.exec()

    # Switches to the Main menu
    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Download File menu
class DownloadMenu(QDialog):
    def __init__(self, username):
        super(DownloadMenu, self).__init__()
        loadUi("downloadMenu.ui", self)
        self.usernameLabel.setText(username)
        self.updateList()
        self.logoutButton.clicked.connect(self.logout)
        self.selectFileButton.clicked.connect(self.selectFile)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.mainMenuButton.clicked.connect(self.goToMainMenu)

    # Gets a list of files saved on the server and displays it on the file list
    def updateList(self):
        client.send(client.FILE_LIST_MESSAGE)
        list = client.receiveList()
        self.fileList.addItems(list)

    # Logs the user out and sends them to the login screen
    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Sets the currently selected file on the file list as the one for download
    def selectFile(self):
        currentIndex = self.fileList.currentRow()
        item = self.fileList.item(currentIndex)
        self.fileSelected.setText(item.text())

    # Downloads the selected file from the server
    def downloadFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
        else:
            client.send(client.FILE_DOWNLOAD_MESSAGE)
            client.send(self.fileSelected.text())
            client.receiveFile()
            dlg = CustomDialog("File Downloaded", "File has been downloaded.")
            dlg.exec()

    # Switches to the Main menu
    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Delete File menu
class DeleteMenu(QDialog):
    def __init__(self, username):
        super(DeleteMenu, self).__init__()
        loadUi("deleteMenu.ui", self)
        self.usernameLabel.setText(username)
        self.updateList()
        self.logoutButton.clicked.connect(self.logout)
        self.selectFileButton.clicked.connect(self.selectFile)
        self.deleteButton.clicked.connect(self.deleteFile)
        self.mainMenuButton.clicked.connect(self.goToMainMenu)

    # Gets a list of files saved on the server and displays it on the file list
    def updateList(self):
        client.send(client.FILE_LIST_MESSAGE)
        list = client.receiveList()
        self.fileList.clear()
        self.fileList.addItems(list)

    # Logs the user out and sends them to the login screen
    def logout(self):

        client.send(client.LOGOUT_MESSAGE)

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Sets the currently selected file on the file list as the one for download
    def selectFile(self):
        currentIndex = self.fileList.currentRow()
        item = self.fileList.item(currentIndex)
        self.fileSelected.setText(item.text())

    # Informs the server to delete the specified file
    def deleteFile(self):
        if self.fileSelected.text() == "":
            print("Error: No file selected")
        else:
            client.send(client.FILE_DELETE_MESSAGE)
            client.send(self.fileSelected.text())
            self.updateList()
            dlg = CustomDialog("File Deleted", "File has been deleted.")
            dlg.exec()

    # Switches to the Main menu
    def goToMainMenu(self):
        mainMenu = MainMenu(self.usernameLabel.text())
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# Popups that appear to the user with certain messages
class CustomDialog(QDialog):
    def __init__(self, windowMessage, dialogMessage):
        super().__init__()

        self.setWindowTitle(windowMessage)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        layout = QVBoxLayout()
        message = QLabel(dialogMessage)
        layout.addWidget(message)
        self.setLayout(layout)

# Initializes the PyQt5 application and displays it
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
app.exec_()