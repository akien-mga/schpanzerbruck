#! /usr/bin/env python
# encoding=UTF-8

##########################################################################
### Schpanzerbrück
### Copyright (C) 2008 The_Schpanzerteam
###
### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

import sys

try:
    from PySFML import sf
except ImportError:
    print >> sys.stderr, "Schpanzerbrück a besoin de PySFML pour fonctionner correctement.\n Vous pouvez l'installer à partir de http://www.sfml-dev.org"
    sys.exit()

import os.path

import contexte
from constantes import chemins, defaut
import parser

# Parsage de ligne de commande
options = parser.retourneOptions()

try:
    if options.psyco:
        import psyco
        psyco.full()

except ImportError:
    options.psyco=False

if options.plein_ecran:
    videoMode = sf.VideoMode.GetDesktopMode()
    style = sf.Style.Close | sf.Style.Fullscreen
else:
    videoMode = sf.VideoMode(1024, 768, 32)
    style = sf.Style.Close

app = sf.RenderWindow(videoMode, "SCHPANZERBRUCK", style)
app.SetFramerateLimit(100)
app.UseVerticalSync(True)
app.OptimizeForNonOpenGL(True)

if os.path.exists(os.path.join(chemins.MAPS, options.carte)):
    carte = os.path.join(chemins.MAPS, options.carte)
else:
    carte = os.path.join(chemins.MAPS, defaut.CARTE)
# Fin parsage


CTX = contexte.ContexteCombat(app, carte)

CTX.lancerBoucle()