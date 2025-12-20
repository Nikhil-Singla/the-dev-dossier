"""
Idle Numbers Game
-----------------
A simple idle numbers game built using Pygame. Players can earn money by pressing buttons, purchase upgrades, and hire managers to automate and see
the number rise.

Author: Nikhil Singla
Last Update: November 2025
"""

import pygame
import logging

# Initialize Pygame
pygame.init()

# ---------------------- Constants ----------------------
# Colors
AQUA = (0, 255, 255)
NAVY = (0, 0, 205)
BLACK = (0, 0, 0)
SKIN = (255, 228, 196)
ORANGE = (255, 97, 3)
METALLIC = (198, 226, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Display Settings
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
FRAME_RATE = 60

# Fonts
FONT_SIZE = 16
FONT = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

# Button Settings
BUTTON_COLORS = [WHITE, RED, AQUA, ORANGE, NAVY]
BUTTON_Y_POSITIONS = [100, 200, 300, 400, 500]
BUTTON_X_POSITIONS = [10, 80, 150, 220, 290]

# Upgrade Scaling Factors
UPGRADE_SCALING = [(1.2, 1.1), (1.35, 1.25), (1.5, 1.4), (1.8, 1.6), (2, 1.6)]
MONEY_INCREASE = [(1, 2), (1.5, 3), (5, 10), (30, 40), (100, 200)]
LATE_GAME_THRESHOLDS = [500, 1000, 1500, 2000, 5000]

# Manager Costs
MANAGER_COSTS = [100, 500, 1000, 3000, 5000]

# ---------------------- Logging Setup ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------- Functions ----------------------
def draw_box(color, y_cord, value, draw, length, speed):
    """Draw the main clicker box and handle progress bar updates."""
    global total_money_earned

    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        total_money_earned += value

    pygame.draw.rect(screen, color, [70, y_cord - 15, 200, 30], 2)
    pygame.draw.rect(screen, color, [70, y_cord - 15, length, 30])
    task = pygame.draw.circle(screen, color, (30, y_cord), 20, 5)
    value_text = FONT.render(str(round(value, 1)), True, WHITE)
    screen.blit(value_text, (16, y_cord - 10))

    return task, length, draw

def draw_buttons(color, x_coord, cost, man_cost, owned):
    """Draw upgrade and manager buttons."""
    color_button = pygame.draw.rect(screen, color, [x_coord, 600, 50, 30])
    color_cost = FONT.render(str(round(cost, 1)), True, BLACK)
    screen.blit(color_cost, (x_coord + 6, 605))

    if not owned:
        manager_button = pygame.draw.rect(screen, color, [x_coord, 670, 50, 30])
        manager_text = FONT.render(str(round(man_cost, 1)), True, BLACK)
        screen.blit(manager_text, (x_coord + 6, 675))
    else:
        manager_button = pygame.draw.rect(screen, BLACK, [x_coord, 670, 50, 30])

    return color_button, manager_button

def handle_events():
    """Handle user input events."""
    global total_money_earned

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logging.info("Game exited by user.")
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(5):
                if tasks[i].collidepoint(event.pos):
                    draw_bar_filling[i] = True

            for i in range(5):
                if manager_buttons[i].collidepoint(event.pos) and total_money_earned >= MANAGER_COSTS[i] and not manager_owned[i]:
                    manager_owned[i] = True
                    total_money_earned -= MANAGER_COSTS[i]

            for i in range(5):
                if upgrade_buttons[i].collidepoint(event.pos) and total_money_earned >= button_upgrade_costs[i]:
                    total_money_earned -= button_upgrade_costs[i]

                    if button_upgrade_costs[i] < LATE_GAME_THRESHOLDS[i]:
                        money_on_button_press[i] += MONEY_INCREASE[i][0]
                        button_upgrade_costs[i] *= UPGRADE_SCALING[i][0]
                    else:
                        money_on_button_press[i] += MONEY_INCREASE[i][1]
                        button_upgrade_costs[i] *= UPGRADE_SCALING[i][1]

    return True

def main():
    """Main game loop."""
    global screen, total_money_earned, draw_bar_filling, percent_fill_for_i, tasks, upgrade_buttons, manager_buttons

    # Initialize game state
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Idle Clicker Game')
    background = BLACK
    clock = pygame.time.Clock()

    # Initialize missing variables
    global bar_filling_speed, money_on_button_press, button_upgrade_costs, manager_owned
    bar_filling_speed = [5, 4, 3, 2, 1]
    money_on_button_press = [1, 2, 3, 4, 5]
    button_upgrade_costs = list(range(1, 6))
    manager_owned = [False] * 5

    total_money_earned = 0
    draw_bar_filling = [False] * 5
    percent_fill_for_i = [0] * 5

    running = True
    while running:
        clock.tick(FRAME_RATE)

        for i in range(5):
            if manager_owned[i] and not draw_bar_filling[i]:
                draw_bar_filling[i] = True

        running = handle_events()

        screen.fill(background)

        tasks = []
        for i in range(5):
            task, percent_fill_for_i[i], draw_bar_filling[i] = draw_box(
                BUTTON_COLORS[i], BUTTON_Y_POSITIONS[i],
                money_on_button_press[i], draw_bar_filling[i],
                percent_fill_for_i[i], bar_filling_speed[i]
            )
            tasks.append(task)

        upgrade_buttons = []
        manager_buttons = []
        for i in range(5):
            upgrade_btn, manager_btn = draw_buttons(
                BUTTON_COLORS[i], BUTTON_X_POSITIONS[i],
                button_upgrade_costs[i], MANAGER_COSTS[i], manager_owned[i]
            )
            upgrade_buttons.append(upgrade_btn)
            manager_buttons.append(manager_btn)

        display_money = FONT.render(f'Money: ${round(total_money_earned, 2)}', True, WHITE, BLACK)
        screen.blit(display_money, (10, 5))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
