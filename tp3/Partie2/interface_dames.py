# Auteurs: Kim et Mathieu

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

        #position ciblée par le joueur
        self.position_cible = None

        #joueur courant
        self.joueur_courant = self.partie.couleur_joueur_courant

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        #message du premier joueur à jouer
        self.messages['foreground'] = 'green'
        self.messages['text'] = "tour du joueur {}.".format(self.joueur_courant)


        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def deplacement_piece(self, position_source, position_cible):

        if self.prise_obligatoire(self.joueur_courant):
            self.message_aux_joueurs('prise')
            if self.deplacement_invalide(position_cible):
                self.message_aux_joueurs('erreur')
            else:
                if self.partie.damier.deplacer(position_source,position_cible) == "prise":
                    self.message_aux_joueurs('ok')
                elif self.partie.damier.deplacer(position_source,position_cible) == 'erreur':
                    self.message_aux_joueurs('erreur')
        else:
            if self.deplacement_invalide(position_cible):
                self.message_aux_joueurs('erreur')
            else:
                if self.partie.damier.deplacer(position_source,position_cible) == "ok":
                    self.message_aux_joueurs('ok')
                elif self.partie.damier.deplacer(position_source,position_cible) == 'erreur':
                    self.message_aux_joueurs('erreur')
        self.canvas_damier.actualiser()
        if self.prise_obligatoire(self.joueur_courant):
            self.message_aux_joueurs('prise')



    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.
         Permet de stocker des positions pour effectuer des déplacements

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
                self.deplacement_piece(self.partie.position_source_selectionnee, self.position_cible)
                self.alterner_joueur(self.partie.position_source_selectionnee)
                #     self.deplacement_piece(self.partie.position_source_selectionnee, self.position_cible)
                #     self.quand_il_y_a_un_deplacement()
                #     resultat_prise = self.partie.damier.deplacer(self.partie.position_source_selectionnee, self.position_cible)
                #     if resultat_prise == "ok":
                #         self.quand_il_y_a_un_deplacement()
                #     else:
                #         self.messages['foreground'] = "red"
                #         self.messages['text'] = "Erreur. Déplacement impossible"
                #         self.partie.position_source_selectionnee = None
                # else:
                #     self.messages['foreground'] = 'red'
                #     self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'

            # else:  # Si le dplacement doit être une prise.
            #     if self.partie.position_source_selectionnee is not None:
            #         self.position_cible = position
            #         if self.partie.damier.piece_peut_faire_une_prise(self.partie.position_source_selectionnee):
            #             resultat_prise = self.partie.damier.deplacer(self.partie.position_source_selectionnee, self.position_cible)
            #             if resultat_prise == "prise":
            #                 self.canvas_damier.actualiser()
            #                 self.messages['foreground'] = 'black'
            #                 if self.partie.damier.piece_peut_faire_une_prise(self.position_cible):
            #                     self.messages['text'] = 'Vous devez faire une autre prise'
            #                     self.partie.position_source_selectionnee = self.position_cible
            #                 else:
            #                     self.messages['text'] = 'Déplacement accepté'
            #                     self.partie.position_source_selectionnee = None
            #                     self.changer_joueur_actif()
            #             else:
            #                 self.messages['foreground'] = 'red'
            #                 self.messages['text'] = 'Vous devez faire une prise'
            #         else:
            #             self.messages['foreground'] = 'red'
            #             self.messages['text'] = 'Vous devez faire une prise'
            #             self.partie.position_source_selectionnee = None

        elif piece.couleur != self.joueur_courant:
            self.message_aux_joueurs('joueur')
            self.nouvelle_piece_source()

        else:
            if self.prise_obligatoire(self.joueur_courant):
                self.message_aux_joueurs('prise')
            if self.partie.position_source_selectionnee is None:
                self.partie.position_source_selectionnee = position
                self.message_aux_joueurs('select')




    def deplacement_invalide(self,position_cible):
        """ Méthode informant le joueur que son déplacement est invalide.

        :param position_source: (Position) : Position de la pièce de départ du joueur.
        :param position_cible: (Position) : Position ciblée par le joueur
        :return: (bool) : True si déplacement invalide. False si autrement.

        """
        return not self.partie.position_cible_valide(position_cible)[0]


    def nouvelle_piece_source(self):

        self.partie.position_source_selectionnee = None

    def prise_multiple(self):
        self.position_cible = self.partie.position_source_forcee
        self.partie.position_source_selectionnee = self.partie.position_source_forcee

    def alterner_joueur(self, position_source):
        if self.partie.damier.piece_peut_faire_une_prise(position_source):
            self.prise_multiple()
            self.message_aux_joueurs('obligatoire')
        elif self.joueur_courant == "blanc":
            self.joueur_courant = "noir"
            self.message_aux_joueurs('joueur')
            self.nouvelle_piece_source()
        else:
            self.joueur_courant = "blanc"
            self.message_aux_joueurs('joueur')
            self.nouvelle_piece_source()
    def nouvelle_partie(self):
        pass

    def quitter(self):
        pass
    def message_aux_joueurs(self, chaine):
        if chaine == 'erreur':
            self.messages['foreground'] = "red"
            self.messages['text'] = "Erreur. Déplacement impossible"
        elif chaine == 'prise':
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'Vous devez faire une prise'
        elif chaine == 'ok':
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Déplacement accepté'
        elif chaine == 'vide':
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
        elif chaine == 'prises':
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Vous devez faire une autre prise'
        elif chaine == 'joueur':
            self.messages['foreground'] = 'green'
            self.messages['text'] = "tour du joueur {}.".format(self.joueur_courant)
        elif chaine == 'select':
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(self.partie.position_source_selectionnee)
        elif chaine == 'obligatoire':
            self.messages['foreground'] = 'black'
            self.messages['text'] = (
                "Posibilité d'une autre prise.  sélectionnée à la position {}.".format(self.partie.position_source_forcee))




    def afficher_couleur_joueur_courant(self):
        self.messages['foreground'] = 'green'
        self.messages['text'] = "tour du joueur {}.".format(self.joueur_courant)



    def prise_obligatoire(self,couleur):
        """
        Méthode permettant de voir si le joeur doit faire une prise pour aider avec la méthode "selectionner".
        :return: (bool) True si le joueur doit faire une prise, False sinon.
        """

        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(couleur):
            return True
        else:
            return False




