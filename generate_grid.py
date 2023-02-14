import random

if __name__ == "__main__":

    grid_col = 100
    grid_row = 50

    for x in range(10):
        moves = ["" for i in range(100)]
        coord = [[""] * 2 for i in range(100)]
        obs = ["" for i in range(100)]
        grid = [[""] * grid_row for i in range(grid_col)]

        for i in range(grid_col):
            for j in range(grid_row):
                print(i,j)
                rand = random.random()
                if 0.5 >= rand > 0:
                    grid[i][j] = "N"
                elif rand > 0.5 and rand > 0.7:
                    grid[i][j] = "H"
                elif rand > 0.7 and rand > 0.9:
                    grid[i][j] = "T"
                else:
                    grid[i][j] = "B"

        for y in range(10):
            initX = random.randint(0, grid_col - 1)
            initY = random.randint(0, grid_row - 1)

            while grid[initX][initY] == "B":
                initX = random.randint(0, grid_col - 1)
                initY = random.randint(0, grid_row - 1)

            player = [initX, initY]

            for i in range(100):
                rand = random.random()
                if 0 < rand <= 0.25:
                    moves[i] = "U"
                elif 0.25 < rand <= 0.50:
                    moves[i] = "D"
                elif 0.50 < rand <= 0.75:
                    moves[i] = "L"
                else:
                    moves[i] = "R"

            # Ground Truth
            for i in range(len(moves)):
                rand = random.random()
                if 0 < rand <= 0.9:
                    if moves[i] == "U" and (player[1] + 1 < grid_row):
                        if grid[player[0]][player[1] + 1] != "B":
                            player[1] += 1

                    elif moves[i] == "D" and (player[1] - 1 > 0):
                        if grid[player[0]][player[1] - 1] != "B":
                            player[1] -= 1

                    elif moves[i] == "L" and (player[0] - 1 > 0):
                        if grid[player[0] - 1][player[1]] != "B":
                            player[0] -= 1

                    elif moves[i] == "R" and (player[0] + 1 < grid_col):
                        if grid[player[0] + 1][player[1]] != "B":
                            player[0] += 1

                coord[i] = [player[0], player[1]]

            # Sensor Reading
            for i in range(len(coord)):
                rand = random.random()
                if 0 < rand <= 0.9:
                    obs[i] = grid[coord[i][0]][coord[i][1]]
                elif 0.9 < rand <= 0.95:
                    if grid[coord[i][0]][coord[i][1]] == "N":
                        obs[i] = "H"
                    if grid[coord[i][0]][coord[i][1]] == "H":
                        obs[i] = "T"
                    if grid[coord[i][0]][coord[i][1]] == "T":
                        obs[i] = "N"
                elif 0.95 < rand <= 1:
                    if grid[coord[i][0]][coord[i][1]] == "N":
                        obs[i] = "T"
                    if grid[coord[i][0]][coord[i][1]] == "H":
                        obs[i] = "N"
                    if grid[coord[i][0]][coord[i][1]] == "T":
                        obs[i] = "H"

            with open('map{}_output{}.txt'.format(x + 1, y + 1), 'w') as f:
                f.write(str(initX) + " " + str(initY))
                f.write("\n")
                f.write("\n")

                for i in range(len(coord)):
                    f.write(str(coord[i][0]) + " " + str(coord[i][1]))
                    f.write("\n")

                for i in range(len(moves)):
                    f.write(moves[i])

                f.write("\n")

                for i in range(len(obs)):
                    f.write(str(obs[i]))

                f.close()

            with open('map{}.txt'.format(x + 1), 'w') as f:
                for j in range(len(grid[j])-1, -1, -1):
                    for i in range(len(grid)):
                        f.write(grid[i][j])
                    f.write("\n")
