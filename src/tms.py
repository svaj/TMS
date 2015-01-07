import time
from conf import settings
from http.server import TMSWebServer
from smtp.server import TMSEmailServer
from db.query import init_db, delete_db
import os
import pwd

if __name__ == "__main__":
    init_db()

    mailServer = TMSEmailServer((settings.LISTEN_IP, settings.SMTP_PORT))
    mailServer.start()

    webServer = TMSWebServer((settings.LISTEN_IP, settings.WEB_PORT))
    webServer.start()

    print "TMS Running"
    running = True
    u = pwd.getpwnam(settings.DROP_TO_USER)
    os.setgid(u.pw_gid)
    os.setuid(u.pw_uid)

    while running:
        try:
            time.sleep(1)
        except:
            mailServer.stop()
            webServer.stop()
            del mailServer
            del webServer
            running = False
            delete_db()
            print "TMS Stopped"
