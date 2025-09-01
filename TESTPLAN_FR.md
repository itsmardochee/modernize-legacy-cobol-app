# Plan de Test - Système de Gestion de Comptes COBOL

## Vue d'ensemble
Ce plan de test couvre toute la logique métier de l'application COBOL composée de trois modules principaux : [`MainProgram`](main.cob), [`Operations`](operations.cob), et [`DataProgram`](data.cob).

## Tests Fonctionnels

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_MAIN_001** | **Interface utilisateur - Affichage du menu principal** | L'application est démarrée | 1. Lancer l'application<br/>2. Observer l'affichage initial | Le menu s'affiche avec :<br/>- "Account Management System"<br/>- Options 1-4 (View Balance, Credit, Debit, Exit)<br/>- Prompt "Enter your choice (1-4):" | | | |
| **TC_MAIN_002** | **Navigation - Sélection option valide (1)** | Menu principal affiché | 1. Saisir "1"<br/>2. Observer le comportement | L'option "View Balance" est sélectionnée et [`Operations`](operations.cob) est appelé avec 'TOTAL ' | | | |
| **TC_MAIN_003** | **Navigation - Sélection option valide (2)** | Menu principal affiché | 1. Saisir "2"<br/>2. Observer le comportement | L'option "Credit Account" est sélectionnée et [`Operations`](operations.cob) est appelé avec 'CREDIT' | | | |
| **TC_MAIN_004** | **Navigation - Sélection option valide (3)** | Menu principal affiché | 1. Saisir "3"<br/>2. Observer le comportement | L'option "Debit Account" est sélectionnée et [`Operations`](operations.cob) est appelé avec 'DEBIT ' | | | |
| **TC_MAIN_005** | **Navigation - Sélection option sortie (4)** | Menu principal affiché | 1. Saisir "4"<br/>2. Observer le comportement | - Message "Exiting the program. Goodbye!" affiché<br/>- Application se termine | | | |
| **TC_MAIN_006** | **Validation - Option invalide** | Menu principal affiché | 1. Saisir une valeur non valide (0, 5, lettre)<br/>2. Observer le comportement | - Message "Invalid choice, please select 1-4." affiché<br/>- Menu s'affiche à nouveau | | | |
| **TC_MAIN_007** | **Boucle - Retour au menu après opération** | Opération terminée (sauf exit) | 1. Effectuer une opération (1, 2, ou 3)<br/>2. Observer après completion | Le menu principal s'affiche à nouveau | | | |

## Tests de Consultation de Solde

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_BAL_001** | **Consultation - Solde initial** | - Application démarrée<br/>- Aucune transaction effectuée | 1. Sélectionner option "1"<br/>2. Observer l'affichage | Message "Current balance: 1000.00" affiché | | | Solde initial par défaut |
| **TC_BAL_002** | **Consultation - Solde après crédit** | Crédit de 200.00 effectué | 1. Sélectionner option "1"<br/>2. Observer l'affichage | Message "Current balance: 1200.00" affiché | | | |
| **TC_BAL_003** | **Consultation - Solde après débit** | Débit de 150.00 effectué | 1. Sélectionner option "1"<br/>2. Observer l'affichage | Solde actuel moins 150.00 affiché | | | |

## Tests de Crédit

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_CRE_001** | **Crédit - Montant valide** | Solde initial : 1000.00 | 1. Sélectionner option "2"<br/>2. Saisir "250.50" quand demandé<br/>3. Observer les messages | - "Enter credit amount:" affiché<br/>- "Amount credited. New balance: 1250.50" affiché<br/>- Solde mis à jour dans [`DataProgram`](data.cob) | | | |
| **TC_CRE_002** | **Crédit - Montant zéro** | Solde initial : 1000.00 | 1. Sélectionner option "2"<br/>2. Saisir "0" quand demandé<br/>3. Observer les messages | - Crédit accepté<br/>- Solde reste 1000.00<br/>- Message de confirmation affiché | | | Test de cas limite |
| **TC_CRE_003** | **Crédit - Montant décimal** | Solde initial : 1000.00 | 1. Sélectionner option "2"<br/>2. Saisir "99.99" quand demandé<br/>3. Observer les messages | - Crédit accepté<br/>- Nouveau solde : 1099.99<br/>- Message de confirmation affiché | | | |
| **TC_CRE_004** | **Crédit - Montant maximum** | Solde initial : 1000.00 | 1. Sélectionner option "2"<br/>2. Saisir "999999.99" quand demandé<br/>3. Observer les messages | Comportement selon limites PIC 9(6)V99 | | | Test de limite supérieure |

## Tests de Débit

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_DEB_001** | **Débit - Montant valide avec fonds suffisants** | Solde initial : 1000.00 | 1. Sélectionner option "3"<br/>2. Saisir "200.00" quand demandé<br/>3. Observer les messages | - "Enter debit amount:" affiché<br/>- "Amount debited. New balance: 800.00" affiché<br/>- Solde mis à jour dans [`DataProgram`](data.cob) | | | |
| **TC_DEB_002** | **Débit - Montant égal au solde** | Solde initial : 1000.00 | 1. Sélectionner option "3"<br/>2. Saisir "1000.00" quand demandé<br/>3. Observer les messages | - Débit accepté<br/>- Nouveau solde : 0.00<br/>- Message de confirmation affiché | | | Test de cas limite |
| **TC_DEB_003** | **Débit - Fonds insuffisants** | Solde initial : 1000.00 | 1. Sélectionner option "3"<br/>2. Saisir "1500.00" quand demandé<br/>3. Observer les messages | - "Insufficient funds for this debit." affiché<br/>- Solde reste 1000.00 (inchangé) | | | Règle métier critique |
| **TC_DEB_004** | **Débit - Montant zéro** | Solde initial : 1000.00 | 1. Sélectionner option "3"<br/>2. Saisir "0" quand demandé<br/>3. Observer les messages | - Débit accepté<br/>- Solde reste 1000.00<br/>- Message de confirmation affiché | | | Test de cas limite |
| **TC_DEB_005** | **Débit - Fonds insuffisants (1 centime)** | Solde initial : 100.00 | 1. Sélectionner option "3"<br/>2. Saisir "100.01" quand demandé<br/>3. Observer les messages | - "Insufficient funds for this debit." affiché<br/>- Solde reste 100.00 (inchangé) | | | Test précision décimale |

