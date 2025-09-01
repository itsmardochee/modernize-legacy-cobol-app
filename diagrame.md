# Diagramme de séquence - Application de gestion de comptes COBOL

```mermaid
sequenceDiagram
    participant User
    participant MainProgram as MainProgram<br/>(main.cob)
    participant Operations as Operations<br/>(operations.cob)
    participant DataProgram as DataProgram<br/>(data.cob)

    User->>MainProgram: Démarre l'application
    MainProgram->>User: Affiche le menu (1-4)
    
    loop Jusqu'à choix = 4
        User->>MainProgram: Sélectionne une option (1-4)
        
        alt 1. Consulter le solde
            MainProgram->>Operations: CALL 'Operations' USING 'TOTAL '
            Operations->>DataProgram: CALL 'DataProgram' USING 'read', FINAL-BALANCE
            DataProgram->>DataProgram: MOVE STORAGE-BALANCE TO BALANCE
            DataProgram-->>Operations: Retourne le solde actuel
            Operations->>User: DISPLAY "Current balance: " FINAL-BALANCE
            
        else 2. Créditer le compte
            MainProgram->>Operations: CALL 'Operations' USING 'CREDIT'
            Operations->>User: DISPLAY "Enter credit amount: "
            User->>Operations: Saisit le montant (ACCEPT AMOUNT)
            Operations->>DataProgram: CALL 'DataProgram' USING 'read', FINAL-BALANCE
            DataProgram->>DataProgram: MOVE STORAGE-BALANCE TO BALANCE
            DataProgram-->>Operations: Retourne le solde actuel
            Operations->>Operations: ADD AMOUNT TO FINAL-BALANCE
            Operations->>DataProgram: CALL 'DataProgram' USING 'WRITE', FINAL-BALANCE
            DataProgram->>DataProgram: MOVE BALANCE TO STORAGE-BALANCE
            DataProgram-->>Operations: Confirme la sauvegarde
            Operations->>User: DISPLAY "Amount credited. New balance: " FINAL-BALANCE
            
        else 3. Débiter le compte
            MainProgram->>Operations: CALL 'Operations' USING 'DEBIT '
            Operations->>User: DISPLAY "Enter debit amount: "
            User->>Operations: Saisit le montant (ACCEPT AMOUNT)
            Operations->>DataProgram: CALL 'DataProgram' USING 'read', FINAL-BALANCE
            DataProgram->>DataProgram: MOVE STORAGE-BALANCE TO BALANCE
            DataProgram-->>Operations: Retourne le solde actuel
            
            alt Fonds suffisants (FINAL-BALANCE >= AMOUNT)
                Operations->>Operations: SUBTRACT AMOUNT FROM FINAL-BALANCE
                Operations->>DataProgram: CALL 'DataProgram' USING 'WRITE', FINAL-BALANCE
                DataProgram->>DataProgram: MOVE BALANCE TO STORAGE-BALANCE
                DataProgram-->>Operations: Confirme la sauvegarde
                Operations->>User: DISPLAY "Amount debited. New balance: " FINAL-BALANCE
            else Fonds insuffisants
                Operations->>User: DISPLAY "Insufficient funds for this debit."
            end
            
        else 4. Quitter
            MainProgram->>MainProgram: MOVE 'NO' TO CONTINUE-FLAG
            MainProgram->>User: DISPLAY "Exiting the program. Goodbye!"
            
        else Choix invalide
            MainProgram->>User: DISPLAY "Invalid choice, please select 1-4."
        end
        
        alt Si choix != 4
            MainProgram->>User: Affiche à nouveau le menu
        end
    end
    
    MainProgram->>MainProgram: STOP RUN
```

## Description du flux

Ce diagramme illustre l'architecture modulaire de l'application COBOL avec trois composants principaux :

- **MainProgram** : Interface utilisateur et contrôle du flux principal
- **Operations** : Logique métier pour les opérations bancaires
- **DataProgram** : Couche de persistance pour le stockage du solde

Chaque opération suit le pattern : **Interface → Logique → Données → Retour**
