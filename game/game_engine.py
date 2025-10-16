import pygame
from .paddle import Paddle
from .ball import Ball
import time

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        self.ball.move()

        # --- Collision check immediately after moving ---
        ball_rect = self.ball.rect()
        player_rect = self.player.rect()
        ai_rect = self.ai.rect()

        if ball_rect.colliderect(player_rect):
            self.ball.x = player_rect.right  # reposition to avoid sticking
            self.ball.velocity_x *= -1

        elif ball_rect.colliderect(ai_rect):
            self.ball.x = ai_rect.left - self.ball.width
            self.ball.velocity_x *= -1

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Move AI paddle
        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self, screen):
        winner = None
        if self.player_score >= 5:
            winner = "Player Wins!"
        elif self.ai_score >= 5:
            winner = "AI Wins!"

        if winner:
            # Draw the message in the center of the screen
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 50)
            text_surface = font.render(winner, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()

            # Keep the message on screen for 3 seconds
            time.sleep(3)

            # Quit the game
            pygame.quit()
            exit()

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))