## Tests de Persistance des Données

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_DATA_001** | **Lecture - Opération READ** | [`DataProgram`](data.cob) initialisé | 1. Appeler DataProgram avec 'READ'<br/>2. Vérifier la valeur retournée | STORAGE-BALANCE est copié vers BALANCE | | | Test unitaire |
| **TC_DATA_002** | **Écriture - Opération WRITE** | [`DataProgram`](data.cob) initialisé | 1. Appeler DataProgram avec 'WRITE' et nouvelle valeur<br/>2. Vérifier STORAGE-BALANCE | STORAGE-BALANCE est mis à jour avec la nouvelle valeur | | | Test unitaire |
| **TC_DATA_003** | **Persistance - Données entre opérations** | Plusieurs transactions effectuées | 1. Effectuer crédit 200.00<br/>2. Consulter solde<br/>3. Effectuer débit 50.00<br/>4. Consulter solde final | - Après crédit : 1200.00<br/>- Après débit : 1150.00<br/>- Données persistent entre appels | | | Test d'intégration |

## Tests d'Intégration

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_INT_001** | **Flux complet - Consultation** | Application démarrée | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 1 → [`Operations`](operations.cob) 'TOTAL '<br/>3. [`Operations`](operations.cob) → [`DataProgram`](data.cob) 'READ'<br/>4. Retour vers utilisateur | Communication entre tous les modules réussie | | | Test de bout en bout |
| **TC_INT_002** | **Flux complet - Crédit** | Application démarrée | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 2 → [`Operations`](operations.cob) 'CREDIT'<br/>3. Saisie montant → calcul → [`DataProgram`](data.cob) 'WRITE'<br/>4. Confirmation utilisateur | Transaction de crédit complète réussie | | | Test de bout en bout |
| **TC_INT_003** | **Flux complet - Débit réussi** | Solde suffisant | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 3 → [`Operations`](operations.cob) 'DEBIT '<br/>3. Validation fonds → calcul → [`DataProgram`](data.cob) 'WRITE'<br/>4. Confirmation utilisateur | Transaction de débit complète réussie | | | Test de bout en bout |
| **TC_INT_004** | **Flux complet - Débit refusé** | Solde insuffisant | 1. [`MainProgram`](main.cob) → menu<br/>2. Option 3 → [`Operations`](operations.cob) 'DEBIT '<br/>3. Validation fonds échoue<br/>4. Message d'erreur utilisateur | Transaction refusée, données inchangées | | | Test règle métier |

## Tests de Robustesse

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status | Comments |
|--------------|----------------------|----------------|------------|-----------------|---------------|---------|----------|
| **TC_ROB_001** | **Gestion - Caractères spéciaux dans montant** | Menu crédit/débit affiché | 1. Sélectionner crédit ou débit<br/>2. Saisir des caractères non numériques<br/>3. Observer le comportement | Comportement défini (erreur ou conversion) | | | Test de validation d'entrée |
| **TC_ROB_002** | **Gestion - Montants négatifs** | Menu crédit/débit affiché | 1. Sélectionner crédit ou débit<br/>2. Saisir un montant négatif<br/>3. Observer le comportement | Comportement défini selon règles métier | | | Test de cas limite |
| **TC_ROB_003** | **Gestion - Sessions multiples** | Plusieurs utilisateurs simultanés | 1. Démarrer plusieurs instances<br/>2. Effectuer des transactions<br/>3. Vérifier la cohérence | Comportement prévisible pour données partagées | | | Test de concurrence |

## Critères d'Acceptation

### Fonctionnalités Critiques (Obligatoires)
- ✅ Consultation du solde sans modification
- ✅ Crédit avec mise à jour correcte du solde
- ✅ Débit avec vérification des fonds
- ✅ Refus des débits avec fonds insuffisants
- ✅ Navigation correcte dans le menu
- ✅ Sortie propre de l'application

### Règles Métier
- ✅ Solde initial : 1000.00
- ✅ Précision : 2 décimales
- ✅ Pas de solde négatif autorisé
- ✅ Persistance des données durant la session

### Performance
- ✅ Temps de réponse < 1 seconde pour chaque opération
- ✅ Interface utilisateur réactive

## Notes pour la Migration Python

Ce plan de test servira de base pour :
1. **Tests unitaires** : Chaque fonction Python correspondante
2. **Tests d'intégration** : Communication entre modules Python
3. **Tests de régression** : Validation que la logique métier reste identique
4. **Tests de validation** : Confirmation avec les parties prenantes

**Fichiers COBOL de référence** :
- [`main.cob`](main.cob) - Interface utilisateur
- [`operations.cob`](operations.cob) - Logique métier  
- [`data.cob`](data.cob) - Persistance des données
