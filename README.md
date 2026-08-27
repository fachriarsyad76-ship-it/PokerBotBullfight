# 🎰 Poker Bot Bullfight & Texas Hold'em

**Advanced AI Poker Bot dengan GTO Strategy, Hand Evaluator & Beautiful GUI**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)

## 📋 Fitur Utama

✅ **Hand Evaluator Super Cepat**
- Menggunakan PokerHandEvaluator (PHEvaluator) dari HenryRLee
- Evaluasi 60M hands/detik
- Support 5-card, 6-card, 7-card, dan Omaha

✅ **GTO Strategy Foundation**
- Counterfactual Regret Minimization (CFR) Basics
- Pot Odds & Equity Calculations
- Nash Equilibrium Approximation
- Exploitative Play Support

✅ **Beautiful GUI**
- PyQt6-based interface (mirip platform asli)
- Real-time hand analysis
- Turn/River prediction
- Game statistics & tracking

✅ **Game Support**
- Texas Hold'em (Full Game)
- Bullfight/Thai Poker
- Cash Games & Tournaments

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/fachriarsyad76-ship-it/PokerBotBullfight.git
cd PokerBotBullfight

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from poker_bot.evaluator import PokerEvaluator
from poker_bot.strategy import GTOStrategy

# Initialize evaluator
evaluator = PokerEvaluator()

# Evaluate hand strength
rank = evaluator.evaluate_hand(
    community_cards=['6c', '2h', '4c', '9h'],
    player_hand=['Ks', 'Kd']
)

print(f"Hand Strength Rank: {rank} (1-7462, lower = stronger)")

# Calculate equity vs opponent
equity = evaluator.calculate_equity(
    your_hand=['Ks', 'Kd'],
    opponent_hand=['As', 'Qs'],
    community=['6c', '2h', '4c', '9h']
)

print(f"Equity: {equity*100:.2f}%")
```

### Launch GUI

```bash
python -m poker_bot.gui.main_window
```

## 📁 Project Structure

```
PokerBotBullfight/
├── poker_bot/
│   ├── __init__.py
│   ├── evaluator.py          # Hand evaluation engine
│   ├── strategy.py           # GTO & decision logic
│   ├── game_engine.py        # Core game mechanics
│   ├── opponent_model.py     # Player profiling
│   ├── utils/
│   │   ├── card_utils.py     # Card manipulation
│   │   ├── math_utils.py     # Poker mathematics
│   │   └── config.py         # Configuration
│   └── gui/
│       ├── main_window.py    # Main GUI window
│       ├── game_display.py   # Game visualization
│       ├── stats_panel.py    # Statistics panel
│       └── themes.py         # UI themes
├── tests/
│   ├── test_evaluator.py
│   ├── test_strategy.py
│   └── test_game_engine.py
├── docs/
│   ├── GTO_BASICS.md
│   ├── API.md
│   └── STRATEGY_GUIDE.md
├── requirements.txt
├── setup.py
└── README.md
```

## 🎯 Architecture

### 1. Hand Evaluator Layer
- **phevaluator**: High-performance C++ binding
- **Rank System**: 1-7462 scale (lower = stronger)
- **Equity Calculation**: Monte Carlo + Exact methods

### 2. Strategy Layer
- **CFR Solver**: Approximate Nash Equilibrium
- **Pot Odds**: Real-time EV calculation
- **Position-Aware**: UTG, CO, BTN, SB, BB strategies

### 3. Game Engine Layer
- **Game State**: Track cards, players, pot
- **Action History**: All moves logged
- **Hand Resolution**: Automatic winner determination

### 4. GUI Layer
- **PyQt6**: Modern, responsive interface
- **Real-time Updates**: Live equity changes
- **Statistics**: Win rates, ROI, variance tracking

## 📊 Key Algorithms

### Counterfactual Regret Minimization (CFR)
```
CFR = ∑ max(0, counterfactual_value) / T

Approaches Nash Equilibrium as iterations increase
Ideal for GTO strategy generation
```

### Equity Calculation
```
Equity = (Winning Outcomes) / (Total Possible Outcomes)

Example: 50% equity = Win against opponent 50% of runouts
```

### Pot Odds Decision
```
Call if: Equity ≥ (Call Amount) / (Pot + Call Amount)

Optimal when: EV[Call] > EV[Fold]
```

## 🔧 Configuration

Edit `poker_bot/utils/config.py`:

```python
# Game Configuration
GAME_CONFIG = {
    'game_type': 'TEXAS_HOLDEM',  # or 'BULLFIGHT'
    'players': 6,
    'big_blind': 10,
    'small_blind': 5,
    'ante': 0,
}

# Strategy Configuration
STRATEGY_CONFIG = {
    'use_gto': True,
    'cfr_iterations': 1000,
    'exploit_adjustment': 0.3,  # 0-1 scale
    'position_aware': True,
}

# GUI Configuration
GUI_CONFIG = {
    'theme': 'dark',  # or 'light'
    'update_interval': 100,  # ms
    'show_equity': True,
    'show_ev': True,
}
```

## 📈 Backtesting

```python
from poker_bot.backtester import Backtester

bt = Backtester(
    strategy='gto',
    starting_stack=1000,
    num_hands=10000
)

results = bt.run()
print(f"Winrate: {results['bb_per_100']:.2f} BB/100")
print(f"ROI: {results['roi']:.2%}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
```

## 🎓 Learning Resources

### GTO Concepts
- [Pot Odds & Implied Odds](docs/STRATEGY_GUIDE.md)
- [Nash Equilibrium Basics](docs/GTO_BASICS.md)
- [CFR Algorithm Explained](docs/CFR_DEEP_DIVE.md)

### References
- DeepStack (2017) - AI Poker Superhuman Performance
- Libratus (2017) - Blueprint Strategy + Real-time Solving
- Pluribus (2019) - Multi-player GTO AI

## ⚠️ Disclaimer

⚠️ **Educational Purpose Only**
- Bot development adalah untuk research & learning
- Use responsibly sesuai local laws
- Respect poker platform terms of service
- Hasil backtest ≠ real-world performance

## 🤝 Contributing

Contributions welcome! Silakan:

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - lihat [LICENSE](LICENSE) file untuk details

## 📞 Support

- 📧 Email: fachriarsyad76@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/fachriarsyad76-ship-it/PokerBotBullfight/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/fachriarsyad76-ship-it/PokerBotBullfight/discussions)

---

**Made with ❤️ by Fachri Arsyad**
