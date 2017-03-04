'''
Created on Mar 4, 2017

@author: Robin

This script is for deleting all email in a specific folder
'''

import imaplib

# input your email address
email = ""
# input your email password
passw = ""
# input imap server. Look at this https://www.arclab.com/en/kb/email/list-of-smtp-and-imap-servers-mailserver-list.html 
imapserver = "imap.gmail.com"

def deleteEmailIMAP(user, password, IMAP):
    mail = imaplib.IMAP4_SSL(IMAP)
    mail.login(user, password)
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    for num in data[0].split():
        mail.store(num, '+FLAGS', r'(\Deleted)')
    mail.expunge()
    mail.close()
    mail.logout()
    
deleteEmailIMAP(email, passw, imapserver)