import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def __str__(self) -> str:
        return "(" + str(self.row) + ", " + str(self.col) + ")"

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class Aki(Agent):
    def init(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map: [[Tile]], goal):
        stack = [[game_map[self.row][self.col]]]

        while stack:
            partial_path = stack.pop(0)
            node = partial_path[-1]
            if node.row == goal[0] and node.col == goal[1]:
                return partial_path

            children_nodes = []
            if node.row - 1 >= 0:
                children_nodes.append(game_map[node.row - 1][node.col])
            if node.row + 1 < len(game_map):
                children_nodes.append(game_map[node.row + 1][node.col])
            if node.col - 1 >= 0:
                children_nodes.append(game_map[node.row][node.col - 1])
            if node.col + 1 < len(game_map[0]):
                children_nodes.append(game_map[node.row][node.col + 1])
            children_nodes.sort(key=lambda elem: -elem.cost())

            for child in children_nodes:
                if child not in partial_path:
                    new_partial_path = partial_path + [child]
                    stack.insert(0, new_partial_path)

class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        queue = [[game_map[self.row][self.col]]]

        while queue:
            partial_path = queue.pop(0)
            node = partial_path[-1]
            if node.row == goal[0] and node.col == goal[1]:
                return partial_path

            children_nodes = []

            # provjera da li ima komsiju na sjeveru
            if node.row - 1 >= 0:
                row = node.row - 1
                col = node.col
                north_node = game_map[row][col]
                number_of_neighbors = 0
                collective_cost = 0.0

                # provjera da li sjeverni komsija ima svog komsiju na sjeveru
                if row - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row - 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li sjeverni komsija ima svog komsiju na zapadu
                if col - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col - 1]
                    collective_cost += neighbor_node.cost()

                # provjera da li sjeverni komsija ima svog komsiju na istoku
                if col + 1 < len(game_map[0]):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col + 1]
                    collective_cost += neighbor_node.cost()

                average_cost = collective_cost / number_of_neighbors
                north_node_with_cost = [north_node, average_cost]
                children_nodes.append(north_node_with_cost)

            # --------------------------------------------------

            # provjera da li ima komsiju na jugu
            if node.row + 1 < len(game_map):
                row = node.row + 1
                col = node.col
                south_node = game_map[row][col]
                number_of_neighbors = 0
                collective_cost = 0.0

                # provjera da li juzni komsija ima svog komsiju na jugu
                if row + 1 < len(game_map):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row + 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li juzni komsija ima svog komsiju na zapadu
                if col - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col - 1]
                    collective_cost += neighbor_node.cost()

                # provjera da li juzni komsija ima svog komsiju na istoku
                if col + 1 < len(game_map[0]):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col + 1]
                    collective_cost += neighbor_node.cost()

                average_cost = collective_cost / number_of_neighbors
                south_node_with_cost = [south_node, average_cost]
                children_nodes.append(south_node_with_cost)

            # --------------------------------------------------

            # provjera da li ima komsiju na zapadu
            if node.col - 1 >= 0:
                row = node.row
                col = node.col - 1
                west_node = game_map[row][col]
                number_of_neighbors = 0
                collective_cost = 0.0

                # provjera da li zapadni komsija ima svog komsiju na jugu
                if row + 1 < len(game_map):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row + 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li zapadni komsija ima svog komsiju na sjeveru
                if row - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row - 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li zapadni komsija ima svog komsiju na zapadu
                if col - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col - 1]
                    collective_cost += neighbor_node.cost()

                average_cost = collective_cost / number_of_neighbors
                west_node_with_cost = [west_node, average_cost]
                children_nodes.append(west_node_with_cost)

            # --------------------------------------------------

            # provjera da li ima komsiju na istoku
            if node.col + 1 < len(game_map[0]):
                row = node.row
                col = node.col + 1
                east_node = game_map[row][col]
                number_of_neighbors = 0
                collective_cost = 0.0

                # provjera da li istocni komsija ima svog komsiju na jugu
                if row + 1 < len(game_map):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row + 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li istocni komsija ima svog komsiju na sjeveru
                if row - 1 >= 0:
                    number_of_neighbors += 1
                    neighbor_node = game_map[row - 1][col]
                    collective_cost += neighbor_node.cost()

                # provjera da li istocni komsija ima svog komsiju na istoku
                if col + 1 < len(game_map[0]):
                    number_of_neighbors += 1
                    neighbor_node = game_map[row][col + 1]
                    collective_cost += neighbor_node.cost()

                average_cost = collective_cost / number_of_neighbors
                east_node_with_cost = [east_node, average_cost]
                children_nodes.append(east_node_with_cost)

            children_nodes.sort(key=lambda elem: elem[1])
            for child in children_nodes:
                child_node = child[0]
                if child_node not in partial_path:
                    new_partial_path = partial_path + [child_node]
                    queue.append(new_partial_path)


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)
