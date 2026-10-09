# ChessAI

**ChessAI** est un moteur d'échecs développé en Python, conçu pour explorer les mécanismes de fonctionnement d'un moteur de jeu et les algorithmes de recherche utilisés en intelligence artificielle.

Le projet est développé progressivement, en mettant l'accent sur la compréhension des algorithmes, la conception logicielle et les performances.

## Objectifs du projet

* Développer un moteur d'échecs à partir de zéro.
* Implémenter une représentation efficace de l'échiquier à l'aide de *bitboards*.
* Générer les coups légaux conformément aux règles des échecs.
* Concevoir un système fiable d'exécution et d'annulation des coups.
* Développer une intelligence artificielle reposant sur des algorithmes de recherche et d'évaluation.
* Améliorer progressivement les performances du moteur.

## Fonctionnalités

Les fonctionnalités sont développées progressivement.

* [x] Représentation de l'échiquier avec des bitboards.
* [x] Structure de données pour les pièces et leurs positions.
* [x] Génération des coups légaux.
* [x] Gestion complète des règles spéciales des échecs.
* [x] Détection des situations de fin de partie.
* [x] Recherche de coups avec l'algorithme Minimax / Negamax.
* [x] Optimisation de la recherche avec l'élagage alpha-bêta.
* [ ] Amélioration de l'ordre d'exploration des coups (*Move Ordering*).
* [ ] Développement progressif de la fonction d'évaluation.

## Architecture

Le moteur est organisé en composants distincts afin de séparer les responsabilités et de faciliter son évolution.

| Composant         | Responsabilité                                                          |
| ----------------- | ----------------------------------------------------------------------- |
| `Position`        | Représentation de l'état courant de la partie.                          |
| `PieceBitboards`  | Gestion des pièces à l'aide de bitboards.                               |
| `AttackGenerator` | Calcul des cases attaquées par les pièces.                              |
| `MoveGenerator`   | Génération des coups légaux.                                            |
| `MoveExecutor`    | Exécution et annulation des coups.                                      |
| `Game`            | Gestion du déroulement et de l'état de la partie.                       |
| `AI`              | Recherche et sélection des coups joués par l'intelligence artificielle. |

*Cette architecture évolue au fil du développement.*

## Intelligence artificielle

L'intelligence artificielle est développée progressivement à partir d'algorithmes de recherche dans l'arbre des coups.

Les pistes de développement comprennent :

* La recherche Minimax et Negamax.
* L'élagage alpha-bêta pour réduire le nombre de positions explorées.
* Le *Move Ordering* pour explorer en priorité les coups les plus prometteurs.
* L'amélioration de la fonction d'évaluation des positions.
* L'optimisation des performances du moteur.

## Technologies

* **Langage :** Python
* **Outils :** Git, GitHub et Visual Studio Code
* **Tests :** pytest
* **Qualité du code :** mypy
* **Documentation :** Sphinx

## Installation

Le projet est en cours de développement. Les instructions d'installation et d'exécution seront complétées au fur et à mesure de la stabilisation de l'architecture.

## État du projet

ChessAI est un projet personnel de développement et d'apprentissage. L'objectif est de construire un moteur d'échecs fonctionnel, puis d'en améliorer progressivement la force de jeu et les performances.