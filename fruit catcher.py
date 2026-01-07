import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
basket_width, basket_height = 100, 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 50
basket_speed = 10

fruit_size = 40
bomb_size = 40
fall_speed = 1

score = 0
timer = 60  # seconds
font = pygame.font.Font(None, 36)

# Load fruit and bomb images
fruit_images = {
    "apple": pygame.image.load("apple.png"),
    "banana": pygame.image.load("banana.png"),
    "strawberry": pygame.image.load("strawberry.png")
}
bomb_image = pygame.image.load("bomb.png")

# Scale images
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (fruit_size, fruit_size))
bomb_image = pygame.transform.scale(bomb_image, (bomb_size, bomb_size))

# Target fruit for Level 1
target_fruit = random.choice(list(fruit_images.keys()))

# Falling objects
falling_objects = []  # List to hold fruits and bombs

# High score tracking
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

# Clock for controlling the frame rate
clock = pygame.time.Clock()


def start_screen():
    """Display the start screen."""
    global high_score
    screen.fill(WHITE)
    title = font.render("Fruit Catcher",True, BLUE)
    start_msg = font.render("Press SPACE to Start", True, GREEN)
    high_score_msg = font.render(f"High Score: {high_score}", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(start_msg, (WIDTH // 2 - start_msg.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_msg, (WIDTH // 2 - high_score_msg.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def display_score_and_timer():
    """Display the score and timer."""
    score_text = font.render(f"Score: {score}", True, BLUE)
    timer_text = font.render(f"Time: {int(timer)}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))


def generate_falling_object():
    """Generate a random fruit or bomb."""
    obj_type = random.choice(["fruit", "bomb"])
    if obj_type == "fruit":
        fruit_name = random.choice(list(fruit_images.keys()))
        falling_objects.append({
            "type": "fruit",
            "name": fruit_name,
            "x": random.randint(0, WIDTH - fruit_size),
            "y": -fruit_size,
            "speed": fall_speed
        })
    else:
        falling_objects.append({
            "type": "bomb",
            "x": random.randint(0, WIDTH - bomb_size),
            "y": -bomb_size,
            "speed": fall_speed 
        })


def handle_falling_objects():
    """Update and display falling objects."""
    global score
    for obj in falling_objects[:]:
        obj["y"] += obj["speed"]

        # Check for collision with basket
        if basket_x < obj["x"] < basket_x + basket_width and basket_y < obj["y"] + fruit_size < basket_y + basket_height:
            if obj["type"] == "fruit":
                if obj["name"] == target_fruit:
                    score += 10  # Bonus for target fruit
                else:
                    score += 5
            elif obj["type"] == "bomb":
                score -= 5
            falling_objects.remove(obj)
        # Remove object if it falls off the screen
        elif obj["y"] > HEIGHT:
            falling_objects.remove(obj)

        # Draw the object
        if obj["type"] == "fruit":
            screen.blit(fruit_images[obj["name"]], (obj["x"], obj["y"]))
        else:
            screen.blit(bomb_image, (obj["x"], obj["y"]))


def level_1():
    """Level 1: Catch specific fruit."""
    global timer, score, target_fruit, basket_x
    target_fruit = random.choice(list(fruit_images.keys()))
    start_time = time.time()
    while timer > 0:
        screen.fill(WHITE)
        display_score_and_timer()

        # Display target fruit
        target_text = font.render(f"Catch: {target_fruit.capitalize()}", True, GREEN)
        screen.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Handle basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        # Generate and update falling objects
        if random.randint(1, 30) == 1:
            generate_falling_object()
        handle_falling_objects()

        # Draw basket
        pygame.draw.rect(screen, YELLOW, (basket_x, basket_y, basket_width, basket_height))

        pygame.display.flip()
        clock.tick(200)

        # Update timer
        timer = 60 - (time.time() - start_time)

    return score


def end_screen():
    """Display the end screen."""
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

    screen.fill(WHITE)
    end_msg = font.render(f"Game Over! Your Score: {score}", True, BLUE)
    high_score_msg = font.render(f"High Score: {high_score}", True, RED)
    screen.blit(end_msg, (WIDTH // 2 - end_msg.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(high_score_msg, (WIDTH // 2 - high_score_msg.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(5)


def main():
    """Main game loop."""
    start_screen()
    level_1()
    end_screen()


if __name__ == "__main__":
    main()


