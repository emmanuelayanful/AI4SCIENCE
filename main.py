import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = (30, 30, 30)
STONE_COLOR = (200, 50, 50)
HIGHLIGHT_COLOR = (50, 200, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 200)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game of Piles")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
end_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
restart_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, 80, BUTTON_WIDTH, BUTTON_HEIGHT)

# Constants for pile rendering
PILE_X_START = 100
PILE_Y_START = SCREEN_HEIGHT - 100
PILE_SPACING_X = 150
STONE_RADIUS = 15
STONE_SPACING_Y = 35

# Functions
def reset_game():
    """Reset the game state."""
    global piles, player_turn, winner, last_move, selected_pile,stones_to_remove, hover_info
    piles = [random.randint(1, 10) for _ in range(4)]
    player_turn = True
    winner = None
    last_move = None
    selected_pile = None
    stones_to_remove = 0
    hover_info = None

def draw_piles():
    """Draw the piles of stones on the screen."""
    for i, pile_size in enumerate(piles):
        x = PILE_X_START + i * PILE_SPACING_X
        for j in range(pile_size):
            y = PILE_Y_START - j * STONE_SPACING_Y
            color = HIGHLIGHT_COLOR if hover_info and hover_info['pile'] == i and j >= hover_info['stone_index'] else STONE_COLOR
            pygame.draw.circle(screen, color, (x, y), STONE_RADIUS)

def display_text(text, x, y, font=font, color=TEXT_COLOR):
    """Render and display text."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def calculate_nim_sum():
    """Calculate the XOR sum of all pile sizes."""
    nim_sum = 0
    for pile in piles:
        nim_sum ^= pile
    return nim_sum

def find_optimal_move():
    """Find the optimal move for the AI."""
    nim_sum = calculate_nim_sum()
    if nim_sum == 0:
        # No winning move, play randomly
        non_empty_piles = [i for i, pile in enumerate(piles) if pile > 0]
        pile = random.choice(non_empty_piles)
        stones = random.randint(1, piles[pile])
        return pile, stones
    # Find a pile to adjust to make nim_sum 0
    for i, pile in enumerate(piles):
        target = pile ^ nim_sum
        if target < pile:  # Valid move
            return i, pile - target
        
def draw_buttons():
    """Draw the End Game and Restart buttons."""
    pygame.draw.rect(screen, BUTTON_COLOR, end_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)
    display_text("End Game", end_button_rect.x + 20, end_button_rect.y + 10, small_font)
    display_text("Restart", restart_button_rect.x + 20, restart_button_rect.y + 10, small_font)

def get_pile_and_stone(mouse_pos):
    """Determine which pile and stone the mouse is hovering over."""
    x, y = mouse_pos
    for i, pile_size in enumerate(piles):
        pile_x = PILE_X_START + i * PILE_SPACING_X
        # Check horizontal proximity
        if abs(x - pile_x) <= STONE_RADIUS + 10:
            # Check vertical range
            for j in range(pile_size):
                stone_y = PILE_Y_START - j * STONE_SPACING_Y
                if abs(y - stone_y) <= STONE_RADIUS + 10:
                    return i, j
    return None, None

# Initialize game state
reset_game()

# Game loop
running = True

while running:
    screen.fill(BG_COLOR)

    # Draw piles
    draw_piles()

    # Draw buttons
    draw_buttons()

    # Display player turn or winner
    if winner:
        display_text(f"{winner} Wins!", SCREEN_WIDTH // 2 - 80, 50, font, HIGHLIGHT_COLOR)
    elif player_turn:
        display_text("Your Turn", SCREEN_WIDTH // 2 - 80, 50)
    else:
        display_text("AI's Turn", SCREEN_WIDTH // 2 - 80, 50)

    # Display the last move
    if last_move:
        display_text(f"Last Move: {last_move}", 20, 20, small_font)

    # Display total stones
    total_stones = sum(piles)
    display_text(f"Total Stones: {total_stones}", 20, 60, small_font)

    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    pile, stone_index = get_pile_and_stone(mouse_pos)
    if pile is not None and stone_index is not None:
        hover_info = {'pile': pile, 'stone_index': stone_index}
    else:
        hover_info = None

    # Event handling
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()  # Immediately stop execution after quitting

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if End Game button is clicked
            if end_button_rect.collidepoint(event.pos):
                running = False
                pygame.quit()
                exit()  # Immediately stop execution after quitting

            # Check if Restart button is clicked
            if restart_button_rect.collidepoint(event.pos):
                reset_game()

            if player_turn and not winner and hover_info:
                selected_pile = hover_info['pile']
                stones_to_remove = piles[selected_pile] - hover_info['stone_index']
                if stones_to_remove > 0:
                    piles[selected_pile] -= stones_to_remove
                    last_move = f"Player removed {stones_to_remove} stone(s) from pile {selected_pile + 1}"
                    selected_pile = None
                    player_turn = False

        if event.type == pygame.KEYDOWN and player_turn and selected_pile is not None:
            # Detect key press to remove stones (1-9)
            if pygame.K_1 <= event.key <= pygame.K_9:
                stones = event.key - pygame.K_0
                if stones <= piles[selected_pile]:
                    piles[selected_pile] -= stones
                    last_move = f"Player removed {stones} stone(s) from pile {selected_pile}"
                    selected_pile = None
                    player_turn = False
    # AI's turn
    if not player_turn and not winner:
        if any(pile > 0 for pile in piles):  # Check if stones remain
            pygame.time.wait(1000)  # Pause for dramatic effect
            pile_ai, stones_ai = find_optimal_move()
            if pile_ai is not None and stones_ai > 0:
                piles[pile_ai] -= stones_ai
                last_move = f"AI removed {stones_ai} stone(s) from pile {pile_ai + 1}"
                player_turn = True
        else:
            winner = "Player"

    # Check for winner
    if all(pile == 0 for pile in piles):
        winner = "Player" if not player_turn else "AI"

    pygame.display.flip()

pygame.quit()
