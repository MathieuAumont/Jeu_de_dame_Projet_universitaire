# Auteurs: Kim et Mathieu

from tkinter import Tk, Label, NSEW, Button, Canvas
from tp3.Partie2.canvas_damier import CanvasDamier
from tp3.Partie1.partie import Partie
from tp3.Partie1.position import Position


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        position_forcee (Position) : Position obligatoire si le joueur peut effectuer plusieurs prises
        position_cible (Position) : Position de déplacement choisi
        joueur_courant (Partie) : Couleur du joueur actif
        message_couleur (Label) : un "widget" affichant la couleur du joueur actif
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        bouton_partie (Button) : un "widget" bouton qui permet de recommencer une partie
        bouton_quitter (Button) : un "widget" bouton qui permet de quitter la partie (autrement que par le X)

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

        # La piece forcée lorsque cette pièce la possibilité de faire une prise après qu'elle aille fait une prise.
        # Créer par Kim et Mathieu
        self.position_forcee = None

        # position ciblée par le joueur
        self.position_cible = None

        # joueur courant
        self.joueur_courant = self.partie.couleur_joueur_courant

        # message du premier joueur à jouer
        self.messages_couleur = Label(self)
        self.messages_couleur.grid()
        self.messages_couleur['foreground'] = 'green'
        self.messages_couleur['text'] = "tour du joueur {}.".format(self.joueur_courant)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Button nouvelle partie
        self.bouton_partie = Button(self, text='Nouvelle Partie', command=self.nouvelle_partie)
        self.bouton_partie.grid()

        # Button quitter
        self.bouton_quitter = Button(self, text='Quitter', command=self.quitter)
        self.bouton_quitter.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

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

        if piece is None:  # Si la position ne contient pas de pièce.
            if self.partie.position_source_selectionnee is not None:  # S'il y a une pièce à la position source
                # sélectionné, alors "piece" est en fait la position cible.
                self.position_cible = position
                self.deplacement_piece(self.partie.position_source_selectionnee, self.position_cible)
            else:  # S'il n'y a pas de pièce à la position source, alors c'est que "piece" était supposée être
                # la pièce à la position source, donc il y a une erreur.
                self.message_aux_joueurs("vide")
                self.canvas_damier.actualiser()

        elif piece.couleur != self.joueur_courant:  # Lorsque la pièce n'appartient pas au joueur.
            if self.position_forcee is not None: # cas de position forcée
                self.message_aux_joueurs('erreur') # message d'erreur de déplacement.
            elif self.partie.position_source_selectionnee is None: # Message de pièce de l'adversaire
                self.message_aux_joueurs('mauvaise piece')
                self.canvas_damier.actualiser()
                self.nouvelle_piece_source()
            else: # Si position_source est déjà sélectionné et qu'elle n'est pas forcée.
                self.message_aux_joueurs("erreur") # erreur de déplacement.
        else:  # Lorsque la pièce lui appartient.
            if self.prise_obligatoire_couleur(self.joueur_courant):
                self.message_aux_joueurs('prise')
            if self.partie.position_source_selectionnee is None:
                self.couleur_selection(position)
                self.partie.position_source_selectionnee = position
                self.message_aux_joueurs('select')
                self.couleur_deplacement_possible(position)
            else:
                self.canvas_damier.actualiser()
                self.couleur_selection(position)
                self.partie.position_source_selectionnee = position
                self.message_aux_joueurs('select')
                self.couleur_deplacement_possible(position)

    def deplacement_piece(self, position_source, position_cible):
        """
        Méthode qui s'occupe de déplacer les pieces dans le canvas.
        :param position_source: (Position) la position de la piece à déplacer
        :param position_cible: (Position) l'arriver voulu de la piece sélectionnee

        """

        if self.prise_obligatoire_couleur(self.joueur_courant):  # Si le joueur courant doit faire une prise.
            if self.position_forcee is not None:  # Si le joueur à une position forcée.
                if self.deplacement_invalide(position_cible):  # Si le déplacement est invalide.
                    self.message_aux_joueurs('erreur')
                if self.partie.damier.piece_peut_sauter_vers(position_source, position_cible):
                    self.partie.damier.deplacer(position_source, position_cible)
                    self.canvas_damier.actualiser()
                    self.alterner_joueur(position_cible)
            else:  # Lorsque le joueur n'a pas de position forcée.
                if self.partie.damier.piece_peut_sauter_vers(position_source, position_cible):
                    self.partie.damier.deplacer(position_source, position_cible)
                    self.canvas_damier.actualiser()
                    self.alterner_joueur(position_cible)
                else:
                    self.message_aux_joueurs('erreur')
                    self.canvas_damier.actualiser()
                    self.nouvelle_piece_source()
        else:  # Si le joueur ne peut pas faire de prise.
            if self.deplacement_invalide(position_cible):
                self.message_aux_joueurs('erreur')
                self.canvas_damier.actualiser()
                self.nouvelle_piece_source()
            elif self.position_forcee is not None:
                self.message_aux_joueurs("prise avec autre piece")
            else:
                if self.partie.damier.piece_peut_se_deplacer_vers(position_source, position_cible):
                    self.partie.damier.deplacer(position_source, position_cible)
                    self.canvas_damier.actualiser()
                    self.alterner_joueur(position_source)
                else:
                    self.message_aux_joueurs('erreur')
                    self.canvas_damier.actualiser()
                    self.nouvelle_piece_source()
        self.victoire()

    def deplacement_invalide(self, position_cible):
        """ Méthode informant le joueur que son déplacement est invalide.

        :param position_source: (Position) : Position de la pièce de départ du joueur.
        :param position_cible: (Position) : Position ciblée par le joueur
        :return: (bool) : True si déplacement invalide. False si autrement.

        """
        return not self.partie.position_cible_valide(position_cible)[0]

    def nouvelle_piece_source(self):
        """
        Méthode donnant la possibilité de choisir une nouvelle piece source.

        """
        self.partie.position_source_selectionnee = None

    def prise_obligatoire_couleur(self, couleur):
        """
        Méthode permettant de voir si le joueur doit faire une prise pour aider avec la méthode "selectionner".
        :return: (bool) True si le joueur doit faire une prise, False sinon.
        """

        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(couleur):
            return True
        else:
            return False

    def prise_multiple(self):
        """
        en cas de prise multiple, cette méthode force le joueur courant à prendre la position forcée.

        """
        self.position_forcee = self.position_cible
        self.partie.position_source_selectionnee = self.position_forcee

    def alterner_joueur(self, position_cible):
        """
        Méthode qui change le joueur actif en s'assurant de ne pas le changer lorsqu'une piece qui c'est déjà déplacer
        peut faire une autre prise
        :param position_cible: (Position) la position finale du précédent déplacement.

        """
        if self.partie.damier.piece_peut_faire_une_prise(position_cible):
            self.prise_multiple()
            self.message_aux_joueurs('obligatoire')
            self.couleur_selection(position_cible)
            self.couleur_deplacement_possible(position_cible)

        elif self.joueur_courant == "blanc":
            self.joueur_courant = "noir"
            self.afficher_couleur_joueur_courant()
            self.message_aux_joueurs("ok")
            self.nouvelle_piece_source()
            self.position_forcee = None

        else:
            self.joueur_courant = "blanc"
            self.afficher_couleur_joueur_courant()
            self.message_aux_joueurs("ok")
            self.nouvelle_piece_source()
            self.position_forcee = None

    def nouvelle_partie(self):
        """
        Méthode permettant de débuter une nouvelle partie en détruisant l'ancienne.

        """

        self.destroy()
        FenetrePartie()

    def quitter(self):
        """
        Méthode permetant de quitter la partie.

        """
        quit()

    def message_aux_joueurs(self, chaine):
        """
        Méthode qui crée les étiquettes pour aider le joueur à savoir ce qui ce passe lors d'une partie (sauf les
        étiquettes indiquant quel joueur est actif, c'est la méthode "aficher joueur courant" qui s'en occupe).

        Pour savoir dans quelle situation l'étiquette sera appelé, vous n'avez qu'à regarder le message
        envoyé au joueur.
        :param chaine: (str) la chaine indiquant ce qui se produit lors d'une partie

        """
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

        elif chaine == "mauvaise piece":
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Cette pièce ne vous appartient pas."

        elif chaine == 'select':
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(
                self.partie.position_source_selectionnee)

        elif chaine == 'obligatoire':
            self.messages['foreground'] = 'black'
            self.messages['text'] = (
                "Posibilité d'une autre prise à partir de la pièce à la position {}."
                "\nSélectionnement une case de déplacement.".format(self.position_forcee))

    def afficher_couleur_joueur_courant(self):
        """
        Méthode qui affiche une étiquette indiquant qui est le joueur courant et s'il a l'obligation de faire une prise.

        """
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.joueur_courant):
            self.messages_couleur['foreground'] = 'green'
            self.messages_couleur['text'] = "tour du joueur {}. \nDOIT FAIRE UNE PRISE".format(self.joueur_courant)
        else:
            self.messages_couleur['foreground'] = 'green'
            self.messages_couleur['text'] = "tour du joueur {}.".format(self.joueur_courant)

    def victoire(self):
        """
        Méthode déterminant s'il y a une victoire. Si oui, une nouvelle fenêtre s'ouvre affichant le gagnant

        """

        police_de_caractere = ('Deja Vu', 30)
        joueur_noir = 0
        joueur_blanc = 0
        for piece in self.partie.damier.cases.values():
            if piece.couleur == "noir":
                joueur_noir += 1
            else:
                joueur_blanc += 1
        if joueur_noir == 0:
            icone = "\u26C0"
            fenetre_victoire = Tk()
            victorieux = Label(fenetre_victoire, text='Victoire du joueur BLANC !')
            victorieux.grid(padx=30, pady=10)
            canvas = Label(fenetre_victoire, text=icone, font=police_de_caractere)
            canvas.grid()
            self.bouton_partie = Button(fenetre_victoire, text='Nouvelle Partie', command=self.nouvelle_partie)
            self.bouton_partie.grid()
            fenetre_victoire.mainloop()
        if joueur_blanc == 0:
            icone = "\u26C2"
            fenetre_victoire = Tk()
            victorieux = Label(fenetre_victoire, text='Victoire du joueur NOIR !')
            victorieux.grid(padx=30, pady=10)
            canvas = Label(fenetre_victoire, text=icone, font=police_de_caractere)
            canvas.grid()
            self.bouton_partie = Button(fenetre_victoire, text='Nouvelle Partie', command=self.nouvelle_partie)
            self.bouton_partie.grid()
            fenetre_victoire.mainloop()
        return False

    def couleur_selection(self, position_source):
        """
        Méthode qui met la case choisie du joueur courant en vert.
        :param position_source: (Position) Position choisie par le joueur

        """
        self.canvas_damier.create_rectangle(position_source.colonne * self.canvas_damier.n_pixels_par_case,
                                            position_source.ligne * self.canvas_damier.n_pixels_par_case,
                                            position_source.colonne * self.canvas_damier.n_pixels_par_case +
                                            self.canvas_damier.n_pixels_par_case,
                                            position_source.ligne * self.canvas_damier.n_pixels_par_case +
                                            self.canvas_damier.n_pixels_par_case, fill="green")

        self.canvas_damier.delete("piece")
        self.canvas_damier.dessiner_pieces()

    def couleur_deplacement_possible(self, position_source):
        """
        Méthode montrant toutes les posibilités de déplacement au joueur courant.
        :param position_source: (Position) Position précédemment choisie par le joueur courant.

        """

        if self.prise_obligatoire_couleur(self.joueur_courant):
            for position in self.partie.position_source_selectionnee.quatre_positions_sauts():
                if self.partie.damier.piece_peut_sauter_vers(position_source, position):
                    self.canvas_damier.create_rectangle(position.colonne * self.canvas_damier.n_pixels_par_case,
                                                        position.ligne * self.canvas_damier.n_pixels_par_case,
                                                        position.colonne * self.canvas_damier.n_pixels_par_case +
                                                        self.canvas_damier.n_pixels_par_case,
                                                        position.ligne * self.canvas_damier.n_pixels_par_case +
                                                        self.canvas_damier.n_pixels_par_case, fill="orange")
                    self.canvas_damier.delete("piece")
                    self.canvas_damier.dessiner_pieces()
        else:
            if self.joueur_courant == "blanc":
                for position in self.partie.position_source_selectionnee.positions_diagonales_haut():
                    if self.partie.damier.piece_peut_se_deplacer_vers(position_source, position):
                        self.canvas_damier.create_rectangle(position.colonne * self.canvas_damier.n_pixels_par_case,
                                                            position.ligne * self.canvas_damier.n_pixels_par_case,
                                                            position.colonne * self.canvas_damier.n_pixels_par_case +
                                                            self.canvas_damier.n_pixels_par_case,
                                                            position.ligne * self.canvas_damier.n_pixels_par_case +
                                                            self.canvas_damier.n_pixels_par_case, fill="orange")
                        self.canvas_damier.delete("piece")
                        self.canvas_damier.dessiner_pieces()
            else:
                for position in self.partie.position_source_selectionnee.positions_diagonales_bas():
                    if self.partie.damier.piece_peut_se_deplacer_vers(position_source, position):
                        self.canvas_damier.create_rectangle(position.colonne * self.canvas_damier.n_pixels_par_case,
                                                            position.ligne * self.canvas_damier.n_pixels_par_case,
                                                            position.colonne * self.canvas_damier.n_pixels_par_case +
                                                            self.canvas_damier.n_pixels_par_case,
                                                            position.ligne * self.canvas_damier.n_pixels_par_case +
                                                            self.canvas_damier.n_pixels_par_case, fill="orange")
                        self.canvas_damier.delete("piece")
                        self.canvas_damier.dessiner_pieces()
