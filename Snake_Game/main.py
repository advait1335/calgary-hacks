# from os import walk_continuous
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BROWN = (36, 15, 7)


class Apple:
    def __init__(self, parent_screen):
        self.apple_img = pygame.image.load(r"resources/images/apple.png").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 14) * SIZE
        
    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))

    def move_to_random_position(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 14) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen  # passing 'surface' to parent_screen
        self.head_img = pygame.image.load(r"resources/images/head.jpg").convert()
        self.body_img = pygame.image.load(r"resources/images/block.jpg").convert()
        self.y = [SIZE] * length
        self.x = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1) # store garbage value for new piece
        self.y.append(-1) # store garbage value for new piece

    def draw(self):
        # Draw the head
        self.parent_screen.blit(self.head_img, (self.x[0], self.y[0]))
        # Draw the body
        for i in range(1, self.length):
            self.parent_screen.blit(self.body_img, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk_continuous(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and apple game by PRINCE")
        pygame.mixer.init()
        self.play_bgmusic()
        self.surface = pygame.display.set_mode((1000, 600))
        self.render_background()
        self.snake = Snake(self.surface, 1)  # snake is the object for class Snake()
        self.snake.draw()  # drawing snake acc to coordinates
        self.apple = Apple(self.surface)
        self.apple.draw()
        
        
    def reset(self):
        self.snake = Snake(self.surface, 1)  # snake is the object for class Snake()
        self.snake.draw()  # drawing snake acc to coordinates
        self.apple = Apple(self.surface)
        self.apple.draw()
        
        
    def render_background(self):
        bg = pygame.image.load(r"resources/images/background.jpg")
        self.surface.blit(bg,(0,0))

    def is_collided(self, snake_x, snake_y, x2, y2):
        if snake_x >= x2 and snake_x < x2 + SIZE:
            if snake_y >= y2 and snake_y < y2 + SIZE:
                return True
        return False

    def play_bgmusic(self):
        pygame.mixer.music.load(r"resources/music/bg_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound_source):
        sound = pygame.mixer.Sound(f"resources/music/{sound_source}")
        pygame.mixer.Sound.play(sound)


    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def play(self):
        self.render_background()
        self.snake.walk_continuous()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colidng with apple
        if self.is_collided(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.move_to_random_position()
            self.play_sound("eating.wav")
            self.snake.increase_length()

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collided(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash.mp3")
                raise "Game over"
            
        check_boundary_collision = False
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        
        # Check if the snake's head is outside the game window boundaries
        if head_x < 0 or head_x > 1000 or head_y < 0 or head_y > 600:
            check_boundary_collision = True  # Collision detected
        if check_boundary_collision:
            self.play_sound("crash.mp3")  # Assuming you have a sound for crashing
            self.show_game_over()  # Show the game over screen
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over and your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter, To exit press escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:  # KEYDOWN is for pressing the key
                    if event.key == K_ESCAPE:
                        running = False
                        
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not pause :
                        if not self.snake.direction == 'right':
                            if event.key == K_LEFT:
                                self.snake.move_left()
                        if not self.snake.direction == 'left':
                            if event.key == K_RIGHT:
                                self.snake.move_right()
                        if not self.snake.direction == 'down':        
                            if event.key == K_UP:
                                self.snake.move_up()
                        if not self.snake.direction == 'up':        
                            if event.key == K_DOWN:
                                self.snake.move_down()
                        
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                # self.snake.length = 1
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()