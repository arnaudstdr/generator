import random
import string
import tkinter as tk
from cryptography.fernet import Fernet

site = "" #Définissons la variable 'site au niveau globla

def mot_aleatoire(longueur):
    lettres = string.ascii_letters + string.digits + string.punctuation
    mot_genere = ''.join(random.choice(lettres) for _ in range(longueur))
    return mot_genere

def generer_mot_de_passe():
    longueur = int(entry_longueur.get())
    mot_de_passe = mot_aleatoire(longueur)
    label_mot_de_passe.config(text=f"Mot de passe généré : {mot_de_passe}")


#cryptography
def generer_cle():
    return Fernet.generate_key()

def chiffrer_mot_de_pass(cle, mot_de_passe):
    cipher_suite = Fernet(cle)
    mot_de_passe_chiffre = cipher_suite.encrypt(mot_de_passe)
    return mot_de_passe_chiffre

def dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre):
    cipher_suite = Fernet(cle)
    mot_de_passe = cipher_suite.decrypt(mot_de_passe_chiffre).decode()
    return mot_de_passe

def sauvegarde_mot_de_passe(cle, mot_de_passe_chiffre):
    with open('mot_de_passe_encrypted.txt', 'a') as fichier:
        ligne = f"{site}: {mot_de_passe_chiffre.decode()}\n"
        fichier.write(ligne)

def charger_cle():
    try :
        with open('cle.txt', 'rb') as fichier:
            cle = fichier.read()
        return cle
    except FileNotFoundError:
        return None

def sauvegarder_cle(cle):
    with open('cle.txt', 'wb') as fichier:
        fichier.write(cle)

def generer_mot_de_passe():
    global site
    cle = charger_cle()

    if not cle:
        cle = generer_cle()
        sauvegarder_cle()

    longueur = int(entry_longueur.get())
    mot_de_passe = mot_aleatoire(longueur)

    site = entry_site.get()  # entrée pour le nom du site

    mot_de_passe_chiffre = chiffrer_mot_de_pass(cle, mot_de_passe.encode())
    sauvegarde_mot_de_passe(cle, mot_de_passe_chiffre)

    # Déchiffrer le mot de passe pour l'afficher
    mot_de_passe_dechiffre = dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre)
    label_mot_de_passe.config(text=f"Mot de passe généré et stocké en toute sécurité pour {site} : {mot_de_passe_dechiffre}")

def afficher_mot_de_passe():
    cle = charger_cle()
    site_a_afficher = entry_site_afficher.get()

    if not cle :
        label_mot_de_passe_afficher.config(text="Erreur : La clé de chiffrement est manquante.")
        return

    with open ('mot_de_passe_encrypted.txt', 'r') as fichier:
        for ligne in fichier:
            if site_a_afficher in ligne:
                mot_de_passe_chiffre = ligne.split(': ')[1].strip()
                mot_de_passe_dechiffre = dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre.encode())
                label_mot_de_passe_afficher.config(text=f"Mot de passe pour {site_a_afficher} : {mot_de_passe_dechiffre}")
                return

    label_mot_de_passe_afficher.config(text=f"Site {site_a_afficher} non trouvé.")


# Interface graphique avec Tkinter
app = tk.Tk()
app.title("Générateur et Stockage Sécurisé de Mot de Passe")

label_longueur = tk.Label(app, text="Longueur du mot de passe :")
label_longueur.pack()

entry_longueur = tk.Entry(app)
entry_longueur.pack()

label_site = tk.Label(app, text="Nom du site :")
label_site.pack()

entry_site = tk.Entry(app)
entry_site.pack()

button_generer = tk.Button(app, text="Générer et Stocker Mot de Passe", command=generer_mot_de_passe)
button_generer.pack()

label_mot_de_passe = tk.Label(app, text="")
label_mot_de_passe.pack()

label_site_afficher = tk.Label(app, text="Nom du site :")
label_site_afficher.pack()

entry_site_afficher = tk.Entry(app)
entry_site_afficher.pack()

button_afficher = tk.Button(app, text="Afficher Mot de Passe", command=afficher_mot_de_passe)
button_afficher.pack()

label_mot_de_passe_afficher = tk.Label(app, text="")
label_mot_de_passe_afficher.pack()

app.mainloop()
