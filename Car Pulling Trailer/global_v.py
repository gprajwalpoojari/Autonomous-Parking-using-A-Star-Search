VERTICES = []
EDGE_LIST = []
DISTANCE = []
PREVIOUS = []

COUNT = 0
SIZE = 640
DENSITY = 10
ROWS = 128
BLACK =(0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (100, 255, 50)

# START = 0
# END = ROWS * ROWS - 1
START = ROWS * 6 + 19
# END = ROWS * 118 + 10
start = START, 19, 6, 0, 4, 6, 0
# final = END, 43, 118, 0, 10, 118, 0
END = ROWS * 122 + 45
final = END, 45, 122, 0, 28, 122, 0
def clear_list():
    global COUNT
    VERTICES.clear()
    EDGE_LIST.clear()
    DISTANCE.clear()
    PREVIOUS.clear()
    COUNT = 0


L = 3
width = 1.75
d1 = 5
pixel = 0.3 # 1 pixel = 0.15m
