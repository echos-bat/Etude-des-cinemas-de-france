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
    """
    Charge un ou plusieurs fichiers CSV en sélectionnant les colonnes et lignes souhaitées.

    Args:
        ligne_dep (int): Ligne de début (1-indexée).
        ligne_arr (int or None): Ligne de fin (incluse), None pour aller jusqu'à la fin.
        *colonne (str): Colonnes à conserver (facultatif).
        **fichier (dict): Dictionnaire de fichiers à charger avec des noms symboliques comme clés.

    Returns:
        list: Liste de listes contenant les données des fichiers importés.
    """
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
    """
    Affiche une description statistique complète pour les variables spécifiées dans un jeu de données.

    Args:
        data (list): Liste de dictionnaires représentant les données.
        *variables (str): Noms des variables à décrire.

    Returns:
        None
    """
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
    """
    Calcule et retourne un résumé statistique pour les variables numériques spécifiées.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        *variables (str): Variables numériques à analyser.

    Returns:
        dict: Résumé statistique pour chaque variable.
    """
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
        *variables (str): Noms des variables à analyser.

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
    Crée un tableau croisé dynamique avec la somme des colonnes numériques groupées par une variable.

    Args:
        data (list): Données sources sous forme de liste de dictionnaires.
        variable_groupement (str): Nom de la variable pour le groupement.
        *colonnes_numeriques (str): Colonnes numériques à agréger.

    Returns:
        list: Tableau croisé sous forme de liste de listes.
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
    """
    Transforme une liste de dictionnaires en une liste de listes pour affichage tabulaire.

    Args:
        data (list): Données sous forme de liste de dictionnaires.

    Returns:
        list: Liste contenant les données transformées en format tableau.
    """
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
    Affiche un nombre défini de lignes d'un tableau en format lisible.

    Args:
        nom (str): Nom du tableau à afficher.
        data (list): Données sous forme de liste de dictionnaires.

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
    Renomme les colonnes d'un jeu de données selon une variable spécifiée.

    Args:
        data (list): Liste de dictionnaires représentant les données.
        variable (dict): Dictionnaire de correspondance {ancien_nom: nouveau_nom}.

    Returns:
        None
    """
    for ligne in data:
        for old_name ,new_name in variable.items():
            ligne[new_name]=ligne[old_name]
            del ligne[old_name]           
def keep_var(data,colonnes):
    """
    Sélectionne certaines colonnes à conserver dans les données.

    Args:
        data (list): Données à filtrer.
        colonnes (tuple): Noms des colonnes à conserver.

    Returns:
        list: Données filtrées ne contenant que les colonnes sélectionnées.
    """
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
    """
    Supprime des colonnes spécifiées dans chaque ligne du jeu de données.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        *vars (str): Noms des colonnes à supprimer.

    Returns:
        None
    """
    for ligne in data:
        for var in vars:
            del ligne[var]

def filtrer_donnees(data,variable,**filtres):
    """
    Filtre les données selon des valeurs précises d'une variable.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        variable (str): Nom de la variable à filtrer.
        **filtres (dict): Valeurs à filtrer (clé/valeur).

    Returns:
        list: Données filtrées.
    """
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
    """
    Extrait et convertit les valeurs numériques valides pour une ou plusieurs variables.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        *variables (str): Noms des variables à extraire.

    Returns:
        list: Liste de valeurs numériques valides.
    """
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
        dictionnaire (dict): Le dictionnaire à analyser.
        cle (str): Nom de la clé à rechercher.

    Returns:
        int: Index de la clé, ou -1 si elle est absente.
    """
    try:
        return list(dictionnaire.keys()).index(cle)
    except ValueError as ve:
        print("Erreur dans la variable",ve)
        return -1


###### TRAITEMENT DES ANOMALIES

def nb_vide_manquante(data, *variables):
    """
    Compte le nombre de lignes avec des variables vides ou absentes.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        *variables (str): Variables à analyser.

    Returns:
        int: Nombre de valeurs manquantes.
    """
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
    """
    Compte les valeurs supérieures à une valeur seuil dans une variable.

    Args:
        data (list): Données sous forme de liste de dictionnaires.
        variable (str): Nom de la variable.
        valeur_aberante (float): Seuil de valeur considérée comme aberrante.

    Returns:
        int: Nombre de valeurs aberrantes.
    """
    compteur = 0
    for ligne in data:
        try:
            if float(ligne[variable]) > valeur_aberante:
                compteur += 1
        except Exception as e:
            print("Erreur lors du comptage des valeurs aberante :", e)
    return compteur

def corriger_valeurs_manquantes(data,*variables,valeur_remplacement):
    """
    Remplace les valeurs manquantes dans certaines variables par une valeur fournie.

    Args:
        data (list): Données à corriger.
        *variables (str): Variables à corriger.
        valeur_remplacement (any): Valeur de remplacement.

    Returns:
        list: Données corrigées.
    """
    for ligne in data:
        for cle in variables:
            if cle not in ligne or ligne[cle] in (None,""):
                ligne[cle] = valeur_remplacement
    return data

def ecarter_null(data,*variables):
    """
    Supprime les lignes contenant des valeurs nulles dans certaines variables.

    Args:
        data (list): Données à filtrer.
        *variables (str): Noms des variables à vérifier.

    Returns:
        list: Lignes sans valeurs nulles pour les variables spécifiées.
    """
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
    """
    Calcule la moyenne arithmétique d'une liste de valeurs numériques.

    Args:
        valeurs (list): Liste de nombres.

    Returns:
        float: Moyenne des valeurs.
    """
    try:
        return sum(valeurs) / len(valeurs)
    except ZeroDivisionError as zde:
        print(f"Division par zéro impossible {zde}")



def mediane(valeurs):
    """
    Calcule la médiane d'une liste de valeurs numériques.

    Args:
        valeurs (list): Liste de nombres.

    Returns:
        float: Médiane des valeurs.
    """
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
    """
    Calcule l'écart-type d'une liste de valeurs numériques.

    Args:
        valeurs (list): Liste de nombres.

    Returns:
        float: Écart-type des valeurs.
    """
    if not valeurs or len(valeurs) < 2:
        return 0
    
    moy = moyenne(valeurs)
    variance = sum((x - moy) ** 2 for x in valeurs) / (len(valeurs) - 1)
    return math.sqrt(variance)


def quartiles(valeurs):
    """
    Calcule le premier (Q1) et le troisième quartile (Q3) d'une liste de valeurs.

    Args:
        valeurs (list): Liste de nombres.

    Returns:
        tuple: (Q1, Q3)
    """
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
    """
    Exporte une liste de dictionnaires dans un fichier CSV.

    Args:
        file (str): Chemin du fichier à créer.
        data (list): Données à exporter.

    Returns:
        None
    """
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
    Exporte une liste de listes dans un fichier CSV.

    Args:
        file (str): Nom du fichier de sortie.
        dataliste (list): Liste de listes à écrire.

    Returns:
        None
    """
    try:
        with open(file, "w", newline='', encoding="utf-8") as fich:
            data=csv.writer(fich, delimiter = ";")
            data.writerows(dataliste)
            
        print("exportation terminer")
    except Exception as e:
        print("Erreur lors de l'exportation des données ",e)


