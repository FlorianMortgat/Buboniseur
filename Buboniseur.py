#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import Tkinter
import os
from Tkinter import W,E, N, S, NW, SW, NE, SE
from math import cos, sin, tan, pi, floor
import wave
import sys
import pickle
"""Un synthétiseur de waves illustrant la physique du son"""

"""Par Florian MORTGAT
Droits de reproduction concédés à tout utilisateur
droits de modification concéeés sauf en ce qui concerne
la présente licence et la sortie du programme, qui doit se
faire par la fonction sortie et doit contenir le message
"Par Florian MORTGAT,
je remercie vivement les Progboards (www.progboards.com)
pour leur aide et Gérard Swinnen pour son tutoriel."
Je ne suis pas responsable des dégats qu'une mauvaise
utilisation du programme, une défaillance du poste,
une modification ultérieure ou toute autre cause
indépendante de ma volontée pourrait causer.
Contact : buboniseur.10.bubonik@spamgourmet.com"""

#----- NOT FROM ORIGINAL RELEASE OF BUBONISEUR -----
'''
The original program used a non-free, hard-coded tune for its wav exports.
So here is another hard-coded tune, but that one is mine and free as this
program is.
'''

DEFAULT_TUNE=(
    ( 0,  1), #    la
    ( 3,  1), #    do
    ( 7,  1), #    mi
    (10,  2), #    sol
    (10,  1), #    sol
    (12,  2), #    la
    (15,  1), #    do
    (10,  2), #    sol
    ( 7,  1), #    mi
    ( 5,  1), #    re
    ( 7,  1), #    mi
    (10,  1), #    sol
    ( 2,  2), #    si,
    (-2,  1), #    sol
    ( 3,  2), #    do
    ( 2,  1), #    si
    ( 0,  6), #    la
)
#----- END NOT FROM ORIGINAL RELEASE -----

def test_fichier (adresse):
    """Teste si le fichier existe"""
    try:
        f = file(adresse,'r')
        f.close()
        return 1
    except:
        return 0

def demiton (dep, x):
    """Fonction de recherche de la fréquence d'une note :
    (les notes de la musique occidentale ont une fréquence basée sur une exponentielle de base 2**(1/12).
    arguments :
        dep : fréquence de départ
        x   : nombre de demi-tons à ajouter à la note de départ
    retourne :
        la fréquence de la note située x demi-tons au dessus de la fréquence de départ
    """
    return dep * 1.0594630943592953**x

sys.ps1 = ""
sys.ps2 = "->"

