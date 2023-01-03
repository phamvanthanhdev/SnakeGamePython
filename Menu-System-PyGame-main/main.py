import pygame, sys
from button import Button

from tabnanny import check
import pygame, sys, random
from pygame.math import Vector2

import time
import threading 

pygame.init()
cell_size = 40
cell_number_width = 25
cell_number_height = 17
screen = pygame.display.set_mode((25 * cell_size,17 * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
straw = pygame.image.load('Graphics/fence.png').convert_alpha()
bullet = pygame.image.load('Graphics/bullet.png').convert_alpha()
monster = pygame.image.load('Graphics/monster1.png').convert_alpha()
spider = pygame.image.load('Graphics/spider.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)
BG = pygame.image.load("assets/Background.png")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)


class SNAKE:
        def __init__(self):
            self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
            self.director = Vector2(1,0)
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
            self.shot_sound = pygame.mixer.Sound('Sound/Sound_shot.wav')

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

        def play_shot_sound(self):
            self.shot_sound.play()

        def reset(self):
            self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
            self.director = Vector2(1,0)

class FRUIT:
        def __init__(self):
            self.randomize()

        def draw_fruit(self):
            fruit_rect = pygame.Rect(int(self.x * cell_size), int(self.y * cell_size), cell_size, cell_size)
            screen.blit(apple, fruit_rect)
            #pygame.draw.rect(screen, (126,166,114), fruit_rect)
            
        def draw_monster(self):
            monster_rect = pygame.Rect(int(self.x * cell_size), int(self.y * cell_size), cell_size, cell_size)
            screen.blit(monster, monster_rect)

        def randomize(self):
            self.x = random.randint(0,cell_number_width - 1)
            self.y = random.randint(0,cell_number_height - 1)
            self.pos = Vector2(self.x, self.y)

class FENCE:
    def __init__(self):
        self.location = []
        self.num_fence = 3
        for i in range(self.num_fence):
            self.x = random.randint(0,cell_number_width - 1)
            self.y = random.randint(0,cell_number_height - 1)
            self.location.append(Vector2(self.x, self.y))

    def draw_fence(self):
        for i in range(self.num_fence):
            fence_rect = pygame.Rect(int(self.location[i].x * cell_size), int(self.location[i].y * cell_size), cell_size, cell_size)
            screen.blit(straw, fence_rect)
        #pygame.draw.rect(screen, (126,166,114), fruit_rect)
    def randomize(self):
        for i in range(self.num_fence):
            self.x = random.randint(0,cell_number_width - 1)
            self.y = random.randint(0,cell_number_height - 1)
            self.location[i] = (Vector2(self.x , self.y))
    def reset_fence(self):
        self.num_fence = 3
        self.randomize()

    def setting_fence(self):
        self.num_fence = 10
        for i in range(self.num_fence):
            self.x = random.randint(0,cell_number_width - 1)
            self.y = random.randint(0,cell_number_height - 1)
            self.location.append(Vector2(self.x, self.y))

class BULLET:
    def __init__(self):
        self.shoted()
        self.isShot = True
        #self.dis_bullet = main_game.snake.director
        self.bullet_relations = Vector2(0,0)

    def draw_bullet(self):
        bullet_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(bullet, bullet_rect)
        #pygame.draw.rect(screen, (126,166,114), fruit_rect)
    def move_bullet(self):
        self.pos = self.pos - self.bullet_relations
        
    def shoted(self):
        self.pos = Vector2(1,1)

class RAINBULLET:
    def __init__(self):
        self.bullet_all = []
        self.many_bl = []
        #self.n = 2
        self.many_relations = []
    def draw_many_bullet(self):
        for bu in self.many_bl:
            bullet_rect = pygame.Rect(int(bu.x * cell_size), int(bu.y * cell_size), cell_size, cell_size)
            screen.blit(bullet, bullet_rect)

    def move_many_bullet(self):
        for index in range(len(self.many_bl)):
            self.many_bl[index] = self.many_bl[index] + self.many_relations[index]

    def shoted(self):
        del self.many_bl[0]

class ACTION:
    def __init__(self):
        self.randomize()
        #self.pos = Vector2(1,1)
        self.action_relations = Vector2(1,0)
        #self.random_relation()
        self.move_action()

    def draw_action(self):
        fruit_rect = pygame.Rect(int(self.pos1.x * cell_size), int(self.pos1.y * cell_size), cell_size, cell_size)
        screen.blit(spider, fruit_rect)
        #pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number_width - 1)
        self.y = random.randint(0,cell_number_height - 1)
        self.pos1 = Vector2(self.x, self.y)

    def move_action(self):
        self.pos1 = self.pos1 - self.action_relations

    def random_relation(self):
        position = [Vector2(1,0), Vector2(0,1),Vector2(-1,0),Vector2(0,-1)]
        self.action_relations = position[random.randint(0,3)]

class MAIN:
        def __init__(self):
            self.snake = SNAKE()
            self.fruit = FRUIT()
            self.fence = FENCE()
            self.bullet = BULLET()
            self.many_bullets = RAINBULLET()
            self.action = ACTION()
            self.mode = "classic"

            #Phan de xu li them rao chan theo tung giay
            self.isAdd = True
            self.num = 0

            #Phan de xu li ban bong
            self.isShot2 = False

            #
            self.isMusic = True
            self.music = pygame.mixer.Sound('Sound/Sound_background.wav')
            self.sound_background()

        def update(self):
            self.snake.move_snake()
            self.check_possition()
            self.check_fail()

            if self.mode == "attack":
                self.action.move_action()

            if self.mode == "rain":
                self.many_bullets.move_many_bullet()

        def draw_elements(self):
            self.draw_grass()
            if main_game.mode == "attack":
                self.action.draw_action()
                self.action_through_wall()
                self.action_around_snake()
                self.fruit.pos = Vector2(-1,-1)
                self.draw_snake_on_head()
            else:
                self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
            #
            if self.mode == "trouble":
                self.fence.draw_fence()
                self.draw_snake_on_head()
            #

            if self.mode == "rain":
                self.many_bullets.draw_many_bullet()
                self.fence.draw_fence()
                self.draw_snake_on_head()

        def check_possition(self):
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

            if self.mode != "attack":
                if self.fruit.pos == self.snake.body[0]:
                    self.fruit.randomize()
                    self.snake.add_block()
                    self.snake.play_crunch_sound()
            else:
                if self.action.pos1 == self.snake.body[0]:
                    self.snake.add_block()
                    self.snake.play_crunch_sound()
                    self.action.randomize()
                    self.action.random_relation()
                for block in self.snake.body[1:]:
                    if block == self.action.pos1:
                        self.snake.add_block()
                        self.snake.play_crunch_sound()
                        self.action.randomize()
                        self.action.random_relation()
            
            if self.mode == "trouble":
                for i in range(self.fence.num_fence):
                    if self.fruit.pos == self.fence.location[i]:
                        self.fruit.randomize()
            
            #Bong cham ke thu thi thiet lap vi tri ke thu moi
            if self.mode == "rain":
                for i in range(len(self.many_bullets.many_bl)):
                    for j in range(self.fence.num_fence):
                        if self.many_bullets.many_bl[i] == self.fence.location[j]:
                            self.snake.add_block()
                            x = random.randint(0,cell_number_width - 1)
                            y = random.randint(0,cell_number_height - 1)
                            self.fence.location[j] = Vector2(x,y)
                            break
            
        def check_fail(self):
            if self.mode == "classic":
                #Chạm tường là thua
                if not 0 <= self.snake.body[0].x < cell_number_width or not 0 <= self.snake.body[0].y < cell_number_height:
                    overGame()

            for block in self.snake.body[1:]:
                if block == self.snake.body[0] :
                    overGame()

            if self.mode == "trouble" or self.mode == "rain":
                #cham vao chuong ngai vat
                for i in range(self.fence.num_fence):
                   if self.fence.location[i] == self.snake.body[0]:
                       overGame()

            #bong ban vao than ran thi thua
            if self.mode == "rain":
                for block in self.snake.body[1:]:
                    if block == self.bullet.pos:
                        overGame()
                
        #xử lí rắn đi xuyên tường
        def draw_snake_on_head(self):
            if 0 > self.snake.body[0].x:
                self.snake.director = Vector2(-1, 0)
                self.snake.body[0] = Vector2(cell_number_width - 1, self.snake.body[0].y)
            if cell_number_width == self.snake.body[0].x:
                self.snake.director = Vector2(1, 0)
                self.snake.body[0] = Vector2(0, self.snake.body[0].y)
            if 0 > self.snake.body[0].y:
                self.snake.director = Vector2(0, -1)
                self.snake.body[0] = Vector2(self.snake.body[0].x, cell_number_height - 1)
            if cell_number_height == self.snake.body[0].y:
                self.snake.director = Vector2(0, 1)
                self.snake.body[0] = Vector2(self.snake.body[0].x, 0)


        def game_over(self):
            self.snake.play_over_sound()
            self.snake.reset()
            #self.fence.reset_fence()

        def draw_grass(self):
            grass_color = (167,209,61)
            for row in range(cell_number_height):
                if row % 2 == 0:
                    for col in range(cell_number_width):
                        if col % 2 == 0:
                            grass_rect = pygame.Rect(col*cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(screen, grass_color, grass_rect)
                else:
                    for col in range(cell_number_width):
                        if col % 2 != 0:
                            grass_rect = pygame.Rect(col*cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(screen, grass_color, grass_rect)

        def draw_score(self):
            score_text = str(len(self.snake.body) - 3)
            score_surface = game_font.render(score_text,True,(57,74,12))
            score_x = int(cell_size*cell_number_width - 60)
            score_y = int(cell_size*cell_number_height - 40)
            score_rect = score_surface.get_rect(center = (score_x, score_y))
            apple_rect = apple.get_rect(midright= (score_rect.left, score_rect.centery))

            screen.blit(score_surface,score_rect)
            screen.blit(apple, apple_rect)
        
        def handle_shots(self):
            #Phan xu li ban bong
            if self.isShot2:
                clock.tick(30)
                #dis_bullet = self.snake.director
                if self.bullet.isShot :
                    self.bullet.bullet_relations = self.snake.body[1] - self.snake.body[0]
                    #self.bullet.pos = Vector2(self.snake.body[0].x + 1, self.snake.body[0].y)
                    self.bullet.isShot = False

                self.bullet.move_bullet()
            else:
                self.bullet.bullet_relations = self.snake.body[1] - self.snake.body[0]
                if self.bullet.bullet_relations == Vector2(-1,0):
                    self.bullet.pos = Vector2(self.snake.body[0].x + 1, self.snake.body[0].y)
                if self.bullet.bullet_relations == Vector2(1,0):
                    self.bullet.pos = Vector2(self.snake.body[0].x - 1, self.snake.body[0].y)
                if self.bullet.bullet_relations == Vector2(0,1):
                    self.bullet.pos = Vector2(self.snake.body[0].x, self.snake.body[0].y - 1)
                if self.bullet.bullet_relations == Vector2(0,-1):
                    self.bullet.pos = Vector2(self.snake.body[0].x, self.snake.body[0].y + 1)
        
        def action_through_wall(self):
            #xu li action di xuyen tuong
            if 0 > self.action.pos1.x:
                self.action.pos1 = Vector2(cell_number_width - 1, self.action.pos1.y)
            if cell_number_width == self.action.pos1.x:
                self.action.pos1 = Vector2(0, self.action.pos1.y)
            if 0 > self.action.pos1.y:
                self.action.pos1 = Vector2(self.action.pos1.x, cell_number_height - 1)
            if cell_number_height == self.action.pos1.y:
                self.action.pos1 = Vector2(self.action.pos1.x, 0)

        def action_around_snake(self):
            if (self.snake.body[0].x - self.action.pos1.x <= 3 or self.snake.body[0].x - self.action.pos1.x <= -3) and self.snake.body[0].y == self.action.pos1.y:
                self.action.random_relation()
            if (self.snake.body[0].y - self.action.pos1.y <= 3 or self.snake.body[0].y - self.action.pos1.y <= -3) and self.snake.body[0].x == self.action.pos1.x:
                self.action.random_relation()

        def sound_background(self):
            self.music.play(-1)
        
        def stop_sound_background(self):
            self.music.stop()

main_game = MAIN()

#Phần GamePlay
def playGame():
    t = time.localtime()
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
                    main_game.snake.isPause = True
                    optionsGame()   
                if event.key == pygame.K_q:
                    if main_game.mode == "rain":
                        handleRainShots()
    

        if main_game.mode == "trouble":
            handleTime(t)

        screen.fill((175,215,70))
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(60)

def handleTime(t):
    s = time.mktime(t)
    t1 = time.localtime()
    s1 = time.mktime(t1) + 1
    num_temp = main_game.fence.num_fence
    
    if main_game.isAdd:
        if int(s1 - s) % 5 == 0:
            main_game.num = int(s1 - s)
            main_game.fence.num_fence = num_temp + 1
            x = random.randint(0,cell_number_width - 1)
            y = random.randint(0,cell_number_height - 1)
            main_game.fence.location.append(Vector2(x ,y))
            main_game.isAdd = False

    if int(s1 - s) == main_game.num + 1:
        main_game.isAdd = True

    #num : sau mỗi lần thêm 1 fence, sau đó 1s isAdd = True và lọt vào điều kiện trên

def handleRainShots() :
    main_game.snake.play_shot_sound()

    bullet_relations_temp = main_game.snake.body[1] - main_game.snake.body[0]
    if bullet_relations_temp == Vector2(-1,0):
        bullet_pos = Vector2(main_game.snake.body[0].x + 1, main_game.snake.body[0].y)
    if bullet_relations_temp == Vector2(1,0):
        bullet_pos = Vector2(main_game.snake.body[0].x - 1, main_game.snake.body[0].y)
    if bullet_relations_temp == Vector2(0,1):
        bullet_pos = Vector2(main_game.snake.body[0].x, main_game.snake.body[0].y - 1)
    if bullet_relations_temp == Vector2(0,-1):
        bullet_pos = Vector2(main_game.snake.body[0].x, main_game.snake.body[0].y + 1)

    main_game.many_bullets.many_bl.append(bullet_pos)
    main_game.many_bullets.many_relations.append(-bullet_relations_temp)

#Phần Đồ họa
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def overGame():
    main_game.snake.play_over_sound()
    time.sleep(0.5)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")

        PLAY_TEXT = get_font(45).render("Diem cua ban : ", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(550, 120))
        screen.blit(PLAY_TEXT, PLAY_RECT)

        SCORE_TEXT = get_font(65).render(str(len(main_game.snake.body) - 3), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(540, 240))
        screen.blit(SCORE_TEXT, SCORE_RECT)

        PLAY_BACK = Button(image=None, pos=(540, 420), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_AGAIN = Button(image=None, pos=(540, 570), 
                            text_input="AGAIN", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)
        PLAY_AGAIN.changeColor(PLAY_MOUSE_POS)
        PLAY_AGAIN.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_game.snake.isPause = False
                    main_game.snake.reset()
                    #main_game.fence.reset_fence()
                    main_game.fruit.randomize()
                    main_menu()
                if PLAY_AGAIN.checkForInput(PLAY_MOUSE_POS):
                    main_game.snake.isPause = False
                    main_game.snake.reset()                 
                    #main_game.fence.reset_fence()
                    playGame()

        if main_game.mode == "rain":
            main_game.fence.randomize()
            main_game.many_bullets.many_bl = []
            main_game.many_bullets.many_relations = []

        if main_game.mode == "trouble":
            main_game.fence.reset_fence()

        pygame.display.update()  

def optionsGame():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(75).render("OPTIONS GAME", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(520, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_RESUME = Button(image=None, pos=(540, 260), 
                            text_input="RESUME", font=get_font(65), base_color="Black", hovering_color="Green")
        OPTIONS_MUSIC = Button(image=None, pos=(540, 400), 
                            text_input="MUSIC", font=get_font(65), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(540, 560), 
                            text_input="BACK", font=get_font(65), base_color="Black", hovering_color="Green")


        for button in [OPTIONS_BACK, OPTIONS_RESUME, OPTIONS_MUSIC]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_RESUME.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.snake.isPause = False
                    playGame()
                if OPTIONS_MUSIC.checkForInput(OPTIONS_MOUSE_POS):
                    if main_game.isMusic:
                        main_game.isMusic = False
                        main_game.stop_sound_background()
                    else:
                        main_game.isMusic = True
                        main_game.sound_background()
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.snake.isPause = False
                    main_game.snake.reset()
                    main_game.fruit.randomize()
                    if main_game.mode == "trouble":
                        main_game.fence.reset_fence()
                    if main_game.mode == "rain":
                        main_game.many_bullets.many_bl = []
                        main_game.many_bullets.many_relations = []
                    main_menu()

        pygame.display.update()

def modeGame():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(65).render("CHOOSE A MODE", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(520, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_CLASSIC = Button(image=None, pos=(540, 230), 
                            text_input="CLASSIC", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_TROUBLE = Button(image=None, pos=(540, 350), 
                            text_input="TROUBLE", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_ATTACK = Button(image=None, pos=(540, 470), 
                            text_input="ATTACK", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_RAIN_ATTACK = Button(image=None, pos=(540, 590), 
                            text_input="RAIN ATTACK", font=get_font(55), base_color="Black", hovering_color="Green")


        for button in [OPTIONS_CLASSIC, OPTIONS_TROUBLE, OPTIONS_ATTACK, OPTIONS_RAIN_ATTACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_CLASSIC.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.mode = "classic"
                    playGame()
                if OPTIONS_TROUBLE.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.fence.num_fence = 3
                    main_game.mode = "trouble"
                    playGame()
                if OPTIONS_ATTACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.mode = "attack"
                    playGame()
                if OPTIONS_RAIN_ATTACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_game.mode = "rain"
                    main_game.fence.setting_fence()
                    playGame()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(75).render("OPTIONS GAME", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(520, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_MUSIC = Button(image=None, pos=(540, 260), 
                            text_input="MUSIC", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_HELP = Button(image=None, pos=(540, 400), 
                            text_input="HELP", font=get_font(55), base_color="Black", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(540, 560), 
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="Green")

        for button in [OPTIONS_BACK, OPTIONS_HELP, OPTIONS_MUSIC]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_MUSIC.checkForInput(OPTIONS_MOUSE_POS):
                    if main_game.isMusic:
                        main_game.isMusic = False
                        main_game.stop_sound_background()
                    else:
                        main_game.isMusic = True
                        main_game.sound_background()
                if OPTIONS_HELP.checkForInput(OPTIONS_MOUSE_POS):
                    help()
                    
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def help():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")
        HELP_TEXT = "HUONG DAN :"
        OPTIONS_TEXT = get_font(15).render(HELP_TEXT, True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 60))
        
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        texts = ["1.Che do choi Classic ", "  * Nguoi choi dieu khien ran an qua se ","    duoc 1 diem","  * Nguoi choi thua khi ran cham tuong hoac ","    can vao than"," ",
                    "2.Che do choi Trouble", "  * Nguoi choi dieu khien ran vuot qua ","    chuong ngai vat va an qua", "  * Game Over khi cham vao chuong ngai vat"," ",
                    "3. Che do choi Attack", "  * Bam q de ban ra dan tieu diet muc tieu", "  * Thua khi khong ban ma cham vao ke dich"," ",
                    "4. Che do choi Rain Attack" , "  * Bam q de ban lien tuc vao muc tieu", "  * Thua khi cham vao muc tieu","  * Nguoi choi dieu khien ran an qua se ","    duoc 1 diem"
                    ]
        line = 80
        for text in texts:
            OPTIONS_TEXT = get_font(15).render(text, True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(topleft=(150, line))
            line+=20
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(540, 560), 
                            text_input="BACK", font=get_font(65), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:        
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    options()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("SNAKE GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(520, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(540, 250 + 50), 
                            text_input="PLAY", font=get_font(75), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(540, 400 + 50), 
                            text_input="OPTIONS", font=get_font(75), base_color="White", hovering_color="Green") #base_color="#d7fcd4", hovering_color="White"
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(540, 550 + 50), 
                            text_input="QUIT", font=get_font(75), base_color="White", hovering_color="Green")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #playGame()
                    modeGame()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()