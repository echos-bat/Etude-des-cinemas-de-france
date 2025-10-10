# -*- coding: utf-8 -*-
import csv 
import pandas as pd
import statistics
import math
"""
=============================================
FONCTION 
=============================================
"""

## ===============================
## CHARGEMENT
## ===============================

def charger_fichier_csv(ligne_dep=1,ligne_arr=None,*colonne,**fichier):
    """Charge un fichier CSV avec sélection des colonnes et lignes."""
    tout_data=[]
    for i in fichier.values():
        try:
            with open (i,"r",encoding="utf-8") as fich:
                data=list(csv.DictReader(fich,delimiter=";"))
                data = data[ligne_dep-1:ligne_arr]
                if colonne == ():
                    tout_data.append(data)
                else:
                    data=keep_var(data,colonne)
                    tout_data.append(data)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            tout_data.append(None)

    return tout_data

## ===============================
## Visualisation
## ===============================

def describe_stat(data, *variables):
    """Fournit une description statistique des données."""
    resume = {}
    for variable in variables:
        try:
            valeurs = obtenir_valeur_modalite(data, variable)
            quartiles = statistics.quantiles(valeurs,n=4)
            resume[variable] = {
                "Nombre de valeurs": len(valeurs),
                "Minimum": min(valeurs) if valeurs else None,
                "Maximum": max(valeurs) if valeurs else None,
                "Moyenne": statistics.mean(valeurs),
                "Mediane": statistics.median(valeurs),
                "Variance":statistics.variance(valeurs),
                "Ecart-type": statistics.stdev(valeurs),
                "q1": quartiles[0],
                "q3": quartiles[2],
                "Mode": statistics.mode(valeurs),
                "Nombre de valeurs nulles ou manquantes": nb_vide_manquante(data,variable)
            }
            print(f"Description de la variable {variable}:")
            for key, value in resume[variable].items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Erreur sur la variable {variable}: {e}")

def describe_math(data, *variables):
    """Fournit une description statistique des données."""
    resume = {}
    for variable in variables:
        try:
            valeurs = obtenir_valeur_modalite(data, variable)
            q1, q3 = quartiles(valeurs)
            resume[variable] = {
                "Nombre de valeurs": len(valeurs),
                "Minimum": min(valeurs) if valeurs else None,
                "Maximum": max(valeurs) if valeurs else None,
                "Moyenne": moyenne(valeurs),
                "Mediane": mediane(valeurs),
                "Ecart-type": ecart_type(valeurs),
                "q1": q1,
                "q3": q3,
                "Nombre de valeurs nulles": nb_vide_manquante(data,variable)
            }
        except Exception as e:
            print(f"Erreur sur la variable {variable}: {e}")

    return resume  

def statistique(data, *variables):
    """
    Calcule des statistiques descriptives pour les variables spécifiées.

    Args:
        data (list): Liste de dictionnaires contenant les données.
        variables (str): Noms des variables à analyser.

    Returns:
        dict: Dictionnaire contenant les statistiques pour chaque variable.
    """
    try:
        resume = {}
        for variable in variables:
            valeurs = obtenir_valeur_modalite(data, variable)
            if valeurs:
                resume[variable] = {
                    "Somme": sum(valeurs),
                    "Nombre de valeurs": len(valeurs),
                    "Minimum": min(valeurs),
                    "Maximum": max(valeurs),
                    "Moyenne": statistics.mean(valeurs),
                    "Mediane": statistics.median(valeurs),
                    "Variance": statistics.variance(valeurs),
                    "Ecart-type": statistics.stdev(valeurs)
                } 
            else:
                resume[variable] = {"Nombre de valeurs": 0}
        return resume
    except Exception as e:
        print("Erreur dans le calcul des statistiques :", e)
        return {}

def tableau_stat(data, variable_groupement, *colonnes_numeriques):
    """
    Crée un tableau croisé avec sommes des colonnes numériques par index.

    Paramètres :
    - data : list[dict] — données sources.
    - index : str — champ pour les lignes.
    - colonnes_numeriques : str — champs pour les colonnes à totaliser.

    Retour :
    - list[list] 
    """

    valeurs_index = sorted(set(ligne[variable_groupement] for ligne in data if variable_groupement in ligne and ligne[variable_groupement] != ""))

    comptage = {}
    for val_index in valeurs_index:
        comptage[val_index] = {col: 0 for col in colonnes_numeriques}
    

    for ligne in data:
        val_index = ligne.get(variable_groupement)
        if val_index :
            for col in colonnes_numeriques:
                try:
                    valeur = float(str(ligne.get(col, "0")).replace(",", ".").replace(" ", ""))
                    comptage[val_index][col] += valeur
                except ValueError:
                    pass  

    tcd_liste = []
    entete = [variable_groupement] + list(colonnes_numeriques)
    tcd_liste.append(entete)

    for val_index in valeurs_index:
        ligne = [val_index]
        for col in colonnes_numeriques:
            ligne.append(comptage[val_index][col])
        tcd_liste.append(ligne)

    return tcd_liste

