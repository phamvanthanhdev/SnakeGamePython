from tabnanny import check
import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.director = Vector2(0,0)
        self.new_block = False
        self.isPause = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()

        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()

        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        
        self.crunch_sound = pygame.mixer.Sound('Sound/Sound_crunch.wav')
        self.over_sound = pygame.mixer.Sound('Sound/Sound_over.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previos_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previos_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previos_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect) 
                else:
                    if previos_block.x == -1 and next_block.y == -1 or next_block.x == -1 and previos_block.y == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previos_block.y == 1 and next_block.x == -1 or next_block.y == 1 and previos_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previos_block.x == 1 and next_block.y == 1 or next_block.x == 1 and previos_block.y == 1:
                        screen.blit(self.body_br, block_rect)
                    elif previos_block.x == 1 and next_block.y == -1 or next_block.x == 1 and previos_block.y == -1:
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(0,-1) : self.head = self.head_down
        elif head_relation == Vector2(0,1) : self.head = self.head_up
        elif head_relation == Vector2(-1,0) : self.head = self.head_right
        elif head_relation == Vector2(1,0) : self.head = self.head_left

    def update_tail_graphics(self):
        tail_relation = self.body[- 2] - self.body[- 1]
        if tail_relation == Vector2(0,-1) : self.tail = self.tail_down
        elif tail_relation == Vector2(0,1) : self.tail = self.tail_up
        elif tail_relation == Vector2(-1,0) : self.tail = self.tail_right
        elif tail_relation == Vector2(1,0) : self.tail = self.tail_left

    def move_snake(self):
        if self.isPause == False:
            if self.new_block == True:
                copy_body = self.body[:]
                copy_body.insert(0, self.body[0] + self.director)
                self.body = copy_body[:]
                self.new_block = False
            else:
                copy_body = self.body[:-1]
                copy_body.insert(0, self.body[0] + self.director)
                self.body = copy_body[:]
        else:
            copy_body = self.body[:]
            self.body = copy_body[:]
    
    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_over_sound(self):
        self.over_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.director = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.x * cell_size), int(self.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (126,166,114), fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

        self.music = pygame.mixer.Sound('Sound/Sound_background.wav')
        self.sound_background()

    def update(self):
        self.snake.move_snake()
        self.check_possition()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_possition(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print("bbb")
                self.game_over()


    def game_over(self):
        self.snake.play_over_sound()
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(57,74,12))
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright= (score_rect.left, score_rect.centery))

        screen.blit(score_surface,score_rect)
        screen.blit(apple, apple_rect)

    def sound_background(self):
        self.music.play(-1)


pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.director.y != 1:
                    main_game.snake.director = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.director.y != -1:
                    main_game.snake.director = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.director.x != 1:
                    main_game.snake.director = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.director.x != -1:
                    main_game.snake.director = Vector2(1,0)
            if event.key == pygame.K_SPACE:
                main_game.snake.isPause = False if main_game.snake.isPause else True
                

    screen.fill((175,215,70))
    main_game.draw_elements()

    if main_game.snake.isPause:
        screen.fill("black")
    pygame.display.update()
    clock.tick(60)  