# But:
Convertir un site Wordpress en un site HTML statique afin qu'il puisse être copié sur une clef USB déconnectée d'Internet !


# Directives:
1) Je veux que tu écrives un script qui aspire tout le site Wordpress:

https://www.melaniezufferey.ch/

dans le dossier 'www'

Afin d'économiser de la bande passante et du temps, vérifie avant de descendre un élément que cet élement n'est pas déjà descendu dans le dossier www ?

2) Après je veux que tu écrives un script bash pour installer le service Apache sur le port 5173 et le démarrer afin de pouvoir servir le site web html statique qui se trouve dans le dossier 'www' avec une adresse ipv4.

3) Après je veux que tu comprares VISUELLEMENT (copies d'écran) avec un script python et avec l'aide du browser local headless chromium, chaque page du site web statique (localhost:5173) avec le site Wordpress original https://www.melaniezufferey.ch/ afin qu'il corresponde TOTALEMENT ?

4) Ecrit le manuel d'utilisation du processus de conversion dnas le fichier manuel.md


# Impératifs:
1) C'est un site Wordpress donc avec PHP, il ne suffit pas simplement de changer les urls www.melaniezufferey.ch ils faut aussi modifier, donc convertir la fonction PHP, toutes les url, à l'intérieur de pages HTML, qui font références à des fonctions PHP ou autres !
Toutes références .php qui pointent sur Wordpress, comme les wp-admin, doivent être supprimées des pages HTML statiques, vu qu'elles ne servent plus à rien. On ne doit plus retrouver de strings '.php' dans les pages HTML !

2) Les scripts javascript, ainsi que les objets https://fonts.googleapis.com ou autres doivent être aussi copiés en local afin de pouvoir utiliser le site web statique VRAIMENT sans connexion à Internet.
Donc il faut BIEN VERIFIER, après coup, que plus rien ne dois faire référence à l'extérieur du site statique !

3) Quand tu trouves des url avec des lettres accentuées, afin d'éliminer les problèmes d'interprétation des différents browsers, il faut enlever les accents et ne travailler qu'avec des minuscules non accentuées

4) Tout doit se trouver dans des scripts bash ou python afin de pouvoir rejouer totalement le processus après coup !

5) LE POINT LE PLUS IMPORTANT!
Ne sois pas trop optimiste, vérifie bien VISUELLEMENT que toutes les images du site web se trouvent bien au bon endroit sur TOUTES les pages du site WEB avec des comparaison de copies d'écran avec le browser headless chromium. 
Tu dois réelement vérifier visuellement entre les deux sites ce qui se passe quand on clique sur chaque images !
Cela ne sert à rien de me dire que tout fonctionne parfaitement et que ce n'est pas le cas au niveau visuel.
Je déteste d'être décu de voir que cela ne fonctionne pas et de te demander de corriger ton travail !
Fais-moi plaisirs en faisant du goog job ;-)


