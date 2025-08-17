import random
from functools import cmp_to_key
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

min_card_value = 5
max_card_value = 12
market_size = 3
hand_size = 2
player_count = 5
wild_count = 4

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


def setup_deck():
    deck = []
    for i in range(1, wild_count+1):
        deck.append({'value': 0, 'chocolate_chips': max_card_value + i})
    deck.append({'value': 1, 'chocolate_chips': 1})
    for rank in range(min_card_value, max_card_value + 1):
        for chocolate_chips in range(1, rank+1):
            deck.append({'value': rank, 'chocolate_chips': chocolate_chips})
    return shuffle_deck(deck)

def rank_hand(cards, hand_cards):
    # Group cards by value
    value_groups = [[] for _ in range(max_card_value + 1)]
    wildcards = []
    
    # Separate cards into value groups and wildcards
    for card in cards:
        if card['value'] == 0:
            wildcards.append(card['chocolate_chips'])
        else:
            value_groups[card['value']].append(card['chocolate_chips'])
    
    # Find the best run by trying to use wildcards with each value
    best_hand = []
    for value in range(1, len(value_groups)):
        current_run = value_groups[value].copy()
        remaining_wildcards = wildcards.copy()
        
        # If we have at least one card of this value, it's a valid run
        if current_run:
            # Add any wildcards we can use
            while remaining_wildcards:
                current_run.append(remaining_wildcards.pop(0))
            
            # Convert to card format and sort by chocolate chips
            run_cards = [{'value': value, 'chocolate_chips': chips} for chips in current_run]
            run_cards.sort(key=lambda x: x['chocolate_chips'])
            
            # Check if at least one card from the run is in the player's hand
            if any(card in hand_cards for card in run_cards):
                if len(run_cards) > len(best_hand):
                    best_hand = run_cards
                elif len(run_cards) == len(best_hand) and best_hand:
                    # If same length, compare by lowest value and chocolate chips
                    if run_cards[0]['value'] < best_hand[0]['value']:
                        best_hand = run_cards
                    elif run_cards[0]['value'] == best_hand[0]['value'] and run_cards[0]['chocolate_chips'] < best_hand[0]['chocolate_chips']:
                        best_hand = run_cards

    return best_hand


def compare_hands(market, hand1, hand2):
    hand1_rank = rank_hand(market + hand1, hand1)
    hand2_rank = rank_hand(market + hand2, hand2)

    # First compare by length of run
    if len(hand1_rank) > len(hand2_rank):
        return 1  # Hand 1 wins
    elif len(hand1_rank) < len(hand2_rank):
        return -1  # Hand 2 wins
    
    # If lengths are equal, compare by lowest value on lowest chocolate chip card
    if hand1_rank[0]["value"] < hand2_rank[0]["value"]:
        return 1
    elif hand1_rank[0]["value"] > hand2_rank[0]["value"]:
        return -1
    
    # If values are equal, compare by fewest chocolate chips on lowest chocolate chip card
    if hand1_rank[0]["chocolate_chips"] < hand2_rank[0]["chocolate_chips"]:
        return 1
    elif hand1_rank[0]["chocolate_chips"] > hand2_rank[0]["chocolate_chips"]:
        return -1
    
    return 0  # Hands are equal

def order_hands(players, market):
    # Create list of (player_index, hand) tuples
    indexed_hands = list(enumerate(players))
    # Sort based on hand comparison
    sorted_hands = sorted(indexed_hands, 
                         key=cmp_to_key(lambda p1, p2: compare_hands(market, p1[1], p2[1])), 
                         reverse=False)
    return sorted_hands

def simulate_round(player_count, market_size=4, hand_size=2):
    deck = setup_deck()
    players = [[] for _ in range(player_count)]
    market = []

    # Deal cards to players
    for i in range(hand_size):
        for player in players:
            if deck:
                player.append(deck.pop(0))

    # Deal cards to the market
    for i in range(market_size):
        market.append(deck.pop(0))

    # Sort each player's hand
    ordered_hands = order_hands(players, market)

    # Print the hands of each player
    for i, hand in enumerate(players):
        print(f"Player {i + 1}: {hand}")

    # Print the market
    print(f"Market: {market}")

    # Print the ordered hands (best hand first)
    print("Ordered Hands:")
    for player_idx, hand in reversed(ordered_hands):  # Reversed to show best hand first
        print(f"Player {player_idx + 1}: {hand}")

    visualize_game(players, market, ordered_hands)
        
