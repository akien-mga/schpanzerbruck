# encoding=UTF-8

from PySFML import sf
import mapmng, gui, img, utils, constantes


class ContexteClient:
    """La classe supervisant un combat (côté client), c'est le GroupeClient qui opère dessus.
    Il s'occupe des phases de rendu à l'écran et de gestion des événements souris/clavier"""
    
    def __init__(self, app, fichierMap, perspective = constantes.defaut.PERSPECTIVE, touches = constantes.defaut.touches):
        self.app = app
        self.L, self.H = self.app.GetWidth(), self.app.GetHeight()
        self.input = app.GetInput()
        self.gestImages = img.GestionnaireImages()
        self.map = mapmng.Map(fichierMap, self.gestImages, perspective)
        self.interface = gui.InterfaceCombat(self.L, self.H)
        
        self.persos = []    # persos[0] est toujours le personnage dont c'est actuellement le tour
        # La liste est mise à jour depuis le serveur
        
        self.vitesseDefil = 700    # Vitesse de défilement de la map (en pixels/seconde)
        self.bordureDefil = 40    # Taille de la bordure pour le défilement (en pixels)
        
        self.touches = touches
        
        self.vueMap = sf.View(sf.FloatRect(0, 0, self.L, self.H))
        self.vueInterface = sf.View(sf.FloatRect(0, 0, self.L, self.H))
    
    
    def persoActuel(self):
        return self.persos[0]
    
    
    def __scrolling(self, curseurX, curseurY):
        """Scrolling de la map"""
        
        defil = self.vitesseDefil * self.app.GetFrameTime()
        
        if curseurX <= self.bordureDefil and self.vueMap.Rect.Left > self.map.rect.Left:   # DEFILEMENT VERS LA GAUCHE
            self.vueMap.Rect.Left -= defil
            self.vueMap.Rect.Right -= defil
            if self.vueMap.Rect.Left < self.map.rect.Left:
                self.vueMap.Rect.Left = self.map.rect.Left
                self.vueMap.Rect.Right = self.map.rect.Left + self.L
        elif curseurX >= self.app.GetWidth() - self.bordureDefil and self.vueMap.Rect.Right < self.map.rect.Right:   # DEFILEMENT VERS LA DROITE
            self.vueMap.Rect.Left += defil
            self.vueMap.Rect.Right += defil
            if self.vueMap.Rect.Right > self.map.rect.Right:
                self.vueMap.Rect.Left = self.map.rect.Right - self.L
                self.vueMap.Rect.Right = self.map.rect.Right
        if curseurY <= self.bordureDefil and self.vueMap.Rect.Top > self.map.rect.Top:   # DEFILEMENT VERS LE HAUT
            self.vueMap.Rect.Top -= defil
            self.vueMap.Rect.Bottom -= defil
            if self.vueMap.Rect.Top < self.map.rect.Top:
                self.vueMap.Rect.Top = self.map.rect.Top
                self.vueMap.Rect.Bottom = self.map.rect.Top + self.H
        elif curseurY >= self.app.GetHeight() - self.bordureDefil and self.vueMap.Rect.Bottom < self.map.rect.Bottom:   # DEFILEMENT VERS LE BAS
            self.vueMap.Rect.Top += defil
            self.vueMap.Rect.Bottom += defil
            if self.vueMap.Rect.Bottom > self.map.rect.Bottom:
                self.vueMap.Rect.Top = self.map.rect.Bottom - self.H
                self.vueMap.Rect.Bottom = self.map.rect.Bottom
    
    
    def lancerBoucle(self):
        """Lancer la boucle principale du combat"""
        
        running = True
        evt = sf.Event()
        while running:
            # GESTION DES EVENEMENTS :
            while running and self.app.GetEvent(evt):
                if evt.Type == sf.Event.Closed:
                    running = False
                elif evt.Type == sf.Event.KeyPressed:
                    if evt.Key.Code == sf.Key.Escape:
                        self.map.noircir()
                        # A FAIRE :
                        # Interface : Afficher le menuEchap
                        running = False
                elif evt.Type == sf.Event.MouseButtonPressed:
                    res = self.interface.gererClic(evt, self.vueInterface)  # L'interface est bien entendu prioritaire sur la Map dans la gestion des clics
                    if res == None:
                        res = self.map.gererClic(evt, self.vueMap)
                    else:
                        running = not res.quitter
            
            # Gestion de la souris en temps réel :
            curseurX, curseurY = self.input.GetMouseX(), self.input.GetMouseY()
            
            # ZOOM de la Map :
            if self.input.IsKeyDown(self.touches.ZOOM_AVANT) and self.vueMap.Zoom < 1:
                self.vueMap.Zoom += self.app.GetFrameTime()
                if self.vueMap.Zoom > 1:
                    self.vueMap.Zoom = 1
            elif self.input.IsKeyDown(self.touches.ZOOM_ARRIERE) and self.vueMap.Zoom > 0.3:
                self.vueMap.Zoom -= self.app.GetFrameTime()
                if self.vueMap.Zoom < 0.3:
                    self.vueMap.Zoom = 0.3
            
            self.__scrolling(curseurX, curseurY)
            
            # DESSIN :
            self.app.SetView(self.vueMap)
            self.app.Draw(self.map)
            self.app.SetView(self.vueInterface)
            self.app.Draw(self.interface)
            self.app.Display()