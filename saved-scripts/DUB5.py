# DUB5 SUITE - PART 1: ARCADE (MEMORY-OPTIMIZED FOR NUMWORKS)
# Version: v2.2
import kandinsky
import ion
from random import randint, choice
from time import sleep, monotonic

K_OK = getattr(ion, 'KEY_OK', 4)
K_UP = getattr(ion, 'KEY_UP', 1)
K_DOWN = getattr(ion, 'KEY_DOWN', 2)
K_LEFT = getattr(ion, 'KEY_LEFT', 0)
K_RIGHT = getattr(ion, 'KEY_RIGHT', 3)
K_BACK = getattr(ion, 'KEY_BACKSPACE', 17)

def any_number_key():
    for name in ('KEY_0','KEY_1','KEY_2','KEY_3','KEY_4','KEY_5','KEY_6','KEY_7','KEY_8','KEY_9'):
        k = getattr(ion, name, None)
        if k is not None:
            try:
                if ion.keydown(k): return True
            except:
                pass
    return False

def key_down(k):
    try:
        return ion.keydown(k)
    except:
        return False

def wait_release():
    while (key_down(K_OK) or key_down(K_UP) or key_down(K_DOWN) or 
           key_down(K_LEFT) or key_down(K_RIGHT) or key_down(K_BACK) or any_number_key()):
        sleep(0.02)

# Bold pure white DUB5 3x pixel art banner
DUB5_GLYPHS = [
    [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E], # D
    [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E], # U
    [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E], # B
    [0x1F, 0x10, 0x10, 0x1E, 0x01, 0x11, 0x0E]  # 5
]

def draw_white_dub5(start_x, start_y, scale=3):
    white = (255, 255, 255)
    cx = start_x
    for glyph in DUB5_GLYPHS:
        for r, row in enumerate(glyph):
            for c in range(5):
                if (row >> (4 - c)) & 1:
                    kandinsky.fill_rect(cx + c * scale, start_y + r * scale, scale, scale, white)
        cx += 5 * scale + 6

