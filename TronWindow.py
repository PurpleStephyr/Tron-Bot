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
        self.grabKeyboard()
        self.bots = [LightCycle('Blue', self, QtCore.Qt.blue,
                                       Direction.add(self.size, (-1, -1)), Direction.Up)]
        self.humanPlayer = LightCycle('Red', self, QtCore.Qt.red, (0,0), Direction.Down)
        self.lightCycles = [self.humanPlayer] + self.bots
        self.deadLightCycles = []
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(200)

    def onTimer(self):
        numKilled = 0
        for lightCycle in self.lightCycles:
            lightCycle.move()
            position = lightCycle.getHeadPosition()
            if position[0] < 0 or position[1] < 0 or position[0] >= self.size[0] or \
               position[1] >= self.size[1]:
                numKilled = numKilled + 1
                self.deadLightCycles.append(lightCycle)
            else:
                collidingCycle = self.checkCollision(position)
                if collidingCycle != None:
                    numKilled = numKilled + 1
                    self.deadLightCycles.append(lightCycle)
                    if lightCycle.getHeadPosition() == collidingCycle.getHeadPosition():
                        numKilled = numKilled + 1
                        self.deadLightCycles.append(collidingCycle)
                else:
                    lightCycle.occupiedSpaces[position[0]][position[1]] = True


        for i in xrange(numKilled):
            self.lightCycles.remove(self.deadLightCycles[-i-1])

        if len(self.lightCycles) == 1:
            self.timer.stop()
            print 'Game over. Winner is ' + self.lightCycles[0].name
        elif len(self.lightCycles) == 0:
            self.timer.stop()
            print 'Tie game: winners are:'
            for i in xrange(numKilled):
                print self.deadLightCycles[-i-1].name
        else:
            for lightCycle in self.lightCycles:
                lightCycle.computeNextDirection()

    def keyPressEvent(self, keyEvent):
        if self.humanPlayer != None and keyEvent.type() == QtCore.QEvent.KeyPress:
            self.humanPlayer.setDirection( {
                        QtCore.Qt.Key_Up : Direction.Up,
                        QtCore.Qt.Key_Down : Direction.Down,
                        QtCore.Qt.Key_Left : Direction.Left,
                        QtCore.Qt.Key_Right : Direction.Right }.get(keyEvent.key(), None) )

    def checkCollision(self, position):
        for otherCycle in self.lightCycles + self.deadLightCycles:
            if otherCycle.occupiedSpaces[position[0]][position[1]]:
                return otherCycle

        return None
