import site
import site
import string
import random
import re
from splinter import Browser
import time
import winsound
import sys
import os

def ran_gen(size = 5, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits, splitter = '-', splitevery = 5):
    return re.sub('(.{' + str(splitevery) + '}(?!$))', '\\1' + str(splitter), ''.join((random.choice(chars) for _ in range(size))), 0)

def playSound(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME)

print ''
print 'If this shows any errors while entering keys, simply restart the program.'
print 'All working keys are stored in workingKeys.log in the running directory.'
print 'Do not minimize the browser window.  Leave it running in the background.'
print '\nLogin information:'
username = raw_input('Username: ')
password = raw_input('Password: ')
print '\nOptions'
debug = raw_input('Do you want to show debugging information (Yes/No): ')
if 'yes' in debug.lower():
    debug = True
raw_input('\nPress Enter to start...')
with Browser() as browser:
    if debug == True:
        print 'Navigating to xbox code redemption website'
    url = 'https://account.xbox.com/en-US/PaymentAndBilling/RedeemCode'
    browser.visit(url)
    browser.find_by_id('redeemCodeBtn').click()
    if debug == True:
        print 'Attempting to log in'
    while browser.is_text_present('Sign in'):
        browser.fill('login', username)
        browser.fill('passwd', password)
        browser.check('KMSI')
        browser.find_by_name('SI').click()
        if browser.is_text_present('Sign in'):
            print 'Incorrect username or password'
            username = raw_input('Username: ')
            password = raw_input('Password: ')
        elif debug == True:
            print 'Log in successful'

    while not url == 'https://account.xbox.com/en-US/PaymentAndBilling/RedeemCode':
        time.sleep(1)

    while True:
        if debug == True:
            print 'Activating code redemption screen'
        browser.find_by_id('redeemCodeBtn').click()
        time.sleep(2)
        with browser.get_iframe('blenderIFrame') as iframe1:
            with iframe1.get_iframe('webBlendHost') as iframe2:
                with iframe2.get_iframe('appHost') as iframe:
                    if debug == True:
                        print 'Requesting key information'
                    randomKey = ran_gen(25, string.ascii_uppercase + string.digits, '-', 5)
                    iframe.find_by_id('tokenField').fill(randomKey)
                    buttons = iframe.find_by_tag('button')
                    buttons[-2].click()
                    time.sleep(1)
                    returnVal = ''
                    if iframe.is_element_present_by_id('ember381'):
                        returnVal = iframe.find_by_id('ember381').first.find_by_tag('h1').first.text
                    else:
                        returnval = 'Confirmed'
                    time.sleep(1)
                    if 'This code has already been used' in returnVal:
                        print 'Key ' + randomKey + ' has already been used'
                        for button in iframe.find_by_tag('button'):
                            if 'Close' in button.text:
                                button.click()

                    elif 'Try the code again' in returnVal:
                        print 'Key ' + randomKey + ' is an invalid key'
                        for button in iframe.find_by_tag('button'):
                            if 'Close' in button.text:
                                button.click()

                    elif 'Confirm' in iframe.find_by_tag('button')[-3].text:
                        print 'Key ' + randomKey + ' is valid'
                        playSound('notify.wav')
                        logFile = open('workingKeys.log', 'a+')
                        logFile.write(randomKey + '\r\n')
                        logFile.close()
                        for button in iframe.find_by_tag('button'):
                            if 'Close' in button.text:
                                button.click()

                    else:
                        print 'Unknown error from key ' + randomKey
                        for button in iframe.find_by_tag('button'):
                            if 'Close' in button.text:
                                button.click()

                    time.sleep(1)