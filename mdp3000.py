import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import random
import string

def mot_aleatoire(longueur):
    lettres = string.ascii_letters + string.punctuation + string.digits
    mot_genere = ""
    for carac in range(0, longueur):
        mot_genere = mot_genere + lettres[random.randint(0, len(lettres) - 1)]
    return mot_genere


def generer_cle():
    return Fernet.generate_key()

def chiffrer_mot_de_passe(cle, mot_de_passe):
    cipher_suite = Fernet(cle)
    mot_de_passe_chiffre = cipher_suite.encrypt(mot_de_passe)
    return mot_de_passe_chiffre

def dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre):
    cipher_suite = Fernet(cle)
    mot_de_passe = cipher_suite.decrypt(mot_de_passe_chiffre).decode()
    return mot_de_passe

def sauvegarder_mot_de_passe(cle, site, mot_de_passe_chiffre):
    with open('mots_de_passe_encrypted.txt', 'a') as fichier:
        ligne = f"{site}: {mot_de_passe_chiffre.decode()}\n"
        fichier.write(ligne)

def charger_cle():
    try:
        with open('cle.txt', 'rb') as fichier:
            cle = fichier.read()
        return cle
    except FileNotFoundError:
        return None

def sauvegarder_cle(cle):
    with open('cle.txt', 'wb') as fichier:
        fichier.write(cle)

def charger_sites():
    try:
        with open('mots_de_passe_encrypted.txt', 'r') as fichier:
            sites = [ligne.split(':')[0].strip() for ligne in fichier]
        return sites
    except FileNotFoundError:
        return []

def generer_mot_de_passe():
    cle = charger_cle()

    if not cle:
        cle = generer_cle()
        sauvegarder_cle(cle)

    longueur = int(entry_longueur.get())
    mot_de_passe = mot_aleatoire(longueur)
    site = entry_site.get()

    mot_de_passe_chiffre = chiffrer_mot_de_passe(cle, mot_de_passe.encode())
    sauvegarder_mot_de_passe(cle, site, mot_de_passe_chiffre)

    # Déchiffrer le mot de passe pour l'afficher
    mot_de_passe_dechiffre = dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre)
    label_mot_de_passe.config(text=f"Mot de passe généré et stocké en toute sécurité pour {site} : {mot_de_passe_dechiffre}")

    # met à jour la liste des sites pour les combobox
    sites_afficher = charger_sites()
    selected_site_afficher = tk.StringVar(value=sites_afficher[0] if sites_afficher else "")
    combo_site_afficher = ttk.Combobox(app, values=sites_afficher, textvariable=selected_site_afficher)
    combo_site_afficher.pack()

    sites_modifier = charger_sites()
    selected_site_modifier = tk.StringVar(value=sites_modifier[0] if sites_modifier else "")
    combo_site_modifier = ttk.Combobox(app, values=sites_modifier, textvariable=selected_site_modifier)
    combo_site_modifier.pack()

def afficher_mot_de_passe():
    cle = charger_cle()
    site_a_afficher = selected_site_afficher.get()

    if not cle:
        label_mot_de_passe_afficher.config(text="Erreur: La clé de chiffrement est manquante.")
        return

    with open('mots_de_passe_encrypted.txt', 'r') as fichier:
        for ligne in fichier:
            if site_a_afficher in ligne:
                mot_de_passe_chiffre = ligne.split(': ')[1].strip()
                mot_de_passe_dechiffre = dechiffrer_mot_de_passe(cle, mot_de_passe_chiffre.encode())
                label_mot_de_passe_afficher.config(text=f"Mot de passe pour {site_a_afficher} : {mot_de_passe_dechiffre}")
                return

    label_mot_de_passe_afficher.config(text=f"Site {site_a_afficher} non trouvé.")

def modifier_mot_de_passe():
    cle = charger_cle()
    site_a_modifier = selected_site_modifier.get()

    if not cle:
        label_mot_de_passe_modifier.config(text="Erreur: La clé de chiffrement est manquante.")
        return

    with open('mots_de_passe_encrypted.txt', 'r') as fichier:
        lignes = fichier.readlines()

    with open('mots_de_passe_encrypted.txt', 'w') as fichier:
        for ligne in lignes:
            if site_a_modifier in ligne:
                longueur = int(entry_longueur_modifier.get())
                nouveau_mot_de_passe = mot_aleatoire(longueur)
                nouveau_mot_de_passe_chiffre = chiffrer_mot_de_passe(cle, nouveau_mot_de_passe.encode())
                ligne_modifiee = f"{site_a_modifier}: {nouveau_mot_de_passe_chiffre.decode()}\n"
                fichier.write(ligne_modifiee)
                label_mot_de_passe_modifier.config(text=f"Mot de passe pour {site_a_modifier} modifié avec succès.")
            else:
                fichier.write(ligne)

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

# Nouveau champ pour afficher le mot de passe avec un tableau déroulant
label_site_afficher = tk.Label(app, text="Nom du site à afficher :")
label_site_afficher.pack()

sites_afficher = charger_sites()
selected_site_afficher = tk.StringVar(value=sites_afficher[0] if sites_afficher else "")
combo_site_afficher = ttk.Combobox(app, values=sites_afficher, textvariable=selected_site_afficher)
combo_site_afficher.pack()

button_afficher = tk.Button(app, text="Afficher Mot de Passe", command=afficher_mot_de_passe)
button_afficher.pack()

label_mot_de_passe_afficher = tk.Label(app, text="")
label_mot_de_passe_afficher.pack()

# Nouveau champ pour modifier le mot de passe avec un tableau déroulant
label_site_modifier = tk.Label(app, text="Nom du site à modifier :")
label_site_modifier.pack()

sites_modifier = charger_sites()
selected_site_modifier = tk.StringVar(value=sites_modifier[0] if sites_modifier else "")
combo_site_modifier = ttk.Combobox(app, values=sites_modifier, textvariable=selected_site_modifier)
combo_site_modifier.pack()

label_longueur_modifier = tk.Label(app, text="Nouvelle longueur du mot de passe :")
label_longueur_modifier.pack()

entry_longueur_modifier = tk.Entry(app)
entry_longueur_modifier.pack()

button_modifier = tk.Button(app, text="Modifier Mot de Passe", command=modifier_mot_de_passe)
button_modifier.pack()

label_mot_de_passe_modifier = tk.Label(app, text="")
label_mot_de_passe_modifier.pack()

app.mainloop()
