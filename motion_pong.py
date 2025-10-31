import cv2
import numpy as np
import pygame
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motion-Controlled Pong")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ball_radius = 15
ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
ball_speed = np.array([5, 4], dtype=float)

paddle_width, paddle_height = 20, 100
paddle_x = 50
paddle_y = HEIGHT // 2 - paddle_height // 2

ai_x = WIDTH - 70
ai_y = HEIGHT // 2 - paddle_height // 2
ai_speed = 4

font = pygame.font.SysFont("Arial", 32)
score = 0

# OpenCV setup
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

# Adjust for your object color (here: blue)
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

    ball_pos += ball_speed

    if ball_pos[1] <= ball_radius or ball_pos[1] >= HEIGHT - ball_radius:
        ball_speed[1] *= -1

    if (paddle_x < ball_pos[0] - ball_radius < paddle_x + paddle_width) and \
       (paddle_y < ball_pos[1] < paddle_y + paddle_height):
        ball_speed[0] *= -1
        score += 1

    if (ai_x < ball_pos[0] + ball_radius < ai_x + paddle_width) and \
       (ai_y < ball_pos[1] < ai_y + paddle_height):
        ball_speed[0] *= -1

    if ai_y + paddle_height/2 < ball_pos[1]:
        ai_y += ai_speed
    elif ai_y + paddle_height/2 > ball_pos[1]:
        ai_y -= ai_speed

    if ball_pos[0] < 0 or ball_pos[0] > WIDTH:
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
        ball_speed = np.array([5, 4], dtype=float)
        score = 0

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, WHITE, ball_pos.astype(int), ball_radius)
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, RED, (ai_x, ai_y, paddle_width, paddle_height))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 60, 20))
    pygame.display.flip()
    clock.tick(60)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
