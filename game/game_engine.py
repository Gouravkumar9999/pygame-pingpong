import pygame
import random
import time
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

        self.winning_score = 5  # default (best of 9 → first to 5)

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
            self.ball.x = player_rect.right
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
        if self.player_score >= self.winning_score:
            winner = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner = "AI Wins!"

        if winner:
            self.show_game_over(screen, winner)

    def show_game_over(self, screen, winner):
        screen.fill(BLACK)
        big_font = pygame.font.SysFont("Arial", 50)
        msg = big_font.render(winner, True, WHITE)

        # --- Center the winner message perfectly ---
        msg_rect = msg.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(msg, msg_rect)

        small_font = pygame.font.SysFont("Arial", 30)
        sub = small_font.render("Press any key for replay options...", True, WHITE)
        sub_rect = sub.get_rect(center=(self.width // 2, self.height // 2 + 20))
        screen.blit(sub, sub_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

        self.show_replay_menu(screen)


    def show_replay_menu(self, screen):
        screen.fill(BLACK)
        title_font = pygame.font.SysFont("Arial", 40)
        opt_font = pygame.font.SysFont("Arial", 30)

        title = title_font.render("Choose Match Type:", True, WHITE)
        options = [
            "Press 3 → Best of 3 (First to 2)",
            "Press 5 → Best of 5 (First to 3)",
            "Press 7 → Best of 7 (First to 4)",
            "Press ESC → Exit Game"
        ]

        screen.blit(title, (self.width // 2 - 170, self.height // 2 - 140))
        for i, opt in enumerate(options):
            txt = opt_font.render(opt, True, WHITE)
            screen.blit(txt, (self.width // 2 - 200, self.height // 2 - 70 + i * 50))

        pygame.display.flip()

        # Wait for player choice
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Reset scores and ball for replay
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
