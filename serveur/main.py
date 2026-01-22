"""Point d'entree principal du serveur mail.

Lance les serveurs SMTP et POP3 en parallele.
Utilisation : python main.py [port_smtp] [port_pop3]
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from serveur.smtp_server import SMTPServer
from serveur.pop3_server import POP3Server


def main():
    """Fonction principale qui lance les serveurs SMTP et POP3."""
    host = "127.0.0.1"
    port_smtp = 2525
    port_pop3 = 1100

    if len(sys.argv) > 1:
        port_smtp = int(sys.argv[1])

    if len(sys.argv) > 2:
        port_pop3 = int(sys.argv[2])

    smtp_server = SMTPServer(host, port_smtp)
    pop3_server = POP3Server(host, port_pop3)

    thread_smtp = threading.Thread(target=smtp_server.start)
    thread_pop3 = threading.Thread(target=pop3_server.start)

    thread_smtp.daemon = True
    thread_pop3.daemon = True

    print("Demarrage du serveur mail...")
    print("SMTP: port " + str(port_smtp) + " (envoi)")
    print("POP3: port " + str(port_pop3) + " (consultation)")
    print("")

    thread_smtp.start()
    thread_pop3.start()

    try:
        while True:
            thread_smtp.join(1)
            thread_pop3.join(1)
    except KeyboardInterrupt:
        print("\nArret des serveurs...")
        smtp_server.stop()
        pop3_server.stop()


if __name__ == "__main__":
    main()
