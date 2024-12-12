from PIL import Image
import pygame
import random
import time
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font("freesansbold.ttf", 20)

# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic screen parameters
WIDTH, HEIGHT = 900, 600
MAX_SPEED = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("INSTALEAP PINGFINITY WARPONG")

clock = pygame.time.Clock()
FPS = 30

# Ball Settings
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_radius = 7
ball_speed = 7
ball_acc = 1.5

# Players Settings
p1_x, p1_y = 50, HEIGHT // 2 - 50
p2_x, p2_y = WIDTH - 60, HEIGHT // 2 - 50
p_width, p_height, p_speed, p_energy = 10, 100, 10, 99

# Files Settings
p1_folder, p2_folder = "./app/player_1", "./app/player_2"
player_direction = "/direction.txt"
player_data = "/data.txt"
player_name = "/name.txt"

energy_recovery_ratio = 1
energy_usage_ratio = 1.5


# Striker class
class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(
        self,
        pos_x,
        pos_y,
        width,
        height,
        speed,
        color,
        energy,
        input_file,
        output_file,
        player_type,
    ):
        self.direction = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.initial_pos_x = pos_x
        self.initial_pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.energy = energy
        self.input_file = input_file
        self.output_file = output_file
        self.player_type = player_type

        self.player_rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.player_disp = pygame.draw.rect(screen, self.color, self.player_rect)

        if self.player_type == "P1":
            self.energy_rect = pygame.Rect(
                WIDTH // 2 - (20 + self.energy), 20, self.energy, 10
            )
            self.energy_frame = pygame.Rect(WIDTH // 2 - 120, 20, 100, 10)
        else:
            self.energy_rect = pygame.Rect(WIDTH // 2 + 20, 20, self.energy, 10)
            self.energy_frame = pygame.Rect(WIDTH // 2 + 20, 20, 100, 10)
        self.frame_disp = pygame.draw.rect(screen, WHITE, self.energy_frame, 3)
        self.energy_disp = pygame.draw.rect(screen, WHITE, self.energy_rect)

    # Used to display the object on the screen
    def display(self):
        self.player_disp = pygame.draw.rect(screen, self.color, self.player_rect)
        self.frame_disp = pygame.draw.rect(screen, WHITE, self.energy_frame, 3)
        self.energy_disp = pygame.draw.rect(screen, WHITE, self.energy_rect)

    def update(self):
        if self.energy > 0:
            self.pos_y = self.pos_y + self.speed * self.direction

        # Restricting the striker to be below the top surface of the screen
        if self.pos_y <= 0:
            self.pos_y = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.pos_y + self.height >= HEIGHT:
            self.pos_y = HEIGHT - self.height

        #
        if self.direction == 0 and self.energy < 100:
            self.energy += energy_recovery_ratio
        elif self.direction != 0 and self.energy >= 1:
            self.energy -= energy_usage_ratio

        # Updating the rect with the new values
        self.player_rect = (self.pos_x, self.pos_y, self.width, self.height)
        if self.player_type == "P1":
            self.energy_rect = (WIDTH // 2 - (20 + self.energy), 20, self.energy, 10)
        else:
            self.energy_rect = (WIDTH // 2 + 20, 20, self.energy, 10)

    def display_score(self, text, score, x, y, color):
        text = font20.render(f"{text} {str(score)}", True, color)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

    def get_rect(self):
        return self.player_rect

    def get_output_file(self):
        return self.output_file

    def get_data(self):
        return f"{self.pos_x},{self.pos_y + (p_height//2)},{self.energy}"

    def reset(self, pos_x, pos_y):
        self.direction = 0
        self.energy = 100
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update()

    def read_direction(self):
        direction = 0
        try:
            f = open(self.input_file, "r")
            direction = int(f.readline())
            f.close()
        except:
            pass
        self.direction = direction
        self.update()


# Ball class
class Ball:
    def __init__(self, pos_x, pos_y, radius, speed, acc, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.initial_speed = speed
        self.speed = speed
        self.acc = acc
        self.color = color
        self.x_fac = 1
        self.y_fac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius
        )
        self.first_time = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius
        )

    def update(self):
        self.pos_x += self.speed * self.x_fac
        self.pos_y += self.speed * self.y_fac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.pos_y <= 0 or self.pos_y >= HEIGHT:
            self.y_fac *= -1
            self.increase_speed()

        if self.pos_x <= 0 and self.first_time:
            self.first_time = 0
            return 1
        elif self.pos_x >= WIDTH and self.first_time:
            self.first_time = 0
            return -1
        else:
            return 0

    def reset(self):
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.x_fac *= 1
        self.y_fac = round(random.uniform(-1, 1), 2)
        self.first_time = 1
        self.speed = self.initial_speed

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.x_fac *= -1
        if self.y_fac < 0:
            self.y_fac -= 0.1
        else:
            self.y_fac += 0.1
        self.increase_speed()

    def get_rect(self):
        return self.ball

    def increase_speed(self):
        self.speed = min(self.speed + self.acc, MAX_SPEED)

    def pause(self, should_stop):
        if should_stop == True:
            self.speed = 0
        else:
            self.speed = self.initial_speed

    def get_position(self):
        return f"{self.pos_x},{self.pos_y}"


# Game Manager
def main():
    running = True
    pause = False

    # Defining the objects
    player1 = Striker(
        p1_x,
        p1_y,
        p_width,
        p_height,
        p_speed,
        GREEN,
        p_energy,
        p1_folder + player_direction,
        p1_folder + player_data,
        "P1",
    )
    player2 = Striker(
        p2_x,
        p2_y,
        p_width,
        p_height,
        p_speed,
        GREEN,
        p_energy,
        p2_folder + player_direction,
        p2_folder + player_data,
        "P2",
    )
    ball = Ball(ball_x, ball_y, ball_radius, ball_speed, ball_acc, WHITE)

    players = [player1, player2]

    # Initial parameters of the players
    player_1_name = "Instaleapers 1"
    player_2_name = "Instaleapers 2"
    player1_score, player2_score = 0, 0

    # Reading team names from files
    try:
        f = open(p1_folder + player_name, "r")
        player_1_name = f.readline()[:15]
        f.close()
    except:
        pass

    try:
        f = open(p2_folder + player_name, "r")
        player_2_name = f.readline()[:15]
        f.close()
    except:
        pass

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Reset Game
                if event.key == pygame.K_r:
                    player1_score = 0
                    player2_score = 0
                    player1.reset(p1_x, p1_y)
                    player2.reset(p2_x, p2_y)
                    ball.reset()
                    ball.pause(pause)
                    pause = not pause

                # Pause Game
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    ball.pause(pause)

        # Collision detection
        for player in players:
            if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
                ball.hit()

        # Updating the objects
        player1.read_direction()
        player2.read_direction()
        point = ball.update()

        # -1 -> P1 has scored
        # +1 -> P2 has scored
        # 0 -> None of them scored
        score_text = ""
        if point == -1:
            player1_score += 1
            score_text = f"{player_1_name} scored !!"
        elif point == 1:
            player2_score += 1
            score_text = f"{player_2_name} scored !!"

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:

            text = font20.render(f"{score_text}", True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)
            player1.display_score(f"{player_1_name}: ", player1_score, 150, 20, WHITE)
            player2.display_score(
                f"{player_2_name}: ", player2_score, WIDTH - 150, 20, WHITE
            )
            player1.display()
            player2.display()
            ball.display()

            ball.reset()
            player1.reset(p1_x, p1_y)
            player2.reset(p2_x, p2_y)
            ball.pause(True)
            pygame.display.update()
            time.sleep(2)
            ball.pause(False)

        for player in players:
            try:
                f = open(player.get_output_file(), "w")
                f.write(f"{player.get_data()},{ball.get_position()}")
                f.close()
            except:
                pass

        # Displaying the scores of the players
        player1.display_score(f"{player_1_name}: ", player1_score, 150, 20, WHITE)
        player2.display_score(
            f"{player_2_name}: ", player2_score, WIDTH - 150, 20, WHITE
        )

        # Displaying the objects on the screen
        player1.display()
        player2.display()
        ball.display()

        pygame.display.update()
        clock.tick(FPS)


try:
    im1 = Image.open(f"{p1_folder}/img.jpg")
    im1 = im1.resize((200, 200))
    im1.show("Player-1")

    im2 = Image.open(f"{p2_folder}/img.jpg")
    im2 = im2.resize((200, 200))
    im2.show("Player-2")
except:
    pass

if __name__ == "__main__":
    main()
    pygame.quit()
