class View:

    def __init__(self, maze):
        self.maze = maze

    def ausgabe(self):

        for y in range(self.maze.get_height()):
            for x in range(self.maze.get_width()):
                print(self.maze.get_maze()[y][x], end=" ")

            print()