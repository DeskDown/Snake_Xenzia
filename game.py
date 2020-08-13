import curses as cs
import random
import time 
import sys

def get_food_char():
    chars = [
        "$",
        "€",
        "£",
        "¥",
        "♥",
        cs.ACS_DIAMOND,
        cs.ACS_PI
    ]
    return random.choice(chars)


def print_end_messages(win, score, food):
    #clear the food
    win.addch(*food," ")
    End, final_score = ["Game Over...", f"Score: {score}"]
    y, x = win.getmaxyx()
    
    win.addstr(y//2, x//2 - len(End)//2, End, cs.A_REVERSE)
    win.addstr(y//2 + 2, x//2 - len(final_score)//2 , final_score)
    win.refresh()


def init_snake():
    snake_x = INITIAL_SNAKE_SIZE
    snake_y = 1 
    return [[snake_y, snake_x - i] for i in range(INITIAL_SNAKE_SIZE)]


def valid_key(k1, k2):
    opposit_key =  {
        cs.KEY_DOWN: cs.KEY_UP,
        cs.KEY_LEFT: cs.KEY_RIGHT,
        cs.KEY_UP: cs.KEY_DOWN,
        cs.KEY_RIGHT: cs.KEY_LEFT,   
    }
    return k1 != opposit_key[k2]


SPEED = 50
PADDING = 2
SCREEN = cs.initscr()
cs.curs_set(0)
SH, SW = SCREEN.getmaxyx()
print(SH, SW)
#WIN = cs.newwin(SH ,SW ,0 ,0)
WIN = SCREEN
cs.start_color()
cs.init_pair(1, cs.COLOR_WHITE, cs.COLOR_BLACK)
WIN.bkgd(" ",cs.color_pair(1))

WIN.keypad(True)
WIN.timeout(SPEED)

INITIAL_SNAKE_SIZE = 5
SNAKE_CHAR = "■" #"■"
snake = init_snake()
key = cs.KEY_RIGHT
food_x = random.randint(PADDING, SW - PADDING)
food_y = random.randint(PADDING, SH - PADDING)
food = [food_y, food_x]
WIN.addch(food_y, food_x, get_food_char())
score = 0

try:
    while True:
        delay = 1/(SPEED*(score//5 + 1))
        time.sleep(delay)
        WIN.box("|","-") 
        WIN.refresh()
        next_key = WIN.getch()
        if next_key != -1 and valid_key(key, next_key): 
            key = next_key

        head = snake[0]
        head_y, head_x = head
        is_snake_hitting_walls = head_y in (0, SH) or head_x in (0, SW)
        is_snake_biting_itself = [head_y, head_x] in snake[1:]

        if is_snake_biting_itself or is_snake_hitting_walls:
            cs.beep()
            print_end_messages(WIN, score, food)
            time.sleep(2)
            cs.endwin()
            quit()

        if key == cs.KEY_DOWN:
            head_y += 1
        if key == cs.KEY_UP:
            head_y -= 1
        if key == cs.KEY_LEFT:
            head_x -= 1
        if key == cs.KEY_RIGHT:
            head_x += 1


        new_head = [head_y, head_x]
        snake.insert(0,new_head)
        
        if food in snake:
            score += 1
            while food is None or food in snake:
                food_x = random.randint(PADDING, SW - PADDING)
                food_y = random.randint(PADDING, SH - PADDING)
                food = [food_y, food_x]
            WIN.addch(food_y, food_x, get_food_char())
        else:
            tail = snake.pop()
            tail_y, tail_x = tail
            WIN.addch(*tail, " ")
        WIN.addch(*head, SNAKE_CHAR)

except  Exception as error:
    print(snake)
    print(head)
    print(food)
    print(error)
    print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))