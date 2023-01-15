import random
import sys


def give_mob_coords(game_map: list, mob_size: int) -> tuple:
    while True:
        continue_condition = False
        x, y = random.randint(mob_size, len(game_map) - mob_size - 1), random.randint(mob_size,
                                                                                      len(game_map) - mob_size - 1)
        if game_map[x][y] == '.':
            for i in range(-mob_size, mob_size + 1, 1):
                for j in range(-mob_size, mob_size + 1, 1):
                    if game_map[x + i][y + j] != '.':
                        continue_condition = True
                        break
                if continue_condition:
                    break
            if not continue_condition:
                return (x, y)


class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class Map:
    def __init__(self, size: tuple):
        self.size = size
        self.leafs: list[Leaf] = []
        l = None
        root: Leaf = Leaf(0, 0, size[0], size[1])
        self.leafs.append(root)
        did_split: bool = True
        self.MIN_LEAF_SIZE = 15

        while did_split:
            did_split = False
            for l in self.leafs:
                if l.leftChild is None or l.rightChild is None:
                    if l.width > self.MIN_LEAF_SIZE or l.height > self.MIN_LEAF_SIZE or random.randint(0, 100) > 25:
                        if l.split():
                            self.leafs.append(l.leftChild)
                            self.leafs.append(l.rightChild)
                            did_split = True

        root.create_rooms()

        self.map = [['x'] * self.size[0] for _ in range(self.size[1])]

        for leaf in self.leafs:
            if leaf.halls.__len__() > 0:
                for i in range(leaf.halls[0][0], leaf.halls[0][0] + leaf.halls[0][2]):
                    for j in range(leaf.halls[0][1], leaf.halls[0][1] + leaf.halls[0][3]):
                        try:
                            self.map[i][j] = '.'
                        except IndexError:
                            print(i, j, 'len > 0')
                            sys.exit()
                if leaf.halls.__len__() == 2:
                    for i in range(leaf.halls[1][0], leaf.halls[1][0] + leaf.halls[1][2]):
                        for j in range(leaf.halls[1][1], leaf.halls[1][1] + leaf.halls[1][3]):
                            try:
                                self.map[i][j] = '.'
                            except IndexError:
                                print(i, j, 'len == 2')
                                sys.exit()
            if leaf.rightChild is not None or leaf.leftChild is not None:
                continue
            for i in range(leaf.x + leaf.roomPos[0] + 1, leaf.x + leaf.roomPos[0] + leaf.roomSize[0]):
                for j in range(leaf.y + leaf.roomPos[1] + 1, leaf.y + leaf.roomPos[1] + leaf.roomSize[1]):
                    self.map[i][j] = '.'

        # f = True
        # for i in range(self.map.__len__()):
        #     for j in range(self.map[i].__len__()):
        #         if self.map[i][j] == '.' and self.map[i + 1][j] == '.' and self.map[i - 1][j] == '.' \
        #                 and self.map[i][j - 1] == '.' and self.map[i + 1][j - 1] == '.' and self.map[i - 1][
        #             j - 1] == '.' and \
        #                 self.map[i + 1][j + 1] == '.' and self.map[i - 1][j + 1] == '.' and self.map[i][j + 1] == '.' \
        #                 and self.map[i][j - 2] == '.' and self.map[i][j - 3] == '.' \
        #                 and self.map[i][j + 2] == '.' and self.map[i][j + 3] == '.' \
        #                 and self.map[i - 2][j] == '.' and self.map[i - 3][j] == '.' \
        #                 and self.map[i + 2][j] == '.' and self.map[i + 3][j] == '.':
        #             self.map[i][j] = 'p'
        #             f = False
        #             break
        #     if not f:
        #         break
        x, y = give_mob_coords(self.map, 4)
        self.map[x][y] = 'p'

        for i in range(3):
            x, y = give_mob_coords(self.map, 1)
            self.map[x][y] = '1'

        # for i in range(2):
        #     x, y = give_mob_coords(self.map, 2)
        #     self.map[x][y] = '2'

        x, y = give_mob_coords(self.map, 6)
        self.map[x][y] = '3'

        with open('map.txt', 'w') as file:
            for i in self.map:
                file.write(''.join(i) + '\n')

        # for i in self.map:
        #     print(''.join(i))