# ==============================================================================
# 1. DUB5 SNAKE (with rearranged menu and improved game over countdown)
# ==============================================================================
def run_dub5_snake():
    DIFF_NAMES = ["Easy", "Normal", "Hard", "Expert"]
    SPEED_DELAYS = [0.13, 0.085, 0.055, 0.035]
    GRID_NAMES = ["Extra Small", "Small", "Normal", "Large", "Extra Large"]
    GRID_SIZES = [8, 10, 16, 20, 24]
    GRID_COLS  = [40, 32, 20, 16, 13]
    GRID_ROWS  = [23, 18, 11, 9, 7]

    S_COLS = [((0, 255, 0), "Green"), ((0, 220, 255), "Cyan"), ((255, 215, 0), "Yellow"), ((200, 70, 255), "Purple"), ((255, 255, 255), "White")]
    F_COLS = [((255, 30, 30), "Red"), ((255, 140, 0), "Orange"), ((255, 60, 160), "Pink"), ((255, 215, 0), "Gold"), ((150, 255, 0), "Lime")]

    high_score = 0
    saved_settings = [1, 2, 0, 0]  # Normal Diff, Normal Grid, Green, Red

    def draw_row(diff_idx, grid_idx, scol, fcol, row_idx, is_sel, y):
        rows = [
            ("HOME", ""),
            ("Difficulty", "< " + DIFF_NAMES[diff_idx] + " >"),
            ("Grid Size", "< " + GRID_NAMES[grid_idx] + " >"),
            ("Snake Color", "< " + S_COLS[scol][1] + " >"),
            ("Fruit Color", "< " + F_COLS[fcol][1] + " >"),
            ("START GAME", "")
        ]
        label, val = rows[row_idx]
        bg = (38, 42, 58) if is_sel else (20, 22, 30)
        fg = (255, 220, 80) if is_sel else (200, 205, 220)
        kandinsky.fill_rect(16, y, 288, 22, bg)
        kandinsky.draw_string(label, 24, y + 2, fg, bg)
        if val:
            kandinsky.draw_string(val, 150, y + 2, (255, 255, 255) if is_sel else (140, 145, 165), bg)
        if row_idx == 3:  # snake color
            kandinsky.fill_rect(275, y + 3, 16, 15, S_COLS[scol][0])
        elif row_idx == 4:  # fruit color
            kandinsky.fill_rect(275, y + 3, 16, 15, F_COLS[fcol][0])

    def spawn_fruit(snake, cols, rows):
        while True:
            f = [randint(0, cols - 1), randint(0, rows - 1)]
            if f not in snake:
                return f

    while True:
        wait_release()
        if any_number_key():
            return
        diff_idx, grid_idx, scol, fcol = saved_settings
        cur_row = 5  # default on START GAME

        kandinsky.fill_rect(0, 0, 320, 240, (14, 15, 20))
        draw_white_dub5(121, 6)
        kandinsky.draw_string("S N A K E", 115, 30, (0, 220, 160), (14, 15, 20))
        kandinsky.draw_string("Highscore: " + str(high_score), 98, 46, (200, 205, 220), (14, 15, 20))

        y_positions = [70, 94, 118, 142, 166, 190]
        for i in range(6):
            draw_row(diff_idx, grid_idx, scol, fcol, i, i == cur_row, y_positions[i])

        while True:
            if any_number_key():
                return
            if key_down(K_OK):
                if cur_row == 0:      # HOME
                    return
                elif cur_row == 5:    # START GAME
                    break
            if key_down(K_UP):
                prev = cur_row
                cur_row = (cur_row - 1) % 6
                draw_row(diff_idx, grid_idx, scol, fcol, prev, False, y_positions[prev])
                draw_row(diff_idx, grid_idx, scol, fcol, cur_row, True, y_positions[cur_row])
                sleep(0.14)
            elif key_down(K_DOWN):
                prev = cur_row
                cur_row = (cur_row + 1) % 6
                draw_row(diff_idx, grid_idx, scol, fcol, prev, False, y_positions[prev])
                draw_row(diff_idx, grid_idx, scol, fcol, cur_row, True, y_positions[cur_row])
                sleep(0.14)
            elif key_down(K_LEFT):
                if cur_row == 1: diff_idx = (diff_idx - 1) % len(DIFF_NAMES)
                elif cur_row == 2: grid_idx = (grid_idx - 1) % len(GRID_NAMES)
                elif cur_row == 3: scol = (scol - 1) % len(S_COLS)
                elif cur_row == 4: fcol = (fcol - 1) % len(F_COLS)
                draw_row(diff_idx, grid_idx, scol, fcol, cur_row, True, y_positions[cur_row])
                sleep(0.14)
            elif key_down(K_RIGHT):
                if cur_row == 1: diff_idx = (diff_idx + 1) % len(DIFF_NAMES)
                elif cur_row == 2: grid_idx = (grid_idx + 1) % len(GRID_NAMES)
                elif cur_row == 3: scol = (scol + 1) % len(S_COLS)
                elif cur_row == 4: fcol = (fcol + 1) % len(F_COLS)
                draw_row(diff_idx, grid_idx, scol, fcol, cur_row, True, y_positions[cur_row])
                sleep(0.14)
            sleep(0.01)

        wait_release()
        saved_settings = [diff_idx, grid_idx, scol, fcol]

        # Game session loop (allows restart without leaving config)
        while True:
            if any_number_key():
                return
            cs = GRID_SIZES[grid_idx]
            cols = GRID_COLS[grid_idx]
            rows = GRID_ROWS[grid_idx]
            speed = SPEED_DELAYS[diff_idx]
            s_color = S_COLS[scol][0]
            f_color = F_COLS[fcol][0]

            top_offset = 24
            playfield_w = cols * cs
            playfield_h = rows * cs
            offset_x = (320 - playfield_w) // 2

            snake = [[cols // 2, rows // 2], [cols // 2 - 1, rows // 2], [cols // 2 - 2, rows // 2]]
            direction = [1, 0]
            food = spawn_fruit(snake, cols, rows)
            score = 0

            kandinsky.fill_rect(0, 0, 320, 240, (14, 15, 20))
            kandinsky.fill_rect(offset_x, top_offset, playfield_w, playfield_h, (18, 20, 26))
            kandinsky.fill_rect(offset_x, top_offset, playfield_w, 1, (70, 75, 95))
            # Removed bottom red border line
            kandinsky.fill_rect(offset_x, top_offset, 1, playfield_h, (70, 75, 95))
            kandinsky.fill_rect(offset_x + playfield_w - 1, top_offset, 1, playfield_h, (70, 75, 95))

            def render_bar(sc):
                kandinsky.fill_rect(0, 0, 320, 22, (0, 0, 0))
                kandinsky.draw_string("DUB5", 8, 3, (255, 255, 255), (0, 0, 0))
                kandinsky.draw_string("SCORE: " + str(sc), 80, 3, (255, 215, 0), (0, 0, 0))
                kandinsky.draw_string("HIGH: " + str(high_score), 215, 3, (200, 205, 220), (0, 0, 0))

            render_bar(score)
            kandinsky.fill_rect(offset_x + food[0]*cs + 1, top_offset + food[1]*cs + 1, cs - 2, cs - 2, f_color)

            restart_requested = False
            while True:
                if any_number_key():
                    return
                if key_down(K_UP) and direction != [0, 1]: direction = [0, -1]
                elif key_down(K_DOWN) and direction != [0, -1]: direction = [0, 1]
                elif key_down(K_LEFT) and direction != [1, 0]: direction = [-1, 0]
                elif key_down(K_RIGHT) and direction != [-1, 0]: direction = [1, 0]

                head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
                if head in snake or head[0] < 0 or head[0] >= cols or head[1] < 0 or head[1] >= rows:
                    if score > high_score: high_score = score
                    kandinsky.fill_rect(50, 90, 220, 60, (10, 12, 18))
                    kandinsky.draw_string("GAME OVER", 100, 100, (255, 60, 60), (10, 12, 18))
                    kandinsky.draw_string("Score: " + str(score), 120, 120, (255, 215, 0), (10, 12, 18))

                    # Improved countdown: check OK more frequently
                    for t in (3, 2, 1):
                        # draw countdown number
                        kandinsky.fill_rect(140, 75, 40, 30, (10, 12, 18))
                        kandinsky.draw_string(str(t), 150, 80, (255, 255, 255), (10, 12, 18))
                        # wait in small increments, checking for OK and number keys
                        for _ in range(10):
                            sleep(0.1)
                            if key_down(K_OK):
                                restart_requested = True
                                break
                            if any_number_key():
                                return
                        if restart_requested:
                            break
                    if restart_requested:
                        # Wait for key release to avoid immediate skip after restart
                        wait_release()
                        break
                    else:
                        break  # go back to config

                snake.insert(0, head)
                if head == food:
                    score += 10
                    if score > high_score: high_score = score
                    render_bar(score)
                    food = spawn_fruit(snake, cols, rows)
                    kandinsky.fill_rect(offset_x + food[0]*cs + 1, top_offset + food[1]*cs + 1, cs - 2, cs - 2, f_color)
                else:
                    tail = snake.pop()
                    kandinsky.fill_rect(offset_x + tail[0]*cs, top_offset + tail[1]*cs, cs, cs, (18, 20, 26))

                kandinsky.fill_rect(offset_x + head[0]*cs, top_offset + head[1]*cs, cs - 1, cs - 1, s_color)
                sleep(speed)

            if restart_requested:
                continue  # restart immediately
            else:
                break  # back to snake config menu

# ==============================================================================
# 2. DUB5 TETRIS (unchanged from v1.7)
# ==============================================================================
def run_dub5_tetris():
    COLS, ROWS, BS, OX, OY = 14, 18, 12, 76, 12
    SHAPES = [[[1,1,1,1]], [[1,0,0],[1,1,1]], [[0,0,1],[1,1,1]], [[1,1],[1,1]], [[0,1,1],[1,1,0]], [[0,1,0],[1,1,1]], [[1,1,0],[0,1,1]]]
    COLORS = [(0,230,255), (50,100,255), (255,140,0), (255,220,0), (50,225,50), (180,70,255), (255,45,45)]

    def rotate(s): return [[s[y][x] for y in range(len(s)-1, -1, -1)] for x in range(len(s[0]))]

    high_score = 0
    while True:
        wait_release()
        if any_number_key():
            return
        kandinsky.fill_rect(0, 0, 320, 240, (12, 14, 22))
        draw_white_dub5(121, 20)
        kandinsky.draw_string("T E T R I S", 110, 48, (0, 230, 255), (12, 14, 22))
        kandinsky.draw_string("Highscore: " + str(high_score), 98, 74, (200, 205, 220), (12, 14, 22))
        kandinsky.draw_string(">> START GAME <<", 80, 120, (255, 215, 0), (12, 14, 22))
        kandinsky.draw_string("DUB5 EDITION - OK", 75, 190, (130, 135, 155), (12, 14, 22))

        while not key_down(K_OK): sleep(0.02)
        wait_release()

        grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        score, lines = 0, 0

        kandinsky.fill_rect(0, 0, 320, 240, (12, 14, 22))
        kandinsky.fill_rect(OX, OY, COLS * BS, ROWS * BS, (22, 26, 38))
        kandinsky.fill_rect(OX - 2, OY - 2, COLS * BS + 4, 2, (70, 75, 95))
        kandinsky.fill_rect(OX - 2, OY + ROWS * BS, COLS * BS + 4, 2, (70, 75, 95))
        kandinsky.fill_rect(OX - 2, OY - 2, 2, ROWS * BS + 4, (70, 75, 95))
        kandinsky.fill_rect(OX + COLS * BS, OY - 2, 2, ROWS * BS + 4, (70, 75, 95))

        def draw_hud():
            kandinsky.draw_string("DUB5", 10, 14, (255, 255, 255), (12, 14, 22))
            kandinsky.draw_string("SCORE", 10, 40, (255, 215, 0), (12, 14, 22))
            kandinsky.draw_string(str(score), 10, 58, (255, 255, 255), (12, 14, 22))
            kandinsky.draw_string("LINES", 10, 84, (0, 230, 255), (12, 14, 22))
            kandinsky.draw_string(str(lines), 10, 102, (255, 255, 255), (12, 14, 22))
            kandinsky.draw_string("HI", 10, 130, (200, 205, 220), (12, 14, 22))
            kandinsky.draw_string(str(high_score), 10, 148, (255, 255, 255), (12, 14, 22))

        def draw_grid():
            for r in range(ROWS):
                for c in range(COLS):
                    col = grid[r][c] or (22, 26, 38)
                    kandinsky.fill_rect(OX + c * BS, OY + r * BS, BS - 1, BS - 1, col)

        def collide(shp, x, y):
            for r, row in enumerate(shp):
                for c, val in enumerate(row):
                    if val:
                        nx, ny = x + c, y + r
                        if nx < 0 or nx >= COLS or ny >= ROWS or (ny >= 0 and grid[ny][nx]): return True
            return False

        def draw_pc(shp, x, y, col, clr=False):
            c_val = (22, 26, 38) if clr else col
            for r, row in enumerate(shp):
                for c, val in enumerate(row):
                    if val and y + r >= 0:
                        kandinsky.fill_rect(OX + (x + c) * BS, OY + (y + r) * BS, BS - 1, BS - 1, c_val)

        draw_hud(); draw_grid()
        game_over = False

        while not game_over:
            if any_number_key():
                return
            s_idx = randint(0, len(SHAPES) - 1)
            shape = SHAPES[s_idx]
            col = COLORS[s_idx]
            px = COLS // 2 - len(shape[0]) // 2
            py = 0
            if collide(shape, px, py): break

            tick = 0
            while True:
                if any_number_key():
                    return
                draw_pc(shape, px, py, col, clr=True)
                if key_down(K_LEFT) and not collide(shape, px - 1, py): px -= 1; sleep(0.06)
                elif key_down(K_RIGHT) and not collide(shape, px + 1, py): px += 1; sleep(0.06)
                if key_down(K_UP):
                    r_shp = rotate(shape)
                    if not collide(r_shp, px, py): shape = r_shp; sleep(0.12)
                if key_down(K_DOWN) and not collide(shape, px, py + 1): py += 1; score += 1; sleep(0.04)
                if key_down(K_OK):
                    while not collide(shape, px, py + 1): py += 1; score += 2
                    break

                tick += 1
                if tick >= 20:
                    tick = 0
                    if not collide(shape, px, py + 1): py += 1
                    else:
                        draw_pc(shape, px, py, col)
                        for r, row in enumerate(shape):
                            for c, val in enumerate(row):
                                if val and 0 <= py + r < ROWS and 0 <= px + c < COLS:
                                    grid[py + r][px + c] = col
                        break
                draw_pc(shape, px, py, col)
                sleep(0.02)

            cleared = 0
            new_g = []
            for r in range(ROWS):
                if all(cell is not None for cell in grid[r]): cleared += 1
                else: new_g.append(grid[r])
            if cleared > 0:
                for _ in range(cleared): new_g.insert(0, [None for _ in range(COLS)])
                grid = new_g
                lines += cleared
                score += 100 * cleared * cleared
                if score > high_score: high_score = score
                draw_grid(); draw_hud()

        kandinsky.fill_rect(OX + 10, 90, COLS * BS - 20, 50, (10, 12, 18))
        kandinsky.draw_string("GAME OVER", OX + 30, 100, (255, 60, 60), (10, 12, 18))
        kandinsky.draw_string("Score: " + str(score), OX + 35, 120, (255, 215, 0), (10, 12, 18))
        sleep(1.4)

# ==============================================================================
# 3. DUB5 FLAPPY BIRD (unchanged from v1.7)
# ==============================================================================
def run_dub5_flappy():
    high_score = 0
    GAP = 95
    while True:
        wait_release()
        if any_number_key():
            return
        kandinsky.fill_rect(0, 0, 320, 240, (135, 206, 235))
        draw_white_dub5(121, 30)
        kandinsky.draw_string("FLAPPY BIRD", 105, 60, (255, 255, 255), (135, 206, 235))
        kandinsky.draw_string("Highscore: " + str(high_score), 105, 90, (0, 60, 120), (135, 206, 235))
        kandinsky.draw_string(">> START GAME <<", 80, 130, (0, 0, 0), (135, 206, 235))
        kandinsky.draw_string("DUB5 - OK", 115, 170, (0, 40, 80), (135, 206, 235))

        while not (key_down(K_OK) or key_down(K_UP)): sleep(0.02)
        wait_release()

        by, bv = 100.0, 0.0
        pipes = [[320, 75]]
        score = 0
        prev_by = int(by)
        jump_db = False

        kandinsky.fill_rect(0, 0, 320, 240, (135, 206, 235))

        while True:
            if any_number_key():
                return
            bv += 0.35; by += bv
            j_now = key_down(K_OK) or key_down(K_UP)
            if j_now and not jump_db: bv = -3.8; jump_db = True
            elif not j_now: jump_db = False

            kandinsky.fill_rect(50, prev_by, 18, 14, (135, 206, 235))
            for p in pipes:
                kandinsky.fill_rect(p[0] + 36, 0, 3, 240, (135, 206, 235))
                p[0] -= 2

            if pipes[-1][0] < 150: pipes.append([320, randint(35, 115)])
            if pipes[0][0] < -40: pipes.pop(0); score += 1

            dead = False
            for p in pipes:
                kandinsky.fill_rect(p[0], 0, 36, p[1], (34, 197, 94))
                kandinsky.fill_rect(p[0], p[1] + GAP, 36, 240 - (p[1] + GAP), (34, 197, 94))
                if 50 + 15 > p[0] and 50 < p[0] + 36:
                    if by < p[1] or by + 12 > p[1] + GAP: dead = True

            if by > 228 or by < 0: dead = True

            int_by = int(by)
            kandinsky.fill_rect(50, int_by, 16, 12, (255, 220, 0))
            kandinsky.fill_rect(62, int_by + 2, 4, 4, (0, 0, 0))
            kandinsky.fill_rect(64, int_by + 6, 4, 3, (255, 140, 0))
            prev_by = int_by

            kandinsky.fill_rect(0, 0, 320, 20, (135, 206, 235))
            kandinsky.draw_string("DUB5", 10, 2, (255, 255, 255), (135, 206, 235))
            kandinsky.draw_string("SCORE: " + str(score) + "  HI: " + str(high_score), 80, 2, (0, 40, 80), (135, 206, 235))

            if dead:
                if score > high_score: high_score = score
                kandinsky.fill_rect(70, 90, 180, 50, (255, 255, 255))
                kandinsky.draw_string("GAME OVER", 110, 100, (255, 0, 0), (255, 255, 255))
                kandinsky.draw_string("Score: " + str(score), 125, 120, (0, 0, 0), (255, 255, 255))
                sleep(1.2)
                break

            sleep(0.02)

# ==============================================================================
# 4. DUB5 PONG (unchanged from v1.7)
# ==============================================================================
def run_dub5_pong():
    high_score = 0
    while True:
        wait_release()
        if any_number_key():
            return
        kandinsky.fill_rect(0, 0, 320, 240, (12, 14, 20))
        draw_white_dub5(121, 30)
        kandinsky.draw_string("P O N G", 122, 60, (0, 255, 200), (12, 14, 20))
        kandinsky.draw_string("Highscore: " + str(high_score), 98, 90, (200, 205, 220), (12, 14, 20))
        kandinsky.draw_string(">> START GAME <<", 80, 130, (255, 215, 0), (12, 14, 20))
        kandinsky.draw_string("DUB5 - OK", 115, 170, (120, 130, 150), (12, 14, 20))

        while not key_down(K_OK): sleep(0.02)
        wait_release()

        py, cy = 90, 90
        bx, by = 160, 120
        dx, dy = 2, 1.5
        pscore, cscore = 0, 0
        paddle_h, cpu_h = 44, 36

        kandinsky.fill_rect(0, 0, 320, 240, (0, 0, 0))

        while True:
            if any_number_key():
                return
            kandinsky.fill_rect(bx, int(by), 8, 8, (0, 0, 0))
            kandinsky.fill_rect(10, py, 10, paddle_h, (0, 0, 0))
            kandinsky.fill_rect(300, int(cy), 10, cpu_h, (0, 0, 0))

            if key_down(K_UP): py = max(0, py - 6)
            if key_down(K_DOWN): py = min(240 - paddle_h, py + 6)

            if by > cy + 22: cy = min(240 - cpu_h, cy + 2)
            elif by < cy + 14: cy = max(0, cy - 2)

            bx += dx; by += dy
            if by <= 2 or by >= 230: dy = -dy

            if 10 <= bx <= 22 and py - 4 <= by <= py + paddle_h + 2:
                dx = abs(dx)
                dy = ((by - (py + paddle_h / 2)) / (paddle_h / 2)) * 2.2
            if 290 <= bx <= 302 and cy - 4 <= by <= cy + cpu_h + 2: dx = -abs(dx)

            if bx < 0:
                cscore += 1; bx, by = 160, 120; dx = 2; sleep(0.3)
            elif bx > 320:
                pscore += 1
                if pscore > high_score: high_score = pscore
                bx, by = 160, 120; dx = -2; sleep(0.3)

            for y_dash in range(0, 240, 16): kandinsky.fill_rect(159, y_dash, 2, 8, (60, 60, 60))
            kandinsky.fill_rect(10, py, 10, paddle_h, (0, 255, 180))
            kandinsky.fill_rect(300, int(cy), 10, cpu_h, (255, 100, 100))
            kandinsky.fill_rect(bx, int(by), 8, 8, (255, 255, 0))

            kandinsky.fill_rect(0, 0, 320, 20, (0, 0, 0))
            kandinsky.draw_string("DUB5", 10, 4, (255, 255, 255), (0, 0, 0))
            kandinsky.draw_string(str(pscore) + " - " + str(cscore) + "   HI: " + str(high_score), 110, 4, (255, 215, 0), (0, 0, 0))
            sleep(0.015)

# ==============================================================================
# MAIN HOMEPAGE (unchanged except any_number_key checks)
# ==============================================================================
def homepage():
    GAMES = ["DUB5 Snake", "DUB5 Tetris", "DUB5 Flappy Bird", "DUB5 Pong"]
    sel_idx = 0

    def render_row(idx, is_sel):
        y = 80 + idx * 28
        bg = (38, 44, 64) if is_sel else (16, 18, 25)
        fg = (255, 255, 255) if is_sel else (165, 175, 195)
        kandinsky.fill_rect(24, y, 272, 22, bg)
        prefix = "> " if is_sel else "  "
        kandinsky.draw_string(prefix + GAMES[idx], 32, y + 2, fg, bg)

    while True:
        wait_release()
        if any_number_key():
            continue  # stay on homepage
        kandinsky.fill_rect(0, 0, 320, 240, (12, 14, 20))
        draw_white_dub5(121, 10)
        kandinsky.draw_string("DUB5 ARCADE", 90, 44, (200, 205, 220), (12, 14, 20))
        kandinsky.draw_string("v2.2", 5, 218, (130, 135, 155), (12, 14, 20))

        for i in range(len(GAMES)):
            render_row(i, i == sel_idx)

        while True:
            if any_number_key():
                continue  # already home
            if key_down(K_OK):
                break
            if key_down(K_UP):
                prev = sel_idx
                sel_idx = (sel_idx - 1) % len(GAMES)
                render_row(prev, False)
                render_row(sel_idx, True)
                sleep(0.14)
            elif key_down(K_DOWN):
                prev = sel_idx
                sel_idx = (sel_idx + 1) % len(GAMES)
                render_row(prev, False)
                render_row(sel_idx, True)
                sleep(0.14)
            sleep(0.01)

        wait_release()
        if sel_idx == 0: run_dub5_snake()
        elif sel_idx == 1: run_dub5_tetris()
        elif sel_idx == 2: run_dub5_flappy()
        elif sel_idx == 3: run_dub5_pong()

homepage()