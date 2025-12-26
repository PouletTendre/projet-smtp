Projet Déploiement de Services et Interopérabilité : E-Mail 
__________________________________________________________________________________ 
M1 R&T / 2A STRI 
 
 
Introduction 
Le courrier électronique (e-mail) est un cas d’école de l’interopérabilité puisqu’il permet à des 
utilisateurs utilisant une grande variété de matériels de communiquer. 
Il est basé essentiellement sur 2 types de protocoles : 
-  Le  premier  permet  de  transférer  des  courriers  électroniques  d’une  machine  à  une  autre 
machine. Il s’agit du premier protocole utilisé pour le mail : SMTP (Simple Mail Transfer 
Protocol)  https://datatracker.ietf.org/doc/html/rfc5321 . 
-  Le second permet de consulter des courriers électroniques à distance. Il s’agit de POP3 
(Post Office Protocol)  https://datatracker.ietf.org/doc/html/rfc1081   et de IMAP (Internet 
Mail Access Protocol)  https://datatracker.ietf.org/doc/html/rfc3501 . 
 
Dans le cadre de ce projet on vous propose de créer un serveur capable de parler le protocole 
SMTP et le protocole POP ou IMAP. 
Côté client, on pourra utiliser un client générique comme telnet ou un client standard comme 
Thunderbird (à condition de gérer suffisamment de commandes du protocole considéré). 
 
Travail demandé 
1)  Version 1 : SMTP simple 
Dans cette première version, on ne vous demande que de gérer les commandes minimales de 
SMTP : MAIL, RCPT et DATA. Le courrier électronique envoyé par le client sera stocké dans 
un fichier (boîte mail) dont le nom correspondra au paramètre de la commande RCPT. 
 
2)  Version 2 : Gestion des commandes HELO et/ou EHLO  
Maintenant,  on  souhaite  pouvoir  gérer  la  procédure  permettant  d’identifier  la  version  du 
protocole parlée par le serveur : HELO pour la version basique du protocole ou EHLO pour la 
version étendue. Étant donné que la gestion complète du protocole est hors périmètre de ce 
projet,  il  conviendra  d’indiquer  une  réponse  502  Command  not  implemented  lors  de  la 
réception de EHLO et ensuite de répondre 250 Ok lors du HELO suivant. Une fois cette version 
terminée votre serveur devrait pouvoir communiquer avec des clients Mail standards comme 
Thunderbird. 
 
3)  Version 3 : ajout de POP3 
On veut désormais que le serveur permette la consultation à distance des courriers stockés dans 
les fichiers (boîtes mail) en suivant le protocole POP3 (ou optionnellement le protocole IMAP). 
Il ne s’agit pas ici d’implémenter la totalité du protocole mais de se concentrer sur la base. 
Pour POP3, notamment, il nous faudra gérer les commandes QUIT, STAT, LIST et RETR. 
 
4)  Version 4 : Options 
Dans cette version finale on pourra implémenter d’autres commandes de SMTP, POP3 ou 
IMAP. On pourra, par exemple, mettre en place une authentification. 
 
 
 
 
 
Organisation du projet et travail attendu 
 
Les groupes projets doivent être composés de trinômes alternants ou de trinômes non-alternants (pas de 
panachage).  
 
Ce projet est à rendre de manière incrémentale. Chaque livrable sera évalué et doit comporter deux 
parties : 
 
Partie I : Conception de l’application 
Concevez  et  rédigez  les  interfaces  de  l’application  permettant  de  répondre  aux  spécifications 
précédemment  énoncées.  Constituez  un  dossier  qui  comportera  les  diagrammes  UML  adéquats 
exprimant le résultat de l’analyse de cette application ainsi que des explications sur le fonctionnement 
de l’application (manuel d’utilisation). 
 
Partie II : Développement de l’application 
Le code commenté de l’application devra être rendu à chaque échéance. 
 
Évaluation 
A chaque échéance, chaque trinôme devra déposer sur stri.fr le rapport lié à la version livrée, le code et 
une courte vidéo montrant l’exécution de l’application (lien vers une vidéo YouTube par exemple). 
Votre projet sera évalué en fonction des choix techniques que vous effectuerez, de la qualité technique 
du code produit, de la qualité de la documentation, de son respect du sujet, du respect des échéances, 
de l’ergonomie de votre application et de son allure générale. 
Tout retard dans la fourniture des livrables sera sanctionné dans l’évaluation. 
Vos livrables pourront être soumis à évaluation d’outils détectant différentes formes de plagiat et de 
génération par Intelligence Artificielle. 
Rappel sur le plagiat : 
Il  existe  de  nombreuses  bibliothèques,  applications  et  outils  qui  réalisent  tout  ou  partie  du  travail 
demandé. Vous pouvez les regarder et vous en inspirer à la condition expresse de citer vos sources. 
Mais, pour la réalisation de ce projet, il vous est interdit : 
- de reprendre du code de ces bibliothèques ; 
- de s’inspirer, de plagier le code ou la conception réalisée par les autres étudiants ou par une IA. 
 
ÉCHEANCES pour les ALTERNANTS : 
- Date de remise de la version 1 : 12/12/2025 
- Date de remise de la version 2 : 9/01/2026 
- Date de remise de la version 3 : 23/01/2026 
 
ÉCHEANCES pour les NON ALTERNANTS : 
- Date de remise de la version 1 : 7/11/2025 
- Date de remise de la version 2 : 12/12/2025 
- Date de remise de la version 3 : 9/01/2026 
 