def afficher_dic(data):
    
    entete=[var for var in data[0].keys()]
    data_dic=[entete]
    
    for ligne in data:
        ligne_dict=[]
        for col in ligne.values():
            ligne_dict.append(col)
        data_dic.append(ligne_dict)
    return data_dic


    
def afficher_liste(nom,data):
    
    """
    Affiche un nombre spécifié de lignes d'un tableau sous forme tabulaire.

    Args:
        nom (str): Nom du tableau.
        data (list): Liste contenant les données du tableau.

    Returns:
        None
    """
    try:
        limit=int(input(f"Combien de ligne voulez-vous afficher dans le fichier {nom} ? : "))+1
        print("-"*50)
        print(f"{nom:^25}")
        print("-"*50)
        cpt=0
        data_list=afficher_dic(data)
        for ligne in data_list :
            if cpt==limit:
                break
            else:
                print(" | ".join(str(elem) for elem in ligne))
                print("_"*121)
                cpt += 1
                
    except Exception as e :
        print("Probleme dans l'affichage",e) 

## ===============================
## PREPARATION DES DONNEES & TRAITEMENT DES ANOMALIES
## ===============================

###### PREPARATION
def renommer_variables(data,variable):
    """
    Permet de renommer les colonnes d'un tableau.

    Args:
        liste_data (list): Liste contenant les colonnes du tableau.

    Returns:
        None
    """
    for ligne in data:
        for old_name ,new_name in variable.items():
            ligne[new_name]=ligne[old_name]
            del ligne[old_name]           
def keep_var(data,colonnes):
    """Permet à l'utilisateur de choisir les colonnes à importer."""
    try:
        data = [{col.strip(): ligne[col.strip()] for col in colonnes if col.strip() in ligne} for ligne in data]
        return data
    except KeyError as ke:
        print("Erreur colonnes introuvables :", ke)
        return data  
    except ValueError as ve:
        print("Erreur dans la sélection des lignes.", ve)
        return data
    
def drop_var(data,*vars):
    for ligne in data:
        for var in vars:
            del ligne[var]

def filtrer_donnees(data,variable,**filtres):
    """Permet à l'utilisateur d'appliquer un filtre sur une colonne."""
    try:
        data_filtre = []
        for ligne in data:
            for val in filtres.values():
                if ligne[variable] == val:
                    data_filtre.append(ligne)
        return data_filtre
    except AttributeError as ae:
        print("erreur dans l'attribut",ae)
        return data
    except KeyError as ke:
        print("La colonne n'existe pas.",ke)
        return data    

def obtenir_valeur_modalite(data, *variables):
    """Extrait les valeurs numériques valides d’une ou plusieurs variables (tuple)."""
    # Déclaration des constantes
    valeurs = []
    try:
        # Parcours de chaque ligne du jeu de données
        for ligne in data:
            ligne_valeurs = []
            valide = True
            # Pour chaque variable, on vérifie et convertit la valeur
            for var in variables:
                if var in ligne and ligne[var] not in (None, ""):
                    try:
                        # Conversion en float après nettoyage (remplacement des espaces et virgules)
                        val = float(str(ligne[var]).replace(" ", "").replace(",", "."))
                        ligne_valeurs.append(val)
                    except Exception as e:
                        valide = False
                        print("les valeurs ne sont pas valide.",e)
                        break
                else:
                    valide = False
                    break
            if valide:
                valeurs.extend(ligne_valeurs)  

        
        return valeurs
    except Exception as e:
        # Afficher une fois l'erreur par variable pour éviter le spam
        print(f"Valeur invalide pour la variable {var} : {ligne[var]}")


def fusionner_donnee(**donnees_par_annee):
    """
    Fusionne des données sous forme de dictionnaires avec une clé d'identification commune.
    Ajoute une colonne 'annee' pour garder la trace de l'origine de chaque ligne.

    Paramètre:
    - donnees_par_annee : dictionnaires nommés (ex : data2019=..., data2020=...)

    Retour:
    - Liste fusionnée des lignes avec origine précisée.
    """
    try:
        data_fus = []
        for annee, donnees in donnees_par_annee.items():
            for ligne in donnees:
                ligne_avec_annee = ligne.copy()
                ligne_avec_annee['annee'] = annee
                data_fus.append(ligne_avec_annee)
        return data_fus
    except Exception as e:
        print("Erreur pour le fusionnement de donnée :", e)
        return []


