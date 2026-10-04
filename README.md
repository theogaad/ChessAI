# ChessAI

Moteur d'échecs développé en Python dans le but d'expérimenter et d'approfondir la conception d'un moteur de jeu, la représentation d'un état de jeu et les algorithmes d'intelligence artificielle appliqués aux échecs.

Le projet évolue progressivement à travers plusieurs architectures. Les précédentes implémentations sont conservées dans des branches Git dédiées afin de pouvoir comparer les différentes approches.

## Objectifs

Cette nouvelle version a pour objectif de construire un moteur d'échecs reposant sur une architecture plus adaptée aux performances et à la recherche de coups.

Les principaux objectifs sont :

* utiliser des **bitboards** pour représenter les pièces ;
* séparer clairement l'état du jeu, la génération des coups et la recherche ;
* minimiser les allocations et copies d'objets lors de la recherche ;
* permettre une application et une annulation rapides des coups ;
* utiliser le **Zobrist hashing** pour identifier efficacement les positions ;
* disposer d'une représentation **FEN** pour charger et sauvegarder des positions ;
* disposer d'une suite de tests permettant notamment de vérifier la génération des coups avec des positions `perft` ;
* construire progressivement une IA capable de rechercher des coups de manière efficace.

L'objectif n'est donc pas uniquement d'obtenir un programme capable de jouer aux échecs, mais de construire un moteur dont l'architecture permet d'expérimenter différentes techniques d'optimisation et d'intelligence artificielle.

---

## Évolution du projet

Ce dépôt contient plusieurs générations du moteur.

Les anciennes implémentations sont conservées dans des branches Git distinctes. Elles constituent des étapes du développement du projet et permettent notamment de comparer différentes représentations des positions et différentes architectures.

La branche actuelle constitue une **nouvelle architecture**, conçue dès le départ autour des bitboards et d'une séparation plus stricte des responsabilités.

L'historique du projet est donc volontairement conservé plutôt que remplacé.

---

## Architecture

Le moteur est organisé autour de plusieurs composants ayant chacun une responsabilité précise.

```text
chess_engine/
│
├── types.py
├── constants.py
│
├── piece_bitboards.py
├── position.py
│
├── attack_generator.py
├── move.py
├── move_generator.py
│
├── zobrist.py
├── fen.py
├── history.py
├── game.py
│
└── ...
```

### Types fondamentaux

`types.py` contient les énumérations utilisées par l'ensemble du moteur :

* `Color`
* `PieceType`
* `MoveType`
* `GameStatus`
* `DrawReason`

### Constantes

`constants.py` contient les constantes liées au plateau et aux bitboards :

* dimensions du plateau ;
* masque des 64 cases ;
* masques des fichiers (colonnes);
* masques des rangées (lignes);
* configuration initiale FEN.

La convention utilisée pour les cases est la suivante :

```text
        a    b    c    d    e    f    g    h
    ┌────┬────┬────┬────┬────┬────┬────┬────┐
8   │  7 │  6 │  5 │  4 │  3 │  2 │  1 │  0 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
7   │ 15 │ 14 │ 13 │ 12 │ 11 │ 10 │  9 │  8 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
6   │ 23 │ 22 │ 21 │ 20 │ 19 │ 18 │ 17 │ 16 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
5   │ 31 │ 30 │ 29 │ 28 │ 27 │ 26 │ 25 │ 24 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
4   │ 39 │ 38 │ 37 │ 36 │ 35 │ 34 │ 33 │ 32 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
3   │ 47 │ 46 │ 45 │ 44 │ 43 │ 42 │ 41 │ 40 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
2   │ 55 │ 54 │ 53 │ 52 │ 51 │ 50 │ 49 │ 48 │
    ├────┼────┼────┼────┼────┼────┼────┼────┤
1   │ 63 │ 62 │ 61 │ 60 │ 59 │ 58 │ 57 │ 56 │
    └────┴────┴────┴────┴────┴────┴────┴────┘
```

Ainsi :

* `h8 = 0`
* `a8 = 7`
* `h1 = 56`
* `a1 = 63`

Une case est donc représentée directement par un entier compris entre `0` et `63`.

---

## Représentation des pièces

Le moteur utilise des **bitboards**.

Un bitboard est un entier Python (`int`) dont les 64 bits correspondent aux 64 cases du plateau.

Douze bitboards représentent les pièces :

```text
White:
    King
    Queen
    Rook
    Bishop
    Knight
    Pawn

Black:
    King
    Queen
    Rook
    Bishop
    Knight
    Pawn
```

Trois bitboards d'occupation sont également maintenus :

```text
white_pieces
black_pieces
occupied
```

avec :

```text
white_pieces = toutes les pièces blanches
black_pieces = toutes les pièces noires
occupied     = white_pieces | black_pieces
```

Cette représentation permet d'effectuer de nombreuses opérations sur le plateau avec des opérations bit à bit.

---

## Position

`Position` représente **l'état actuel d'une position d'échecs**.

Elle contient notamment :

```text
Position
├── PieceBitboards
├── side_to_move
├── castling_rights
├── en_passant_square
└── halfmove_clock
```

La `Position` ne contient pas l'historique complet de la partie et ne gère pas elle-même la recherche de coups.

Une position peut être créée à partir d'un FEN.

---

## Attaques et coups

La génération des attaques et la génération des coups sont séparées.

### `AttackGenerator`

