# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:46:17 2024

Ce script permet de découper une image en plusieurs morceaux correspondant à des feuilles A4,
afin de l'imprimer plus facilement. Il a été initialement conçu pour imprimer des personnes célèbres
en taille réelle, mais fonctionne pour tout type d'image nécessitant un agrandissement sur plusieurs pages.

@author: Jason Dellai
"""

from PIL import Image

############################################################################################################################
#Chemin de l'image à découper
myImage = Image.open("Input/Shrek.jpg");

#on indique la taille du bonhomme en pixel et en cm (ou de n'importe quel objet permettant de faire une conversion)
#utiliser paint pour compter les pixels
taille_bonhomme_cm = 200                
taille_bonhomme_pixel = 1930      

#Dimension papier imprimante
largeur = 21                        #21 pour du A4
longueur = 29.7                     #29.7 pour du A4
############################################################################################################################


#on récupère l'équivalence cm en pixel
scale = taille_bonhomme_pixel / taille_bonhomme_cm 

#on récupère le nombre de pixel qu'on va mettre sur chaque feuille
largeur_papier_pixel = round(largeur * scale)
longueur_papier_pixel = round(longueur * scale)

# Récupérer les dimensions de l'image
x_image_pixel, y_image_pixel = myImage.size

#Déterminer le nombre de feuilles nécessaire ainsi que la meilleur orientation du papier
nombre_de_feuilles_de_large_paysage = round((x_image_pixel / largeur_papier_pixel)+0.5)
nombre_de_feuilles_de_haut_paysage  = round((y_image_pixel / longueur_papier_pixel)+0.5)

nombre_de_feuilles_paysage = nombre_de_feuilles_de_large_paysage *nombre_de_feuilles_de_haut_paysage  

nombre_de_feuilles_de_large_portrait = round((x_image_pixel / longueur_papier_pixel)+0.5)
nombre_de_feuilles_de_haut_portrait = round((y_image_pixel / largeur_papier_pixel)+0.5)

nombre_de_feuilles_portrait = nombre_de_feuilles_de_large_portrait *nombre_de_feuilles_de_haut_portrait  

#s'il faut plus de feuille en paysage on se met en portrait et inversement
if nombre_de_feuilles_paysage>nombre_de_feuilles_portrait:
    x_feuille_pixel = longueur_papier_pixel
    y_feuille_pixel = largeur_papier_pixel    
    nb_feuilles_large = nombre_de_feuilles_de_large_portrait
    nb_feuilles_haut = nombre_de_feuilles_de_haut_portrait
else:
    x_feuille_pixel = largeur_papier_pixel
    y_feuille_pixel = longueur_papier_pixel
    nb_feuilles_large = nombre_de_feuilles_de_large_paysage
    nb_feuilles_haut = nombre_de_feuilles_de_haut_paysage
    
# on découpe et on sauvegarde dans le dossier output
morceau_numero = 0

for i in range(nb_feuilles_haut):
    for j in range(nb_feuilles_large):
        # Définir la boîte de découpe
        gauche = j * x_feuille_pixel
        haut = i * y_feuille_pixel
        droite = gauche + x_feuille_pixel
        bas = haut + y_feuille_pixel

        # Créer une image blanche de la taille de la feuille
        morceau = Image.new("RGB", (x_feuille_pixel, y_feuille_pixel), "white")

        # Définir la zone réelle à copier depuis l'image source
        box = (gauche, haut, min(droite, x_image_pixel), min(bas, y_image_pixel))
        morceau_crop = myImage.crop(box)

        # Coller la partie de l'image sur le fond blanc
        morceau.paste(morceau_crop, (0, 0))

        # Sauvegarder l'image découpée
        morceau.save(f'Output/morceaux_{morceau_numero}.jpg')
        morceau_numero += 1
