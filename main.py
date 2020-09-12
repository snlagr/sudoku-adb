# import os
# device = os.popen("adb devices").read()
# print(device)

from ppadb.client import Client
from PIL import Image
import pytesseract
import copy
from sudoku import solve, print_board


adb = Client()
devices = adb.devices()

if len(devices) == 0:
	print("No devices attached")
	quit()
device = devices[0]

result = device.screencap()
with open("screen.png", "wb") as fp:
    fp.write(result)

im = Image.open("screen.png")
# im.show()

# imcrop = im.crop((0,280,120,400))
# imcrop.show()
# print(pytesseract.image_to_string(imcrop, config='--psm 10'))
x, y = 3, 285
dx, dy = 112, 114
grid = []
touch = []
for j in range(1,10):
	ans = []
	t = []
	xc = x
	for i in range(1,10):
		imcrop = im.crop((x,y,x+dx,y+dy))
		imcrop = imcrop.crop((16,13,98,104))
		t.append( ((2*x+dx)//2, (2*y+dy)//2) )
		# if (j==2 and i==9):
		# 	imcrop.show()
		if i%3==0:
			x += 11
		else:
			x += 7
		# imcrop.show()
		temp = pytesseract.image_to_string(imcrop, config='--psm 10')
		if (temp[0].isnumeric()):
			temp = int(temp[0])
		else:
			temp = 0
		ans.append(temp)
		x += dx
	x = xc
	if (j%3==0):
		y += dy + 12
	else:
		y += dy + 8
	grid.append(ans)
	touch.append(t)

orig_grid = copy.deepcopy(grid)
solve(grid)
print_board(grid)

def click(i, j):
	device.shell(f'input touchscreen tap {touch[i][j][0]} {touch[i][j][1]}')

def select(n):
	arr = [123, 212, 314, 410, 515, 623, 724, 839, 937]
	device.shell(f'input touchscreen tap {arr[n-1]} 1453')

for i in range(len(grid)):
	for j in range(len(grid[0])):
		if (orig_grid[i][j] == 0):
			select(grid[i][j])
			click(i, j)


# print_board(grid)
# device.shell('input touchscreen swipe 500 500 500 500 2000')