Calcule les cases attaquées par les différentes pièces :

* pions ;
* cavaliers ;
* rois ;
* fous ;
* tours ;
* dames.

Les attaques des cavaliers et des rois peuvent être pré-calculées, tandis que les attaques des pièces à déplacement glissant dépendent de l'occupation du plateau.

### `MoveGenerator`

Utilise `AttackGenerator` pour produire les coups.

Il gère notamment :

* déplacements des pièces ;
* captures ;
* déplacements des pions ;
* doubles déplacements des pions ;
* promotions ;
* prises en passant ;
* roques ;
* vérification de la légalité des coups.

La génération finale fournit uniquement des **coups légaux**.

---

## Coups et annulation

Un coup décrit uniquement l'action à effectuer :

```text
Move
├── start_square
├── end_square
├── move_type
└── promotion_piece_type
```

Les informations nécessaires à l'annulation d'un coup sont séparées dans `UndoInfo`.

Cette séparation permet au moteur de modifier une position puis de la restaurer rapidement pendant la recherche.

Le moteur privilégie ainsi :

```text
make_move()
    ↓
recherche
    ↓
undo_move()
```

plutôt que de créer une copie complète de la position à chaque nœud de recherche.

---

## Zobrist hashing

Chaque position possède un hash de Zobrist permettant de l'identifier rapidement.

Le hash prend notamment en compte :

* les pièces présentes sur les cases ;
* le joueur au trait ;
* les droits de roque ;
* l'information d'en passant.

Le hash est mis à jour incrémentalement lors de l'application et de l'annulation des coups.

Il sera utilisé notamment pour :

* détecter les répétitions ;
* identifier rapidement les positions ;
* construire ultérieurement une table de transposition pour l'IA.

Un hash de Zobrist est un identifiant et **ne permet pas de reconstruire directement une position**. Si une reconstruction complète d'une position est nécessaire, elle devra être assurée par une autre structure.

---

## Historique et fin de partie

L'historique permet notamment de détecter les répétitions de position.

Les statuts possibles d'une partie sont :

```text
ONGOING
CHECKMATE
STALEMATE
DRAW
```

Lorsqu'une partie est nulle, la raison peut être :

```text
REPETITION
FIFTY_MOVES
INSUFFICIENT_MATERIAL
```

---

## FEN

Le format **Forsyth–Edwards Notation (FEN)** est utilisé pour représenter une position complète sous forme textuelle.

Exemple de position initiale :

```text
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

Le support du FEN permet notamment :

* d'initialiser une position précise ;
* de tester des situations particulières ;
* de réaliser des tests `perft` ;
* de sauvegarder et restaurer des positions ;
* de faciliter le débogage du moteur.

---

## Tests

La génération des coups constitue une partie critique du moteur.

Des tests dédiés seront notamment utilisés pour vérifier :

* les déplacements de chaque pièce ;
* les captures ;
* les promotions ;
* les prises en passant ;
* les roques ;
* les positions en échec ;
* les positions où le roi ne peut pas se déplacer ;
* la génération complète des coups avec des positions `perft`.

La priorité est d'obtenir une génération de coups **correcte avant d'optimiser la recherche**.

---

## Intelligence artificielle

L'intelligence artificielle sera développée indépendamment du cœur des règles du jeu.

L'architecture pourra progressivement accueillir :

* minimax / negamax ;
* alpha-beta pruning ;
* recherche itérative ;
* ordonnancement des coups ;
* quiescence search ;
* table de transposition ;
* fonction d'évaluation ;
* gestion du temps de recherche ;
* éventuellement ouverture et tables de finales.

Le moteur de recherche utilisera les mêmes `Position`, `Move`, `make_move()` et `undo_move()` que le reste du programme.

Cette séparation doit permettre de modifier l'IA sans modifier le fonctionnement fondamental des règles d'échecs.

---

## Interface utilisateur

L'interface graphique n'a pas vocation à contenir la logique du moteur.

Elle communiquera avec celui-ci par l'intermédiaire de l'API du jeu.

```text
Interface
    ↓
Game
    ↓
Position / MoveGenerator
    ↓
Bitboards
```

Le moteur doit ainsi pouvoir fonctionner sans interface graphique, notamment pour les tests et les expérimentations de recherche.

---

## État actuel du développement

Le projet est actuellement dans une phase de **conception et de mise en place de l'architecture**.

L'objectif immédiat est de définir l'ensemble des interfaces du moteur avant d'implémenter leur logique :

1. types fondamentaux ;
2. constantes et bitboards ;
3. représentation d'une position ;
4. génération des attaques ;
5. génération des coups ;
6. application et annulation des coups ;
7. Zobrist hashing ;
8. FEN ;
9. historique et gestion de partie ;
10. tests ;
11. intelligence artificielle.

Les différentes méthodes seront d'abord définies avec leurs signatures et leur documentation, puis implémentées progressivement.

---

## Philosophie du projet

Cette version privilégie la **compréhension de l'architecture et des mécanismes internes** plutôt que l'utilisation d'une implémentation existante.

Chaque composant doit avoir une responsabilité clairement définie.

L'objectif final est de disposer d'un moteur :

* correct ;
* testable ;
* modulaire ;
* suffisamment performant pour expérimenter des algorithmes de recherche ;
* et surtout suffisamment clair pour permettre d'analyser et de comprendre les choix effectués.
