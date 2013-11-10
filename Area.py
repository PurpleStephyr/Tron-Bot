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

import Direction

class Area:
    def __init__(self, window, position):
        self.corners = []
        self.window = window
        # Find a wall to follow
        wallDirection = None
        for direction in Direction.All:
            if not self.window.checkPosition(Direction.add(position, direction)):
                wallDirection = direction
                break
        currentPosition = position
        currentDirection = (wallDirection[1], wallDirection[0])
        while True:
            wallStopped = self.window.checkPosition(Direction.add(currentPosition, wallDirection))
            foundNewWall = not self.window.checkPosition(Direction.add(currentPosition,
                                                                       currentDirection))
            if wallStopped or foundNewWall:
                self.corners.append(currentPosition)
                if wallStopped:
                    temp = currentDirection
                    currentDirection = wallDirection
                    wallDirection = (temp[0]*-1, temp[1]*-1)
                else:
                    temp = wallDirection
                    wallDirection = currentDirection
                    currentDirection = (temp[0]*-1, temp[1]*-1)

            currentPosition = Direction.add(currentPosition, currentDirection)
            if currentPosition == position:
                break
