#Auteurs: Kim et Mathieu

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

        # Le dictionnaire ci-dessous n'est que pour permettre de tester les prises obligatoires dans le jeu.
        # Par exemple, lorsque deux pièce peut faire une prise,il faut s'assurer que seul la pièce ayant déjà  fait une
        # prise peut bouger.

        # self.cases = {
        # Position(7, 6): Piece("blanc", "pion"),
        # Position(6, 5): Piece("noir", "pion"),
        # Position(4, 3): Piece("noir", "pion"),
        # Position(6, 7): Piece("blanc", "pion"),
        # Position(5, 6): Piece("noir", "pion"),
        # }

        # Le dictionnaire ci-dessous n'est que pour permettre de tester les fonctionnalité des dames.
        # self.cases = {
            # Position(7, 0): Piece("blanc", "dame"),
            # Position(7, 2): Piece("blanc", "dame"),
            # Position(7, 4): Piece("blanc", "dame"),
            # Position(7, 6): Piece("blanc", "dame"),
            # Position(6, 1): Piece("blanc", "dame"),
            # Position(6, 3): Piece("blanc", "dame"),
            # Position(6, 5): Piece("blanc", "dame"),
            # Position(6, 7): Piece("blanc", "dame"),
            # Position(5, 0): Piece("blanc", "dame"),
            # Position(5, 2): Piece("blanc", "dame"),
            # Position(5, 4): Piece("blanc", "dame"),
            # Position(5, 6): Piece("blanc", "dame"),
            # Position(2, 1): Piece("noir", "dame"),
            # Position(2, 3): Piece("noir", "dame"),
            # Position(2, 5): Piece("noir", "dame"),
            # Position(2, 7): Piece("noir", "dame"),
            # Position(1, 0): Piece("noir", "dame"),
            # Position(1, 2): Piece("noir", "dame"),
            # Position(1, 4): Piece("noir", "dame"),
            # Position(1, 6): Piece("noir", "dame"),
            # Position(0, 1): Piece("noir", "dame"),
            # Position(0, 3): Piece("noir", "dame"),
            # Position(0, 5): Piece("noir", "dame"),
            # Position(0, 7): Piece("noir", "dame"),
        # }

    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:  # Si la position ne contient pas de pièce, il ne faut rien retourner.
            return None

        return self.cases[position]  # Il n'y aura pas de "key error" grace aux ligne au-dessus.

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """

        return position.ligne in range(0, self.n_lignes) and position.colonne in range(0, self.n_colonnes)

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
        # Les cas d'exeptions ou il pourrait se produire une erreur.
        if self.recuperer_piece_a_position(position_cible) is not None:  # Le cas où il y a une piece à
            # la position cible.
            return False
        if not self.position_est_dans_damier(position_cible):  # Le cas où la position cible n'est pas dans le damier.
            return False
        if self.recuperer_piece_a_position(
                position_piece) is None:  # Le cas où à la position initiale il n'y a pas de piece.
            return False

        # il faut regarder la couleur et le type de piece pour avoir les vrai bon déplacement.

        piece_qui_deplace = self.recuperer_piece_a_position(position_piece)

        if piece_qui_deplace.type_de_piece == "pion":
            if piece_qui_deplace.couleur == "noir":  # Cette pièce est un pion noir.
                return position_cible in position_piece.positions_diagonales_bas()
            else:  # Cette pièce est un pion blanc.
                return position_cible in position_piece.positions_diagonales_haut()
        else:  # Cette piece est une dame.
            return position_cible in position_piece.quatre_positions_diagonales()

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
        # Les cas où:
        # 1. la position de la pièce initiale n'est pas dans le plateau
        # 2. La position cible contient une piece
        # 3. La position cible est impossible à atteindre avec un saut.
        # 4. La position cible n'set pas dans le plateau.
        # Si la situation ce trouve dans un des cas, alors la pièce ne peut pas faire de prises.

        if (position_piece not in self.cases or position_cible in self.cases or
                position_cible not in position_piece.quatre_positions_sauts() or
                not self.position_est_dans_damier(position_cible)):
            return False

        # Cette étape permet de determiner la position ou il y aurait possiblement une piece.
        # Cela se fait en trouvant la case commune entre la position initiale et la position cible.
        position_centre = None
        for position in position_piece.quatre_positions_diagonales():
            if position in position_cible.quatre_positions_diagonales():
                position_centre = position

        # Si la case centrale est vide ou si la pièce ce faisant possiblement "manger" a la même couleur que la piece
        # à la position initiale, alors une prise est impossible.
        if (position_centre not in self.cases or
                self.cases[position_centre].couleur == self.cases[position_piece].couleur):
            return False

        return True

    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """
        # On enlève le cas d'execption où la position de la pièce n'est pas dans le damier.
        if position_piece not in self.cases:
            return False

        piece = self.recuperer_piece_a_position(position_piece)

        if piece.type_de_piece == "dame":
            for position in position_piece.quatre_positions_diagonales():
                if position not in self.cases and self.position_est_dans_damier(position):
                    # Si la position d'arriver et qu'elle est dans le damier, alors la dame peut se déplacer.
                    return True

        elif piece.couleur == "noir":
            for position in position_piece.positions_diagonales_bas():
                if position not in self.cases and self.position_est_dans_damier(position):
                    # Si la position d'arriver et qu'elle est dans le damier, alors le pion noir peut se déplacer.
                    return True

        else:
            for position in position_piece.positions_diagonales_haut():
                if position not in self.cases and self.position_est_dans_damier(position):
                    # Si la position d'arriver et qu'elle est dans le damier, alors le pion blanc peut se déplacer.
                    return True

        return False

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
        if self.recuperer_piece_a_position(position_piece) is None:
            # Le cas où à la position initiale il n'y a pas de piece.
            return False

        for position in position_piece.quatre_positions_sauts():
            if self.piece_peut_sauter_vers(position_piece, position):
                return True

        return False

    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """
        for piece in self.cases:  # En regardant toutes les pièces, si elle est de la couleur demander et que cette
            # pièce peut se déplacer, alors la pièce de la couleur peut se déplacer.
            if self.cases[piece].couleur == couleur and self.piece_peut_se_deplacer(piece):
                return True
        return False

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
        for element in self.cases: # En regardant toutes les pièces, si elle est de la couleur demander et que cette
            # pièce peut faire une prise, alors la pièce de la couleur spécifique peut faire une prise.
            if self.cases[element].couleur == couleur and self.piece_peut_faire_une_prise(element):
                return True
        return False


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
        # Le cas d'execption ou la position source et cible ne se trouve pas dans le damier.
        if not self.position_est_dans_damier(position_source) or not self.position_est_dans_damier(position_cible):
            return "erreur"

        if self.piece_peut_faire_une_prise(position_source):  # Ceci permet de déterminer si la pièce source peut
            # faire une prise.
            for index in range(0, 4):
                if (position_cible == position_source.quatre_positions_sauts()[index] and
                        self.cases[position_source.quatre_positions_diagonales()[index]] is not None):
                    # Ceci vérifie si la position cible est valide pour faire une prise.
                    # Cela modifie le damier après le déplacement
                    self.cases.pop(position_source.quatre_positions_diagonales()[index])
                    self.cases[position_cible] = self.cases[position_source]
                    self.cases.pop(position_source)  # On retire la position source, car celle-ci c'est déplacé.
                    # vérifie s'il y a un cas de promotion chez les blancs.
                    if self.cases[position_cible].couleur == "blanc":
                        if position_cible.ligne == 0:
                            self.cases[position_cible].promouvoir()
                    # On fais la même chose chez les noirs.
                    else:
                        if position_cible.ligne == 7:
                            self.cases[position_cible].promouvoir()
                    return "prise"
            return "erreur"
        # Ceci détermine si la pièce peut se déplacer.
        elif self.piece_peut_se_deplacer(position_source):
            if self.cases[position_source].type_de_piece == "dame":
                # Cela s'occupe du cas où la piece est une dame
                if position_cible in position_source.quatre_positions_diagonales():
                    # On verifie si position cible est possible. Si cela l'est, alors on modifie le damier.
                    self.cases[position_cible] = self.cases[position_source]
                    self.cases.pop(position_source)
                    return "ok"
            else:  # Cela s'occupe du cas où la pièce est un pion.
                if self.cases[position_source].couleur == "blanc":  # Ici c'est le cas d'un piont blanc.
                    if position_cible in position_source.positions_diagonales_haut():
                        self.cases[position_cible] = self.cases[position_source]
                        self.cases.pop(position_source)
                        if position_cible.ligne == 0:
                            self.cases[position_cible].promouvoir()
                        return "ok"
                else:                                               # Ici c'est le cas d'un pion noir.
                    if position_cible in position_source.positions_diagonales_bas():
                        self.cases[position_cible] = self.cases[position_source]
                        self.cases.pop(position_source)
                        if position_cible.ligne == 7:
                            self.cases[position_cible].promouvoir()
                        return "ok"
        return "erreur"

    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i) + "| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)]) + " | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()

    # Test piece_peut_sauter_vers().
    damier_test = Damier()
    damier_test.cases[Position(4, 3)] = Piece("noir", "pion")
    damier_test.cases[Position(4, 5)] = Piece("blanc", "pion")
    damier_test.cases[Position(3,2)] = Piece("blanc", "dame")
    assert un_damier.piece_peut_sauter_vers(Position(7, 1), Position(5, 4)) is False
    assert un_damier.piece_peut_sauter_vers(Position(6, 6), Position(4, 4)) is False
    assert un_damier.piece_peut_sauter_vers(Position(5, 2), Position(3, 4)) is False
    assert damier_test.piece_peut_sauter_vers(Position(5, 2), Position(3, 4)) is True
    assert damier_test.piece_peut_sauter_vers(Position(5, 6), Position(3, 4)) is False

    # Tests piece_peut_se_deplacer().
    assert un_damier.piece_peut_se_deplacer(Position(1, 0)) is False
    assert un_damier.piece_peut_se_deplacer(Position(5, 4)) is True
    assert damier_test.piece_peut_se_deplacer(Position(3, 2)) is True
    assert un_damier.piece_peut_se_deplacer(Position(7, 2)) is False

    # Tester les position_est_dans_damier.
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

    # Tester piece_peut_deplacer_vers.

    # Le teste où la position finale est hors du tableau.
    assert not un_damier.piece_peut_se_deplacer_vers(Position(0, 1), Position(0, 8))
    # Le teste où la position de départ ne contient pas de piece.
    assert not un_damier.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste que la position finale contient une piece.
    assert not un_damier.piece_peut_se_deplacer_vers(Position(1, 0), Position(2, 1))
    # Teste réussit pour pion noir.
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(3, 0))
    # Teste non réussit pour pion noir.
    assert not un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(2, 0))
    # Teste réussit pour pion blanc.
    assert un_damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 1))
    # Teste non réussit pour pion blanc.
    assert not un_damier.piece_peut_se_deplacer_vers(Position(5, 0), Position(4, 0))

    damier_teste_kim = Damier()

    damier_teste_kim.cases[Position(4, 1)] = Piece("noir", "dame")
    # Teste réussit pour une dame noir.
    assert damier_teste_kim.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste non réussit pour une dame noir.
    assert not damier_teste_kim.piece_peut_se_deplacer_vers(Position(4, 1), Position(4, 0))
    damier_teste_kim.cases[Position(4, 1)] = Piece("blanc", "dame")
    # Teste réussit pour une dame blanche.
    assert damier_teste_kim.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0))
    # Teste non réussit pour une dame blanche.
    assert not damier_teste_kim.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 1))

    # Création d'un damier vide.
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

    # Testes piece_peut_manger().

    # Teste si la position de départ ne contient pas de pièce.
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 0))
    # Teste d'une dame pouvant manger.
    damier_vide.cases[Position(0, 1)] = Piece("noir", "dame")
    damier_vide.cases[Position(1, 2)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste d'une dame si la personne à manger est de même couleur.
    damier_vide.cases[Position(1, 2)] = Piece("noir", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste dame s'il n'y a personne mangé.
    damier_vide.cases.pop(Position(1,2))
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste dame s'il l'arriver n'est pas dans le damier.
    damier_vide.cases[Position(1, 0)] = Piece("noir", "dame")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste dame s'il l'arriver contient une piece.
    damier_vide.cases.pop(Position(1, 0))
    damier_vide.cases[Position(1, 2)] = Piece("blanc", "pion")
    damier_vide.cases[Position(2, 3)] = Piece("blanc", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    damier_vide.cases.pop(Position(2, 3))

    # Teste d'un pion noir pouvant manger.
    damier_vide.cases[Position(0, 1)] = Piece("noir", "pion")
    damier_vide.cases[Position(1, 2)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste pion noir si la pièce à manger est de même couleur.
    damier_vide.cases[Position(1, 2)] = Piece("noir", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste pion noir s'il n'y a personne mangé.
    damier_vide.cases.pop(Position(1, 2))
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste pion noir s'il l'arriver n'est pas dans le damier.
    damier_vide.cases[Position(1, 0)] = Piece("blanc", "dame")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste pion noir s'il l'arriver contient une piece.
    damier_vide.cases.pop(Position(1, 0))
    damier_vide.cases[Position(1, 2)] = Piece("blanc", "pion")
    damier_vide.cases[Position(2, 3)] = Piece("noir", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    damier_vide.cases.pop(Position(0, 1))
    damier_vide.cases.pop(Position(1, 2))
    damier_vide.cases.pop(Position(2, 3))

    # Teste pion blanc peut manger.
    damier_vide.cases[Position(7, 1)] = Piece("blanc", "pion")
    damier_vide.cases[Position(6, 2)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(7, 1))
    # Teste pion blanc si la personne à manger est de même couleur.
    damier_vide.cases[Position(6, 2)] = Piece("blanc", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(7, 1))
    # Teste pion blanc s'il n'y a personne mangé.
    damier_vide.cases.pop(Position(6, 2))
    assert not damier_vide.piece_peut_faire_une_prise(Position(7, 1))
    # Teste pion blanc s'il l'arriver n'est pas dans le damier.
    damier_vide.cases[Position(6, 0)] = Piece("noir", "dame")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    # Teste pion blanc s'il l'arriver contient une piece.
    damier_vide.cases.pop(Position(6, 0))
    damier_vide.cases[Position(6, 2)] = Piece("noir", "pion")
    damier_vide.cases[Position(5, 3)] = Piece("noir", "pion")
    assert not damier_vide.piece_peut_faire_une_prise(Position(0, 1))
    damier_vide.cases.pop(Position(6, 2))
    damier_vide.cases.pop(Position(7, 1))
    damier_vide.cases.pop(Position(5, 3))

    # Teste tous type de piece peut manger dans toutes les directions.
    damier_vide.cases[Position(3, 3)] = Piece("noir", "dame")
    damier_vide.cases[Position(2, 2)] = Piece("blanc", "dame")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 2))
    damier_vide.cases[Position(2, 4)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 4))
    damier_vide.cases[Position(4, 2)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 2))
    damier_vide.cases[Position(4, 4)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 4))

    damier_vide.cases[Position(3, 3)] = Piece("blanc", "dame")
    damier_vide.cases[Position(2, 2)] = Piece("noir", "dame")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 2))
    damier_vide.cases[Position(2, 4)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 4))
    damier_vide.cases[Position(4, 2)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 2))
    damier_vide.cases[Position(4, 4)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 4))

    damier_vide.cases[Position(3, 3)] = Piece("blanc", "pion")
    damier_vide.cases[Position(2, 2)] = Piece("noir", "dame")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 2))
    damier_vide.cases[Position(2, 4)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 4))
    damier_vide.cases[Position(4, 2)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 2))
    damier_vide.cases[Position(4, 4)] = Piece("noir", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 4))

    damier_vide.cases[Position(3, 3)] = Piece("noir", "pion")
    damier_vide.cases[Position(2, 2)] = Piece("blanc", "dame")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 2))
    damier_vide.cases[Position(2, 4)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(2, 4))
    damier_vide.cases[Position(4, 2)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 2))
    damier_vide.cases[Position(4, 4)] = Piece("blanc", "pion")
    assert damier_vide.piece_peut_faire_une_prise(Position(3, 3))
    damier_vide.cases.pop(Position(4, 4))
    damier_vide.cases.pop(Position(3, 3))

    # test piece_de_couleur_peut_se_deplacer.
    assert un_damier.piece_de_couleur_peut_se_deplacer("noir") is True
    assert un_damier.piece_de_couleur_peut_se_deplacer("blanc") is True
    damier_vide.cases[Position(2,0)] = Piece("noir", "pion")
    damier_vide.cases[Position(2, 2)] = Piece("noir", "pion")
    damier_vide.cases[Position(3, 1)] = Piece("blanc", "pion")
    assert damier_vide.piece_de_couleur_peut_se_deplacer("blanc") is False

    # Teste piece_de_couleur_peut_faire_une_prise.
    assert not un_damier.piece_de_couleur_peut_faire_une_prise("noir")
    assert not un_damier.piece_de_couleur_peut_faire_une_prise("blanc")
    damier_teste_kim.cases[Position(4, 1)] = Piece("noir", "pion")
    assert damier_teste_kim.piece_de_couleur_peut_faire_une_prise("blanc")
    assert not damier_teste_kim.piece_de_couleur_peut_faire_une_prise("noir")

    # tests deplacer().
    assert damier_teste_kim.deplacer(Position(5,0), Position(3,2)) == "prise"
    assert damier_teste_kim.deplacer(Position(2,5), Position(3,4)) == "ok"
    damier_vide.cases[Position(6,0)] = Piece("noir","pion")
    assert damier_vide.deplacer(Position(6,0), Position(7,1)) == "ok"
    assert damier_vide.cases[Position(7,1)].type_de_piece == "dame"
    assert damier_vide.deplacer(Position(1,3), Position(2,4)) == "erreur"
    assert damier_teste_kim.deplacer(Position(4,1), Position(3,1)) == "erreur"


    print("damier de base\n", un_damier)
    print("damier Kim\n", damier_teste_kim)
    print("damier Mathieu\n", damier_test)
    print("damier Vide\n", damier_vide)

    print('Test unitaires passés avec succès!')
