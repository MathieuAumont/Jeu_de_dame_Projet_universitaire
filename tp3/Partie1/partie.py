# Auteur.trice.s: Kim vaillancourt et Mathieu Aumont

from tp3.Partie1.damier import Damier
from tp3.Partie1.position import Position
# le prochain est pour les testes
from tp3.Partie1.piece import Piece


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """
    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        if self.position_source_forcee is None:  # S'il n'y a pas de position source forcée.
            if self.damier.position_est_dans_damier(position_source):  # Est-ce que c'est dans le damier?
                if position_source not in self.damier.cases:  # Est-ce qu'il y a une piece à la case choisit?
                    return False, "Il n'y a pas de piece dans votre case."
                elif self.damier.recuperer_piece_a_position(position_source).couleur != self.couleur_joueur_courant:
                    # Est-ce que la piece appartient au joueur?
                    return False, "Cette piece ne vous appartient pas."
            else:
                return False, "Vous n'êtes pas dans le damier."

            if not (self.damier.piece_de_couleur_peut_faire_une_prise
                    (self.damier.recuperer_piece_a_position(position_source).couleur)):
                # Est-ce que le joueur de couleure peut faire une prise?
                if self.damier.piece_peut_se_deplacer(position_source):  # Puisque le joueur ne peut pas faire de prise,
                    # est-ce que la piece peut se déplacer?
                    return True, ""
                else:
                    return False, "Cette piece ne peut pas se déplacer."
            # Est-ce que cette piece peut faire une prise lorsque le joueur peut faire une prise?
            elif self.damier.piece_peut_faire_une_prise(position_source):
                return True, ""
            else:
                return (False,
                        "Vous ne pouvez pas bougez cette piece parce qu'une autre piece à la possibilité de manger.")
        else:
            if position_source == self.position_source_forcee:
                return True, ""
            else:
                return False, "Vous devez prendre la même pièce pour faire une prise"

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """

        if not self.damier.position_est_dans_damier(position_cible):  # La position cible est-elle dans le damier?
            return False, "La position cible choisi n'est pas dans le damier."
        elif position_cible in self.damier.cases:  # La position cible est-elle déjà occupée?
            return (False, "Cette case est déjà occupée par un.e {}."
                    .format(self.damier.cases[position_cible].type_de_piece))

        # Le cas où il y a une prise.
        if self.damier.piece_peut_faire_une_prise(self.position_source_selectionnee):  # Est-ce qu'il y a une prise?
            # Est-ce que la position cible fait partie des choix de prise?
            if self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):
                return True, ""
            else:
                # Le choix ne fait pas partie des prises.
                return False, "Votre choix n'est pas une prise possible. Veuillez choisir une prise."
        # La case de déplacement.
        elif self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):
            # La position cible fait-elle partie des choix de déplacement ?
            return True, ""
        else:
            # Le choix ne fait pas partie des déplacements possibles.
            return False, "Vous ne pouvez vous déplacer à cette endroit."

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        # Demandez pour la position source.
        erreur_position_source = True
        while erreur_position_source is True:
            try:
                position_source_ligne = int(input("Veuillez entrer votre position source(ligne) : "))
                position_source_colonne = int(input("Veuillez entrer votre position source(colonne) : "))
                if (position_source_colonne not in range(0, self.damier.n_colonnes) or position_source_ligne not in
                        range(0, self.damier.n_lignes)):
                    raise TypeError
                self.position_source_selectionnee = Position(position_source_ligne, position_source_colonne)
                if self.position_source_valide(self.position_source_selectionnee)[1] != "":
                    raise PositionError
                erreur_position_source = False
            # Si erreur de frappe, le joueur peut entrer à nouveau ses positions.
            except ValueError:
                print("Vous n'avez pas tapé un chiffre.\n-Veuillez recommencer.-")
            except TypeError:
                print("Vous n'avez pas tapé un chiffre valide, il ne se trouve pas dans le damier."
                      "\n-Veuillez recommencer.-")
            except PositionError:
                print(self.position_source_valide(self.position_source_selectionnee)[1])

        # Demander pour la position cible.
        erreur_position_cible = True
        position_cible_selectionnee = None
        while erreur_position_cible is True:
            try:
                position_cible_ligne = int(input("Veuillez entrer votre position cible (ligne) : "))
                position_cible_colonne = int(input("Veuillez entrer votre position cible (colonne) : "))
                if (position_cible_colonne not in range(0, self.damier.n_colonnes) or position_cible_ligne not in
                        range(0, self.damier.n_lignes)):
                    raise TypeError()
                position_cible_selectionnee = Position(position_cible_ligne, position_cible_colonne)
                if self.position_cible_valide(position_cible_selectionnee)[1] != "":
                    raise PositionError()
                erreur_position_cible = False
            # Si erreur de frappe' le joueur peut entrer à nouveau ses positions.
            except ValueError:
                print("vous n'avez pas tapé un chiffre.\n-Veuillez Recommencer.-")
            except TypeError:
                print("Vous n'avez pas tapé un chiffre valide, il ne se trouve pas dans le damier."
                      "\n-Veuillez recommencer.-")
            except PositionError:
                print(self.position_cible_valide(position_cible_selectionnee)[1])

        return self.position_source_selectionnee, position_cible_selectionnee

    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu.
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")

        # Demandez les positions.
        position_source, position_cible = self.demander_positions_deplacement()

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée).
        # Une variable qui retourne True s'il n'y a pas de déplacement avec prise.
        pas_de_prise = self.damier.piece_peut_se_deplacer_vers(position_source, position_cible)

        # Déplacement de la pièce
        self.damier.deplacer(position_source, position_cible)

        # Ceci mets à jour les attributs de la classe.
        # Le cas de déplacement sans prise.
        if pas_de_prise:
            # On change de jouer courant.
            if self.couleur_joueur_courant == "noir":
                self.couleur_joueur_courant = "blanc"
            else:
                self.couleur_joueur_courant = "noir"
        # Le cas de déplacement avec une prise.
        else:
            # S'il ne faut pas changer pas de joueur courant.
            if self.damier.piece_peut_faire_une_prise(position_cible):
                self.position_source_forcee = position_cible  # On force la position à selectionner
                self.position_source_selectionnee = self.position_source_forcee
            else:
                # On change de joueur courant.
                if self.couleur_joueur_courant == "noir":
                    self.couleur_joueur_courant = "blanc"
                else:
                    self.couleur_joueur_courant = "noir"
                # On remet les valeurs par défaut du damier.
                self.doit_prendre = False
                self.position_source_forcee = None

    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"


