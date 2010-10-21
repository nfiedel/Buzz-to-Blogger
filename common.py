

import os


def GetBaseUri():
    if os.environ['SERVER_SOFTWARE'].find('Development') >= 0:
        return 'http://localhost:8080'
    else:
        return 'http://buzztoblogger.appspot.com'
