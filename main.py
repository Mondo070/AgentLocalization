# This is a sample Python script.
from enum import Enum
import random

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import mplcursors
from tkinter import *
from matplotlib.pyplot import figure


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class State(Enum):
    N = 0
    H = 1
    T = 2
    B = 3


class Move(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Cell:
    def __init__(self, row=int, col=int, probability=float, state=State):
        self.row = row
        self.col = col
        self.probability = probability
        self.state = state


class Grid:
    def __init__(self, col_cnt=int, row_cnt=int):
        self.col_cnt = col_cnt
        self.row_cnt = row_cnt
        self.grid = [[Cell() for x in range(col_count)] for y in range(row_count)]

    def set_grid(self, blocked_cells=int, layout=list):
        regular_cells = (100 * 50) - blocked_cells
        for i in range(row_count):
            for j in range(col_count):
                if layout[i][j] != 'B':
                    self.grid[i][j] = Cell(i, j, (1 / regular_cells), layout[i][j])
                else:
                    self.grid[i][j] = Cell(i, j, 0, layout[i][j])

    def get_cell(self, row=int, col=int):
        return self.grid[row][col]

    def set_probability(self, row=int, col=int, prob=int):
        self.grid[row][col].probability = prob

    def moving_to_blocked(self, cell=Cell(), move=str):
        if move == "R":
            if cell.col == self.col_cnt - 1:
                return True
            neighbor = self.get_cell(cell.row, cell.col + 1)
            if neighbor.state == State.B:
                return True
        elif move == "L":
            if cell.col == 0:
                return True
            neighbor = self.get_cell(cell.row, cell.col - 1)
            if neighbor.state == State.B:
                return True
        elif move == "U":
            if cell.row == self.row_cnt - 1:
                return True
            neighbor = self.get_cell(cell.row + 1, cell.col)
            if neighbor.state == State.B:
                return True
        elif move == "D":
            if cell.row == 0:
                return True
            neighbor = self.get_cell(cell.row - 1, cell.col)
            if neighbor.state == State.B:
                return True
        return False

    def get_prob_grid(self):
        prob_grid = [[0 for x in range(col_count)] for y in range(row_count)]
        for x in range(self.row_cnt):
            for y in range(self.col_cnt):
                cell = self.get_cell(x, y)
                prob_grid[x][y] = cell.probability

        return np.array(prob_grid)

    def print_grid(self):
        for i in range(self.row_cnt):
            for j in range(self.col_cnt):
                cell = self.get_cell(i, j)
                print("[%d, %d] %s: %f   " % (cell.row, cell.col, cell.state, cell.probability), end='')
            print()

        print()


class Filter:
    def __init__(self, grid=Grid):
        self.grid = grid

    def normalize(self):
        total = 0
        for i in range(50):
            for j in range(100):
                total += self.grid.get_cell(i, j).probability

        for i in range(50):
            for j in range(100):
                new_prob = round(self.grid.get_cell(i, j).probability / total, 10)
                self.grid.set_probability(i, j, new_prob)

    def next_step(self, move=str, state=str):
        for i in range(self.grid.row_cnt):
            for j in range(self.grid.col_cnt):
                cell = self.grid.get_cell(i, j)

                if move == "R":
                    if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                        self.grid.set_probability(cell.row, cell.col, cell.probability)
                    elif self.grid.moving_to_blocked(cell, "L"):
                        new_prob = cell.probability * .1
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    elif self.grid.moving_to_blocked(cell, "R"):
                        left_cell = self.grid.get_cell(i, j - 1)
                        new_prob = cell.probability + (left_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    else:
                        left_cell = self.grid.get_cell(i, j - 1)
                        new_prob = (cell.probability * .1) + (left_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)


                elif move == "L":
                    if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                        self.grid.set_probability(cell.row, cell.col, cell.probability)
                    elif self.grid.moving_to_blocked(cell, "R"):
                        new_prob = cell.probability * .1
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    elif self.grid.moving_to_blocked(cell, "L"):
                        right_cell = self.grid.get_cell(i, j + 1)
                        new_prob = cell.probability + (right_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    else:
                        right_cell = self.grid.get_cell(i, j + 1)
                        new_prob = (cell.probability * .1) + (right_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)


                elif move == "U":
                    if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                        self.grid.set_probability(cell.row, cell.col, cell.probability)
                    elif self.grid.moving_to_blocked(cell, "D"):
                        new_prob = cell.probability * .1
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    elif self.grid.moving_to_blocked(cell, "U"):
                        down_cell = self.grid.get_cell(i - 1, j)
                        new_prob = cell.probability + (down_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    else:
                        down_cell = self.grid.get_cell(i - 1, j)
                        new_prob = (cell.probability * .1) + (down_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)

                elif move == "D":
                    if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                        self.grid.set_probability(cell.row, cell.col, cell.probability)
                    elif self.grid.moving_to_blocked(cell, "U"):
                        new_prob = cell.probability * .1
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    elif self.grid.moving_to_blocked(cell, "D"):
                        up_cell = self.grid.get_cell(i + 1, j)
                        new_prob = cell.probability + (up_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    else:
                        up_cell = self.grid.get_cell(i + 1, j)
                        new_prob = (cell.probability * .1) + (up_cell.probability * .9)
                        self.grid.set_probability(cell.row, cell.col, new_prob)

                if cell.state == state:
                    new_prob = cell.probability * .9
                    self.grid.set_probability(cell.row, cell.col, new_prob)
                else:
                    new_prob = cell.probability * .05
                    self.grid.set_probability(cell.row, cell.col, new_prob)

        self.normalize()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    col_count, row_count = 3, 3
    # grid2 = Grid(col_count, row_count)
    # grid2.set_grid()
    # grid2.print_grid()
    #
    # engine = Filter(grid2)
    # engine.next_step(Move.RIGHT, State.N)
    #
    # grid2.print_grid()
    file = open("map1.txt", 'r')
    grid_text = file.read().splitlines()
    file.close()

    file2 = open("map1_output1.txt", "r")
    output_text = file2.read().splitlines()
    file2.close()

    actions = output_text[102]
    observations = output_text[103]

    col_count, row_count = 100, 50
    total_blocked = 0
    for i in range(col_count):
        for j in range(row_count):
            print(i,j)
            if grid_text[j][i] == "B":
                total_blocked += 1

    root = tk.Tk()
    root.geometry("4000x4000")

    x_coord = []
    y_coord = []

    for i in range(50):
        y_coord.append(i)

    for i in range(100):
        if i % 10 == 0:
            x_coord.append(i)
        else:
            x_coord.append(None)

    grid2 = Grid(col_count, row_count)
    grid2.set_grid(total_blocked, grid_text)

    grid2.print_grid()

    engine = Filter(grid2)
    # engine.next_step(Move.RIGHT, "N")

    grid2.print_grid()

    # for i in range(100):
    #     engine.next_step(actions[i], observations[i])

    mapArr = grid2.get_prob_grid()

    # fig = matplotlib.figure.Figure()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(15.5, 8.5)

    # ax = fig.add_subplot()

    plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
    heatmap = plt.imshow(mapArr, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
    plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
    plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")

    # ax.set_xticks(np.arange(len(x_coord)), labels=x_coord)
    # ax.set_yticks(np.arange(len(y_coord)), labels=y_coord)

    # heatmap = ax.imshow(mapArr, cmap="gray", interpolation='nearest', vmin=0, vmax=.1)

    cb = fig.colorbar(heatmap)

    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().place(x=0, y=0)

    toolbarFrame = Frame(master=root)
    toolbarFrame.grid(row=0, column=0, columnspan=3)


    def next_grid(move_number):
        global toolbarFrame
        global button_next
        global button_agent
        global cursor

        engine.next_step(actions[move_number], observations[move_number])
        mapArr2 = grid2.get_prob_grid()

        # grid2.print_grid()

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
        heatmap2 = plt.imshow(mapArr2, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
        plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
        plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")
        plt.xlim([0, 100])

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().place(x=0, y=0)

        cursor.remove()
        cursor = mplcursors.cursor(heatmap2, hover=True)

        button_next = Button(root, text="next", command=lambda: next_grid(move_number + 1))
        button_agent = Button(root, text="agent", command=agent)
        button_next.grid(row=1, column=0)
        button_agent.grid(row=1, column=1)


    def agent():
        return


    button_next = Button(root, text="next", command=lambda: next_grid(0))
    button_agent = Button(root, text="agent", command=agent)
    button_next.grid(row=1, column=0)
    button_agent.grid(row=1, column=1)

    cursor = mplcursors.cursor(heatmap, hover=True)


    @cursor.connect("add")
    def on_add(sel):
        i, j = sel.target.index
        sel.annotation.set_text(mapArr[i, j])


    tk.mainloop()
