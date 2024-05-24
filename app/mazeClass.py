from flask import request
import numpy as np
import pygame
from random import shuffle
import sys

sys.setrecursionlimit(10000)


class Maze:
    def __init__(
        self,
        tileSize,
        width,
        height,
        start,
        end,
        wallType,
        wallColor,
        bgColor,
        startColor,
        endColor,
        solveColor,
    ):
        self.tileSize = tileSize
        self.width = width
        self.height = height
        self.start = (start[0] - 1, start[1] - 1)
        self.end = (end[0] - 1, end[1] - 1)
        self.wallType = wallType
        self.wallColor = wallColor
        self.bgColor = bgColor
        self.startColor = startColor
        self.endColor = endColor
        self.solveColor = solveColor

        self.maze = [
            [["UDLR", self.bgColor] for c in range(self.width)]
            for r in range(self.height)
        ]

        self.makeMazeVisited = [
            [False for c in range(self.width)] for r in range(self.height)
        ]

        self.solve = []
        self.solveVisited = [
            [False for c in range(self.width)] for r in range(self.height)
        ]

        if self.wallType == "line":
            self.maze[self.start[1]][self.start[0]][1] = self.startColor
            self.maze[self.end[1]][self.end[0]][1] = self.endColor

        self.createMaze()

    def createMaze(self):
        if self.wallType == "solid":
            print("solid")
        elif self.wallType == "line":
            self.createLineMaze(self.start[0], self.start[1])

    def getSolve(self):
        self.solveMaze(self.start[0], self.start[1], [])

    def createSolidMaze(self, start):
        img = None
        return img

    def createLineMaze(
        self,
        c,
        r,
    ):
        cell = self.maze[r][c]
        self.makeMazeVisited[r][c] = True
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        shuffle(directions)
        for direction in directions:
            if (
                0 <= c + direction[0]
                and c + direction[0] < len(self.maze[0])
                and 0 <= r + direction[1]
                and r + direction[1] < len(self.maze)
            ):
                nextCell = self.maze[r + direction[1]][c + direction[0]]
                if not self.makeMazeVisited[r + direction[1]][c + direction[0]]:
                    match direction:
                        case (0, -1):
                            cell[0] = cell[0].replace("U", "")
                            nextCell[0] = nextCell[0].replace("D", "")
                        case (0, 1):
                            cell[0] = cell[0].replace("D", "")
                            nextCell[0] = nextCell[0].replace("U", "")
                        case (-1, 0):
                            cell[0] = cell[0].replace("L", "")
                            nextCell[0] = nextCell[0].replace("R", "")
                        case (1, 0):
                            cell[0] = cell[0].replace("R", "")
                            nextCell[0] = nextCell[0].replace("L", "")
                    self.createLineMaze(c + direction[0], r + direction[1])

    def solveMaze(self, c, r, path):
        cell = self.maze[r][c]
        if cell[1] == self.endColor:
            self.solve = path[:-1]
        else:
            self.solveVisited[r][c] = True
            directions = []
            if "U" not in cell[0]:
                directions.append((0, -1))
            if "D" not in cell[0]:
                directions.append((0, 1))
            if "L" not in cell[0]:
                directions.append((-1, 0))
            if "R" not in cell[0]:
                directions.append((1, 0))

            for direction in directions:
                if (
                    0 <= c + direction[0]
                    and c + direction[0] < len(self.maze[0])
                    and 0 <= r + direction[1]
                    and r + direction[1] < len(self.maze)
                ):
                    if not self.solveVisited[r + direction[1]][c + direction[0]]:
                        path.append((c + direction[0], r + direction[1]))
                        self.solveMaze(c + direction[0], r + direction[1], path)
                        path.pop()

    def displayMaze(self, screen):
        # if self.wallType == "solid":
        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):
                cell = self.maze[r][c]
                if self.wallType == "line":
                    pygame.draw.rect(
                        screen,
                        cell[1],
                        (
                            c * self.tileSize,
                            r * self.tileSize,
                            self.tileSize,
                            self.tileSize,
                        ),
                    )

                else:
                    pass

        self.displaySolve(screen)

        if self.wallType == "line":
            self.displayLineWall(screen)

    def displaySolve(self, screen):
        for i in range(len(self.solve)):
            c, r = self.solve[i]
            if self.wallType == "line":
                pygame.draw.rect(
                    screen,
                    self.solveColor,
                    (
                        c * self.tileSize,
                        r * self.tileSize,
                        self.tileSize,
                        self.tileSize,
                    ),
                )

    def displayLineWall(self, screen):
        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):
                cell = self.maze[r][c]
                if self.wallType == "line":
                    wallSize = self.tileSize / 10
                    if "U" in cell[0]:
                        pygame.draw.rect(
                            screen,
                            self.wallColor,
                            (
                                c * self.tileSize - wallSize / 2,
                                r * self.tileSize - wallSize / 2,
                                self.tileSize + wallSize,
                                wallSize,
                            ),
                        )
                    if "L" in cell[0]:
                        pygame.draw.rect(
                            screen,
                            self.wallColor,
                            (
                                c * self.tileSize - wallSize / 2,
                                r * self.tileSize - wallSize / 2,
                                wallSize,
                                self.tileSize + wallSize,
                            ),
                        )
                    if "R" in cell[0]:
                        pygame.draw.rect(
                            screen,
                            self.wallColor,
                            (
                                c * self.tileSize + self.tileSize - wallSize / 2,
                                r * self.tileSize - wallSize / 2,
                                wallSize,
                                self.tileSize + wallSize,
                            ),
                        )
                    if "D" in cell[0]:
                        pygame.draw.rect(
                            screen,
                            self.wallColor,
                            (
                                c * self.tileSize - wallSize / 2,
                                r * self.tileSize + self.tileSize - wallSize / 2,
                                self.tileSize + wallSize,
                                wallSize,
                            ),
                        )


class Cell:
    def __init__(self, color):
        # self.walls = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        # self.walls = np.array([self.up, self.down, self.left, self.right])  # UDLR
        self.visited = False
        self.color = color


def makeMaze():
    tileSize = request.form["tile"]
    width = request.form["width"]
    height = request.form["height"]
    start = (request.form["startx"], request.form["starty"])
    end = (request.form["endx"], request.form["endy"])
    wallType = request.form["wall"]
    wallColor = request.form["wall_color"]
    bgColor = request.form["bg_color"]
    startColor = request.form["start_color"]
    endColor = request.form["end_color"]
    solveColor = request.form["solve_color"]

    return Maze(
        int(tileSize),
        int(width),
        int(height),
        (int(start[0]), int(start[1])),
        (int(end[0]), (int(end[1]))),
        wallType,
        wallColor,
        bgColor,
        startColor,
        endColor,
        solveColor,
    )


def getImage(maze):
    pygame.init()
    screen = pygame.display.set_mode(
        (maze.width * maze.tileSize, maze.height * maze.tileSize), flags=pygame.HIDDEN
    )
    maze.displayMaze(screen)
    pygame.display.update()

    pygame.image.save(screen, "app/static/maze.png")

    maze.getSolve()
    maze.displayMaze(screen)
    pygame.display.update()
    pygame.image.save(screen, "app/static/mazeSolve.png")
