import socket
import re

# ici on va vérifier si le format d'adresse mail est correcte ou non ! 
def demander_et_envoyer(prompt, sock):
    while True:
        email = input(prompt)
        if re.match(r".+@.+\..+", email):
            sock.sendall(email.encode('utf-8'))
            break
        print("Format invalide. Veuillez entrer une adresse du type x@y.z")

if __name__ == '__main__':
    # Etape 1 : création de la socket cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Etape 1 suite : connexion
        s.connect(('localhost', 65432))
        # lecture clavier d'une chaine

        ## On va rentrer notre adresse mail et on check que ça suit le format x@y.z.
        ## C'est la meme protocole à suivre que ça soit Email destinataire ou bien Emission.
        demander_et_envoyer("MAIL FROM : ", s)
        demander_et_envoyer("MAIL TO : ", s)

        while True:
            st = input("Tapez une chaine (. pour arreter): ")
            # condition d'arrêt, dans la consigne, c'est un .
            if st == ".":
                break
            # Etape 2 : émission de la chaine après encodage
            s.sendall(st.encode('utf-8'))
            
            # Etape 2 suite : réception de la chaine
            data = s.recv(1024)
            # décodage de la chaine
            st = data.decode('utf-8')
            # affichage de la chaine
            print('Received', st)