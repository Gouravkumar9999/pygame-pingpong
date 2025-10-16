import pygame
from game.paddle import Paddle
from game.ball import Ball

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # --- Create paddles ---
        paddle_width, paddle_height = 15, 100
        self.player_paddle = Paddle(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)
        self.ai_paddle = Paddle(width - 45, height // 2 - paddle_height // 2, paddle_width, paddle_height)

        # --- Create ball ---
        ball_size = 15
        self.ball = Ball(width // 2 - ball_size // 2, height // 2 - ball_size // 2,
                         ball_size, ball_size, width, height)

        # --- Scoring ---
        self.player_score = 0
        self.ai_score = 0

        # Font for score rendering
        self.font = pygame.font.Font(None, 36)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_paddle.move(-self.player_paddle.speed, self.height)
        if keys[pygame.K_DOWN]:
            self.player_paddle.move(self.player_paddle.speed, self.height)

    def update(self):
        # AI follows the ball
        self.ai_paddle.auto_track(self.ball, self.height)

        # Ball movement & collisions
        self.ball.move(self.player_paddle, self.ai_paddle)

        # --- Scoring check ---
        if self.ball.x < 0:
            self.ai_score += 1
            self.ball.reset()

        elif self.ball.x > self.width:
            self.player_score += 1
            self.ball.reset()
        self.check_game_over(pygame.display.get_surface())

    def render(self, screen):
        # Draw paddles & ball
        pygame.draw.rect(screen, (255, 255, 255), self.player_paddle.rect())
        pygame.draw.rect(screen, (255, 255, 255), self.ai_paddle.rect())
        pygame.draw.rect(screen, (255, 255, 255), self.ball.rect())

        # Draw center line
        pygame.draw.aaline(screen, (255, 255, 255), (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        score_text = self.font.render(f"{self.player_score}   {self.ai_score}", True, (255, 255, 255))
        screen.blit(score_text, (self.width // 2 - 40, 20))
    
    def check_game_over(self, screen):
        WIN_SCORE = 5
        if self.player_score >= WIN_SCORE or self.ai_score >= WIN_SCORE:
            winner = "Player" if self.player_score >= WIN_SCORE else "AI"

            # Fill screen and show message
            screen.fill((0, 0, 0))
            game_over_text = self.font.render(f"{winner} Wins!", True, (255, 255, 255))
            info_text = self.font.render("Restarting in 3 seconds...", True, (200, 200, 200))

            # Center texts
            screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2 - 40))
            screen.blit(info_text, (self.width // 2 - info_text.get_width() // 2, self.height // 2 + 10))

            pygame.display.flip()

            # Wait a bit so players can see the result
            pygame.time.wait(3000)

            # Quit game
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()