def Index_variable(dictionnaire, cle):
    """
    Retourne l'index d'une clé dans un dictionnaire.

    Args:
        dictionnaire (dict): Le dictionnaire à parcourir.
        cle (str): La clé dont on veut connaître l'index.

    Returns:
        int: L'index de la clé si elle existe, sinon -1.
    """
    try:
        return list(dictionnaire.keys()).index(cle)
    except ValueError as ve:
        print("Erreur dans la variable",ve)
        return -1


###### TRAITEMENT DES ANOMALIES

def nb_vide_manquante(data, *variables):
    """Compte le nombre de lignes où chaque variable est vide ou absente (variables en tuple)."""
    try:
        compteur = 0
        for variable in variables:
            for ligne in data:
                if variable not in ligne or ligne[variable] in (None, ""):
                    compteur += 1
        return compteur
    except Exception as e:
        print("Erreur lors du comptage des valeurs nulles :", e)
        return None
    
def nb_valeur_aberante(data, variable,valeur_aberante=1000000):
    """Compte le nombre de valeurs aberrantes supérieures à 1 000 000 dans une liste de dictionnaires."""
    compteur = 0
    for ligne in data:
        try:
            if float(ligne[variable]) > valeur_aberante:
                compteur += 1
        except Exception as e:
            print("Erreur lors du comptage des valeurs aberante :", e)
    return compteur

def corriger_valeurs_manquantes(data,*variables,valeur_remplacement):
    """Corrige les anomalies en remplaçant les erreurs par une valeur de remplacement."""
    for ligne in data:
        for cle in variables:
            if cle not in ligne or ligne[cle] in (None,""):
                ligne[cle] = valeur_remplacement
    return data

def ecarter_null(data,*variables):
    lignes = []
    for ligne in data:
        ligne_valide = True
        for cle in variables:
            if cle not in ligne or ligne[cle] in (None, ""):
                ligne_valide = False
                break
        if ligne_valide:
            lignes.append(ligne)
    return lignes

###### INDICATEURS STATISTIQUES
def moyenne(valeurs):
    """Calcule la moyenne d'une liste de valeurs."""
    try:
        return sum(valeurs) / len(valeurs)
    except ZeroDivisionError as zde:
        print(f"Division par zéro impossible {zde}")



def mediane(valeurs):
    try:
        val_triee = sorted(valeurs)
        nb = len(val_triee)
        milieu = nb // 2
        if nb % 2 == 0:
            return (val_triee[milieu - 1] + val_triee[milieu]) / 2
        else:
            return val_triee[milieu]
    except Exception as e:
        print(f"Erreur dans les valeurs : {e}")
        return None

def ecart_type(valeurs):
    if not valeurs or len(valeurs) < 2:
        return 0
    
    moy = moyenne(valeurs)
    variance = sum((x - moy) ** 2 for x in valeurs) / (len(valeurs) - 1)
    return math.sqrt(variance)


def quartiles(valeurs):
    try:
        val_triee = sorted(valeurs)
        n = len(val_triee)
        q1_index = n // 4
        q3_index = 3 * n // 4
        q1 = val_triee[q1_index]
        q3 = val_triee[q3_index]

        return q1, q3 
    
    except Exception as e:
        print(f"Erreur dans les valeurs : {e}")
        return None,None

###### EXPORTATION
def exportation_fich_dictionnaire(file,data):
    try :
        with open(file, "w", newline ="",encoding="utf-8") as fich : 
            fields= [var for var in data[0].keys()] 
            writer = csv.DictWriter(fich, fieldnames = fields, delimiter = ";")
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print("un probleme dans l'exportation des données",e)
        
        
def exporter_liste(file,dataliste):
    """
    La fonction exporte une liste dans un fichier csv
    Paramètres :
    liste : list
    nom_fichier : 
    """
    try:
        with open(file, "w", newline='', encoding="utf-8") as fich:
            data=csv.writer(fich, delimiter = ";")
            data.writerows(dataliste)
            
        print("exportation terminer")
    except Exception as e:
        print("Erreur lors de l'exportation des données ",e)



    
    







# Description des données

"""
===================================================================
PROGRAMME PRINCIPALE
===================================================================
"""
#importation des données
data=charger_fichier_csv(1,5,fichier1="../data/etablissements-cinematographiques.csv",fichier2="../data/Données cartographie 2021.csv",fichier3="../data/Données cartographie 2020.csv")
#affichage des données
data_etablissement_cin=data[0]
data_carto2021=data[1]
data_carto2020=data[2]
for ligne in data_carto2020:
    ligne['annee'] = 2020

for ligne in data_carto2021:
    ligne['annee'] = 2021

# On fusionne les deux listes
data_fusion_20_21 = data_carto2020 + data_carto2021
exportation_fich_dictionnaire("donnee_fusionner.csv",data_fusion_20_21)
data_tout=fusionner_donnee(d2020=data_carto2020,d2021=data_carto2021)
