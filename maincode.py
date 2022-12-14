#Importing Libraries
import pygame
import sys

#Defining Constants
FPS = 60
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
LIGHT_GRAY = (160, 160, 160)
DARK_GRAY = (140, 140, 140)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)
TRACK_CURVATURES = [0, 0.0015, 0, 0, 0.0015, 0, 0, -0.0015, 0]
TRACK_INDEX = 0
SEGMENT_DIVIDER_POSITION = SCREEN_HEIGHT//5

#Defining Pygame Objects
clock = pygame.time.Clock()
main_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('FOREST DASH')

#Function to Draw Sky
def draw_sky():
    sky_rectangle = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//5)
    pygame.draw.rect(main_window, BLUE, sky_rectangle)

#Function to Draw a Straight Road
def draw_straight_road(forward_backward_offset, left_right_offset):
    ORIGINAL_TEXTURE_WIDTH = (4 * SCREEN_HEIGHT//5) // 5
    for y in range(SCREEN_HEIGHT, SCREEN_HEIGHT//5 - 1, -1):
        THRESHOLD = 6
        SCALING_FACTOR = 20
        ROAD_SLOPE_INVERSE = 0.35
        STRIPE_SLOPE_INVERSE = 0.08
        BOUNDARY_WIDTH = 20
        STRIPE_WIDTH = 30
        z_map = SCREEN_HEIGHT/y * SCALING_FACTOR + forward_backward_offset
        while (z_map >= 2 * THRESHOLD):
            z_map -= 2 * THRESHOLD
        while (z_map < 0):
            z_map += 2 * THRESHOLD
        if z_map <= THRESHOLD:
            ROAD_COLOR = LIGHT_GRAY
            BOUNDARY_COLOR = RED
            GRASS_COLOR = LIGHT_GREEN
        else:
            ROAD_COLOR = DARK_GRAY
            BOUNDARY_COLOR = WHITE
            GRASS_COLOR = DARK_GREEN
        if SCREEN_HEIGHT - y <= ORIGINAL_TEXTURE_WIDTH:
            BOUNDARY_START_INDEX = BOUNDARY_WIDTH - (ORIGINAL_TEXTURE_WIDTH - (SCREEN_HEIGHT - y)) * ROAD_SLOPE_INVERSE + left_right_offset
            if BOUNDARY_START_INDEX < 0:
                BOUNDARY_END_INDEX = SCREEN_WIDTH - BOUNDARY_START_INDEX + 2 * left_right_offset
                pygame.draw.line(main_window, ROAD_COLOR, (0, y), (BOUNDARY_END_INDEX, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_END_INDEX, y), (BOUNDARY_END_INDEX + BOUNDARY_WIDTH, y))
                pygame.draw.line(main_window, GRASS_COLOR, (BOUNDARY_END_INDEX + BOUNDARY_WIDTH, y), (SCREEN_WIDTH, y))
            else:
                BOUNDARY_END_INDEX = SCREEN_WIDTH - BOUNDARY_START_INDEX + 2 * left_right_offset
                if BOUNDARY_START_INDEX - BOUNDARY_WIDTH > 0:
                    pygame.draw.line(main_window, GRASS_COLOR, (0, y), (BOUNDARY_START_INDEX - BOUNDARY_WIDTH, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_START_INDEX - BOUNDARY_WIDTH, y), (BOUNDARY_START_INDEX, y))
                pygame.draw.line(main_window, ROAD_COLOR, (BOUNDARY_START_INDEX, y), (BOUNDARY_END_INDEX, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_END_INDEX, y), (BOUNDARY_END_INDEX + BOUNDARY_WIDTH, y))
                if BOUNDARY_END_INDEX + BOUNDARY_WIDTH < SCREEN_WIDTH:
                    pygame.draw.line(main_window, GRASS_COLOR, (BOUNDARY_END_INDEX + BOUNDARY_WIDTH, y), (SCREEN_WIDTH, y))
            if ROAD_COLOR == DARK_GRAY:
                ROAD_WIDTH = BOUNDARY_END_INDEX - BOUNDARY_START_INDEX  
                LEFT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH - 0.5 * ROAD_WIDTH) + left_right_offset
                RIGHT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH + 0.5 * ROAD_WIDTH) + left_right_offset
                CURR_STRIPE_WIDTH = STRIPE_WIDTH - 0.5 * (SCREEN_HEIGHT - y) * STRIPE_SLOPE_INVERSE
                LEFT_STRIPE_START = LEFT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                LEFT_STRIPE_END = LEFT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_START = RIGHT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_END = RIGHT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                pygame.draw.line(main_window, WHITE, (LEFT_STRIPE_START, y), (LEFT_STRIPE_END, y))
                pygame.draw.line(main_window, WHITE, (RIGHT_STRIPE_START, y), (RIGHT_STRIPE_END, y))
        else:
            ROAD_WIDTH = SCREEN_WIDTH - 2 * ROAD_SLOPE_INVERSE * (SCREEN_HEIGHT - y - ORIGINAL_TEXTURE_WIDTH) 
            ROAD_START_X = 0.5 * (SCREEN_WIDTH - ROAD_WIDTH) + left_right_offset
            ROAD_END_X = 0.5 * (SCREEN_WIDTH + ROAD_WIDTH) + left_right_offset
            pygame.draw.line(main_window, GRASS_COLOR, (0, y), (ROAD_START_X, y))
            pygame.draw.line(main_window, BOUNDARY_COLOR, (ROAD_START_X, y), (ROAD_START_X + BOUNDARY_WIDTH, y))
            pygame.draw.line(main_window, ROAD_COLOR, (ROAD_START_X + BOUNDARY_WIDTH, y), (ROAD_END_X - BOUNDARY_WIDTH, y))
            pygame.draw.line(main_window, BOUNDARY_COLOR, (ROAD_END_X - BOUNDARY_WIDTH, y), (ROAD_END_X, y))
            pygame.draw.line(main_window, GRASS_COLOR, (ROAD_END_X, y), (SCREEN_WIDTH, y))
            if ROAD_COLOR == DARK_GRAY: 
                ROAD_WIDTH = ROAD_END_X - ROAD_START_X - 2 * BOUNDARY_WIDTH
                LEFT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH - 0.5 * ROAD_WIDTH) + left_right_offset
                RIGHT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH + 0.5 * ROAD_WIDTH) + left_right_offset
                CURR_STRIPE_WIDTH = STRIPE_WIDTH - 0.5 * (SCREEN_HEIGHT - y) * STRIPE_SLOPE_INVERSE
                LEFT_STRIPE_START = LEFT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                LEFT_STRIPE_END = LEFT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_START = RIGHT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_END = RIGHT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                pygame.draw.line(main_window, WHITE, (LEFT_STRIPE_START, y), (LEFT_STRIPE_END, y))
                pygame.draw.line(main_window, WHITE, (RIGHT_STRIPE_START, y), (RIGHT_STRIPE_END, y))

