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

import Direction
from Dot import *
from Area import *

class LightCycle(QtCore.QObject):
    def __init__(self, name, tronWindow, colour, position, initialDirection):
        QtCore.QObject.__init__(self, tronWindow)
        self.name = name
        self.tronWindow = tronWindow
        self.colour = colour
        self.direction = initialDirection

        self.occupiedSpaces = [[False for j in xrange(0, self.tronWindow.size[1])]
                               for i in xrange(0, self.tronWindow.size[1])]

        self.nodes = [Dot(self.tronWindow, position, self.colour)]
        self.occupiedSpaces[position[0]][position[1]] = True

    def __del__(self):
        for node in self.nodes:
            node.deleteLater()

    def setDirection(self, direction):
        if(direction == Direction.Up or
           direction == Direction.Down or
           direction == Direction.Left or
           direction == Direction.Right):
            self.direction = direction

    def move(self):
        self.nodes.append(Dot(self.tronWindow,
                              Direction.add(self.getHeadPosition(), self.direction),
                              self.colour))

    def getHeadPosition(self):
        return self.nodes[-1].position

    def computeNextDirection(self):
        otherPossiblePositions = []
        for lightCycle in self.tronWindow.lightCycles:
            if lightCycle != self:
                for direction in Direction.All:
                    otherPossiblePositions.append(Direction.add(lightCycle.getHeadPosition(),
                                                                direction))
        maxArea = 0
        desirableDirections = []
        desiredDirectionCollides = False
        for direction in Direction.All:
            attemptedPosition = Direction.add(self.getHeadPosition(), direction)
            if self.tronWindow.checkPosition(attemptedPosition):
                currentArea = Area(self.tronWindow, attemptedPosition)
                bounds = getBounds(currentArea.corners)
                estimatedArea = getArea(bounds)
                if estimatedArea > maxArea:
                    desirableDirections = [(direction, bounds)]
                    maxArea = estimatedArea
                    desiredDirectionCollides = attemptedPosition in otherPossiblePositions
                elif estimatedArea == maxArea and (desiredDirectionCollides):
                    if attemptedPosition in otherPossiblePositions:
                        desirableDirections.append((direction, bounds))
                    else:
                        desirableDirections = [(direction, bounds)]
                        desiredDirectionCollides = False
                elif estimatedArea == maxArea and not attemptedPosition in otherPossiblePositions:
                    desirableDirections.append((direction, bounds))

        bestDirectionRanking = 0
        bestDirection = None
        for directionAndBounds in desirableDirections:
            direction = directionAndBounds[0]
            bounds = directionAndBounds[1]
            if direction == Direction.Up:
                bounds = (bounds[0], bounds[1], bounds[2],
                          min(bounds[3], self.tronWindow.humanPlayer.getHeadPosition()[1]))
            elif direction == Direction.Down:
                bounds = (bounds[0], bounds[1],
                          max(bounds[2], self.tronWindow.humanPlayer.getHeadPosition()[1]),
                          bounds[3])
            elif direction == Direction.Left:
                bounds = (bounds[0],
                             min(bounds[1], self.tronWindow.humanPlayer.getHeadPosition()[0]),
                             bounds[2], bounds[3])
            else:
                bounds = (max(bounds[0], self.tronWindow.humanPlayer.getHeadPosition()[0]),
                          bounds[1], bounds[2], bounds[3])
            directionRanking = getArea(bounds)
            if directionRanking > bestDirectionRanking:
                bestDirection = direction
                bestDirectionRanking = directionRanking
            elif directionRanking == bestDirectionRanking and direction == self.direction:
                bestDirection = direction

        if bestDirection != None:
            self.direction = bestDirection
