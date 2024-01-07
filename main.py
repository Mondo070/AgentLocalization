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
import copy
import math


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
        self.grid = [[Cell() for x in range(col_cnt)] for y in range(row_cnt)]

    def set_grid(self, blocked_cells=int, layout=list):
        # regular_cells = (100 * 50) - blocked_cells
        # for y in range(row_count):
        #     for x in range(col_count):
        #         if layout[y][x] != 'B':
        #             self.grid[y][x] = Cell(y, x, (1 / regular_cells), layout[y][x])
        #         else:
        #             self.grid[y][x] = Cell(y, x, 0, layout[y][x])

        regular_cells = (100 * 50) - blocked_cells
        for y in range(row_count - 1, -1, -1):
            for x in range(col_count):
                if layout[y][x] != 'B':
                    self.grid[y][x] = Cell(y, x, (1 / regular_cells), layout[y][x])
                else:
                    self.grid[y][x] = Cell(y, x, 0, layout[y][x])

    def copy(self):
        # Create a new Grid object with a copied grid
        copied_grid = Grid(col_cnt=self.col_cnt, row_cnt=self.row_cnt)
        copied_grid.grid = [row.copy() for row in self.grid]
        return copied_grid

    def get_cell(self, row=int, col=int):
        return self.grid[row][col]

    def set_probability(self, row=int, col=int, prob=int):
        self.grid[row][col].probability = prob

    def moving_to_blocked(self, cell=Cell(), move=str):
        if move == "R":
            if cell.col == self.col_cnt - 1:
                return True
            neighbor_col = cell.col + 1
            neighbor = self.get_cell(cell.row, neighbor_col)
            if neighbor.state == "B":
                return True

        elif move == "L":
            if cell.col == 0:
                return True
            neighbor_col = cell.col - 1
            neighbor = self.get_cell(cell.row, neighbor_col)
            if neighbor.state == "B":
                return True

        elif move == "D":
            if cell.row == self.row_cnt - 1:
                return True
            neighbor = self.get_cell(cell.row + 1, cell.col)
            if neighbor.state == "B":
                return True

        elif move == "U":
            if cell.row == 0:
                return True
            neighbor = self.get_cell(cell.row - 1, cell.col)
            if neighbor.state == "B":
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
                print(f"[{cell.col}, {row_count - 1 - cell.row}] {cell.state}: {cell.probability:.9f}   ", end='')
            print()

        print()


