#!/usr/bin/python3

'''
Subcounter accesses Reddit and pulls the subcscriber count
for some of the subs I mod. Using that data it: prints it
to the terminal, appends a file, and emails me a digest.

You can of course use it for any subs you want the subscriber count of. Enjoy!

To have it run automatically you will need to use cron or something of the like
and make this file executable.

I use .format() in this as the Raspberry Pi does not yet support f'strings since
it runs on an older version of Python 3. If you're running this on an updated
device, or you have manually updated your Pi's Python, then it's up to your choice.
'''

import praw, time, datetime, smtplib, ssl, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# I like when code prints in a staggered time, if you don't like this, remove sleepy() and all of its calls.
def sleepy():
	time.sleep(0.5)

# Reddit access
reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET', 
                     password='YOUR PASSWORD', 
                     user_agent='NEEDS DESCRIPTION - VERSION COUNT - (by /u/YOUR USERNAME)',
                     username='YOUR USERNAME')

# This runs in read only mode, this can be changed.
reddit.read_only = True

'''
Example uses r/learnpython and favorites of mine r/meholdingstuff & r/JenniferMillsNews.
You can have as many of these as you would like. I personally track 4 subreddits.
'''

learnpython = reddit.subreddit('learnpython').subscribers
meholdingstuff = reddit.subreddit('meholdingstuff').subscribers
jennifermillsnews = reddit.subreddit('jennifermillsnews').subscribers
lp = 'r/LearnPython has {0} subscribers'.format(learnpython)
mhs = 'r/MeHoldingStuff has {0} subscribers'.format(meholdingstuff)
jmn = 'r/JenniferMillsNews has {0} subscribers'.format(jennifermillsnews)

print('Fetching subscriber counts...\n')
sleepy()
print(lp)
sleepy()
print(mhs)
sleepy()
print(jmn)
sleepy()
print('\nUpdating subcounter.txt...\n')
sleepy()

'''
This writes to the file to keep a log. The try and except blocks are only
useful if you are looking to run this in the console manually. People who
are automating may want to have it send an email or something if it fails.
'''
try:
    f = open('FILE_PATH_TO_DATA_STORAGE_DOCUMENT.txt', 'a')
    # This datetime below just uses seconds and above.
    f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n' + lp + '\n' + mhs + '\n' + jmn + '\n\n')
    f.close()
    print('File saved successfully at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
except Exception:
    print('Error in saving file at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

sleepy()

print('\nSending Email...\n')

'''
This below is all email. You may change the settings condsiderably.
This is set up for use with gmail. It is not typically a good idea to
have your password saved, so if not automating, maybe change the password
variable to an input.
'''
port = 465  # For SSL
password = "GMAIL PASSWORD"
sender_email = "SENDER_EMAIL@gmail.com"
receiver_email = "RECEIVER.EMAIL.com"
message = """\
Subject: Subcounter Update

{}
{}
{}""".format(lp, mhs, jmn)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("SENDER_GMAIL@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)
    
sleepy()
print('Email sent')

sleepy()

print('This program brought to you by Grizzled Labs')
