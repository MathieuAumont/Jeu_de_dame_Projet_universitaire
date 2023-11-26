# Auteurs: Kim et Mathieu

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
        if self.damier.position_est_dans_damier(position_source):  # Est-ce que c'est dans le damier
            if self.damier.recuperer_piece_a_position(position_source) is None:  # Est-ce qu'il y a une piece à la case
                return False, "Il n'y a pas de piece dans votre case."
            elif self.damier.recuperer_piece_a_position(position_source).couleur != self.couleur_joueur_courant:
                # Est-ce que la piece t'appartient
                return False, "Cette piece ne vous appartient pas."
        else:
            return False, "Vous n'êtes pas dans le damier."

        if not self.damier.piece_de_couleur_peut_faire_une_prise(self.damier.recuperer_piece_a_position(position_source).couleur):
            # Est-ce que le joueur peut faire une prise?
            if self.damier.piece_peut_se_deplacer(position_source):  # Puisque le joueur peut pas faire de prise,
                # est-ce que la piece peut se déplacer
                return True, ""
            else:
                return False, "Cette piece ne peut pas se déplacer."
        elif self.damier.piece_peut_faire_une_prise(position_source):  # Est-ce que cette piece peut faire une prise
            return True, ""
        else:
            return False, "Vous ne pouvez pas bougez cette piece parce qu'une autre piece à la possibilité de manger."

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """
        #TODO: À compléter

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        # ON NE SAIT PAS COMMENT S'OCCUPPER DES CAS D'EXEPTION ENCORE, IL VA FALLOIR Y RETOURNER
        # J'AGIS COMME SI CE N'EST QUE DES ENTIERS QU'IL VONT RENTRER
        position_source_ligne = ""
        position_source_colone = ""
        position_cible_ligne = ""
        position_cible_colone = ""

        while position_source_ligne == "" and position_source_colone == "" and position_cible_ligne == "" and position_cible_colone == "":
            position_source_ligne = int(input("Veuillez entrer votre position source (ligne) : "))
            position_source_colone = int(input("Veuillez entrer votre position source (colone) : "))
            position_cible_ligne = int(input("Veuillez entrer votre position cible (ligne) : "))
            position_cible_colone = int(input("Veuillez entrer votre position cible (colone) : "))
            position_source_selectionnee = Position(position_source_ligne, position_source_colone)
            position_cible_selectionnee = Position(position_cible_ligne, position_cible_colone)

            if not self.position_source_valide(position_source_selectionnee)[0]:
                print("Votre position source est invalide car: ", self.position_source_valide(position_source_selectionnee)[1])
                position_source_ligne = ""
                position_source_colone = ""
                position_cible_ligne = ""
                position_cible_colone = ""

            # position_cible_valide pas encore écrit au moment de l'écriture
            elif not self.position_cible_valide(position_cible_selectionnee)[0]:
                print("Votre position source est invalide car: ", self.position_cible_valide(position_cible_selectionnee)[1])
                position_source_ligne = ""
                position_source_colone = ""
                position_cible_ligne = ""
                position_cible_colone = ""
        # Il n'y aura pas le probleme mentionner,
        # parce qu'il ne sortira jamais du "while" sans avoir de position source et cible valide
        return (position_source_selectionnee, position_cible_selectionnee)




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

        # Affiche l'état du jeu
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

        # Demander les positions
        # TODO: À compléter

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        # TODO: À compléter

        # Mettre à jour les attributs de la classe
        # TODO: À compléter

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


# NON ÉVALUER MAIS POUR M'AIDER
if __name__ == "__main__":

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
    print(essaie_partie.demander_positions_deplacement())
    print("assert réussit")
