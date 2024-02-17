from gpiozero import Button
import time
from ADCDevice import *

import pygame
import random

Z_Pin = 18      # define Z_Pin
button = Button(Z_Pin) # define Button pin according to BCM Numbering
adc = ADCDevice() # Define an ADCDevice class object

center_x, center_y = 129, 132
left, right = center_x + 50, center_x - 50
up, down = center_y + 50, center_x - 50

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        # print("No correct I2C address found, \n"
        # "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        # "Program Exit. \n");
        exit(-1)

def loop():

    def display_text(text, x, y):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

    def compute_distance(x, y):
        return ((x[0] - y[0])**2 + (x[1] - y[1])**2) ** 0.5

    def check_for_collision_with_targets(player, targets, radius, margin_of_error, compute_distance):
        t1, t2, t3 = targets["target1"], targets["target2"], targets["target3"]
        d1 = compute_distance(player, t1)
        d2 = compute_distance(player, t2)
        d3 = compute_distance(player, t3)
        if d1 <= 2 * radius + margin_of_error:
            return (True, "target1")
        elif d2 <= 2 * radius + margin_of_error:
            return (True, "target2")
        elif d3 <= 2 * radius + margin_of_error:
            return (True, "target3")
        else:
            return (False, "")
        
    def get_random_coordinates():
        x_left = 10
        x_right = 790
        y_bottom = 10
        y_top = 500
        return [random.randint(x_left, x_right), random.randint(y_bottom, y_top)]
    
    def check_targets_overlap(targets, radius, margin_of_error, get_random_coordinates, compute_distance):
        t1, t2, t3 = targets["target1"], targets["target2"], targets["target3"]
        while True:
            d12 = compute_distance(t1, t2)
            d13 = compute_distance(t1, t3)
            d23 = compute_distance(t2, t3)
            if d12 <= 2 * radius + margin_of_error:
                t1 = get_random_coordinates()
                continue
            if d13 <= 2 * radius + margin_of_error:
                t3 = get_random_coordinates()
                continue
            if d23 <= 2 * radius + margin_of_error:
                t3 = get_random_coordinates()
                continue
            break
        return dict(target1 = t1, target2 = t2, target3 = t3)
    
    def spawn_new_ball(to_replace, targets, player_1, npc, radius, margin_of_error, get_random_coordinates, compute_distance):
        t1, t2, t3 = targets["target1"], targets["target2"], targets["target3"]
        old_coordinates = targets[to_replace]
        while True:
            
            if to_replace == "target1":
                t1 = get_random_coordinates()

                # Compute distances
                d2self = compute_distance(t1, old_coordinates)
                d12 = compute_distance(t1, t2)
                d13 = compute_distance(t1, t3)
                d2player = compute_distance(t1, player_1)
                d2npc = compute_distance(t1, npc)

                if d2self <= 2 * radius + margin_of_error:
                    t1 = get_random_coordinates()
                    continue
                if d12 <= 2 * radius + margin_of_error:
                    t1 = get_random_coordinates()
                    continue
                if d13 <= 2 * radius + margin_of_error:
                    t1 = get_random_coordinates()
                    continue
                if d2player <= 2 * radius + margin_of_error:
                    t1 = get_random_coordinates()
                    continue
                if d2npc <= 2 * radius + margin_of_error:
                    t1 = get_random_coordinates()
                    continue
                
                break

            elif to_replace == "target2":
                t2 = get_random_coordinates()
                
                # Compute distances
                d2self = compute_distance(t2, old_coordinates)
                d12 = compute_distance(t1, t2)
                d23 = compute_distance(t2, t3)
                d2player = compute_distance(t2, player_1)
                d2npc = compute_distance(t2, npc)

                if d2self <= 2 * radius + margin_of_error:
                    t2 = get_random_coordinates()
                    continue
                if d12 <= 2 * radius + margin_of_error:
                    t2 = get_random_coordinates()
                    continue
                if d23 <= 2 * radius + margin_of_error:
                    t2 = get_random_coordinates()
                    continue
                if d2player <= 2 * radius + margin_of_error:
                    t2 = get_random_coordinates()
                    continue
                if d2npc <= 2 * radius + margin_of_error:
                    t2 = get_random_coordinates()
                    continue
                break
            else:
                t3 = get_random_coordinates()
                
                # Compute distances
                d2self = compute_distance(t3, old_coordinates)
                d13 = compute_distance(t1, t3)
                d23 = compute_distance(t2, t3)
                d2player = compute_distance(t3, player_1)
                d2npc = compute_distance(t3, npc)

                if d2self <= 2 * radius + margin_of_error:
                    t3 = get_random_coordinates()
                    continue
                if d13 <= 2 * radius + margin_of_error:
                    t3 = get_random_coordinates()
                    continue
                if d23 <= 2 * radius + margin_of_error:
                    t3 = get_random_coordinates()
                    continue
                if d2player <= 2 * radius + margin_of_error:
                    t3 = get_random_coordinates()
                    continue
                if d2npc <= 2 * radius + margin_of_error:
                    t3 = get_random_coordinates()
                    continue
                break
        return dict(target1 = t1, target2 = t2, target3 = t3)


    def move_npc(position, targets, player_score, npc_score, compute_distance):
        npc_speed = 2.2
        if player_score > npc_score and npc_score > 0:
            multiplier = (player_score / npc_score)
        else:
            multiplier = 1
        npc_speed *= multiplier
        t1, t2, t3 = targets["target1"], targets["target2"], targets["target3"]
        dt1 = compute_distance(t1, position)
        dt2 = compute_distance(t2, position)
        dt3 = compute_distance(t3, position)
        if dt1 <= dt2 and dt1 <= dt3:
            # move towards 1
            target = t1
        elif dt2 <= dt1 and dt2 <= dt3:
            # move towards 2
            target = t2
        else:
            # move towards 3
            target = t3
        x = target[0] - position[0]
        y = target[1] - position[1]
        norm = (x**2 + y**2) ** 0.5
        x /= norm
        y /= norm
        position[0] += x * npc_speed
        position[1] += y * npc_speed
        return position
    
    pygame.init()

    # Game variables
    TOTAL_GAME_TIME = 60
    score = 0
    npc_score = 0
    timer = TOTAL_GAME_TIME
    speed = 3
    start_count_down = 5
    game_over = False
    
    # helps handle collision margin of error on the distance computation
    margin_of_error = 2 

    in_main_menu = True
    counting_down = False
    

    # Set up the screen
    size = width, height = 800, 600
    bg_color = 152, 152, 255
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Capture the Balls")
    font = pygame.font.Font(None, 36)

    # Button set up
    button_color = (96, 96, 96)
    button_hover_color = (128, 128, 128)
    button_text_color = (255, 255, 255)
    start_button_text = font.render("Start Game", True, button_text_color)
    start_button = pygame.Rect(width // 2 - 75, height // 2 - 25, 150, 50)
    restart_button_text = font.render("Restart Game", True, button_text_color)
    restart_button = pygame.Rect(width // 2 - 80, height // 2 , 175, 50)

    # Set up the dot
    dot_radius = 10
    dot_color = 255, 255, 255
    target_dot_color = 255, 51, 51

    # Set up player 1
    player_1_position = [width // 2, height // 2]

    # Set up NPC
    npc_position = [width // 2, height // 2]
    npc_color = 0, 0, 0

    # Set up targets
    target_dot_position = get_random_coordinates()
    targets = dict(
        target1 = get_random_coordinates(),
        target2 = get_random_coordinates(),
        target3 = get_random_coordinates()
    )
    targets = check_targets_overlap(targets, dot_radius, margin_of_error, get_random_coordinates, compute_distance)
    
    while True:
        # check for events - looking for quit and for hitting the Start Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN: # hit start button
                mouse_pos = pygame.mouse.get_pos()
                if game_over:
                    # look for restart button click
                    if restart_button.collidepoint(mouse_pos):
                        # restart button clicked - reset variables and go to main menu
                        targets = dict(
                            target1 = get_random_coordinates(),
                            target2 = get_random_coordinates(),
                            target3 = get_random_coordinates()
                        )
                        targets = check_targets_overlap(targets, dot_radius, margin_of_error, get_random_coordinates, compute_distance)
                        score = 0
                        npc_score = 0
                        in_main_menu = True
                        counting_down = False
                        timer = TOTAL_GAME_TIME
                        start_count_down = 5
                        game_over = False
                else:
                    # in main menu looking for start button click
                    if start_button.collidepoint(mouse_pos):
                        in_main_menu = False
                        counting_down = True
                        count_down_clock = pygame.time.Clock()                
                
        if game_over:
            screen.fill(bg_color)
            display_text(f"Player score: {score}", width // 2 - 72, height // 2 - 170)
            display_text(f"NPC score: {npc_score}", width // 2 - 72, height // 2 - 115)
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, button_hover_color, restart_button)
            else:
                pygame.draw.rect(screen, button_color, restart_button)
            screen.blit(restart_button_text, (restart_button.x + 10, restart_button.y + 10))
            pygame.display.flip()
            val_Z = not button.value     # read digital value of axis Z
            if val_Z == 0:
                # restart button clicked - reset variables and go to main menu
                targets = dict(
                    target1 = get_random_coordinates(),
                    target2 = get_random_coordinates(),
                    target3 = get_random_coordinates()
                )
                targets = check_targets_overlap(targets, dot_radius, margin_of_error, get_random_coordinates, compute_distance)
                score = 0
                npc_score = 0
                in_main_menu = True
                counting_down = False
                timer = TOTAL_GAME_TIME
                start_count_down = 5
                game_over = False
            continue
        
        if in_main_menu:
            val_Z = not button.value     # read digital value of axis Z
            if val_Z == 0:
                in_main_menu = False
                counting_down = True
                count_down_clock = pygame.time.Clock()
                continue
            screen.fill(bg_color)
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, button_hover_color, start_button)
            else:
                pygame.draw.rect(screen, button_color, start_button)
            screen.blit(start_button_text, (start_button.x + 10, start_button.y + 10))
            pygame.display.flip()
        else:
            if counting_down:
                start_count_down -= count_down_clock.get_time() / 1000
                if start_count_down <= 0:
                    counting_down = False
                    # start the clock for the game
                    clock = pygame.time.Clock()
                else:
                    screen.fill(bg_color)
                    display_text(f"Starting in {int(start_count_down)}", width//2 - 72, height // 2 - 15)
                    pygame.display.flip()
                    count_down_clock.tick(60)
                    continue

            # Code doesn't get here until the Count Down has ended and the game has begun
            if timer > 0:
                # There is still time on the clock
                timer -= clock.get_time() / 1000
            else:
                # Time has ended...so has the game
                game_over = True
                continue
            

            # print(f"Distance to target: {distance_to_target}")
            val_Y = adc.analogRead(0)    # read analog value of axis X and Y
            val_X = adc.analogRead(1)

            if val_X >= left and player_1_position[0] > dot_radius:
                player_1_position[0] -= speed
            elif val_X <= right and player_1_position[0] < width - dot_radius:
                player_1_position[0] += speed
            if val_Y >= up and player_1_position[1] > dot_radius:
                player_1_position[1] -= speed
            elif val_Y <= down and player_1_position[1] < height - dot_radius:
                player_1_position[1] += speed
            
            npc_position = move_npc(npc_position, targets, score, npc_score, compute_distance)

            # Fill the screen with the background color to erase the previous frame
            screen.fill(bg_color)

            # Draw the dot
            pygame.draw.circle(screen, dot_color, player_1_position, dot_radius)
            pygame.draw.circle(screen, npc_color, npc_position, dot_radius)

            # Check for colisiondistance_to_targets = distance_to_targets(player_1_position, targets)
            player_collision = check_for_collision_with_targets(player_1_position, targets, dot_radius, margin_of_error, compute_distance)
            if player_collision[0]:
                collided_with = player_collision[1]
                score += 1
                targets = spawn_new_ball(collided_with, targets, player_1_position, npc_position, dot_radius, margin_of_error, get_random_coordinates, compute_distance)
                time.sleep(0.01)

            npc_collision = check_for_collision_with_targets(npc_position, targets, dot_radius, margin_of_error, compute_distance)
            if npc_collision[0]:
                collided_with = npc_collision[1]
                npc_score += 1
                targets = spawn_new_ball(collided_with, targets, player_1_position, npc_position, dot_radius, margin_of_error, get_random_coordinates, compute_distance)
                time.sleep(0.01)
            
            for t in targets:
                pygame.draw.circle(screen, target_dot_color, targets[t], dot_radius)

            display_text(f"Score: {score}", 10, 10)
            display_text(f"NPC Score: {npc_score}", 200, 10)
            display_text(f"Time: {int(timer)}", width - 150, 10)
            pygame.display.flip()
            clock.tick(60)

def destroy():
    adc.close()
    button.close()


if __name__ == '__main__':
    print ('Program is starting ... ') # Program entrance
    setup()
    try:
        loop()
        destroy()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        print("Ending program")
