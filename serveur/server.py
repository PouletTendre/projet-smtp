"""Point d'entree du serveur SMTP.

Lance le serveur sur le port specifie en argument (par defaut 2525).
Utilisation : python server.py [port]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from serveur.smtp_server import SMTPServer


def main():
    """Fonction principale qui lance le serveur SMTP."""
    host = "127.0.0.1"
    port = 2525

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = SMTPServer(host, port)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