class Filter:
    def __init__(self, grid=Grid):
        self.grid = grid

    # def normalize(self):
    #     total = 0
    #     for i in range(50):
    #         for j in range(100):
    #             total += self.grid.get_cell(i, j).probability
    #
    #     for i in range(50):
    #         for j in range(100):
    #             new_prob = round(self.grid.get_cell(i, j).probability / total, 10)
    #             self.grid.set_probability(i, j, new_prob)

    def normalize(self):
        total = 0

        for i in range(50):
            for j in range(100):
                total += self.grid.get_cell(i, j).probability

        if total != 0:
            for i in range(50):
                for j in range(100):
                    new_probability = round(float(self.grid.get_cell(i, j).probability / total), 9)
                    self.grid.set_probability(i, j, new_probability)

    def next_step(self, move=str, state=str):

        previous_probabilities = copy.deepcopy(self.grid)

        for i in range(self.grid.row_cnt):
            for j in range(self.grid.col_cnt):
                cell = self.grid.get_cell(i, j)

                if cell.state != "B":
                    if move == "R":
                        if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                            self.grid.set_probability(cell.row, cell.col, cell.probability)

                        elif self.grid.moving_to_blocked(cell, "L"):
                            new_prob = cell.probability * .1
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        elif self.grid.moving_to_blocked(cell, "R"):
                            left_cell = previous_probabilities.get_cell(cell.row, cell.col - 1)
                            new_prob = cell.probability + (left_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        else:
                            left_cell = previous_probabilities.get_cell(cell.row, cell.col - 1)
                            # left_cell = self.grid.get_cell(cell.row, cell.col - 1)
                            new_prob = (cell.probability * .1) + (left_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                    elif move == "L":
                        if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                            self.grid.set_probability(cell.row, cell.col, cell.probability)

                        elif self.grid.moving_to_blocked(cell, "R"):
                            new_prob = cell.probability * .1
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        elif self.grid.moving_to_blocked(cell, "L"):
                            right_cell = previous_probabilities.get_cell(cell.row, cell.col + 1)
                            # right_cell = self.grid.get_cell(i, j + 1)
                            new_prob = cell.probability + (right_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        else:
                            right_cell = previous_probabilities.get_cell(cell.row, cell.col + 1)
                            # right_cell = self.grid.get_cell(i, j + 1)
                            new_prob = (cell.probability * .1) + (right_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                    elif move == "U":
                        if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                            self.grid.set_probability(cell.row, cell.col, cell.probability)

                        elif self.grid.moving_to_blocked(cell, "D"):
                            new_prob = cell.probability * .1
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        elif self.grid.moving_to_blocked(cell, "U"):
                            down_cell = previous_probabilities.get_cell(cell.row + 1, cell.col)
                            # down_cell = self.grid.get_cell(i - 1, j)
                            new_prob = cell.probability + (down_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        else:
                            down_cell = previous_probabilities.get_cell(cell.row + 1, cell.col)
                            # down_cell = self.grid.get_cell(i - 1, j)
                            new_prob = (cell.probability * .1) + (down_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                    elif move == "D":
                        if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                            self.grid.set_probability(cell.row, cell.col, cell.probability)

                        elif self.grid.moving_to_blocked(cell, "U"):
                            new_prob = cell.probability * .1
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        elif self.grid.moving_to_blocked(cell, "D"):
                            up_cell = previous_probabilities.get_cell(cell.row - 1, cell.col)
                            # up_cell = self.grid.get_cell(i + 1, j)
                            new_prob = cell.probability + (up_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                        else:
                            up_cell = previous_probabilities.get_cell(cell.row - 1, cell.col)
                            # up_cell = self.grid.get_cell(i + 1, j)
                            new_prob = (cell.probability * .1) + (up_cell.probability * .9)
                            self.grid.set_probability(cell.row, cell.col, new_prob)

                    if cell.state == state:
                        new_prob = cell.probability * .9
                        self.grid.set_probability(cell.row, cell.col, new_prob)
                    else:
                        new_prob = cell.probability * .05
                        self.grid.set_probability(cell.row, cell.col, new_prob)

                # if move == "R":
                #     if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                #         self.grid.set_probability(cell.row, cell.col, cell.probability)
                #     elif self.grid.moving_to_blocked(cell, "L"):
                #         new_prob = cell.probability * .1
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     elif self.grid.moving_to_blocked(cell, "R"):
                #         left_cell = self.grid.get_cell(i, j - 1)
                #         new_prob = cell.probability + (left_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     else:
                #         left_cell = self.grid.get_cell(i, j - 1)
                #         new_prob = (cell.probability * .1) + (left_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #
                #
                # elif move == "L":
                #     if self.grid.moving_to_blocked(cell, "R") and self.grid.moving_to_blocked(cell, "L"):
                #         self.grid.set_probability(cell.row, cell.col, cell.probability)
                #     elif self.grid.moving_to_blocked(cell, "R"):
                #         new_prob = cell.probability * .1
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     elif self.grid.moving_to_blocked(cell, "L"):
                #         right_cell = self.grid.get_cell(i, j + 1)
                #         new_prob = cell.probability + (right_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     else:
                #         right_cell = self.grid.get_cell(i, j + 1)
                #         new_prob = (cell.probability * .1) + (right_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #
                #
                # elif move == "U":
                #     if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                #         self.grid.set_probability(cell.row, cell.col, cell.probability)
                #     elif self.grid.moving_to_blocked(cell, "D"):
                #         new_prob = cell.probability * .1
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     elif self.grid.moving_to_blocked(cell, "U"):
                #         down_cell = self.grid.get_cell(i - 1, j)
                #         new_prob = cell.probability + (down_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     else:
                #         down_cell = self.grid.get_cell(i - 1, j)
                #         new_prob = (cell.probability * .1) + (down_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #
                # elif move == "D":
                #     if self.grid.moving_to_blocked(cell, "U") and self.grid.moving_to_blocked(cell, "D"):
                #         self.grid.set_probability(cell.row, cell.col, cell.probability)
                #     elif self.grid.moving_to_blocked(cell, "U"):
                #         new_prob = cell.probability * .1
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     elif self.grid.moving_to_blocked(cell, "D"):
                #         up_cell = self.grid.get_cell(i + 1, j)
                #         new_prob = cell.probability + (up_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #     else:
                #         up_cell = self.grid.get_cell(i + 1, j)
                #         new_prob = (cell.probability * .1) + (up_cell.probability * .9)
                #         self.grid.set_probability(cell.row, cell.col, new_prob)
                #
                # if cell.state == state:
                #     new_prob = cell.probability * .9
                #     self.grid.set_probability(cell.row, cell.col, new_prob)
                # else:
                #     new_prob = cell.probability * .05
                #     self.grid.set_probability(cell.row, cell.col, new_prob)

        self.normalize()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = open("map1/map1.txt", 'r')
    grid_text = file.read().splitlines()
    file.close()

    file2 = open("map1/output1/map1_output1.txt", "r")
    output_text = file2.read().splitlines()
    file2.close()

    actions = output_text[102]
    observations = output_text[103]

    col_count, row_count = 100, 50
    total_blocked = 0
    for i in range(col_count):
        for j in range(row_count):
            print(i, j)
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

    #Generation of all heatmaps here
    # col_count, row_count = 100, 50
    #
    # root = tk.Tk()
    # root.geometry("4000x4000")
    #
    # x_coord = []
    # y_coord = []
    #
    # for i in range(50, -1, -1):
    #     if i % 5 == 0:
    #         y_coord.append(i)
    #     else:
    #         y_coord.append(None)
    #
    # for i in range(100):
    #     if i % 10 == 0:
    #         x_coord.append(i)
    #     else:
    #         x_coord.append(None)
    #
    # # fig, ax = plt.subplots(figsize=(15.5, 8.5))
    # # plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
    # #
    # # initial_data = [[0]]
    # # im = ax.imshow(initial_data, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
    # # cb = plt.colorbar(im, ax=ax)
    #
    # belief_experiment_arr = []
    # distance_experiment_arr = []
    # for map_number in range(1, 11):
    #     print("map number {}".format(map_number))
    #     map_path = "map{}/map{}.txt".format(map_number, map_number)
    #     map_file = open(map_path, 'r')
    #     map_text = map_file.read().splitlines()
    #     map_file.close()
    #
    #     for file_number in range(1, 11):
    #         print("output file {}".format(file_number))
    #         output_path = "map{}/output{}/map{}_output{}.txt".format(map_number, file_number, map_number, file_number)
    #         output_file = open(output_path, 'r')
    #         output_text = output_file.read().splitlines()
    #         output_file.close()
    #
    #         max_lines = 102
    #         lines_processed = 0
    #         number_pairs = []
    #         for line in output_text:
    #             if any(char.isdigit() for char in line):
    #                 # Split the line into two numbers
    #                 x, y = map(int, line.split())
    #                 number_pairs.append((x, y))
    #             if lines_processed >= max_lines:
    #                 break
    #
    #         actions = output_text[102]
    #         observations = output_text[103]
    #
    #         total_blocked = 0
    #         for row in range(row_count):
    #             for col in range(col_count):
    #                 if map_text[row][col] == "B":
    #                     total_blocked += 1
    #
    #         # root = tk.Tk()
    #         # root.geometry("4000x4000")
    #         #
    #         # x_coord = []
    #         # y_coord = []
    #         #
    #         # for i in range(50, -1, -1):
    #         #     if i % 5 == 0:
    #         #         y_coord.append(i)
    #         #     else:
    #         #         y_coord.append(None)
    #         #
    #         # for i in range(100):
    #         #     if i % 10 == 0:
    #         #         x_coord.append(i)
    #         #     else:
    #         #         x_coord.append(None)
    #         #
    #         # grid = Grid(col_count, row_count)
    #         grid = Grid(col_count, row_count)
    #         grid.set_grid(total_blocked, map_text)
    #
    #         engine = Filter(grid)
    #
    #         probability_at_agent_cell = []
    #         distance_from_agent_cell = []
    #         for x in range(100):
    #             agent_position = number_pairs[x]
    #             agent_cell = grid.get_cell(49 - agent_position[1], agent_position[0])
    #             probability_at_agent_cell.append(agent_cell.probability)
    #
    #             max_likelihood_est_cell = grid.get_cell(0, 0)
    #             for i in range(row_count):
    #                 for j in range(col_count):
    #                     if max_likelihood_est_cell.probability < grid.get_cell(i, j).probability:
    #                         max_likelihood_est_cell = grid.get_cell(i, j)
    #
    #             distance = math.sqrt((agent_cell.col - max_likelihood_est_cell.col) ** 2 +
    #                                  (agent_cell.row - max_likelihood_est_cell.row) ** 2)
    #             distance_from_agent_cell.append(distance)
    #
    #             # print(probability_at_agent_cell)
    #             engine.next_step(actions[x], observations[x])
    #
    #         belief_experiment_arr.append(probability_at_agent_cell)
    #         distance_experiment_arr.append(distance_from_agent_cell)
    #
    #         plt.plot(probability_at_agent_cell)
    #         plt.xlabel('Agent Steps')
    #         plt.ylabel('Belief in Agent Cell')
    #         plt.title('Agent Movement and Belief in Agent Cell for Map {}, Output {}'.format(map_number, file_number))
    #         save_path = "map{}/output{}/map{}_output{}_prob_at_agent_pos.png".format(map_number, file_number,
    #                                                                                  map_number, file_number)
    #         plt.savefig(save_path)
    #         plt.clf()
    #
    #         plt.plot(distance_from_agent_cell)
    #         plt.xlabel('Agent Steps')
    #         plt.ylabel('Distance Between Max Likelihood Est and Agent Pos')
    #         plt.title(
    #             'Agent Movement and Distance to Max Likelihood Estimation for Map {}, Output {}'.format(map_number,
    #                                                                                                     file_number))
    #         save_path = "map{}/output{}/map{}_output{}_dist_from_agent_pos.png".format(map_number, file_number,
    #                                                                                  map_number, file_number)
    #         plt.savefig(save_path)
    #         plt.clf()
            #GENERATION CODE ENDS HERE

            # #HEATMAP CODE STARTS HERE
            # for i in range(100):
            #     engine.next_step(actions[i], observations[i])
            #     if i == 9 or i == 49 or i == 99:
            #         mapArr = grid.get_prob_grid()
            #
            #         im.set_array(mapArr)  # Update the mappable object with new data
            #
            #         heatmap = plt.imshow(mapArr, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
            #
            #         plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
            #         plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")
            #
            #         canvas = FigureCanvasTkAgg(fig, root)
            #         canvas.get_tk_widget().place(x=0, y=0)
            #
            #         save_path = "map{}/output{}/map{}_output{}_heatmap_step{}.png".format(map_number, file_number,
            #                                                                               map_number, file_number,
            #                                                                               (i + 1))
            #         fig.savefig(save_path)
            # #HEATMAP CODE ENDS HERE

    # average_agent_prob = []
    # for x in range(len(belief_experiment_arr)):
    #     prob_zipped_array = list(zip(*belief_experiment_arr))
    #     distance_zipped_array = list(zip(*distance_experiment_arr))
    #     # Calculate the average for each group
    #     average_agent_prob = [sum(prob_values) / len(prob_values) for prob_values in prob_zipped_array]
    #     average_distance = [sum(dis_values) / len(dis_values) for dis_values in distance_zipped_array]
    #
    # print(average_agent_prob)
    # plt.plot(average_agent_prob)
    # plt.xlabel('Agent Steps')
    # plt.ylabel('Avg Belief in Agent Cell')
    # plt.title('Agent Movement and Avg Belief in Agent Cell')
    # save_path = "avg_prob_at_agent_pos.png"
    # plt.savefig(save_path)
    # plt.clf()
    #
    # plt.xlim(5, 100)
    # print(average_distance)
    # plt.plot(average_distance)
    # plt.xlabel('Agent Steps')
    # plt.ylabel('Avg Distance Between Max Likelihood Est and Agent Pos')
    # plt.title('Agent Movement and Avg Distance to Max Likelihood Estimation')
    # save_path = "avg_dist_from_agent_pos.png"
    # plt.savefig(save_path)
    # plt.clf()


    # for i in range(100):
    #     engine.next_step(actions[i], observations[i])
    #     if i == 9 or i == 49 or i == 99:
    #         mapArr = grid2.get_prob_grid()
    #
    #         # fig = matplotlib.figure.Figure()
    #         fig = matplotlib.pyplot.gcf()
    #         fig.set_size_inches(15.5, 8.5)
    #
    #         # ax = fig.add_subplot()
    #
    #         plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
    #         heatmap = plt.imshow(mapArr, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
    #
    #         plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
    #         plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")
    #
    #         # ax.set_xticks(np.arange(len(x_coord)), labels=x_coord)
    #         # ax.set_yticks(np.arange(len(y_coord)), labels=y_coord)
    #
    #         # heatmap = ax.imshow(mapArr, cmap="gray", interpolation='nearest', vmin=0, vmax=.1)
    #
    #         cb = fig.colorbar(heatmap)
    #
    #         canvas = FigureCanvasTkAgg(fig, root)
    #         canvas.get_tk_widget().place(x=0, y=0)
    #
    #         fig.savefig("map1/output2/map1_output2_heatmap_step100.png")
    #
    # mapArr = grid2.get_prob_grid()
    #
    # # fig = matplotlib.figure.Figure()
    # fig = matplotlib.pyplot.gcf()
    # fig.set_size_inches(15.5, 8.5)
    #
    # # ax = fig.add_subplot()
    #
    # plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
    # heatmap = plt.imshow(mapArr, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
    #
    # plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
    # plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")
    #
    # # ax.set_xticks(np.arange(len(x_coord)), labels=x_coord)
    # # ax.set_yticks(np.arange(len(y_coord)), labels=y_coord)
    #
    # # heatmap = ax.imshow(mapArr, cmap="gray", interpolation='nearest', vmin=0, vmax=.1)
    #
    # cb = fig.colorbar(heatmap)
    #
    # canvas = FigureCanvasTkAgg(fig, root)
    # canvas.get_tk_widget().place(x=0, y=0)
    #
    # fig.savefig("map1/output2/map1_output2_heatmap_step100.png")
    #
    # toolbarFrame = Frame(master=root)
    # toolbarFrame.grid(row=0, column=0, columnspan=3)

    def next_grid(move_number):
        global toolbarFrame
        global button_next
        global button_agent
        global cursor

        engine.next_step(actions[move_number], observations[move_number])
        mapArr2 = grid2.get_prob_grid()
        grid2.print_grid()

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

        move_number += 1

        button_next = Button(root, text="next", command=lambda: next_grid(move_number))
        button_agent = Button(root, text="agent", command=lambda: agent(move_number))
        button_next.grid(row=1, column=0)
        button_agent.grid(row=1, column=1)


    def agent(move_number):
        global toolbarFrame
        global button_next
        global button_agent
        global cursor

        reveal_agent_grid = copy.deepcopy(grid2)
        agent_position = number_pairs[move_number]
        agent_cell = reveal_agent_grid.get_cell(49 - agent_position[1], agent_position[0])
        print(49 - agent_position[1], agent_position[0])
        agent_cell.probability = 1
        prob_grid = reveal_agent_grid.get_prob_grid()

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.99, top=0.95)
        heatmap2 = plt.imshow(prob_grid, cmap=plt.cm.get_cmap("Reds"), interpolation="nearest", aspect="auto")
        plt.xticks(range(len(x_coord)), x_coord, rotation=90, va="top", ha="center")
        plt.yticks(range(len(y_coord)), y_coord, rotation=90, va="top", ha="center")
        plt.xlim([0, 100])

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().place(x=0, y=0)

        cursor.remove()
        cursor = mplcursors.cursor(heatmap2, hover=True)

        move_number += 1

        button_next = Button(root, text="next", command=lambda: next_grid(move_number))
        button_agent = Button(root, text="agent", command=lambda: agent(move_number))
        button_next.grid(row=1, column=0)
        button_agent.grid(row=1, column=1)


    move_number = 0

    button_next = Button(root, text="next", command=lambda: next_grid(move_number))
    button_agent = Button(root, text="agent", command=lambda: agent(move_number))
    button_next.grid(row=1, column=0)
    button_agent.grid(row=1, column=1)

    cursor = mplcursors.cursor(heatmap, hover=True)


    @cursor.connect("add")
    def on_add(sel):
        i, j = sel.target.index
        sel.annotation.set_text(mapArr[i, j])


    tk.mainloop()
