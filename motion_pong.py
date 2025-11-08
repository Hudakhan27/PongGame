import cv2
import numpy as np
import pygame
import sys
import os

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motion-Controlled Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load Background Image
background = pygame.image.load("background.jpg")  # <-- your image file
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Semi-transparent dark overlay for professional look
overlay = pygame.Surface((WIDTH, HEIGHT))
overlay.set_alpha(90)  # Transparency: 0 (clear) to 255 (opaque)
overlay.fill((0, 0, 0))

# Load Assets (make sure files exist in the same folder)
bat_img = pygame.image.load("bat.png")
bat_img = pygame.transform.scale(bat_img, (90, 120))  # resize for player

bat_img_ai = pygame.transform.flip(bat_img, True, False)  # flipped for AI

ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (30, 30))

# Optional sound effect
if os.path.exists("ping.wav"):
    hit_sound = pygame.mixer.Sound("ping.wav")
else:
    hit_sound = None

# Ball setup
ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
ball_speed = np.array([5, 4], dtype=float)
ball_radius = 15

# Paddle setup
paddle_width, paddle_height = 60, 120
paddle_x = 50
paddle_y = HEIGHT // 2 - paddle_height // 2

ai_x = WIDTH - 110
ai_y = HEIGHT // 2 - paddle_height // 2
ai_speed = 4

font = pygame.font.SysFont("Arial", 36, bold=True)
score = 0

# OpenCV setup
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

# Adjust for your object color (example: blue glove/object)
lower_color = np.array([90, 100, 100])
upper_color = np.array([130, 255, 255])

clock = pygame.time.Clock()

def detect_hand_y(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return y + h // 2
    return None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    hand_y = detect_hand_y(frame)
    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    if hand_y is not None:
        mapped_y = int(np.interp(hand_y, [0, 240], [0, HEIGHT - paddle_height]))
        paddle_y = mapped_y

    # Ball movement
    ball_pos += ball_speed

    # Wall bounce
    if ball_pos[1] <= ball_radius or ball_pos[1] >= HEIGHT - ball_radius:
        ball_speed[1] *= -1
        if hit_sound:
            hit_sound.play()

    # Player paddle collision
    if (paddle_x < ball_pos[0] - ball_radius < paddle_x + paddle_width) and \
       (paddle_y < ball_pos[1] < paddle_y + paddle_height):
        ball_speed[0] *= -1
        score += 1
        if hit_sound:
            hit_sound.play()

    # AI paddle collision
    if (ai_x < ball_pos[0] + ball_radius < ai_x + paddle_width) and \
       (ai_y < ball_pos[1] < ai_y + paddle_height):
        ball_speed[0] *= -1
        if hit_sound:
            hit_sound.play()

    # Simple AI movement
    if ai_y + paddle_height / 2 < ball_pos[1]:
        ai_y += ai_speed
    elif ai_y + paddle_height / 2 > ball_pos[1]:
        ai_y -= ai_speed

    # Reset ball if it goes off screen
    if ball_pos[0] < 0 or ball_pos[0] > WIDTH:
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
        ball_speed = np.array([5, 4], dtype=float)
        score = 0

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(ball_img, (ball_pos[0] - 15, ball_pos[1] - 15))
    screen.blit(bat_img, (paddle_x, paddle_y))
    screen.blit(bat_img_ai, (ai_x, ai_y))

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 70, 20))

    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
