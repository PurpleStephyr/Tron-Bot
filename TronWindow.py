# Copyright 2013 Steph Kraemer.
# This file is part of TronBot.

# TronBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TronBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TronBot.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui
from PyQt4 import QtCore

from LightCycle import *
import Dot
import Direction

class TronWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.size = (25,25)
        self.resize(self.size[0]*Dot.PIXELS_PER_SQUARE,self.size[1]*Dot.PIXELS_PER_SQUARE)
        self.startButton = QtGui.QPushButton('Start', self)
        self.startButton.clicked.connect(self.startGame)
        self.startButton.move(self.width()/2 - self.startButton.width()/2,
                              self.height()/2 - self.startButton.height()/2)
        self.show()

    def startGame(self):
        self.startButton.hide()
        self.lightCycles = [LightCycle(self, QtCore.Qt.red, (0,0), Direction.Down),
                            LightCycle(self, QtCore.Qt.blue, Direction.add(self.size, (-1, -1)),
                                       Direction.Up)]
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(200)

    def onTimer(self):
        for lightCycle in self.lightCycles:
            lightCycle.move()
