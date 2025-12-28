"""
Client SMTP interactif.
Permet d'envoyer des emails via un serveur SMTP.
"""

import sys
from archives.client_functions import ClientSMTP


def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 50)
    print("CLIENT SMTP - Menu Principal")
    print("=" * 50)
    print("1. Envoyer un email")
    print("2. Envoyer un email rapide (mode automatique)")
    print("3. Quitter")
    print("=" * 50)


def mode_interactif(client: ClientSMTP):
    """
    Mode interactif pour envoyer un email.
    
    :param client: Instance du client SMTP connecté
    """
    print("\n📧 Envoi d'un email")
    print("-" * 50)
    
    expediteur = input("Adresse de l'expéditeur : ").strip()
    destinataire = input("Adresse du destinataire : ").strip()
    
    print("\nContenu du message (tapez 'FIN' sur une ligne seule pour terminer) :")
    lignes_contenu = []
    while True:
        ligne = input()
        if ligne.strip().upper() == "FIN":
            break
        lignes_contenu.append(ligne)
    
    contenu = "\n".join(lignes_contenu)
    
    print("\n📤 Envoi en cours...")
    succes = client.envoyer_mail(expediteur, destinataire, contenu)
    
    if succes:
        print("✅ Email envoyé avec succès !")
    else:
        print("❌ Échec de l'envoi de l'email.")


def mode_automatique(client: ClientSMTP):
    """
    Mode automatique pour envoyer un email de test.
    
    :param client: Instance du client SMTP connecté
    """
    print("\n📧 Envoi d'un email de test")
    print("-" * 50)
    
    expediteur = "test@example.com"
    destinataire = "user@example.com"
    contenu = """Bonjour,

Ceci est un message de test envoyé depuis le client SMTP.

Cordialement,
Le client SMTP"""
    
    print(f"De: {expediteur}")
    print(f"À: {destinataire}")
    print(f"Contenu:\n{contenu}\n")
    
    print("📤 Envoi en cours...")
    succes = client.envoyer_mail(expediteur, destinataire, contenu)
    
    if succes:
        print("✅ Email de test envoyé avec succès !")
    else:
        print("❌ Échec de l'envoi de l'email de test.")


def main():
    """Fonction principale du client."""
    print("=" * 50)
    print("CLIENT SMTP")
    print("=" * 50)
    
    # Configuration de la connexion
    if len(sys.argv) == 3:
        host = sys.argv[1]
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("❌ Le port doit être un nombre entier.")
            sys.exit(1)
    else:
        host = input("Adresse du serveur SMTP (par défaut: localhost) : ").strip() or "localhost"
        port_str = input("Port du serveur (par défaut: 2525) : ").strip() or "2525"
        try:
            port = int(port_str)
        except ValueError:
            print("❌ Le port doit être un nombre entier.")
            sys.exit(1)
    
    # Créer et connecter le client
    client = ClientSMTP(host, port)
    print(f"\n🔌 Connexion à {host}:{port}...")
    
    if not client.connecter():
        print("❌ Impossible de se connecter au serveur.")
        sys.exit(1)
    
    print("✅ Connecté au serveur SMTP !")
    
    # Boucle principale
    try:
        while True:
            afficher_menu()
            choix = input("\nVotre choix : ").strip()
            
            if choix == "1":
                mode_interactif(client)
            elif choix == "2":
                mode_automatique(client)
            elif choix == "3":
                print("\n👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide. Veuillez réessayer.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur...")
    finally:
        client.deconnecter()


if __name__ == "__main__":
    main()