class Timbre:
    """La classe Timbre permet de créer des timbres d'instruments."""
    def __init__ (self, base=220, vol=3,
                  amp= ( 3,  3,    5),
                  det= ( 0,  6,   14),
                  bat=(( 3,  3,    3),
                       ( 5,  3,    1),
                       ( 1,  6,    0)),
                  dimin=(7,6),
                  nom="Par défaut"):
        """Initialise l'instrument en paramétrant le timbre.
        arguments :
            -base : fréquence de base pour le timbre à paramétrer
            -vol : volume général du timbre
            -amp : liste de l'amplitude de chaque harmonique du timbre
            -det : liste du demi-ton au dessus de la fréquence de base de chaque
                   harmonique
            -bat : trois listes permettant de créer les battements :
                   1°) celle de l'amplitude minimum de chaque harmonique
                   2°) celle de l'amplitude maximum relative de chaque harmonique
                   3°) celle de la fréquence du battement de chaque harmonique
                       (attention : cette fréquence doit être très faible, elle n'a
                       rien à voir avec la fréquence de l'harmonique ! Par exemple,
                       1 ou 2 sont des valeurs assez bonnes)."""
        self.amp=amp
        self.det=det
        self.bat=bat
        self.n_sons=len(self.amp)
        self.base=base
        self.vol=vol
        self.dimin=dimin
        self.last_chain=""
        if len(nom) < 30: self.nom=nom+" "*(30-len(nom))
        else: self.nom=nom[0:30]
    
    def chaine_son (self, det=0, longueur=15000):
        """Méthode de création d'une chaine de son"""
        ret = ""
        vol=self.vol/2.5
        for n0 in range (longueur):
            x=n0/1760.0
            part = 0
            for n in range (self.n_sons):
                #met l'amplitude et la fréquence
                part += ((vol*self.amp[n]*sin(demiton(self.base*self.det[n],det)*x))
                #met le battement
                * (self.bat[0][n]+0.1*self.bat[1][n]*sin(self.bat[2][n]*x)))              
            #diminue le volume
            part /= (self.dimin[0]+self.dimin[1]*x)
            part = int(part)
            #traduit en caractères
            ret+=chr((127+part)%256)
        self.last_chain = ret
        return ret

    def creer_melodie (self, tempo=2000, note=DEFAULT_TUNE
                       ):
        """Méthode de création d'une mélodie.
        arguments :
            tempo :
            note :
        retourne :
            une chaine de caractères correspondant au son wave créé."""
        ret = ""
        for i in note:
            ret += self.chaine_son (i[0],i[1]*tempo)
        return ret

    def ecrire_wave (self, adresse="wave0.wav", chaine="", frequence=11025):
        """Méthode de création d'un ficher wave mono non compressé à partir d'une chaine."""
        if chaine == "":
            chaine = self.last_chain
        try:
            e=wave.open(adresse, "w")
            e.setparams ((1, 1, frequence, 1, "NONE", "not compressed"))
            e.writeframes (chaine)
            e.close()
        except IOError:
            print '''Le fichier "'''+adresse+'''" n'a pas pu être écrit.'''
            return

    def sauver (self, adresse="Fichiers/Instruments/defaut.txt"):
        """Méthode d'enregistrement de l'instrument dans un fichier."""
        last_chain = self.last_chain
        self.last_chain = ""
        try:
            e=file(adresse, "w")
            pickle.dump (self, e)
            e.close()
        except IOError:
            print '''Le fichier "'''+adresse+'''" n'a pas pu être écrit.'''
            return
        self.last_chain = last_chain
    def charger (self, adresse="Fichiers/Instruments/defaut.txt"):
        try:
            l=file(adresse, "r")
            self = pickle.load (l)
            l.close()
            return self
        except IOError:
            print '''Le fichier "'''+adresse+'''" n'a pas pu être lu.'''
            return 0