#Function to Draw a Curved Road
def draw_curved_road(forward_backward_offset, left_right_offset, curr_speed = 0):
    global TRACK_INDEX, SEGMENT_DIVIDER_POSITION
    leading_segment_curvature = TRACK_CURVATURES[(TRACK_INDEX + 1) % len(TRACK_CURVATURES)]
    lagging_segment_curvature = TRACK_CURVATURES[TRACK_INDEX]
    ORIGINAL_TEXTURE_WIDTH = (4 * SCREEN_HEIGHT//5) // 5
    SCALING_FACTOR = 20
    if SEGMENT_DIVIDER_POSITION > SCREEN_HEIGHT:
        SEGMENT_DIVIDER_POSITION = SCREEN_HEIGHT//5
        TRACK_INDEX = (TRACK_INDEX + 1) % len(TRACK_CURVATURES)
    if SEGMENT_DIVIDER_POSITION < SCREEN_HEIGHT//5:
        SEGMENT_DIVIDER_POSITION = SCREEN_HEIGHT
        TRACK_INDEX = TRACK_INDEX - 1
        if TRACK_INDEX < 0:
            TRACK_INDEX = len(TRACK_CURVATURES) - 1
    leading_segment_curvature = TRACK_CURVATURES[(TRACK_INDEX + 1) % len(TRACK_CURVATURES)]
    lagging_segment_curvature = TRACK_CURVATURES[TRACK_INDEX]
    curvature_offset_increase = 0
    curvature_offset = 0
    for y in range(SCREEN_HEIGHT, SCREEN_HEIGHT//5 - 1, -1):
        THRESHOLD = 6
        ROAD_SLOPE_INVERSE = 0.35
        STRIPE_SLOPE_INVERSE = 0.08
        BOUNDARY_WIDTH = 20
        STRIPE_WIDTH = 30
        z_map = SCREEN_HEIGHT/y * SCALING_FACTOR + forward_backward_offset
        if y >= SEGMENT_DIVIDER_POSITION:
            curr_segment_curvature = lagging_segment_curvature
        else:
            curr_segment_curvature = leading_segment_curvature
        curvature_offset_increase += curr_segment_curvature
        curvature_offset += curvature_offset_increase
        while (z_map >= 2 * THRESHOLD):
            z_map -= 2 * THRESHOLD
        while (z_map < 0):
            z_map += 2 * THRESHOLD
        if z_map <= THRESHOLD:
            ROAD_COLOR = LIGHT_GRAY
            BOUNDARY_COLOR = RED
            GRASS_COLOR = LIGHT_GREEN
        else:
            ROAD_COLOR = DARK_GRAY
            BOUNDARY_COLOR = WHITE
            GRASS_COLOR = DARK_GREEN
        if SCREEN_HEIGHT - y <= ORIGINAL_TEXTURE_WIDTH:
            BOUNDARY_START_INDEX = BOUNDARY_WIDTH - (ORIGINAL_TEXTURE_WIDTH - (SCREEN_HEIGHT - y)) * ROAD_SLOPE_INVERSE + left_right_offset
            if BOUNDARY_START_INDEX < 0:
                BOUNDARY_END_INDEX = SCREEN_WIDTH - BOUNDARY_START_INDEX + 2 * left_right_offset
                pygame.draw.line(main_window, ROAD_COLOR, (0, y), (BOUNDARY_END_INDEX + curvature_offset, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_END_INDEX + curvature_offset, y), (BOUNDARY_END_INDEX + BOUNDARY_WIDTH + curvature_offset, y))
                pygame.draw.line(main_window, GRASS_COLOR, (BOUNDARY_END_INDEX + BOUNDARY_WIDTH + curvature_offset, y), (SCREEN_WIDTH, y))
            else:
                BOUNDARY_END_INDEX = SCREEN_WIDTH - BOUNDARY_START_INDEX + 2 * left_right_offset
                if BOUNDARY_START_INDEX - BOUNDARY_WIDTH > 0:
                    pygame.draw.line(main_window, GRASS_COLOR, (0, y), (BOUNDARY_START_INDEX - BOUNDARY_WIDTH + curvature_offset, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_START_INDEX - BOUNDARY_WIDTH + curvature_offset, y), (BOUNDARY_START_INDEX + curvature_offset, y))
                pygame.draw.line(main_window, ROAD_COLOR, (BOUNDARY_START_INDEX + curvature_offset, y), (BOUNDARY_END_INDEX + curvature_offset, y))
                pygame.draw.line(main_window, BOUNDARY_COLOR, (BOUNDARY_END_INDEX + curvature_offset, y), (BOUNDARY_END_INDEX + BOUNDARY_WIDTH + curvature_offset, y))
                if BOUNDARY_END_INDEX + BOUNDARY_WIDTH < SCREEN_WIDTH:
                    pygame.draw.line(main_window, GRASS_COLOR, (BOUNDARY_END_INDEX + BOUNDARY_WIDTH + curvature_offset, y), (SCREEN_WIDTH, y))
            if ROAD_COLOR == DARK_GRAY:
                ROAD_WIDTH = BOUNDARY_END_INDEX - BOUNDARY_START_INDEX  
                LEFT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH - 0.5 * ROAD_WIDTH) + left_right_offset
                RIGHT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH + 0.5 * ROAD_WIDTH) + left_right_offset
                CURR_STRIPE_WIDTH = STRIPE_WIDTH - 0.5 * (SCREEN_HEIGHT - y) * STRIPE_SLOPE_INVERSE
                LEFT_STRIPE_START = LEFT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                LEFT_STRIPE_END = LEFT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_START = RIGHT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_END = RIGHT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                pygame.draw.line(main_window, WHITE, (LEFT_STRIPE_START + curvature_offset, y), (LEFT_STRIPE_END + curvature_offset, y))
                pygame.draw.line(main_window, WHITE, (RIGHT_STRIPE_START + curvature_offset, y), (RIGHT_STRIPE_END + curvature_offset, y))
        else:
            ROAD_WIDTH = SCREEN_WIDTH - 2 * ROAD_SLOPE_INVERSE * (SCREEN_HEIGHT - y - ORIGINAL_TEXTURE_WIDTH) 
            ROAD_START_X = 0.5 * (SCREEN_WIDTH - ROAD_WIDTH) + left_right_offset
            ROAD_END_X = 0.5 * (SCREEN_WIDTH + ROAD_WIDTH) + left_right_offset
            pygame.draw.line(main_window, GRASS_COLOR, (0, y), (ROAD_START_X + curvature_offset, y))
            pygame.draw.line(main_window, BOUNDARY_COLOR, (ROAD_START_X + curvature_offset, y), (ROAD_START_X + BOUNDARY_WIDTH + curvature_offset, y))
            pygame.draw.line(main_window, ROAD_COLOR, (ROAD_START_X + BOUNDARY_WIDTH + curvature_offset, y), (ROAD_END_X - BOUNDARY_WIDTH + curvature_offset, y))
            pygame.draw.line(main_window, BOUNDARY_COLOR, (ROAD_END_X - BOUNDARY_WIDTH + curvature_offset, y), (ROAD_END_X + curvature_offset, y))
            pygame.draw.line(main_window, GRASS_COLOR, (ROAD_END_X + curvature_offset, y), (SCREEN_WIDTH, y))
            if ROAD_COLOR == DARK_GRAY: 
                ROAD_WIDTH = ROAD_END_X - ROAD_START_X - 2 * BOUNDARY_WIDTH
                LEFT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH - 0.5 * ROAD_WIDTH) + left_right_offset
                RIGHT_STRIPE_CENTER = 0.5 * (SCREEN_WIDTH + 0.5 * ROAD_WIDTH) + left_right_offset
                CURR_STRIPE_WIDTH = STRIPE_WIDTH - 0.5 * (SCREEN_HEIGHT - y) * STRIPE_SLOPE_INVERSE
                LEFT_STRIPE_START = LEFT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                LEFT_STRIPE_END = LEFT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_START = RIGHT_STRIPE_CENTER - 0.5 * CURR_STRIPE_WIDTH
                RIGHT_STRIPE_END = RIGHT_STRIPE_CENTER + 0.5 * CURR_STRIPE_WIDTH
                pygame.draw.line(main_window, WHITE, (LEFT_STRIPE_START + curvature_offset, y), (LEFT_STRIPE_END + curvature_offset, y))
                pygame.draw.line(main_window, WHITE, (RIGHT_STRIPE_START + curvature_offset, y), (RIGHT_STRIPE_END + curvature_offset, y))
    SEGMENT_DIVIDER_POSITION += curr_speed


