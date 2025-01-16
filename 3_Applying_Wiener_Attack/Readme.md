## Présentation  
Ce dossier contient l'application de l'attaque de Wiener sur des clés RSA vulnérables. L'objectif est de factoriser des entiers `N` associés à des exposants publics `e` à l'aide de l'attaque basée sur les fractions continues tel que presente par Wiener.  

## Contenu du dossier  
- **`integers_to_factorize.txt`** : Liste des entiers `N` et exposants `e`.  
- **`factorization_script.py`** : Script Python principal implémentant l'attaque de Wiener.  
- **`cracked_keys_d.txt`** : Résultats de la factorisation (clé privée `d`).  
- **`check_wiener.py`** : Script de vérification des résultats de factorisation.  
- **`wiener_attack_v2.py`** : Code source de l'attaque de Wiener utilisant les fractions continues.  
- **`boneh_durfee.sage`** : Implémentation SageMath de l'attaque de Boneh-Durfee pour des clés RSA faibles.  
- **`sage_wiener.sage`** : Version SageMath de l'attaque de Wiener.  
- **`results_second_batch.txt`** : Tentatives infructueuses sur un second lot d'entiers.  
- **`second_batch_attempts/`** : Dossier avec scripts supplémentaires et explorations sur le deuxième lot.  

## Utilisation  
### Python  
1. **Lancer l'attaque :**  
   ```bash
   python factorization_script.py

### Sage  
1. **Lancer l'attaque :**  
   ```bash
   sage sage_wiener.sage
