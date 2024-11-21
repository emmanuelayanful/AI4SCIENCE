import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
BG_COLOR = (20, 20, 40)  # Darker background for a polished look
STONE_COLOR = (220, 70, 70)
HIGHLIGHT_COLOR = (70, 220, 70)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 100, 200)
LEVEL_BUTTON_COLOR = (100, 150, 250)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game of Piles")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

end_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
restart_button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, 2 * BUTTON_MARGIN + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
easy_button_rect = pygame.Rect(BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
normal_button_rect = pygame.Rect(2 * BUTTON_MARGIN + BUTTON_WIDTH, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)
hard_button_rect = pygame.Rect(3 * BUTTON_MARGIN + 2 * BUTTON_WIDTH, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT)

# Input and Set Piles Button
input_box = pygame.Rect(700, SCREEN_HEIGHT - 100, 100, 40)
set_piles_button_rect = pygame.Rect(820, SCREEN_HEIGHT - 100, BUTTON_WIDTH, 40)
input_active = False
input_text = ""

# Functions
def reset_game():
    """Reset the game state."""
    global piles, player_turn, winner, last_move, highlighted_stones, stone_positions, ai_difficulty, game_over
    piles = [random.randint(1, 10) for _ in range(2)]
    player_turn = True
    winner = None
    last_move = None
    highlighted_stones = []
    stone_positions = generate_stone_positions()
    game_over = False
    
def reset_piles(num_piles):
    """Reset the piles with a specified number of piles."""
    global piles, stone_positions
    piles = [random.randint(1, 10) for _ in range(num_piles)]
    stone_positions = generate_stone_positions()
    game_over = False

def generate_stone_positions():
    """Generate positions for stones based on piles."""
    positions = []
    for i, pile_size in enumerate(piles):
        pile_x = 100 + i * 200  # Adjust spacing for better layout
        positions.append([(pile_x, SCREEN_HEIGHT - 150 - j * 35) for j in range(pile_size)])
    return positions

def draw_piles():
    """Draw the piles of stones on the screen."""
    for pile_index, pile in enumerate(stone_positions):
        for stone_index, (x, y) in enumerate(pile):
            color = HIGHLIGHT_COLOR if (pile_index, stone_index) in highlighted_stones else STONE_COLOR
            pygame.draw.circle(screen, color, (x, y), 15)

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
    """Find the optimal move for the AI based on the difficulty level."""
    if ai_difficulty == "Easy":
        # Easy: Random biased play
        non_empty_piles = [i for i, pile in enumerate(piles) if pile > 0]
        pile = random.choice(non_empty_piles)
        stones = random.randint(1, piles[pile])
        return pile, stones

    elif ai_difficulty == "Normal":
        # Normal: Random valid move
        non_empty_piles = [i for i, pile in enumerate(piles) if pile > 0]
        if random.random() >= 0.5:
            pile = random.choice(non_empty_piles)
            stones = random.randint(1, piles[pile])
        else:
            nim_sum = calculate_nim_sum()
            for i, pile in enumerate(piles):
                target = pile ^ nim_sum
                if target < pile:  # Valid move
                    return i, pile - target
        return pile, stones

    elif ai_difficulty == "Hard":
        # Hard: XOR strategy
        nim_sum = calculate_nim_sum()
        if nim_sum == 0:
            # No winning move, play randomly
            non_empty_piles = [i for i, pile in enumerate(piles) if pile > 0]
            pile = random.choice(non_empty_piles)
            stones = random.randint(1, piles[pile])
            return pile, stones
        for i, pile in enumerate(piles):
            target = pile ^ nim_sum
            if target < pile:  # Valid move
                return i, pile - target

def remove_stones(pile_index, stones):
    """Remove stones from a pile."""
    piles[pile_index] -= stones
    stone_positions[pile_index] = stone_positions[pile_index][:-stones]


# Add this variable to keep track of the selected difficulty level
selected_difficulty = "Normal"  # Default difficulty level

# Update the draw_buttons function to change the color based on selection
def draw_buttons():
    """Draw the buttons, highlighting the selected difficulty."""
    # Set colors for difficulty buttons based on the selection
    easy_color = LEVEL_BUTTON_COLOR if selected_difficulty != "Easy" else (50, 180, 50)
    normal_color = LEVEL_BUTTON_COLOR if selected_difficulty != "Normal" else (50, 180, 50)
    hard_color = LEVEL_BUTTON_COLOR if selected_difficulty != "Hard" else (50, 180, 50)
    
    # Draw the End Game and Restart buttons
    pygame.draw.rect(screen, BUTTON_COLOR, end_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)
    
    # Draw the difficulty level buttons with appropriate colors
    pygame.draw.rect(screen, easy_color, easy_button_rect)
    pygame.draw.rect(screen, normal_color, normal_button_rect)
    pygame.draw.rect(screen, hard_color, hard_button_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, set_piles_button_rect)
    pygame.draw.rect(screen, (255, 255, 255) if input_active else (200, 200, 200), input_box, 2)
    
    # Render button text
    display_text("End Game", end_button_rect.x + 20, end_button_rect.y + 10, small_font)
    display_text("Restart", restart_button_rect.x + 20, restart_button_rect.y + 10, small_font)
    display_text("Easy", easy_button_rect.x + 40, easy_button_rect.y + 10, small_font)
    display_text("Normal", normal_button_rect.x + 30, normal_button_rect.y + 10, small_font)
    display_text("Hard", hard_button_rect.x + 40, hard_button_rect.y + 10, small_font)
    display_text("Set Piles", set_piles_button_rect.x + 20, set_piles_button_rect.y + 10, small_font)
    display_text(input_text, input_box.x + 10, input_box.y + 5, small_font)

def get_hovered_stone(mouse_pos):
    """Check if the mouse is hovering over a stone."""
    for pile_index, pile in enumerate(stone_positions):
        for stone_index, (x, y) in enumerate(pile):
            if abs(mouse_pos[0] - x) < 20 and abs(mouse_pos[1] - y) < 20:
                return pile_index, stone_index
    return None, None

# Initialize game state
piles = []
stone_positions = []
highlighted_stones = []
player_turn = True
winner = None
last_move = None
ai_difficulty = selected_difficulty # Default difficulty level
game_over = False
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
        display_text(f"{winner} Wins!", SCREEN_WIDTH // 2 - 100, 100, font, HIGHLIGHT_COLOR)
    elif player_turn:
        display_text("Your Turn", SCREEN_WIDTH // 2 - 80, 100)
    else:
        display_text("AI's Turn", SCREEN_WIDTH // 2 - 80, 100)

    # Display the last move
    if last_move:
        display_text(f"Last Move: {last_move}", 20, SCREEN_HEIGHT - 80, small_font)

    # Display total stones
    total_stones = sum(piles)
    display_text(f"Total Stones: {total_stones}", 20, SCREEN_HEIGHT - 50, small_font)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if end_button_rect.collidepoint(event.pos):
                running = False
            
            elif input_box.collidepoint(event.pos):
                input_active = True
                    
            elif restart_button_rect.collidepoint(event.pos):
                reset_game()
                
            elif easy_button_rect.collidepoint(event.pos):
                selected_difficulty = ai_difficulty = "Easy"
                
            elif normal_button_rect.collidepoint(event.pos):
                selected_difficulty = ai_difficulty = "Normal"
                
            elif hard_button_rect.collidepoint(event.pos):
                selected_difficulty = ai_difficulty = "Hard"
                
            else:
                pile_index, stone_index = get_hovered_stone(event.pos)
                if pile_index is not None and player_turn:
                    stones_to_remove = len(stone_positions[pile_index]) - stone_index
                    remove_stones(pile_index, stones_to_remove)
                    last_move = f"Player removed {stones_to_remove} stone(s) from pile {pile_index + 1}"
                    player_turn = False
                
                input_active = False
                if set_piles_button_rect.collidepoint(event.pos) and input_text.isdigit():
                    reset_piles(int(input_text))
                    input_text = ""
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
                if set_piles_button_rect.collidepoint(event.pos) and input_text.isdigit():
                    reset_piles(int(input_text))
                    input_text = ""

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if input_text.isdigit():
                    reset_game()
                    reset_piles(int(input_text))
                    input_text = ""
            else:
                input_text += event.unicode

    # AI's turn
    if not player_turn and not winner and not game_over:
        if any(pile > 0 for pile in piles):
            pygame.time.wait(1000)
            pile, stones = find_optimal_move()
            remove_stones(pile, stones)
            last_move = f"AI removed {stones} stone(s) from pile {pile + 1}"
            player_turn = True

    # Check for winner
    if all(pile == 0 for pile in piles) and not game_over:
        winner = "Player" if not player_turn else "AI"
        game_over = True
    
    # Highlight stones
    if player_turn:
        mouse_pos = pygame.mouse.get_pos()
        pile_index, stone_index = get_hovered_stone(mouse_pos)
        if pile_index is not None and stone_index is not None:
            highlighted_stones = [(pile_index, i) for i in range(stone_index, len(stone_positions[pile_index]))]
        else:
            highlighted_stones = []
        
    pygame.display.flip()

pygame.quit()