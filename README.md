python -m mypy --check-untyped-defs src tests
python -m pytest
.\.venv\Scripts\python.exe -m pip install pygame


--------------- Conventions ---------------

Typer tous les attributs, paramètre, variables et retours de fonction
Aération du code : 
    Saut de ligne : (Les sauts de ligne se combinent)
        - Avant/Après if/elif/else et for/while sauf si ils se suivent
        - Avant return
        - Entre des blocs de codes
        - Après raise
        - Après vérification du type des paramètres
    Double saut de ligne entre chaque méthode/fonction
    Triple saut de ligne :
        - Entre différentes classes
        - Après les imports
Trier les imports par ordre alphabétique
Les commentaires ne sont pas considérés comme des sauts de ligne

Par gain de temps, les fichiers de test ne sont pas soumis aux conventions.