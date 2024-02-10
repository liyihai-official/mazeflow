from random import randint
from numpy import zeros, abs, maximum
from noise import pnoise2 
from mazeflow.lib import load_maze


# class Shape2D():
#     def __init__(self, str: shape) -> None:
#         pass

class Generator2D():
    def __init__(self, shape, start, goal):
        self.height, self.width = shape # [height, width]

        self.start = start
        self.goal = goal

        self.wall_map = zeros((self.height, self.width), dtype=int)

        self.get_big_nums()

    def get_big_nums(self):
        big_num = 2 ** 16
        self.x = randint(-big_num, big_num)
        self.y = randint(-big_num, big_num)

    def generate_noise_array(self):
        noise_map = zeros((self.height, self.width))
        for i in range(self.height):
            i1 = i / 10 + self.x
            for j in range(self.width):
                j1 = j / 10 + self.y
                noise_map[i][j] = pnoise2(i1, j1)
        abs(noise_map, out=noise_map)
        return noise_map

    def generate_walls_array(self, threshold=0.5):
        
        def set_outer_to_one(matrix):
            matrix[0, :] = 1
            matrix[-1, :] = 1
            matrix[:, 0] = 1
            matrix[:, -1] = 1
            return matrix
        
        noise_map = self.generate_noise_array()
        self.wall_map[noise_map < threshold] = 1
        self.wall_map = set_outer_to_one(self.wall_map)

        self.wall_map[self.start] = 0
        self.wall_map[self.goal] = 0

        return self.wall_map

    def print(self, contents):
        print(contents)

    def save(self, filename=None, save=False):
        contents = []
        for i, row in enumerate(self.wall_map):
            row_ = []
            for j, col in enumerate(row):
                if (i, j) == self.goal:
                    row_.append("B")
                elif (i, j) == self.start:
                    row_.append("A")
                elif col:
                    row_.append("#")
                else:
                    row_.append(" ")
            contents.append(row_)
    
        if save:
            with open(filename, 'w') as file:
                for i, row in enumerate(self.wall_map):
                    for j, col in enumerate(row):
                        if (i, j) == self.goal:
                            file.write("B")
                        elif (i, j) == self.start:
                            file.write("A")
                        elif col:
                            file.write(f"#")
                        else:
                            file.write(f" ")
                    file.write('\n')
        return contents
                
    def plot(self, filename):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        # Load the image you want to use for filling
        fill_image = Image.open("wall.png")  # Replace with the path to your image

        for i, row in enumerate(self.wall_map):
            for j, col in enumerate(row):

                # Walls
                if col:
                    # Paste the fill image for walls
                    img.paste(fill_image, (j * cell_size, i * cell_size))


                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


    

