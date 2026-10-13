class Maze:
    def __init__(self):
        self.begehbare_zellen = None
        self.width = 0
        self.height = 0
        self.maze = []

    def get_maze(self):
        return self.maze

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_maze(self,maze):
        self.find_dimension(maze)#finde die Dim der Labyinth. In maze(eine Liste die alle Chars(zeilenweise ohne Leerzeichen am Anfang und Ende) hat,die der Labyrinth .txt besitzt
        self.create_field(maze)

    def find_dimension(self, maze):
        for line in maze:
            if "Dimensions" in line:
                test = line.split()
                self.height = int(test[1])
                self.width = int(test[3])
                print("Höhe:", self.height)
                print("Breite:", self.width)

    def create_field(self, maze):

        self.maze = []

        maze_lines = []
        for line in maze:
            if "Legend" in line:
                break
            maze_lines.append(line.split())

        # Nur die ersten height Zeilen übernehmen (falls vorhanden)
        self.maze = maze_lines[:self.height]

    def find_start_end(self):

        start = None
        goal = None

        for y in range(self.height):

            for x in range(self.width):

                if self.maze[y][x] == "S":
                    start = (x, y)

                elif self.maze[y][x] == "E":
                    goal = (x, y)

        return start, goal

