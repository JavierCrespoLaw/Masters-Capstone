import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import time
import pyotp
import qrcode

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import os
import shutil

def emailQRCodes(username, email_server, password_server, email_receiver, code1, code2, code3):

    tempdir = ".\\Temp\\" + username
    os.makedirs(tempdir, exist_ok=True)

    #qrFile1 = NamedTemporaryFile(suffix=".png", dir=tempdir.name)
    #qrFile2 = NamedTemporaryFile(suffix=".png", dir=tempdir.name)
    #qrFile3 = NamedTemporaryFile(suffix=".png", dir=tempdir.name)

    totp1 = pyotp.TOTP(code1)
    totp2 = pyotp.TOTP(code2)
    totp3 = pyotp.TOTP(code3)

    uri1 = totp1.provisioning_uri(name="File Storage System", 
                                  issuer_name = f"{username} Code 1")
    uri2 = totp2.provisioning_uri(name="File Storage System", 
                                  issuer_name = f"{username} Code 2")
    uri3 = totp3.provisioning_uri(name="File Storage System", 
                                  issuer_name = f"{username} Code 3")
    
    qrcode.make(uri1).save(tempdir + "\\QRFile1.png")
    qrcode.make(uri2).save(tempdir + "\\QRFile2.png")
    qrcode.make(uri3).save(tempdir + "\\QRFile3.png")

    message = MIMEMultipart()
    message['FROM'] = email_server
    message['TO'] = email_receiver
    message['SUBJECT'] = f"{username} 2FA codes"

    body = f"""Hello {username},
            \n\nThis email was sent to you because you have just registered an account with this email.
            \n\nAttached are the 2FA codes associated with your account. Please scan them with Google Authenticator to use for your login process.
            \n\nReminder: Only use the code with the number selected during registration. Failure to do so will result in a temporary lock on your account.
            \n\nIf you did not create an account, you may ignore this email.
            """
    message.attach(MIMEText(body, 'plain'))

    attachment1 = open(tempdir + "\\QRFile1.png", 'rb')
    part1 = MIMEBase('application', 'octet-stream')
    part1.set_payload((attachment1).read())
    encoders.encode_base64(part1)
    part1.add_header('Content-Disposition', "attachment; filename=QR_Code_1.png")

    attachment2 = open(tempdir + "\\QRFile2.png", 'rb')
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment2).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename=QR_Code_2.png")

    attachment3 = open(tempdir + "\\QRFile3.png", 'rb')
    part3 = MIMEBase('application', 'octet-stream')
    part3.set_payload((attachment3).read())
    encoders.encode_base64(part3)
    part3.add_header('Content-Disposition', "attachment; filename=QR_Code_3.png")

    message.attach(part1)
    message.attach(part2)
    message.attach(part3)

    text = message.as_string()

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(email_server, password_server)

    server.sendmail(email_server, email_receiver, text)

    print(f"Email has been sent from {email_server} to {email_receiver}. ")
    attachment1.close()
    attachment2.close()
    attachment3.close()

    shutil.rmtree(tempdir)