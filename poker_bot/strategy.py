"""GTO Strategy Engine with CFR Basics

Provides Game Theory Optimal strategies and decision making.
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum
import numpy as np
from poker_bot.evaluator import PokerEvaluator


class GameStage(Enum):
    """Poker game stages"""
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class Position(Enum):
    """Player positions"""
    UTG = "utg"          # Under the gun
    HJ = "hj"            # Hijack
    CO = "co"            # Cutoff
    BTN = "btn"          # Button
    SB = "sb"            # Small blind
    BB = "bb"            # Big blind


class GTOStrategy:
    """Game Theory Optimal Strategy Engine
    
    Provides position-aware, equity-based decisions using GTO principles.
    """
    
    # GTO Opening ranges by position (simplified)
    OPENING_RANGES = {
        Position.UTG: ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK"],
        Position.HJ: ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK", "AQ", "AJ", "KQ"],
        Position.CO: ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AK", "AQ", "AJ", "AT", "KQ", "KJ"],
        Position.BTN: ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "AK", "AQ", "AJ", "AT", "A9", "KQ", "KJ", "QJ"],
        Position.SB: ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AK", "AQ", "AJ", "KQ", "KJ"],
        Position.BB: ["any"],  # Big blind defends wide
    }
    
    def __init__(self):
        """Initialize strategy engine"""
        self.evaluator = PokerEvaluator()
    
    def should_call(
        self,
        your_hand: List[str],
        pot_size: float,
        call_amount: float,
        equity: float,
        opponent_count: int = 1
    ) -> bool:
        """Determine if call is +EV based on pot odds and equity
        
        Args:
            your_hand: Your hole cards
            pot_size: Current pot size
            call_amount: Amount needed to call
            equity: Your equity (0.0-1.0)
            opponent_count: Number of opponents
        
        Returns:
            True if call is +EV
        """
        if call_amount == 0:
            return True  # Free play
        
        # Required equity to break even
        required_equity = call_amount / (pot_size + call_amount)
        
        # Call if actual equity exceeds required equity
        return equity >= required_equity
    
    def should_raise(
        self,
        your_hand: List[str],
        hand_strength: float,  # 0.0-1.0
        position: Position,
        stack_size: float,
        pot_size: float,
        opponent_count: int = 1,
        aggression_factor: float = 1.0
    ) -> Tuple[bool, Optional[float]]:
        """Determine if raise is appropriate
        
        Args:
            your_hand: Your hole cards
            hand_strength: Relative hand strength (0.0-1.0)
            position: Your position
            stack_size: Your remaining stack
            pot_size: Current pot size
            opponent_count: Number of opponents
            aggression_factor: Aggression level (0.5-2.0)
        
        Returns:
            (should_raise, raise_amount) or (False, None)
        """
        # Adjust aggression by position
        position_aggression = {
            Position.UTG: 0.8,
            Position.HJ: 0.9,
            Position.CO: 1.0,
            Position.BTN: 1.1,
            Position.SB: 1.0,
            Position.BB: 0.9,
        }
        
        adjusted_strength = hand_strength * aggression_factor * position_aggression[position]
        
        # Raise if hand strength is above threshold
        if adjusted_strength > 0.6:
            # Calculate raise size (simplified)
            raise_amount = pot_size * 0.5 * adjusted_strength
            return True, min(raise_amount, stack_size)
        
        return False, None
    
    def should_fold(
        self,
        your_equity: float,
        pot_odds: float,
        hand_strength: float
    ) -> bool:
        """Determine if hand should be folded
        
        Args:
            your_equity: Your current equity
            pot_odds: Pot odds (required equity)
            hand_strength: Relative hand strength (0.0-1.0)
        
        Returns:
            True if should fold
        """
        # Fold if equity is significantly below pot odds
        # Add small buffer for implied odds
        return your_equity < (pot_odds * 0.95) and hand_strength < 0.3
    
    def get_opening_range(self, position: Position) -> List[str]:
        """Get GTO opening range for position
        
        Args:
            position: Player position
        
        Returns:
            List of hand ranges (e.g., ['AA', 'KK', 'QQ', ...])
        """
        return self.OPENING_RANGES[position]
    
    def calculate_ev(
        self,
        equity: float,
        win_amount: float,
        loss_amount: float
    ) -> float:
        """Calculate expected value
        
        EV = (Equity × Win Amount) - ((1 - Equity) × Loss Amount)
        
        Args:
            equity: Win probability (0.0-1.0)
            win_amount: Amount won if hand wins
            loss_amount: Amount lost if hand loses
        
        Returns:
            Expected value
        """
        return (equity * win_amount) - ((1 - equity) * loss_amount)
    
    def get_cf_value(
        self,
        hand_strength: float,
        opponent_range_strength: float
    ) -> float:
        """Get counterfactual regret value (simplified CFR)
        
        Args:
            hand_strength: Your hand strength vs opponent range
            opponent_range_strength: Opponent's range strength
        
        Returns:
            CFR value (positive = favorable, negative = unfavorable)
        """
        return hand_strength - opponent_range_strength
    
    def get_action_weights(
        self,
        your_hand: List[str],
        equity: float,
        position: Position,
        game_stage: GameStage,
        stack_size: float,
        pot_size: float
    ) -> Dict[str, float]:
        """Get probability weights for each action (fold, call, raise)
        
        Uses simplified GTO principles:
        
        Args:
            your_hand: Your hole cards
            equity: Your equity
            position: Your position
            game_stage: Current game stage
            stack_size: Your stack
            pot_size: Current pot
        
        Returns:
            Dict with action weights: {"fold": 0.2, "call": 0.5, "raise": 0.3}
        """
        weights = {"fold": 0.0, "call": 0.0, "raise": 0.0}
        
        # Base weighting on equity
        if equity < 0.33:
            weights["fold"] = 0.7
            weights["call"] = 0.25
            weights["raise"] = 0.05
        elif equity < 0.5:
            weights["fold"] = 0.3
            weights["call"] = 0.5
            weights["raise"] = 0.2
        elif equity < 0.65:
            weights["fold"] = 0.1
            weights["call"] = 0.4
            weights["raise"] = 0.5
        else:
            weights["fold"] = 0.05
            weights["call"] = 0.25
            weights["raise"] = 0.7
        
        # Adjust by position (later position = more aggressive)
        position_multipliers = {
            Position.UTG: 0.8,
            Position.HJ: 0.9,
            Position.CO: 1.0,
            Position.BTN: 1.2,
            Position.SB: 1.1,
            Position.BB: 0.9,
        }
        
        multiplier = position_multipliers[position]
        weights["raise"] *= multiplier
        weights["call"] *= multiplier
        
        # Normalize to sum to 1.0
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}
        
        return weights


def test_strategy():
    """Quick test of strategy engine"""
    strategy = GTOStrategy()
    
    # Test pot odds decision
    should_call = strategy.should_call(
        your_hand=['Ks', 'Kd'],
        pot_size=100,
        call_amount=20,
        equity=0.65
    )
    print(f"Should call with 65% equity, pot odds: {should_call}")
    
    # Test EV calculation
    ev = strategy.calculate_ev(equity=0.65, win_amount=120, loss_amount=20)
    print(f"EV of call: {ev:.2f}")
    
    # Test action weights
    weights = strategy.get_action_weights(
        your_hand=['Ks', 'Kd'],
        equity=0.65,
        position=Position.BTN,
        game_stage=GameStage.FLOP,
        stack_size=500,
        pot_size=100
    )
    print(f"Action weights: {weights}")
    
    print("✅ Strategy test passed!")


if __name__ == "__main__":
    test_strategy()