class PositionError(Exception):
    """
    Classe d'exception personnalisée permettant d'envoyé un message au joueur lors du choix de position invalide.
    """
    pass


# NON ÉVALUER MAIS POUR NOUS AIDER
if __name__ == "__main__":
    print("tests unitaires de la classe 'Partie'...")
    # Teste position_source_valide
    essaie_partie = Partie()
    assert essaie_partie.position_source_valide(Position(-1, 5)) == (False, "Vous n'êtes pas dans le damier.")
    assert essaie_partie.position_source_valide(Position(3, 3)) == (False, "Il n'y a pas de piece dans votre case.")
    assert essaie_partie.position_source_valide(Position(0, 1)) == (False, "Cette piece ne vous appartient pas.")
    assert essaie_partie.position_source_valide(Position(7, 0)) == (False, "Cette piece ne peut pas se déplacer.")
    assert essaie_partie.position_source_valide(Position(5, 0)) == (True, "")
    essaie_partie.damier.cases[Position(4, 3)] = Piece("noir", "pion")
    assert (essaie_partie.position_source_valide(Position(5, 0)) ==
            (False, "Vous ne pouvez pas bougez cette piece parce qu'une autre piece à la possibilité de manger."))
    assert essaie_partie.position_source_valide(Position(5, 2)) == (True, "")
    essaie_partie.damier.cases.pop(Position(4, 3))

    print("tests unitaires passés avec succès!")
