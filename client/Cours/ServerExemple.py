import socket
if __name__ == '__main__':
    # Etape 1 : création de la socket d'écoute
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ecoute:
        # Permet de relancer le serveur immédiatement sans erreur "Address already in use"
        ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Etape 1 suite : liaison de la socket d'écoute (choix du port)
        ecoute.bind(('', 65432))
        # Etape 2 : ouverture du service
        ecoute.listen()
        while True:
            # Etape 3 : attente et acceptation d'une nouvelle connexion
            service, addr = ecoute.accept()
            # on fermera automatiquement la connexion
            with service:
                print('Connecté à ', addr)
                while True:
                    # Etape 4 : réception d'au max 1024 octets
                    data = service.recv(1024)
                    # si le client a fermé la connexion on arrête la boucle
                    if not data:
                        break
                    # décodage et affichage des données reçues
                    st = data.decode('utf-8')
                    print(st)
                    # Etape 4 suite : on renvoi les données au client
                    service.sendall(data)
    # Etape 5 : fermeture socket de service
    # (automatiquement par le with service)
    # Etape 6 : fermeture de la socket d'écoute
    # (automatiquement par le with ecoute)