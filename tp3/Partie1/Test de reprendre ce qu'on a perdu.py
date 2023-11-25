# Auteurs: À compléter

from tp3.Partie1.piece import Piece
from tp3.Partie1.position import Position


class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        if position.ligne in range(0, self.n_lignes):
            return position.colonne in range(0, self.n_colonnes)
        else:
            return False

    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """
        if self.recuperer_piece_a_position(position_cible) is not None:  # cas où il y a une piece à la position cible
            return False
        if not self.position_est_dans_damier(position_cible):  # cas où la position cible n'est pas dans le damier
            return False
        if self.recuperer_piece_a_position(position_piece) is None:  # cas où à la position initiale il n'y a pas de piece
            return False

        # il faut regarder la couleur et le type de piece pour avoir les vrai bon déplacement.

        piece_qui_deplace = self.recuperer_piece_a_position(position_piece)

        if piece_qui_deplace.type_de_piece == "pion":
            if piece_qui_deplace.couleur == "noir":
                return position_piece.positions_diagonales_bas()[0] == position_cible or position_piece.positions_diagonales_bas()[1] == position_cible
            else:  # alors elle est blanche
                return position_piece.positions_diagonales_haut()[0] == position_cible or position_piece.positions_diagonales_haut()[1] == position_cible
        else:  # alors elle est de type dame
            return position_piece.quatre_positions_diagonales()[0] == position_cible or position_piece.quatre_positions_diagonales()[1] == position_cible or position_piece.quatre_positions_diagonales()[2] == position_cible or position_piece.quatre_positions_diagonales()[3] == position_cible

    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """
        #TODO: À compléter

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        #TODO: À compléter

    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """
        if self.recuperer_piece_a_position(position_piece) is None:  # cas où à la position initiale il n'y a pas de piece
            return False

        piece_qui_deplace = self.recuperer_piece_a_position(position_piece)

        # Pour les dames (la couleur n'a pas d'importance)
        if piece_qui_deplace.type_de_piece == "dame":  # si c'est une dame
            for index in range(0, 4):
                if self.position_est_dans_damier(position_piece.quatre_positions_sauts()[index]):  # est-ce que le saut est dans le damier
                    if self.recuperer_piece_a_position(position_piece.quatre_positions_sauts()[index]) is None:  # est-ce qu'il y a personne à l'arriver
                        if self.recuperer_piece_a_position(position_piece.quatre_positions_diagonales()[index]) is not None:  # s'il y a une piece à mager
                            if self.recuperer_piece_a_position(position_piece.quatre_positions_diagonales()[index]).couleur != self.recuperer_piece_a_position(position_piece).couleur:  # S'ils n'ont pas la même couleur
                                return True
        # Pour le pion blanc
        elif piece_qui_deplace.couleur == "blanc":  # obliger que ça soir pion, donc on cherche sa couleur
            for index in range(0, 2):
                if self.position_est_dans_damier(position_piece.quatre_positions_sauts()[index+2]): # est-ce que le saut est dans le damier
                    if self.recuperer_piece_a_position(position_piece.quatre_positions_sauts()[index+2]) is None: # est-ce qu'il y a personne à l'arriver([2] parce que c'est celui correspondant à diagonale haut [0])
                        if self.recuperer_piece_a_position(position_piece.positions_diagonales_haut()[index]) is not None:  # s'il y a une piece à mager
                            if self.recuperer_piece_a_position(position_piece.positions_diagonales_haut()[index]).couleur == "noir":  # si la piece à manger est noir
                                return True
        # Pour pion noir
        else:  # obliger que ça soit pion noir
            for index in range(0,2):
                if self.position_est_dans_damier(position_piece.quatre_positions_sauts()[index]):  # est-ce que le saut est dans le damier
                    if self.recuperer_piece_a_position(position_piece.quatre_positions_sauts()[index]) is None:  # est-ce qu'il y a personne à l'arriver([0] parce que c'est celui correspondant à diagonale bas [0])
                        if self.recuperer_piece_a_position(position_piece.positions_diagonales_bas()[index]) is not None:  # s'il y a une piece à mager
                            if self.recuperer_piece_a_position(position_piece.positions_diagonales_bas()[index]).couleur == "blanc":  # si la piece à manger est blanche
                                return True
        return False  # si t'es arriver ici, il n'y a aucune piece à manger

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """
        #TODO: À compléter

    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """


    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """
        #TODO: À compléter


    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i)+"| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)])+" | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()

    # Tester les position_est_dans_damier
    piece = Position(-1, 0)
    assert not un_damier.position_est_dans_damier(piece)
    piece = Position(0, -1)
    assert not un_damier.position_est_dans_damier(piece)
    piece = Position(0, 0)
    assert un_damier.position_est_dans_damier(piece)
    piece = Position(8, 0)
    assert not un_damier.position_est_dans_damier(piece)
    piece = Position(0, 8)
    assert not un_damier.position_est_dans_damier(piece)

    # Tester piece_peut_deplacer_vers
    # Teste position finale hors tableau
    assert not un_damier.piece_peut_se_deplacer_vers(Position(0, 1), Position(0, 8))
    # Teste position depart ne contient pas de piece
    assert not un_damier.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste position finale contient une piece
    assert not un_damier.piece_peut_se_deplacer_vers(Position(1, 0), Position(2, 1))
    # Teste bon pour pion noir
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(3, 0))
    # Teste pas bon pour pion noir
    assert not un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(2, 0))
    # Teste bon pour pion blanc
    assert un_damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 1))
    # Teste pas bon pour pion blanc
    assert not un_damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 0))
    damier_teste = Damier()
    damier_teste.cases[Position(4,1)] = Piece("noir", "dame")
    # Teste bon pour une dame noir
    assert damier_teste.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste pas bon pour dame noir
    assert not damier_teste.piece_peut_se_deplacer_vers(Position(4, 1), Position(4, 0))
    damier_teste.cases[Position(4, 1)] = Piece("blanc", "dame")
    # Teste bon pour une dame blanche
    assert damier_teste.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste pas bon pour une dame blanche
    assert not damier_teste.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 1))

    # Tester piece_peut_manger
    # IL FAUDRAIT PROBABLEMENT FAIRE PLUS DE TESTE ET QU'ON PEUT RETIRER DES PIECES
    # Teste si position de départ contient pas de pièce
    assert not un_damier.piece_peut_faire_une_prise(Position(0, 0))
    # Teste dame ne peut pas faire de prise
    assert not damier_teste.piece_peut_faire_une_prise(Position(4, 0))
    damier_teste.cases[Position(6, 1)] = Piece("blanc", "dame")
    # Teste dame ne peut pas faire une prise à cause de la couleur
    assert not damier_teste.piece_peut_faire_une_prise(Position(6, 1))
    damier_teste.cases[Position(6, 1)] = Piece("noir", "dame")
    # Teste dame peut faire une prise
    assert damier_teste.piece_peut_faire_une_prise(Position(6, 1))
    # Teste pion noir ne peut pas faire une prise
    assert not damier_teste.piece_peut_faire_une_prise(Position(2, 1))
    damier_teste.cases[Position(3, 2)] = Piece("noir", "dame")
    # Teste pion noir ne peut pas faire une prise à cause de la couleur
    assert not damier_teste.piece_peut_faire_une_prise(Position(2, 1))
    damier_teste.cases[Position(3, 2)] = Piece("blanc", "dame")
    # Teste pion noir peut faire une prise
    assert damier_teste.piece_peut_faire_une_prise(Position(2, 1))
    # Teste pion blanc ne peut pas faire une prise à cause d'un blocage à l'arriver
    assert not damier_teste.piece_peut_faire_une_prise(Position(7, 0))
    damier_teste.cases[Position(4, 1)] = Piece("noir", "dame")
    # Teste pion blanc peut faire une prise
    assert damier_teste.piece_peut_faire_une_prise(Position(5, 2))
    damier_teste.cases.pop(Position(7, 0))



    # Prise 2 des testes piece_peut_manger
    damier_vide = Damier()
    damier_vide.cases.pop(Position(0, 1))
    damier_vide.cases.pop(Position(0, 3))
    damier_vide.cases.pop(Position(0, 5))
    damier_vide.cases.pop(Position(0, 7))
    damier_vide.cases.pop(Position(1, 0))
    damier_vide.cases.pop(Position(1, 2))
    damier_vide.cases.pop(Position(1, 4))
    damier_vide.cases.pop(Position(1, 6))
    damier_vide.cases.pop(Position(2, 1))
    damier_vide.cases.pop(Position(2, 3))
    damier_vide.cases.pop(Position(2, 5))
    damier_vide.cases.pop(Position(2, 7))
    damier_vide.cases.pop(Position(5, 0))
    damier_vide.cases.pop(Position(5, 2))
    damier_vide.cases.pop(Position(5, 4))
    damier_vide.cases.pop(Position(5, 6))
    damier_vide.cases.pop(Position(6, 1))
    damier_vide.cases.pop(Position(6, 3))
    damier_vide.cases.pop(Position(6, 5))
    damier_vide.cases.pop(Position(6, 7))
    damier_vide.cases.pop(Position(7, 0))
    damier_vide.cases.pop(Position(7, 2))
    damier_vide.cases.pop(Position(7, 4))
    damier_vide.cases.pop(Position(7, 6))
    # Teste si position de départ contient pas de pièce
    assert not un_damier.piece_peut_faire_une_prise(Position(0, 0))

    print('Test unitaires passés avec succès!')

    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(un_damier)
    print(damier_teste)
    print(damier_vide)