class Reglage_timbre:
    """Interface de réglages de l'instrument"""
    def __init__ (self):
        """Initialise l'interface de configuration"""
        #Variables relatives au timbre
        self.t_dim_0 = 6    # dimin (0)
        self.t_dim_c = 1    # d_dimin/d_t
        self.t_ampl   = 11  # volume du son
        self.t_freq   = 220 # fréquence de base
        self.t_nom     = "Orgue1"
        self.t_harmonique = []
        self.filename=self.t_nom + ".txt"
        #Variables relatives aux couleurs et variables temporaires
        self.labeltemp=()
        
        #Fenêtre principale
        self.fen = Tkinter.Tk()
        self.fen.title ("Le Buboniseur>> Configuration de l'instrument")
        #Menus :
        self.barre_menus=Tkinter.Frame(self.fen, bg="#AABBAA")
        self.barre_menus.grid(row=0,column=0,sticky=NW,columnspan=5)
        #Menus : définition des conteneurs (menu_fichier, menu_options)
        #Menus : fichier
        self.menu_fichier=Tkinter.Menubutton(self.barre_menus, text="Fichier",bg="#AABBAA")
        self.menu_fichier.grid(row=0, column=0, sticky=W)
        #Menus : options
        self.menu_options=Tkinter.Menubutton(self.barre_menus, text="Options",bg="#AABBAA")
        self.menu_options.grid(row=0, column=1, sticky=W)
        #Menus : aide
        self.menu_aide   =Tkinter.Menubutton(self.barre_menus, text="Aide",bg="#AABBAA")
        self.menu_aide.grid   (row=0, column=2, sticky=E, padx=10)
        #Menus : définition des contenus des menus
        #Menus : fichier
        self.m_fichier=Tkinter.Menu (self.menu_fichier)
        self.m_fichier.add_command(label="Quitter",             command=self.sortir)
        self.m_fichier.add_command(label="Ouvrir...",           command=self.charger)
        self.m_fichier.add_command(label="Sauvegarder sous...", command=self.sauver_sous)
        self.m_fichier.add_command(label="Sauvegarder",         command=self.sauver)
        #Menus : options
        self.m_options=Tkinter.Menu (self.menu_options)
        self.m_options.add_command(label="Configurer",          command=self.sortir)
        self.m_options.add_command(label="Synthétiser",         command=self.synthetiser)
        #Menus : aide
        self.m_aide   =Tkinter.Menu (self.menu_aide)
        self.m_aide.add_command    (label="La physique du son", command=aide_physique)
        self.m_aide.add_command    (label="Le buboniseur",      command=aide_logiciel)
        #Menus : liaison des menus entre eux
        self.menu_fichier.configure(menu=self.m_fichier)
        self.menu_options.configure(menu=self.m_options)
        self.menu_aide.configure   (menu=self.m_aide)

        #Entrées
        self.boutons=Tkinter.Frame(self.fen,height=30)
        self.boutons.grid(row=7,columnspan=8)
        self.e_t_nom   = Tkinter.Entry(self.boutons, width=30)
        self.e_t_ampl  = Tkinter.Entry(self.boutons, width=4)
        self.e_t_freq  = Tkinter.Entry(self.boutons, width=4)
        self.e_t_dim_0 = Tkinter.Entry(self.boutons, width=3)
        self.e_t_dim_c = Tkinter.Entry(self.boutons, width=3)
        #Entrées : Légendes
        Tkinter.Label(self.boutons,text=" Nom de l'instrument=").grid (row=0,column=0)
        Tkinter.Label(self.boutons,text=" Volume=").grid              (row=0,column=2)
        Tkinter.Label(self.boutons,text=" Fréquence de base=").grid   (row=1,column=2)
        Tkinter.Label(self.boutons,text=" Affaiblissement en 0=").grid(row=0,column=4)
        Tkinter.Label(self.boutons,text=" Affaiblissement=").grid     (row=1,column=4)
        #Entrées : emplacement
        self.e_t_nom.grid  (row=0,column=1)
        self.e_t_ampl.grid (row=0,column=3)
        self.e_t_freq.grid (row=1,column=3)
        self.e_t_dim_0.grid(row=0,column=5)
        self.e_t_dim_c.grid(row=1,column=5)
        #Entrées : valeurs par défaut
        self.e_t_nom.insert  (0,self.t_nom)
        self.e_t_ampl.insert (0,self.t_ampl)
        self.e_t_freq.insert (0,self.t_freq)
        self.e_t_dim_0.insert(0,self.t_dim_0)
        self.e_t_dim_c.insert(0,self.t_dim_c)
        #Entrées : commande liée
        self.e_t_nom.bind   ('<Return>', self.tracer_courbe)
        self.e_t_ampl.bind  ('<Return>', self.tracer_courbe)
        self.e_t_freq.bind  ('<Return>', self.tracer_courbe)
        self.e_t_dim_0.bind ('<Return>', self.tracer_courbe)
        self.e_t_dim_c.bind ('<Return>', self.tracer_courbe)
        
        #Légendes des lignes de réglage des harmoniques
        Tkinter.Frame(width=1000,height=30,bg="#A0A0A0").grid     (row=1,column=0,columnspan=8)
        Tkinter.Label(self.fen,text="Harmoniques :").grid         (row=1,column=0)
        Tkinter.Label(self.fen,text="Amplitude du son").grid      (row=2,column=0)
        Tkinter.Label(self.fen,text="Fréquence du son").grid      (row=3,column=0)
        Tkinter.Label(self.fen,text="Amplitude minimum").grid     (row=4,column=0)
        Tkinter.Label(self.fen,text="Amplitude de battement").grid(row=5,column=0)
        Tkinter.Label(self.fen,text="Fréquence de battement").grid(row=6,column=0)
        #Canevas (pour tracer la courbe)
        self.zone=Tkinter.Canvas(self.fen,width=1000,height=400,bg="#AFA0B9")

        self.info = Tkinter.Label (self.fen, text="Bienvenue dans Le Buboniseur !")
        self.info.grid (row=9, columnspan=2)

        #Boutons de réglage des harmoniques
        for i in range(5):
            self.t_harmonique.append(self.Harmonique(self.fen,self,i+1))
        self.update ()
        self.fen.mainloop()

    class Harmonique:
        """Interface de réglage d'une harmonique"""
        def __init__ (self, maitre,ref_maitre, num=0, ligne=1, texte="Harmonique ",
                      ampl=0,mini=0,freq=0,b_freq=0,b_ampl=0):
            """Initialise l'interface"""
            #variables de l'harmonique
            if ampl!=None:   self.h_ampl=11-num
            else:            self.h_ampl=ampl
            if freq!=None:   self.h_freq=num*2
            else:            self.h_freq=freq
            if mini!=None:    self.h_mini=1
            else:            self.h_mini=mini
            if b_ampl!=None:  self.b_ampl=5
            else:            self.b_ampl=b_ampl
            if b_freq!=None: self.b_freq=0
            else:            self.b_freq=b_freq
            #variables de l'interface
            self.num=num
            self.maitre=maitre
            self.r_maitre=ref_maitre
            # échelles
            Tkinter.Label(self.maitre, text=texte+str(self.num)).grid(column=num,row=ligne)
            self.e_h_ampl=Tkinter.Scale(self.maitre,
                                        length=150,
                                        orient=Tkinter.VERTICAL,
                                        troughcolor ='#000000',
                                        sliderlength =30,
                                        showvalue =3,
                                        from_=20,
                                        to=-20,
                                        fg="#FF0000",
                                        command=self.update)
            self.e_h_freq=Tkinter.Scale(self.maitre,
                                        length=125,
                                        orient=Tkinter.HORIZONTAL,
                                        troughcolor ='#001020',
                                        sliderlength =30,
                                        showvalue =3,
                                        from_=1,
                                        to=20,
                                        fg="#FF0000",
                                        command=self.update)
            self.e_h_mini=Tkinter.Scale(self.maitre,
                                        length=125,
                                        orient=Tkinter.HORIZONTAL,
                                        troughcolor ='#002040',
                                        sliderlength =30,
                                        showvalue =3,
                                        from_=0,
                                        to=5,
                                        fg="#FF0000",
                                        command=self.update)
            self.e_b_ampl=Tkinter.Scale(self.maitre,
                                        length=125,
                                        orient=Tkinter.HORIZONTAL,
                                        troughcolor ='#003060',
                                        sliderlength =30,
                                        showvalue =3,
                                        from_=0,
                                        to=10,
                                        fg="#0000FF",
                                        command=self.update)
            self.e_b_freq=Tkinter.Scale(self.maitre,
                                        length=125,
                                        orient=Tkinter.HORIZONTAL,
                                        troughcolor ='#004080',
                                        sliderlength =30,
                                        showvalue =3,
                                        from_=0,
                                        to=15,
                                        fg="#0000FF",
                                        command=self.update)
            #disposition des échelles
            self.e_h_ampl.grid (row=ligne+1,column=num)
            self.e_h_freq.grid (row=ligne+2,column=num)
            self.e_h_mini.grid (row=ligne+3,column=num)
            self.e_b_ampl.grid (row=ligne+4,column=num)
            self.e_b_freq.grid (row=ligne+5,column=num)
            #valeurs initiales
            self.e_h_ampl.set (self.h_ampl)
            self.e_h_freq.set (self.h_freq)
            self.e_h_mini.set (self.h_mini)
            self.e_b_ampl.set (self.b_ampl)
            self.e_b_freq.set (self.b_freq)

        def update (self,event=None):
            self.h_ampl = self.e_h_ampl.get()
            self.h_freq = self.e_h_freq.get()
            self.h_mini = self.e_h_mini.get()
            self.b_ampl = self.e_b_ampl.get()
            self.b_freq = self.e_b_freq.get()
            self.r_maitre.tracer_courbe()

        def get (self,num=0):
            if num==0: return self.h_ampl
            if num==1: return self.h_freq
            if num==2: return self.h_mini
            if num==3: return self.b_ampl
            if num==4: return self.b_freq


    def sortir (self, message = None):
        """Quitte le programme (plus tard, fermera seulement la fenêtre)"""
        self.fen.destroy ()
        fen=Tkinter.Tk()
        fen.title ("Le Buboniseur>> Fin du programme")
        Tkinter.Button (fen, text="""Par Florian MORTGAT,
je remercie vivement les Progboards (www.progboards.com)
pour leur aide et Gérard Swinnen pour son tutoriel.""",
                         bg = "#22AACC",
                         fg="#AA0000",
                         command=fen.destroy).grid (row=0,column=0)
        Tkinter.Button (fen, text="Au revoir !",
                        bg = "#000031", fg="#11AABB",
                        command=fen.destroy).grid (row=1, column=0)
        fen.mainloop()
        sys.exit()

    def sauver (self, adresse = os.getcwd()):
        """Sauvegarde l'instrument en cours à l'adresse donnée."""
        def ecraser (event=None):
            diminution=(self.t_dim_0, self.t_dim_c)
            amplitude=[]
            frequence=[]
            battement=[[],[],[]]
            #Récupération des paramètres
            for i in self.t_harmonique:
                amplitude.append(i.h_ampl)
                frequence.append(i.h_freq)
                battement[0].append(i.h_mini)
                battement[1].append(i.b_ampl)
                battement[2].append(i.b_freq)
            #Création de l'objet Timbre
            self.timbre=Timbre(base=self.t_freq, vol=self.t_ampl,
                  amp=amplitude,
                  det=frequence,
                  bat=battement,
                  dimin=diminution,
                  nom=self.t_nom)
            self.timbre.sauver (adresse)
            self.info.configure(text="Le fichier a bien été enregistré.", fg="#0000FF")
            fen.destroy()
            return

        fen=Tkinter.Tk()
        adresse += "/"+self.filename
        if test_fichier(adresse):
            Tkinter.Label(fen,text="Le fichier").grid        (row=0,column=0,columnspan=2)
            Tkinter.Label(fen,text=adresse,fg="#FF0000").grid(row=1,column=0,columnspan=2)
            Tkinter.Label(fen,text="existe déjà").grid       (row=2,column=0,columnspan=2)
            Tkinter.Button(fen,
                           text="Ecraser le fichier",
                           command=ecraser,
                           width=30, height=3).grid(row=3,column=0)
            Tkinter.Button(fen,
                           text="Annuler",
                           command=fen.destroy,
                           width=30, height=3).grid(row=3,column=1)
        else:
            Tkinter.Label(fen,text="Le fichier").grid        (row=0,column=0,columnspan=2)
            Tkinter.Label(fen,text=adresse,fg="#0000FF").grid(row=1,column=0,columnspan=2)
            Tkinter.Label(fen,text="va être écrit").grid     (row=2,column=0,columnspan=2)
            Tkinter.Button(fen,
                           text="Enregistrer",
                           command=ecraser,
                           width=30, height=3).grid(row=3,column=0)
            Tkinter.Button(fen,
                           text="Annuler",
                           command=fen.destroy,
                           width=30, height=3).grid(row=3,column=1)
        fen.mainloop()

    def sauver_sous (self, event=None):
        """Demande à l'utilisateur où il veut sauver son truc"""
        self.interface_fichiers ("Enregistrer sous...", "Enregistrer", self.sauver)

    def charger (self):
        """Charge un instrument préalablement enregistré."""
        def charger (adresse=None):
            adresse=os.getcwd()+"/"+self.filename
            self.timbre=Timbre()
            if not test_fichier(adresse):
                self.info.configure(text="Le fichier\n"+adresse+"\nn'a pas pu être chargé.", fg="#FF0000")
                return
            else:
                self.timbre = self.timbre.charger(os.getcwd()+"/"+self.filename)
                self.info.configure(text="Le fichier a été chargé.", fg="#0000FF")
                #Variables relatives au timbre
                self.t_dim_0 = self.timbre.dimin[0]
                self.t_dim_c = self.timbre.dimin[1]
                self.t_ampl  = self.timbre.vol
                self.t_freq  = self.timbre.base
                self.t_nom   = self.timbre.nom
                self.filename=self.t_nom + ".txt"
                for i in range(5):
                    self.t_harmonique[i].e_h_ampl.set(self.timbre.amp[i])
                    self.t_harmonique[i].e_h_freq.set(self.timbre.det[i])
                    self.t_harmonique[i].e_h_mini.set(self.timbre.bat[0][i])
                    self.t_harmonique[i].e_b_ampl.set(self.timbre.bat[1][i])
                    self.t_harmonique[i].e_b_freq.set(self.timbre.bat[2][i])
                    print self.timbre.bat
                self.tracer_courbe()
                return
        self.interface_fichiers ("Charger un timbre", "Charger", charger)
        return
    
    def interface_fichiers (self, titre="Enregistrer sous...",
                            bouton="Enregistrer", commande=None):
        """Interface de navigation de fichiers"""
        def aff_liste (event=None):
            """Affiche"""
            Tkinter.Label (liste, text="Fichiers du répertoire :", bg="#22FFFF").grid(row=0)
            texte=""
            for i in os.listdir(chemin.get()):
                texte+=i+"\n"
            reps.grid(row=1,column=0, sticky=W)
            reps.configure (text=texte)
            return
        def update (event=None):
            self.filename=fichier.get()
            fen.after (300, update)
            return
        fen=Tkinter.Tk()
        fen.title ("Le Buboniseur>> "+titre)
        liste=Tkinter.Frame (fen, width=200, bg="#000000")
        liste.grid(row=0,column=2,rowspan=3)
        liste_etiquette=Tkinter.Label (liste, text="Fichiers du répertoire :", bg="#22FFFF")
        liste_etiquette.grid (row=0)
        reps=Tkinter.Label(liste)
        #légendes et bouton
        Tkinter.Label (fen,text="Répertoire : ").grid(row=0,column=0,sticky=W)
        Tkinter.Label (fen,text="Fichier : ").grid   (row=1,column=0,sticky=W)
        Tkinter.Button(fen,text=bouton, command=commande).grid(row=3,columnspan=3)
        #champs de saisie
        chemin  = Tkinter.Entry (fen, width=80)
        fichier = Tkinter.Entry (fen, width=30)
        chemin.insert (0,os.getcwd())
        fichier.insert(0,self.t_nom+".txt")
        chemin.grid  (row=0,column=1,sticky=W)
        fichier.grid (row=1,column=1,sticky=W)
        chemin.bind("<Return>", aff_liste)
        fichier.bind("<Return>", commande)
        aff_liste()
        update()
        fen.mainloop()
        
        
    def configurer (self, event=None):
        """Configure les couleurs du programme"""
        pass

    def synthetiser (self, event=None):
        diminution=(self.t_dim_0, self.t_dim_c)
        amplitude=[]
        frequence=[]
        battement=[[],[],[]]
        #Récupération des paramètres
        for i in self.t_harmonique:
            amplitude.append(i.h_ampl)
            frequence.append(i.h_freq)
            battement[0].append(i.h_mini)
            battement[1].append(i.b_ampl)
            battement[2].append(i.b_freq)
        #Création de l'objet Timbre
        self.timbre=Timbre(base=self.t_freq, vol=self.t_ampl,
              amp=amplitude,
              det=frequence,
              bat=battement,
              dimin=diminution,
              nom=self.t_nom)
        a=self.e_t_nom.get()
        self.timbre.ecrire_wave(os.getcwd()+"/"+a+".wav", self.timbre.creer_melodie())
        n=len(a)
        self.e_t_nom.delete(0,n)
        if ord(a[len(a)-1])>=48 and ord(a[len(a)-1])<=57:
            index=int(a[len(a)-1])
            a=a[0:len(a)-1]+str(index+1)
        else:
            a+="0"
        self.e_t_nom.insert(0,a)

    def tracer_courbe (self, precision=1):
        """Trace une courbe"""
        self.zone.grid(row=8,column=0,columnspan=6)
        self.axe=(self.zone.create_line(10, 200, 1000, 200,
                         width=1, fill="#000000", arrow=Tkinter.LAST),
                  self.zone.create_line(10, 10,  10,   400,
                         width=1, fill="#000000", arrow=Tkinter.FIRST)
                  )
        courbe=[]
        x=0.0
        self.t_ampl =eval(self.e_t_ampl.get ())
        self.t_freq =eval(self.e_t_freq.get ())
        self.t_dim_0=eval(self.e_t_dim_0.get())
        self.t_dim_c=eval(self.e_t_dim_c.get())

        while x < 990:
            n=0
            for i in self.t_harmonique:
                n=(n+i.h_ampl * sin ((i.h_freq*self.t_freq)*x/2200)*
                   (i.h_mini+i.b_ampl*sin(x*i.b_freq/1000)))
            courbe.append((x, 200-int(n*self.t_ampl/(self.t_dim_0+self.t_dim_c*(x/60)))))
            x+=1.1

        if "courbe" in self.__dict__: self.zone.delete(self.courbe)
        self.courbe=self.zone.create_line (courbe, fill="#FF0000", smooth=1)
        return

    def update (self, event=None):
        self.t_nom=self.e_t_nom.get()
        self.info.grid (row=9, columnspan=2)
        self.t_nom=self.e_t_nom.get()
        self.fen.after (500, self.update)
        return

