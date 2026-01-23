"""Point d'entree du serveur POP3.

Lance le serveur POP3 sur le port specifie en argument.
Utilisation : python server_pop3.py [port]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from serveur.pop3_server import POP3Server


def main():
    """Fonction principale qui lance le serveur POP3."""
    host = "127.0.0.1"
    port = 1100

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    server = POP3Server(host, port)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
