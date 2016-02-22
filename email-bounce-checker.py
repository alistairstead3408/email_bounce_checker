#!/usr/bin/env python
#
# Alistair Stead
# Extension of code borrowed from https://gist.github.com/robulouski/7441883
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime
import re
import getpass
import time
from collections import Counter

# Things to do: 
# - Improve keyword search
# - Improve blacklist
# - Test on all messages received on my account


EMAIL_ADDRESS = "rutherfordbounces@gmail.com"
EMAIL_FOLDER = "INBOX"

EMAIL_REGEX_PATTERN = ("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)")

DOMAINS_TO_IGNORE = ["isaacphysics.org", "cl.cam.ac.uk", "postmaster", "google.com", "mailer-daemon"]

# Method to scan through the mailbox to check for bounced emails
# - checks using a combination of keywords
#
def scan_for_bounces(mailbox):
    """Scans a given mailbox for DNS emails.

       - Starts by checking X-Failed-Recipients
       - Then checks MIME type
       - Then looks for keywords
    """
    results = []
    rv, data = mailbox.search(None, "unseen")

    if rv != 'OK':
        print "No messages found!"
        return [None]
    print "Mailbox size: ", str(len(data[0].split()))

    # Iterate through each unread email
    for num in data[0].split():
        print "Processing email", num
        rv, data = mailbox.fetch(num, '(RFC822)')
        if rv != 'OK':
            print " - ERROR getting message", num
            continue
        
        #Mark everything as read so we don't look at it again
        #mailbox.store(num, '+FLAGS', 'SEEN')

        msg = email.message_from_string(data[0][1])

        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])

        decode = email.header.decode_header(msg['X-Failed-Recipients'])[0]
        failed_recipients = unicode(decode[0])

        # In the best case, the email will use X-Failed-Recipients (see http://stackoverflow.com/questions/5298285/detecting-if-an-email-is-a-delivery-status-notification-and-extract-informatio)
        # if failed_recipients != "None":
        #     results.append(failed_recipients)
        #     print " - X-Failed-Recipients found", failed_recipients
        #     continue

        # In the medium case, the email will declare its type as delivery status, and we can scan for the email
        # if msg.is_multipart() and len(msg.get_payload()) > 1 and msg.get_payload(1).get_content_type() == 'message/delivery-status':
        #     print msg.get_payload(0).get_payload()
        #     print " - DNS MIME type found"

        # In the worst case, the email won't declare itself a DSN, and we'll have to scan for keywords (returning at most one email)
        keywordRegexp = ("mail delivery failed", "failure", "no such email")
        totalMessage = subject.lower() + msg.as_string().lower()

        if not any(s in totalMessage for s in keywordRegexp):
            print " - no keyword match"
            continue 

        parsedEmailList = []

        for email_match in re.finditer(EMAIL_REGEX_PATTERN, msg.as_string()):
            if email_match.group(0) != EMAIL_ADDRESS:
                parsedEmailList.append(email_match.group(0))

        print " - " + str(len(parsedEmailList)) + " email addresses found during scan"

        # Assume that the correct email to return does not contain a domain on our blacklist and appears more than once
        for item in DOMAINS_TO_IGNORE:
            filter(lambda a: re.search(item, a), parsedEmailList)

        print " - " + str(len(Counter(parsedEmailList))) + " unique emails found"
        print " - Picking most common " + str(Counter(parsedEmailList).most_common)
        results.append(Counter(parsedEmailList).most_common)


    return results

    


# Method to update the API with email addresses that have bounced
# - checks using a combination of keywords
#
def update_API_with_bounced_email_addresses(emails):
    print str(len(emails)) + " emails found"
    print str(emails)



if __name__ == '__main__':
    mailbox = imaplib.IMAP4_SSL('imap.gmail.com')


    print "Please enter the password:"
    password = getpass.getpass()

    try:
        rv, data = mailbox.login(EMAIL_ADDRESS, password)
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!"
        sys.exit(1)

    print rv, data

    rv, data = mailbox.select(EMAIL_FOLDER)
    if rv == 'OK':
        print "Processing mailbox...\n"
        bouncedEmailAddresses = scan_for_bounces(mailbox)
        mailbox.close()
    else:
        print "ERROR: Unable to open mailbox ", rv

    print "List of bounced email addresses:"
    update_API_with_bounced_email_addresses(bouncedEmailAddresses)

    mailbox.logout()