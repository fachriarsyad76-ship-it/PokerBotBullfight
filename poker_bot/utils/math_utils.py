"""Poker mathematics utilities"""

import math
from typing import Tuple


def pot_odds(call_amount: float, pot_size: float) -> float:
    """Calculate pot odds (required equity to break even)
    
    Args:
        call_amount: Amount you need to call
        pot_size: Current pot size
    
    Returns:
        Required equity (0.0-1.0)
    """
    if pot_size + call_amount == 0:
        return 0.0
    return call_amount / (pot_size + call_amount)


def implied_odds(
    call_amount: float,
    pot_size: float,
    future_winnings: float
) -> float:
    """Calculate implied odds (accounting for future bets)
    
    Args:
        call_amount: Amount to call now
        pot_size: Current pot
        future_winnings: Additional amount you expect to win
    
    Returns:
        Required equity
    """
    total_win = pot_size + call_amount + future_winnings
    return call_amount / total_win


def expected_value(
    equity: float,
    win_amount: float,
    loss_amount: float
) -> float:
    """Calculate expected value of a decision
    
    EV = (Equity × Win) - ((1 - Equity) × Loss)
    
    Args:
        equity: Win probability (0.0-1.0)
        win_amount: Amount won if successful
        loss_amount: Amount lost if unsuccessful
    
    Returns:
        Expected value
    """
    return (equity * win_amount) - ((1 - equity) * loss_amount)


def ev_gain(equity: float, call_amount: float, pot_size: float) -> float:
    """Calculate EV gain from calling
    
    Args:
        equity: Your equity
        call_amount: Amount to call
        pot_size: Current pot size
    
    Returns:
        Expected value gain/loss
    """
    win_amount = pot_size + call_amount
    loss_amount = call_amount
    return expected_value(equity, win_amount, loss_amount)


def variance(equity: float, num_hands: int) -> float:
    """Calculate variance over N hands (Bernoulli)
    
    Args:
        equity: Win probability
        num_hands: Number of hands
    
    Returns:
        Variance
    """
    return num_hands * equity * (1 - equity)


def standard_deviation(equity: float, num_hands: int) -> float:
    """Calculate standard deviation
    
    Args:
        equity: Win probability
        num_hands: Number of hands
    
    Returns:
        Standard deviation
    """
    return math.sqrt(variance(equity, num_hands))


def confidence_interval(
    equity: float,
    num_hands: int,
    confidence_level: float = 0.95
) -> Tuple[float, float]:
    """Calculate confidence interval for equity
    
    Args:
        equity: Observed equity
        num_hands: Sample size
        confidence_level: Confidence level (default 95%)
    
    Returns:
        (lower_bound, upper_bound)
    """
    z_score = 1.96 if confidence_level == 0.95 else 2.576  # 99%
    margin = z_score * standard_deviation(equity, num_hands) / math.sqrt(num_hands)
    return (equity - margin, equity + margin)