def aide (rubrique="Logiciel"):
    fen=Tkinter.Tk()
    fen.title("Le Buboniseur>> Aide à la configuration de l'instrument")
    Tkinter.Label(fen, text="Le Buboniseur :", bg = "#000000",fg="#555555").grid(row=0,column=0)
    Tkinter.Label(fen, text="""Le buboniseur est un logiciel libre que j'ai écrit
pour apprendre à utiliser Tkinter et parce-que je m'intéresse à la
synthèse de son.

1-Réglages :
  Vous pouvez régler les paramètres de l'instrument en
  faisant glisser les curseurs sur les échelles
  correspondantes. Un graphe correspondant à votre
  timbre s'affiche en bas de la fenêtre.

2-Enregistrement :
  Pour enregistrer votre instrument dans le fichier par
  défaut ou dans le dernier fichier d'enregistrement,
      -Menu "Fichier->Sauvegarder"
  Pour enregistrer dans un autre fichier,
      -Menu "Fichier->Sauvegarder sous..."
      Une fenêtre s'affiche alors avec deux champs de
      saisie. Dans le premier, entrez l'adresse du
      répertoire d'enregistrement.
      Si vous appuyez sur "Entrée" pendant que vous
      saisissez l'adresse, les fichiers et dossiers
      du répertoire courant s'afficheront dans la liste
      à droite.
      Le second champ de saisie est destiné au nom
      du fichier d'enregistrement. Si vous appuyez sur
      Entrée lorsque le curseur de saisie est activé,
      votre instrument est enregistré.

3-Chargement :
  Pour charger un fichier,
      -Menu "Fichier->Charger"
      Une fenêtre similaire à la fenêtre d'enregistrement
      s'affiche. Naviguez de la même manière pour trouver
      le bon répertoire et tapez dans le second champ
      le nom du fichier.""").grid(row=1,column=0)
    fen.mainloop()
    fen.destroy()


def aide_logiciel(event=None):
    aide ("Logiciel")
def aide_physique(event=None):
    aide ("Physique")

if __name__ == "__main__": Reglage_timbre()


