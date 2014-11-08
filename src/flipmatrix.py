import sys

grid = sys.argv[1]
newgrid = []

for i in range(len(grid)):
    row = grid[i]
    row = row[::-1]
    newgrid.append(row)

print(newgrid)
