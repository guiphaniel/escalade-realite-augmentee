# Escalade en réalité augmentée

## Crédits

* MAADOUR Dalil
* RICHAUD Guilhem
* STUBLJAR Baptiste

## Contexte

Dans le cadre de notre projet tuteuré réalisé au cours de notre deuxième année d’études à l’IUT
Lyon 1 (site de Bourg-en-Bresse), nous avons dû réaliser un logiciel permettant de pratiquer de
l’escalade en réalité augmentée. L’objectif était ainsi de proposer une expérience étendue de ce sport,
au travers de jeux vidéo grandeur nature.
Le jeux disponibles sont :
* Le Pong (2 joueurs)
* Les Cibles
* Le Parcours (gestion de parcours, de joueurs, et de scores pour les compétitions)

Ce projet nécessite : une caméra, un ordinateur, un vidéoprojecteur

## Guide d'installation

(python3 est requis pour ce projet : `apt install python3`)

1. Télécharger le projet (branche main) sur votre machine
2. A la racine du projet, créer un environnement virtuel Python : `python3 -m venv venv`
3. Activer l'environnement virtuel : 
* Linux : `source venv/bin/activate`
* Windows : `.\venv\Scripts\activate`
4. S'assurer que la variable `venv/pyvenv.cfg:home` soit correcte (doit correspondre à l'emplacement de python3 votre la machine. (Tip : `which python3`))
5. Installer les packages nécessaires 
* automatiquement : 
    * `pip3 install -r requirements.txt`
* manuellement :
    * Mediapipe : `pip install mediapipe`
    * Pygame : `pip install pygame`

6. Lancer le projet : `python3 __main__.py`