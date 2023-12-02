# Auteurs: À compléter

from tkinter import Tk, Label, NSEW
from tp3.Partie2.canvas_damier import CanvasDamier
from tp3.Partie1.partie import Partie
from tp3.Partie1.position import Position
#pour tester
from tp3.Partie1.piece import Piece


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        jouer (Partie) :


    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)
        self.position_cible = None


        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


    def piece_peut_etre_deplacer(self, position):


        if self.partie.damier.piece_peut_se_deplacer(position):
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Votre pièce peut se déplacer'




    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)

        if piece is None:
            if self.partie.position_source_selectionnee is not None:
                self.position_cible = position
                resultat_prise = self.partie.damier.deplacer(self.partie.position_source_selectionnee, self.position_cible)
                if resultat_prise == "ok":
                    self.canvas_damier.actualiser()
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Déplacement accepté'
                    self.partie.position_source_selectionnee = None
                    if self.partie.couleur_joueur_courant == "noir":
                        self.partie.couleur_joueur_courant = "blanc"
                    else:
                        self.partie.couleur_joueur_courant = "noir"
                elif resultat_prise == "prise":
                    self.canvas_damier.actualiser()
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Déplacement accepté'
                    self.partie.position_source_selectionnee = None
                    if self.partie.couleur_joueur_courant == "noir":
                        self.partie.couleur_joueur_courant = "blanc"
                    else:
                        self.partie.couleur_joueur_courant = "noir"
                else:
                    self.messages['foreground'] = "red"
                    self.messages['text'] = "Erreur. Déplacement impossible"
                    self.partie.position_source_selectionnee = None
            else:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
        elif piece.couleur != self.partie.couleur_joueur_courant:
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Erreur: pièce de l'adversaire."
            self.partie.position_source_selectionnee = None
        else:
            if self.partie.position_source_selectionnee is None:
                self.partie.position_source_selectionnee = position
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)
            else:
                self.position_cible = position


    def deplacement_invalide(self,position_cible):
        """ Méthode informant le joueur que son déplacement est invalide.

        :param position_source: (Position) : Position de la pièce de départ du joueur.
        :param position_cible: (Position) : Position ciblée par le joueur
        :return: (bool) : True si déplacement invalide. False si autrement.

        """
        if self.partie.position_cible_valide(position_cible)[0]:
            return (self.partie.damier.deplacer(self.partie.position_source_selectionnee, position_cible) == "ok" or
                    self.partie.damier.deplacer(self.partie.position_source_selectionnee, position_cible) == "prise")

        else:
            self.messages['foreground'] = "red"
            self.messages['text'] = self.partie.position_cible_valide(position_cible)[1]



