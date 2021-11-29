DISTANCE = []
PREVIOUS = []

SIZE = 640
DENSITY = 10
ROWS = 128
BLACK =(0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (100, 255, 50)

START = ROWS * 7 + 4
END = ROWS * 120 + 33
start = START, 4, 7, 0
final = END, 33, 120, 0

def clear_list():
    global COUNT
    VERTICES.clear()
    EDGE_LIST.clear()
    DISTANCE.clear()
    PREVIOUS.clear()
    COUNT = 0
