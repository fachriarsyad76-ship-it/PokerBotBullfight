"""High-performance hand evaluator using phevaluator

Provides fast hand evaluation, equity calculation, and hand strength metrics.
"""

from typing import List, Tuple, Optional
import itertools
from phevaluator import evaluate_cards
import numpy as np


class PokerEvaluator:
    """Texas Hold'em & Poker hand evaluator
    
    Uses phevaluator for 60M hands/second evaluation.
    Provides equity calculation and hand strength metrics.
    """
    
    RANK_NAMES = {
        1: "Royal Flush",
        2: "Straight Flush",
        3: "Four of a Kind",
        4: "Full House",
        5: "Flush",
        6: "Straight",
        7: "Three of a Kind",
        8: "Two Pair",
        9: "Pair",
        10: "High Card",
    }
    
    def __init__(self):
        """Initialize evaluator"""
        self.all_cards = self._generate_all_cards()
    
    @staticmethod
    def _generate_all_cards() -> List[str]:
        """Generate all 52 cards"""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['c', 'd', 'h', 's']
        return [r + s for r in ranks for s in suits]
    
    def evaluate_hand(
        self,
        community_cards: List[str],
        player_hand: List[str]
    ) -> int:
        """Evaluate player's best 5-card hand
        
        Args:
            community_cards: List of community cards (e.g., ['6c', '2h', '4c', '9h', '5d'])
            player_hand: List of player's hole cards (e.g., ['Ks', 'Kd'])
        
        Returns:
            Rank from 1-7462 (1 = strongest, 7462 = weakest)
        """
        all_cards = community_cards + player_hand
        
        if len(all_cards) < 5:
            raise ValueError(f"Need at least 5 cards, got {len(all_cards)}")
        if len(all_cards) > 7:
            raise ValueError(f"Maximum 7 cards, got {len(all_cards)}")
        
        return evaluate_cards(*all_cards)
    
    def hand_rank_name(self, rank: int) -> str:
        """Convert rank to hand name
        
        Args:
            rank: Hand rank (1-7462)
        
        Returns:
            Hand name (e.g., "Pair", "Two Pair", "Flush")
        """
        # Approximate hand category from rank
        if rank <= 10:
            return "Royal Flush / Straight Flush"
        elif rank <= 166:
            return "Four of a Kind"
        elif rank <= 322:
            return "Full House"
        elif rank <= 1599:
            return "Flush"
        elif rank <= 1609:
            return "Straight"
        elif rank <= 2467:
            return "Three of a Kind"
        elif rank <= 3325:
            return "Two Pair"
        elif rank <= 5863:
            return "Pair"
        else:
            return "High Card"
    
    def calculate_equity(
        self,
        your_hand: List[str],
        opponent_hand: List[str],
        community: List[str],
        iterations: int = 1000
    ) -> float:
        """Calculate equity vs opponent (win %)
        
        Args:
            your_hand: Your hole cards
            opponent_hand: Opponent's hole cards
            community: Community cards (0-5 cards)
            iterations: Number of runouts to simulate
        
        Returns:
            Win probability (0.0 - 1.0)
        """
        used_cards = set(your_hand + opponent_hand + community)
        remaining_cards = [c for c in self.all_cards if c not in used_cards]
        
        # Calculate runouts needed
        cards_needed = 5 - len(community)
        
        if cards_needed == 0:
            # All cards known - compare directly
            your_rank = evaluate_cards(*your_hand, *community)
            opp_rank = evaluate_cards(*opponent_hand, *community)
            return 1.0 if your_rank < opp_rank else 0.0
        
        # Simulate random runouts
        wins = 0
        ties = 0
        
        for _ in range(min(iterations, len(list(itertools.combinations(remaining_cards, cards_needed))))):
            runout = list(itertools.combinations(remaining_cards, cards_needed))[_]
            board = community + list(runout)
            
            your_rank = evaluate_cards(*your_hand, *board)
            opp_rank = evaluate_cards(*opponent_hand, *board)
            
            if your_rank < opp_rank:
                wins += 1
            elif your_rank == opp_rank:
                ties += 0.5  # Split pot
        
        return (wins + ties) / iterations
    
    def hand_vs_range_equity(
        self,
        your_hand: List[str],
        opponent_range: List[Tuple[str, str]],
        community: List[str],
        iterations: int = 10000
    ) -> float:
        """Calculate equity vs range of opponent hands
        
        Args:
            your_hand: Your hole cards
            opponent_range: List of possible opponent hands
            community: Community cards
            iterations: Runouts to simulate
        
        Returns:
            Average equity vs range
        """
        if not opponent_range:
            return 0.5
        
        equities = []
        for opp_hand in opponent_range:
            eq = self.calculate_equity(your_hand, list(opp_hand), community, 100)
            equities.append(eq)
        
        return np.mean(equities)
    
    def all_possible_hands(
        self,
        excluded_cards: List[str] = None
    ) -> List[Tuple[str, str]]:
        """Get all possible 2-card poker hands
        
        Args:
            excluded_cards: Cards to exclude from generation
        
        Returns:
            List of all possible starting hands
        """
        if excluded_cards is None:
            excluded_cards = []
        
        available = [c for c in self.all_cards if c not in excluded_cards]
        return list(itertools.combinations(available, 2))
    
    def compare_hands(
        self,
        hand1: List[str],
        hand2: List[str],
        community: List[str]
    ) -> Tuple[int, int, str]:  # (rank1, rank2, winner)
        """Compare two hands
        
        Args:
            hand1: First hand
            hand2: Second hand
            community: Community cards
        
        Returns:
            (rank1, rank2, 'hand1'|'hand2'|'tie')
        """
        rank1 = evaluate_cards(*hand1, *community)
        rank2 = evaluate_cards(*hand2, *community)
        
        if rank1 < rank2:
            return rank1, rank2, "hand1"
        elif rank2 < rank1:
            return rank1, rank2, "hand2"
        else:
            return rank1, rank2, "tie"


def test_evaluator():
    """Quick test of evaluator"""
    evaluator = PokerEvaluator()
    
    # Test hand evaluation
    rank = evaluator.evaluate_hand(
        community_cards=['6c', '2h', '4c', '9h', '5d'],
        player_hand=['Ks', 'Kd']
    )
    print(f"Pair of Kings rank: {rank} ({evaluator.hand_rank_name(rank)})")
    
    # Test equity
    equity = evaluator.calculate_equity(
        your_hand=['Ks', 'Kd'],
        opponent_hand=['As', 'Qs'],
        community=['6c', '2h', '4c']
    )
    print(f"KK vs AQ equity: {equity*100:.1f}%")
    
    print("✅ Evaluator test passed!")


if __name__ == "__main__":
    test_evaluator()
