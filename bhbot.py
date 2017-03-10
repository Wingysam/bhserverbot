import os
import sys
import ast
import time

def receiveMessage(message):
    message = str(message).lower()
    message = ast.literal_eval(message)
    for trigger_response in triggers_responses:
        if trigger_response[0].lower() in str(message):
            sendMessage(trigger_response[1])

def sendMessage(message):
    os.system("osascript -e 'tell application " + '"BlockheadsServer" to activate' + "'")
    time.sleep(1)
    for char in message:
        os.system('osascript -e ' + "'tell application " + '"System Events" to keystroke "' + str(char) + '"'  + "'")
    os.system('osascript -e ' + "'tell application " + '"System Events" to keystroke ' + str('return') + ''  + "'")

def readsyslog():
    global bhlog
    syslogfile = open('/private/var/log/system.log')
    syslog = syslogfile.read()
    syslogfile.close()
    syslog = syslog.replace(' ', '<spaceforpythonscript>').replace('\n', ' ').split()
    syslog = ast.literal_eval(str(syslog).replace('<spaceforpythonscript>', ' '))
    bhlog = []
    for item in syslog:
        if 'BlockheadsServer' in item:
            bhlog += [item]


def bot():
    global triggers_responses
    global bhlog
    print('Go to the server app and click the "Send Message" box.\n\nGo to this terminal, and Hold the Control key and press C to quit.')
    try:
        triggers_responses = open('/Users/Shared/bhserverbotdatabase').read()
        triggers_responses = ast.literal_eval(triggers_responses)
    except:
        triggers_responses = []
        os.system('echo "[]" > /Users/Shared/bhserverbotdatabase')
    while True:

        readsyslog()
        log = bhlog[len(bhlog) - 1]
        log = log[log.find(']'):]
        log = log[log.find(' - '):]
        clog = log
        if ':' in log:
            olog = log
            while str(clog) == str(olog):
                time.sleep(1)
                readsyslog()
                clog = bhlog[len(bhlog) - 1]
                clog = clog[clog.find(']'):]
                clog = clog[clog.find(' - '):]
                if str(clog) != str(log):
                    cmsg = bhlog[len(bhlog) - 1]
                    cmsg = cmsg[cmsg.find(' - '):]
                    cmsg = cmsg[cmsg.find(':'):]
                    try:
                        cmsg = cmsg[cmsg.find(cmsg[2]):]
                    except:
                        pass
            receiveMessage([cmsg])
        time.sleep(1)

if sys.version[:1] == '2':
    def input(message):
        return(raw_input(message))

os.system('clear')
print('''
-- Menu --
1. Run bot
2. View triggers
3. Add trigger
4. Remove trigger
5. Reset triggers
6. Take over the world
''')
response = str(input('Choice: '))
if response == '1':
    bot()
elif response == '2':
    try:
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    except:
        os.system('echo "[]" > /Users/Shared/bhserverbotdatabase')
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    db = ast.literal_eval(dbfile.read())
    dbfile.close()
    i = 0
    for item in db:
        print(str(i) + '. ' + str(item))
        i += 1
elif response == '3':
    trigger = input('Trigger: ')
    response = input('Response: ')
    try:
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    except:
        os.system('echo "[]" > /Users/Shared/bhserverbotdatabase')
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    db = ast.literal_eval(dbfile.read())
    dbfile.close()
    db += [[trigger, response]]
    dbfile = open('/Users/Shared/bhserverbotdatabase', 'w')
    dbfile.write(str(db))
    dbfile.close()
    exit('Trigger Added!')
elif response == '4':
    try:
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    except:
        os.system('echo "[]" > /Users/Shared/bhserverbotdatabase')
        dbfile = open('/Users/Shared/bhserverbotdatabase')
    db = ast.literal_eval(dbfile.read())
    dbfile.close()
    i = 0
    for item in db:
        print(str(i) + '. ' + str(item))
        i += 1
    trigger_to_remove = input('Trigger to remove: ')
    if len(db) - 1 < int(trigger_to_remove):
        exit('Does not exist')
    db.pop(int(trigger_to_remove))
    dbfile = open('/Users/Shared/bhserverbotdatabase', 'w')
    dbfile.write(str(db))
    dbfile.close()
elif response == '5':
    try:
        dbfile = open('/Users/Shared/bhserverbotdatabase','w')
    except:
        os.system('echo "[]" > /Users/Shared/bhserverbotdatabase')
        dbfile = open('/Users/Shared/bhserverbotdatabase','w')
    dbfile.write('[]')
    dbfile.close()
elif response == '6':
    exit("You're not allowed to do that!")
elif response == '':
    bot()
else:
    exit('Unknown response.')
