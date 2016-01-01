import hashlib
import requests
import time
import config
import re
import sys
import json
from pprint import pprint

BASE_URL = 'http://forum.toribash.com'

# Save a page html to verify what has happened. 
def saveHTML(filename, data):
    file = open(filename + '.html', 'w')
    file.write((data.text).encode('utf-8'))

# Send a pm.
def sendPm(session, recipient, title, message):
    print "Getting pm page."
    pm_page =  session.get(BASE_URL + '/private.php')

    # Get admin hash and security token value necessary to pm.
    s = getS(session, pm_page)
    security_token = getSecurity(session, pm_page)

    # Pm info parameters.
    payload = {
    'recipients': recipient,
    'bccrecipients': '',
    'title': title,
    'message': message,
    'wysiwyg': 1,
    'iconid' : 0,
    's': s,
    'securitytoken': security_token,
    'do': 'insertpm',
    'pmid': '',
    'forward': '',
    'sbutton': 'Submit Message',
    'savecopy': 1,
    'signature': 1,
    'parseurl': 1
    }

    # Actually send the pm.
    print "PMing %s" % (recipient)
    r = session.post(BASE_URL + '/private.php?do=insertpm&pmid=', payload)

# Get the s value from a page.
def getS(session, page):
    snumber = re.search(r'<input type="hidden" name="s" value="(.*)" />', page.text)
    return snumber.group(1)

# Get the security token value from a page.
def getSecurity(session, page):
    sectoken = re.search(r'<input type="hidden" name="securitytoken" value="(.*)" />', page.text)
    return sectoken.group(1)

# Get the thread number given a thread url.
def getThreadNum(thread):
    return thread.split('=')[1]

# Get the last post value from a thread.
def getLastPost(session, page):
    sectoken = re.search(r'var ajax_last_post = (.*);', page.text)
    return sectoken.group(1)

# Get the admin hash necessary for some mod tools.
def getAdminHash(session, page):
    adminhash = re.search(r'<input type="hidden" name="adminhash" value="(.*)" />', page.text)
    return adminhash.group(1)

# Get a thread's title.
def getTitle(session, page):
    title = re.search(r'<title> (.*) - Toribash Community</title>', page.text)
    return title.group(1)

# Post a message.
def postMessage(session, lastpost, message, s, securitytoken, thread):
    page =  session.get(thread)
    t = getThreadNum(thread)
    s = getS(session, page)
    security_token = getSecurity(session, page)
    last_post = getLastPost(session, page)

    payload = {
    'ajax': '1',
    'ajax_lastpost': lastpost,
    'do': 'postreply',
    'fromquickreply': '1',
    'loggedinuser': '436450',
    'message': message,
    'p': 'who cares',
    'parseurl': '1',
    's': s,
    'securitytoken': [security_token, security_token],
    'signature': '1',
    'specifiedpost': '0',
    'styleid': '0',
    't': t,
    'wysiwyg': '1'
    }

    r = session.post(BASE_URL + '/newreply.php?do=postreply&t=%s' % (t), payload)
    print "Posted the message."

# Send item(s) to a user. 
def sendItem(session, itemid, recipient, override=False, shop_admin=False, omit_errors=False):
    # Send info parameters.
    payload = {
    'action': 'senditem',
    'userid': '436450',
    'to_username': recipient,
    'message' : '',
    'giftid[]': str(itemid) # If multiple items are to be sent then the itemid argument should be a list with the itemids as strings within.
    }

    # Handle extra non default tsa options.
    if override:
        payload['use_admin_override'] = 'on'
        
    if shop_admin:
        payload['via_shop_admin'] = 'on'

    if omit_errors:
        payload['omit_items_with_errors'] = 'on'

    r = session.post(BASE_URL + '/tori_utilities.php', payload)
    print "Sent item to %s" % (recipient)

# Find usernames by ip.
def findNames(session, ip):
    print "Getting name list."
    ip_page =  session.get(BASE_URL + ('/tori_login_history.php?ip=%s&status=0&groupby=userid' % ip))

    # Regex to find all usernames.
    return re.findall(r'data-userid="[0-9]*">(.*)</a>', ip_page.text)
    
# Ban a user.
def banUser(session, name, reason, length):
    print "Getting ban page."
    ban_page = session.get(BASE_URL + '/modcp/banning.php?do=banuser')

    # Grab ban page to get admin hash and security token value necessary to ban.
    admin_hash = getAdminHash(session, ban_page)
    security_token = getSecurity(session, ban_page)

    # Ban info parameters.
    payload = {
    'do': 'dobanuser',
    'adminhash': admin_hash,
    'securitytoken': security_token,
    'username' : name,
    'usergroupid': '137', # Suspended/banned.
    'period': length, # The ban length.
    'reason': reason # The reason
    }

    # Actually do the ban.
    print ("Banning user %s" % name)
    r = session.post(BASE_URL + '/modcp/banning.php?do=dobanuser', payload)

# Get a token needed for official Toribash API stuff.
def getToken(session):
    return session.get(BASE_URL + '/bank_ajax.php?bank_ajax=get_token').json()['token']

# Login. Mode can be set to 'admin' for admincp functions and 'mod' for modcp functions.
def login(mode = None):
    with requests.Session() as login_session:

        # Login info parameters.
        payload = {
        'do': 'login',
        'vb_login_md5password': hashlib.md5(config.password.encode()).hexdigest(),
        'vb_login_md5password_utf': hashlib.md5(config.password.encode()).hexdigest(),
        'vb_login_username': config.username,
        'vb_login_password': ''
        }

        print "Grabbing login page."
        if mode == None:
            url = '/login.php?do=login'
            login_page =  login_session.get(BASE_URL + url)
        elif mode == 'mod':
            url = '/modcp/index.php'
            payload['url'] = url
            payload['logintype'] = 'modcplogin'
            login_page =  login_session.get(BASE_URL + url)
        elif mode == 'admin':
            url = '/admincp/index.php'
            payload['url'] = url
            payload['logintype'] = 'cplogin'
            login_page =  login_session.get(BASE_URL + url, auth=(config.admin_username, config.admin_password))

        # Grab login page to get security token value and s value.
        payload['s'] = getS(login_session, login_page)
        payload['security_token'] = getSecurity(login_session, login_page)

        # Actually login.
        print "Logging in."
        login_result = login_session.post(BASE_URL + '/login.php?do=login', payload)
        return login_session