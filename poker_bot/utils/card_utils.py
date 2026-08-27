"""Card manipulation utilities"""

from typing import List, Tuple


class Card:
    """Card representation and utilities"""
    
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    SUITS = ['c', 'd', 'h', 's']
    SUIT_SYMBOLS = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    
    def __init__(self, card_str: str):
        """Initialize card from string (e.g., 'As', 'Kd')"""
        if len(card_str) != 2:
            raise ValueError(f"Invalid card: {card_str}")
        
        self.rank = card_str[0]
        self.suit = card_str[1].lower()
        
        if self.rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {self.rank}")
        if self.suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {self.suit}")
    
    def __str__(self) -> str:
        return f"{self.rank}{self.SUIT_SYMBOLS[self.suit]}"
    
    def __repr__(self) -> str:
        return f"Card('{self.rank}{self.suit}')"
    
    def to_string(self) -> str:
        """Return card as standard string (e.g., 'As')"""
        return f"{self.rank}{self.suit}"


def parse_hand_string(hand_str: str) -> List[str]:
    """Parse hand string into card list
    
    Args:
        hand_str: Hand string (e.g., 'AsKd 2c 3h')
    
    Returns:
        List of card strings
    """
    # Handle different formats
    hand_str = hand_str.replace(' ', '').replace(',', '')
    
    cards = []
    for i in range(0, len(hand_str), 2):
        if i + 1 < len(hand_str):
            cards.append(hand_str[i:i+2])
    
    return cards


def format_hand(cards: List[str]) -> str:
    """Format cards with suit symbols
    
    Args:
        cards: List of card strings
    
    Returns:
        Formatted string (e.g., 'A♠ K♦')
    """
    formatted = []
    for card_str in cards:
        card = Card(card_str)
        formatted.append(str(card))
    return " ".join(formatted)