class Leaf:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room = None
        self.leftChild = None
        self.rightChild = None
        self.halls: list[tuple] = []
        self.MIN_LEAF_SIZE = 15

    def create_rooms(self):
        if self.leftChild is not None or self.rightChild is not None:
            if self.leftChild is not None:
                self.leftChild.create_rooms()
            if self.rightChild is not None:
                self.rightChild.create_rooms()
            if self.leftChild is not None and self.rightChild is not None:
                self.createHall(self.leftChild.getRoom(), self.rightChild.getRoom())
        else:
            self.roomSize: tuple = (random.randint(10, self.width - 2),
                                    random.randint(10, self.height - 2))
            self.roomPos: tuple = \
                (random.randint(1, self.width - self.roomSize[0] - 1),
                 random.randint(1, self.height - self.roomSize[1] - 1))
            self.room = (self.roomPos[0] + self.x, self.roomPos[1] + self.y,
                         self.roomSize[0], self.roomSize[1])

    def split(self) -> bool:
        if self.leftChild is not None or self.rightChild is not None:
            return False
        splitH: bool = random.randint(0, 10) > 5
        if self.width > self.height and self.width / self.height >= 1.25:
            splitH = False
        elif self.width <= self.height and self.height / self.width >= 1.25:
            splitH = True
        max: int = 0
        if splitH:
            max = self.height - self.MIN_LEAF_SIZE
        else:
            max = self.width - self.MIN_LEAF_SIZE
        if max <= self.MIN_LEAF_SIZE:
            return False
        split: int = random.randint(self.MIN_LEAF_SIZE, max)
        if splitH:
            self.leftChild = Leaf(self.x, self.y, self.width, split)
            self.rightChild = Leaf(
                self.x, self.y + split, self.width, self.height - split)
        else:
            self.leftChild = Leaf(self.x, self.y, split, self.height)
            self.rightChild = Leaf(
                self.x + split, self.y, self.width - split, self.height)
        return True

    def getRoom(self) -> tuple[int]:
        if self.room is not None:
            return self.room
        else:
            if self.leftChild is not None:
                lRoom = self.leftChild.getRoom()
            if self.rightChild is not None:
                rRoom = self.rightChild.getRoom()
            if lRoom is None and rRoom is not None:
                return None
            elif rRoom is None:
                return lRoom
            elif lRoom is None:
                return rRoom
            elif random.randint(0, 100) > 50:
                return lRoom
            else:
                return rRoom

    def createHall(self, l: tuple[int], r: tuple[int]) -> None:
        point1 = Pair(random.randint(l[0] + 3, l[0] + l[2] - 3),
                      random.randint(l[1] + 3, l[1] + l[3] - 3))
        point2 = Pair(random.randint(r[0] + 3, r[0] + r[2] - 3),
                      random.randint(r[1] + 3, r[1] + r[3] - 3))
        w: int = point2.first - point1.first
        h: int = point2.second - point1.second

        coridor: int = 5
        # ширина коридора

        if w < 0:
            if h < 0:
                if random.randint(0, 100) < 50:
                    self.halls.append((point2.first, point1.second, abs(w), coridor))
                    self.halls.append((point2.first, point2.second, coridor, abs(h)))
                else:
                    self.halls.append((point2.first, point2.second, abs(w), coridor))
                    self.halls.append((point1.first, point2.second, coridor, abs(h)))
            elif h > 0:
                if random.randint(0, 100) < 50:
                    self.halls.append((point2.first, point1.second, abs(w), coridor))
                    self.halls.append((point2.first, point1.second, coridor, abs(h)))
                else:
                    self.halls.append((point2.first, point2.second, abs(w), coridor))
                    self.halls.append((point1.first, point1.second, coridor, abs(h)))
            else:
                self.halls.append((point2.first, point2.second, abs(w), coridor))
        elif w > 0:
            if h < 0:
                if random.randint(0, 100) < 50:
                    self.halls.append((point1.first, point2.second, abs(w), coridor))
                    self.halls.append((point1.first, point2.second, coridor, abs(h)))
                else:
                    self.halls.append((point1.first, point1.second, abs(w), coridor))
                    self.halls.append((point2.first, point2.second, coridor, abs(h)))
            elif h > 0:
                if random.randint(0, 100) < 50:
                    self.halls.append((point1.first, point1.second, abs(w), coridor))
                    self.halls.append((point2.first, point1.second, coridor, abs(h)))
                else:
                    self.halls.append((point1.first, point2.second, abs(w), coridor))
                    self.halls.append((point1.first, point1.second, coridor, abs(h)))
            else:
                self.halls.append((point1.first, point1.second, abs(w), coridor))
        else:
            if h < 0:
                self.halls.append((point2.first, point2.second, coridor, abs(h)))
            elif h > 0:
                self.halls.append((point1.first, point1.second, coridor, abs(h)))