def visualize_game(players, market, ordered_hands, ax):
    y = 0
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    # Plot each player's hand in the order determined by ordered_hands
    for player_idx, hand in ordered_hands:
        x = 0
        for card in hand:
            rect = mpatches.Rectangle((x, y), 0.8, 0.8, color=colors[player_idx % len(colors)], alpha=0.7)
            ax.add_patch(rect)
            ax.text(x + 0.4, y + 0.4, f"{card['value']}", ha='center', va='center', color='white', fontsize=12)
            # Add chocolate chip dots
            for i in range(card['chocolate_chips']):
                if i < 5:  # First line of dots
                    ax.plot(x + 0.2 + i * 0.1, y + 0.2, 'ko', markersize=3)
                else:  # Second line of dots
                    ax.plot(x + 0.2 + (i - 5) * 0.1, y + 0.1, 'ko', markersize=3)
            x += 1
        ax.text(-3, y + 0.4, f"Player {player_idx + 1}", va='center', fontsize=12, fontweight='bold')
        y += 1
    # Plot market
    x = 0
    for card in market:
        rect = mpatches.Rectangle((x, y), 0.8, 0.8, color='gray', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + 0.4, y + 0.4, f"{card['value']}", ha='center', va='center', color='white', fontsize=12)
        # Add chocolate chip dots
        for i in range(card['chocolate_chips']):
            if i < 5:  # First line of dots
                ax.plot(x + 0.2 + i * 0.1, y + 0.2, 'ko', markersize=3)
            else:  # Second line of dots
                ax.plot(x + 0.2 + (i - 5) * 0.1, y + 0.1, 'ko', markersize=3)
        x += 1
    ax.text(-3, y + 0.4, "Market", va='center', fontsize=12, fontweight='bold')
    y += 1
    ax.set_xlim(-4, max(len(hand) for hand in players) + len(market) + 3)
    ax.set_ylim(-0.5, y)
    ax.axis('off')

def monte_carlo_simulation(num_rounds, player_count, market_size, hand_size):
    best_run_lengths = []
    best_round = None
    worst_round = None
    median_round = None
    best_run_length = 0
    worst_run_length = float('inf')
    median_run_length = 0
    for _ in range(num_rounds):
        deck = setup_deck()
        players = [[] for _ in range(player_count)]
        market = []

        # Deal cards to players
        for i in range(hand_size):
            for player in players:
                if deck:
                    player.append(deck.pop(0))

        # Deal cards to the market
        for i in range(market_size):
            market.append(deck.pop(0))

        # Sort each player's hand
        ordered_hands = order_hands(players, market)

        # Find the best run length
        current_best_run_length = 0
        for player_idx, hand in ordered_hands:
            run = rank_hand(market + hand, hand)
            if len(run) > current_best_run_length:
                current_best_run_length = len(run)
        best_run_lengths.append(current_best_run_length)

        # Update best round if current round has a better run
        if current_best_run_length > best_run_length:
            best_run_length = current_best_run_length
            best_round = (players, market, ordered_hands)

        # Update worst round if current round has a worse run
        if current_best_run_length < worst_run_length:
            worst_run_length = current_best_run_length
            worst_round = (players, market, ordered_hands)

    # Calculate median run length
    best_run_lengths.sort()
    median_run_length = best_run_lengths[len(best_run_lengths) // 2]

    # Find the median round
    for _ in range(num_rounds):
        deck = setup_deck()
        players = [[] for _ in range(player_count)]
        market = []

        # Deal cards to players
        for i in range(hand_size):
            for player in players:
                if deck:
                    player.append(deck.pop(0))

        # Deal cards to the market
        for i in range(market_size):
            market.append(deck.pop(0))

        # Sort each player's hand
        ordered_hands = order_hands(players, market)

        # Find the best run length
        current_best_run_length = 0
        for player_idx, hand in ordered_hands:
            run = rank_hand(market + hand, hand)
            if len(run) > current_best_run_length:
                current_best_run_length = len(run)

        if current_best_run_length == median_run_length:
            median_round = (players, market, ordered_hands)
            break

    # Create a figure with four subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(24, 6))  # Increased width

    # Display the frequency of best run lengths
    ax1.hist(best_run_lengths, bins=range(1, 8), alpha=0.7, color='blue', edgecolor='black')
    ax1.set_xlabel('Best Run Length')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Monte Carlo Simulation: Frequency of Best Run Lengths')
    ax1.grid(True)

    # Display the best round
    if best_round:
        players, market, ordered_hands = best_round
        visualize_game(players, market, ordered_hands, ax2)
        ax2.set_title('Best Round Visualization')

    # Display the worst round
    if worst_round:
        players, market, ordered_hands = worst_round
        visualize_game(players, market, ordered_hands, ax3)
        ax3.set_title('Worst Round Visualization')

    # Display the median round
    if median_round:
        players, market, ordered_hands = median_round
        visualize_game(players, market, ordered_hands, ax4)
        ax4.set_title('Median Round Visualization')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    monte_carlo_simulation(100000, player_count, market_size, hand_size)  # Run 1000 rounds with 5 players