#Function to Draw Objects
def draw_function(forward_backward_offset = 0, left_right_offset = 0, curr_speed = 0):
    draw_sky()
    draw_curved_road(forward_backward_offset, left_right_offset, curr_speed)
    pygame.display.update()

#Main Game Loop
def main():
    run = True
    clock.tick(FPS)
    FORWARD_BACKWARD_OFFSET = 0
    LEFT_RIGHT_OFFSET = 0
    FORWARD_ACCELERATION_COUNTER = 0
    BACKWARD_ACCELERATION_COUNTER = 0
    curvature_counter = 0
    curr_speed = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP]:
            if FORWARD_ACCELERATION_COUNTER < 300:
                FORWARD_ACCELERATION_COUNTER = FORWARD_ACCELERATION_COUNTER + 1
            if FORWARD_ACCELERATION_COUNTER <= 50:
                FORWARD_BACKWARD_OFFSET += 0.01
                curvature_counter += 1
                curr_speed = 0.01
            elif FORWARD_ACCELERATION_COUNTER <= 100:
                FORWARD_BACKWARD_OFFSET += 0.03
                curvature_counter += 2
                curr_speed = 0.03
            elif FORWARD_ACCELERATION_COUNTER <= 150:
                FORWARD_BACKWARD_OFFSET += 0.09
                curvature_counter += 3
                curr_speed = 0.09
            elif FORWARD_ACCELERATION_COUNTER <= 200:
                FORWARD_BACKWARD_OFFSET += 0.27
                curvature_counter += 4
                curr_speed = 0.27
            elif FORWARD_ACCELERATION_COUNTER <= 250:
                FORWARD_BACKWARD_OFFSET += 0.81
                curvature_counter += 5
                curr_speed = 0.81
            else:
                FORWARD_BACKWARD_OFFSET += 2.43
                curvature_counter += 6
                curr_speed = 2.43
        else:
            if FORWARD_ACCELERATION_COUNTER >= 250:
                FORWARD_BACKWARD_OFFSET += 2.43
                curvature_counter += 6
                curr_speed = 2.43
            elif FORWARD_ACCELERATION_COUNTER >= 200:
                FORWARD_BACKWARD_OFFSET += 0.81
                curvature_counter += 5
                curr_speed = 0.81
            elif FORWARD_ACCELERATION_COUNTER >= 150:
                FORWARD_BACKWARD_OFFSET += 0.27
                curvature_counter += 4
                curr_speed = 0.27
            elif FORWARD_ACCELERATION_COUNTER >= 100:
                FORWARD_BACKWARD_OFFSET += 0.09
                curvature_counter += 3
                curr_speed = 0.09
            elif FORWARD_ACCELERATION_COUNTER >= 50:
                FORWARD_BACKWARD_OFFSET += 0.03
                curvature_counter += 2
                curr_speed = 0.03
            elif FORWARD_ACCELERATION_COUNTER > 0:
                FORWARD_BACKWARD_OFFSET += 0.01
                curvature_counter += 1
                curr_speed = 0.01
            if FORWARD_ACCELERATION_COUNTER > 0:
                FORWARD_ACCELERATION_COUNTER = FORWARD_ACCELERATION_COUNTER - 1
        if keys_pressed[pygame.K_DOWN]:
            if BACKWARD_ACCELERATION_COUNTER < 300:
                BACKWARD_ACCELERATION_COUNTER = BACKWARD_ACCELERATION_COUNTER + 1
            if BACKWARD_ACCELERATION_COUNTER <= 50:
                FORWARD_BACKWARD_OFFSET -= 0.01
                curvature_counter -= 1
                curr_speed = -0.01
            elif BACKWARD_ACCELERATION_COUNTER <= 100:
                FORWARD_BACKWARD_OFFSET -= 0.03
                curvature_counter -= 2
                curr_speed = -0.03
            elif BACKWARD_ACCELERATION_COUNTER <= 150:
                FORWARD_BACKWARD_OFFSET -= 0.09
                curvature_counter -= 3
                curr_speed = -0.09
            elif BACKWARD_ACCELERATION_COUNTER <= 200:
                FORWARD_BACKWARD_OFFSET -= 0.27
                curvature_counter -= 4
                curr_speed = -0.27
            elif BACKWARD_ACCELERATION_COUNTER <= 250:
                FORWARD_BACKWARD_OFFSET -= 0.81
                curvature_counter -= 5
                curr_speed = -0.81
            else:
                FORWARD_BACKWARD_OFFSET -= 2.43
                curvature_counter -= 6  
                curr_speed = -2.43 
        else:
            if BACKWARD_ACCELERATION_COUNTER >= 250:
                FORWARD_BACKWARD_OFFSET -= 2.43
                curvature_counter -= 6
                curr_speed = -2.43
            elif BACKWARD_ACCELERATION_COUNTER >= 200:
                FORWARD_BACKWARD_OFFSET -= 0.81
                curvature_counter -= 5
                curr_speed = -0.81
            elif BACKWARD_ACCELERATION_COUNTER >= 150:
                FORWARD_BACKWARD_OFFSET -= 0.27
                curvature_counter -= 4
                curr_speed = -0.27
            elif BACKWARD_ACCELERATION_COUNTER >= 100:
                FORWARD_BACKWARD_OFFSET -= 0.09
                curvature_counter -= 3
                curr_speed = -0.09
            elif BACKWARD_ACCELERATION_COUNTER >= 50:
                FORWARD_BACKWARD_OFFSET -= 0.03
                curvature_counter -= 2
                curr_speed = -0.03
            elif BACKWARD_ACCELERATION_COUNTER > 0:
                FORWARD_BACKWARD_OFFSET -= 0.01
                curvature_counter -= 1
                curr_speed = -0.01
            if BACKWARD_ACCELERATION_COUNTER > 0:
                BACKWARD_ACCELERATION_COUNTER = BACKWARD_ACCELERATION_COUNTER - 1 
        if keys_pressed[pygame.K_LEFT]:
            LEFT_RIGHT_OFFSET += 5
        if keys_pressed[pygame.K_RIGHT]:
            LEFT_RIGHT_OFFSET -= 5       
        draw_function(FORWARD_BACKWARD_OFFSET, LEFT_RIGHT_OFFSET, curr_speed)
    pygame.quit()

#Gatekeeper Function
if __name__ == '__main__':
    main()