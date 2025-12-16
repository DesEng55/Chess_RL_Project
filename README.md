# ♟️ Chess RL Multi-Agent System

A real-time chess reinforcement learning system where multiple AI agents compete, learn, and evolve through self-play. Watch agents battle on a beautiful web interface with live updates, ELO ratings, and detailed statistics.


## 🌟 Features

### 🎮 Real-Time Visualization
- **Live Chess Board**: Watch games unfold move-by-move with smooth animations
- **Move History**: Track every move with position evaluations
- **Active Player Highlighting**: See which agent is currently thinking
- **WebSocket Updates**: Zero-latency real-time communication

### 🤖 Multi-Agent System
- **4 Independent Agents**: Each with their own neural network
- **ELO Rating System**: Track agent strength with dynamic ratings
- **Complete Statistics**: Wins, losses, draws, games played, win rate
- **Smart Matchmaking**: Agents compete against different opponents

### 🧠 Neural Network Architecture
- **ResNet-Based**: 3 residual blocks with 64 channels
- **Policy Head**: Move probability distribution
- **Value Head**: Position evaluation (-1 to +1)
- **12-Channel Input**: Encodes all piece positions (6 types × 2 colors)

### 📊 Training & Analytics
- **Training Sessions**: Run multiple matches automatically
- **Progress Tracking**: Real-time progress bar and match counter
- **System Logs**: Detailed event logging with timestamps
- **Agent Comparison**: Compare all agents side-by-side

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
Modern web browser (Chrome, Firefox, Safari, Edge)
```

### Installation

1. **Clone or download the repository**

```bash
# If using git
git clone <https://github.com/DesEng55/Chess_RL_Project/>
cd chess-rl-system

# Or simply download and extract the files
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

Required packages:
- `flask` - Web framework
- `flask-socketio` - Real-time WebSocket communication
- `flask-cors` - Cross-origin resource sharing
- `python-chess` - Chess game logic and move validation
- `torch` - PyTorch for neural networks
- `numpy` - Numerical computations
- `python-socketio` - SocketIO client/server

### Running the Application

1. **Start the Backend Server**

```bash
python app.py
```

You should see:
```
♟️ Chess RL Backend Running on http://localhost:5000
📊 Dashboard available at: http://localhost:5000
🤖 Population size: 4 agents
⚡ WebSocket connections enabled
```

2. **Open the Frontend**

**Option A: Direct File Access**
```bash
# Simply open index.html in your browser
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

**Option B: Local HTTP Server** (Recommended)
```bash
# Python 3
python -m http.server 8080

# Then open http://localhost:8080/index.html in your browser
```

3. **Start Playing!**
   - Click **"▶️ Play Match"** for a single game
   - Click **"🚀 Start Training"** for 10 consecutive matches
   - Click **"🔄 Reset"** to create fresh agents

## 📖 User Guide

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  🤖 Multi-Agent Chess RL Visualizer  [●Connected]       │
├──────────────────────┬──────────────────────────────────┤
│                      │  📊 Training Status              │
│  ⚪ White Agent      │  ━━━━━━━━━━━━━━━━ 60%           │
│  ELO: 1245  Wins: 3  │                                  │
│                      │  📝 Move History                 │
│  ┌────────────────┐  │  1. e4    (+0.12)               │
│  │  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜│  │  1... e5  (-0.08)               │
│  │  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟│  │  2. Nf3   (+0.15)               │
│  │                │  │                                  │
│  │                │  │  🤖 Active Agents                │
│  │  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙│  │  Agent 0 ⚪  ELO: 1245         │
│  │  ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖│  │  Agent 1 ⚫  ELO: 1198         │
│  └────────────────┘  │  Agent 2     ELO: 1223         │
│                      │  Agent 3     ELO: 1187         │
│  ⚫ Black Agent      │                                  │
│  ELO: 1198  Wins: 1  │  📟 System Log                   │
│                      │  [14:23:45] ✅ Connected        │
│  [▶️Play] [🚀Train]  │  [14:23:50] 🎮 Match started    │
└──────────────────────┴──────────────────────────────────┘
```

### Playing Matches

**Single Match**
1. Click **"▶️ Play Match"**
2. Watch two random agents compete
3. See real-time moves on the board
4. View ELO updates after the game
5. Check updated statistics in the sidebar

**Training Session**
1. Click **"🚀 Start Training"**
2. System automatically plays 10 matches
3. Progress bar shows completion percentage
4. All agents compete in different combinations
5. Final statistics display strongest agent

### Understanding the Interface

**Connection Status** (Top Right)
- 🟢 **Connected**: Backend server is running
- 🔴 **Disconnected**: Cannot reach server

**Player Info Cards**
- Shows current agent ID and color
- Displays ELO rating and total wins
- Highlights active player during their turn
- Glows blue when it's their move

**Chess Board**
- Standard 8×8 board with Unicode pieces
- Light squares: Cream (#f0d9b5)
- Dark squares: Brown (#b58863)
- Last move highlighting in yellow

**Training Status Panel**
- Current match number (e.g., "5/10")
- Total matches played this session
- Current move in algebraic notation
- Visual progress bar

**Move History**
- Numbered moves in standard notation
- Position evaluation for each move
- Green (+) for good moves, Red (-) for bad
- Auto-scrolls to latest move

**Active Agents Panel**
- Lists all 4 agents
- Shows ELO, games played, W/L/D record
- Win rate percentage
- Highlights agents currently playing (⚪⚫)

**System Log**
- Timestamped events
- Connection status changes
- Match results and outcomes
- Error messages if any

## 🏗️ Architecture


### System Components

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │ Flask Server │ ◄─────► │   Agents    │
│             │  HTTP   │              │  Python │             │
│  index.html │ WebSocket│    app.py   │         │  agents.py  │
│             │         │              │         │             │
│  JavaScript │         │  SocketIO    │         │ PolicyNet   │
│   Socket    │         │   Events     │         │  model.py   │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │                        │                        │
      ▼                        ▼                        ▼
  Real-time UI          API Endpoints           Neural Networks
  Visualization        WebSocket Comm          Move Selection
```

### Data Flow

1. **Game Start**
   ```
   User clicks button → API request → Agent selection → 
   Board initialization → WebSocket emit → UI update
   ```

2. **Move Execution**
   ```
   Agent thinks → Neural network forward pass → 
   Best move selected → Board updated → 
   WebSocket emit → UI animated → Next agent turn
   ```

3. **Game End**
   ```
   Game over detected → Result calculated → 
   ELO updated → Statistics recorded → 
   WebSocket emit → UI displays results
   ```

## 🧩 Technical Details

### Board Encoding

The chess board is encoded as a **12×8×8 tensor**:
- **12 channels**: 6 piece types (Pawn, Knight, Bishop, Rook, Queen, King) × 2 colors
- **8×8 spatial**: Standard chess board dimensions
- **Binary encoding**: 1 if piece present, 0 otherwise

```python
Channels:
[0] White Pawns     [6] Black Pawns
[1] White Knights   [7] Black Knights  
[2] White Bishops   [8] Black Bishops
[3] White Rooks     [9] Black Rooks
[4] White Queens    [10] Black Queens
[5] White Kings     [11] Black Kings
```

### Neural Network Architecture

```
Input: 12×8×8 (Board State)
    ↓
Conv2d(12→64, 3×3) + ReLU
    ↓
ResidualBlock(64) ×3
    ↓
    ├─→ Policy Head                   ├─→ Value Head
    │   Conv2d(64→2, 1×1)             │   Conv2d(64→1, 1×1)
    │   BatchNorm + ReLU              │   BatchNorm + ReLU
    │   Flatten                       │   Flatten
    │   Linear(128→128)               │   Linear(64→64)
    │   ReLU                          │   ReLU + Dropout(0.3)
    │   Linear(128→64)                │   Linear(64→1)
    │   Softmax                       │   Tanh
    │   Output: Move probs            │   Output: Position value
    └───────────────────────────────────┘
```

### ELO Rating System

Standard ELO calculation with K-factor of 32:

```python
Expected = 1 / (1 + 10^((Opponent_ELO - Player_ELO) / 400))
New_ELO = Old_ELO + K × (Actual_Score - Expected)

Where:
- Actual_Score: 1.0 (win), 0.5 (draw), 0.0 (loss)
- K = 32 (rating volatility)
```

### Move Selection Algorithm

```python
For each legal move:
    1. Make move on board copy
    2. Encode resulting position
    3. Forward pass through neural network
    4. Get value estimation
    5. Negate value (opponent's perspective)
    6. Undo move
    
Select move with highest value
```

## 🔧 Configuration

### Adjust Agent Population

Edit `app.py`:
```python
system = MultiAgentChessSystem(population_size=4)  # Change to 6, 8, etc.
```

### Change Training Length

Edit the frontend JavaScript or modify API call:
```javascript
body: JSON.stringify({ num_matches: 10 })  // Change to 20, 50, etc.
```

Or in `app.py`:
```python
num_matches = data.get("num_matches", 10)  # Change default
```

### Adjust Move Delay

Edit `agents.py`:
```python
time.sleep(0.3)  # Change delay between moves (seconds)
```

### Modify ELO K-Factor

Edit `agents.py`:
```python
K = 32  # Higher = more volatile ratings
```

### Change Neural Network Size

Edit `model.py`:
```python
self.input_conv = nn.Conv2d(12, 64, 3, padding=1)  # Change 64 to 128, 256
self.res_blocks = nn.Sequential(
    *[ResidualBlock(64) for _ in range(3)]  # Change 3 to 5, 10
)
```

## 📊 API Reference

### REST Endpoints

**POST /api/play-match**
- Starts a single match between two random agents
- Returns: `{"status": "match_started"}`

**POST /api/start-training**
- Starts a training session with multiple matches
- Body: `{"num_matches": 10}`
- Returns: `{"status": "training_started", "num_matches": 10}`

**POST /api/reset**
- Resets system with new agents at 1200 ELO
- Returns: `{"status": "reset"}`

**GET /api/agents**
- Retrieves current agent statistics
- Returns: `{"agents": [...]}`

### WebSocket Events

**Client → Server**
- `connect` - Initial connection
- `disconnect` - Client disconnects
- `request_agents` - Request agent statistics

**Server → Client**
- `board_update` - Initial board state
  ```json
  {"fen": "...", "white_agent": 0, "black_agent": 1}
  ```

- `move_made` - Move executed
  ```json
  {
    "fen": "...",
    "move_san": "e4",
    "move_number": 1,
    "evaluation": 0.12,
    "current_turn": "white"
  }
  ```

- `match_complete` - Game finished
  ```json
  {
    "result": "1-0",
    "winner": "White",
    "white_agent": 0,
    "black_agent": 1,
    "white_elo": 1232.5,
    "black_elo": 1167.5,
    "total_moves": 45
  }
  ```

- `agents_update` - Agent statistics
  ```json
  {
    "agents": [
      {
        "id": 0,
        "elo": 1245.3,
        "games_played": 15,
        "wins": 8,
        "losses": 5,
        "draws": 2
      }
    ]
  }
  ```

- `training_started` - Training begins
- `match_starting` - New match in training
- `training_complete` - Training session ends

## 🐛 Troubleshooting

### Connection Issues

**Problem**: "Disconnected" status in UI

**Solutions**:
1. Verify backend is running: `python app.py`
2. Check port 5000 is not in use: `lsof -i :5000` (Mac/Linux)
3. Check firewall settings
4. Try `http://127.0.0.1:5000` instead of `localhost`

### CORS Errors

**Problem**: Console shows CORS policy errors

**Solution**: Use a local HTTP server instead of `file://` protocol
```bash
python -m http.server 8080
# Open http://localhost:8080/index.html
```

### Training Won't Start

**Problem**: "Training already in progress" error

**Solutions**:
1. Wait for current training to complete
2. Restart the backend server
3. Click "Reset" button

### Slow Performance

**Problem**: Games taking too long

**Solutions**:
1. Reduce move delay in `agents.py`:
   ```python
   time.sleep(0.1)  # Instead of 0.3
   ```
2. Reduce training matches:
   ```javascript
   body: JSON.stringify({ num_matches: 5 })
   ```

### Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

**Problem**: `Address already in use` error

**Solution**: Kill process using port 5000
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 🚧 Known Limitations

### Current Version

1. **No Actual Learning**: Neural networks don't update weights during training. Agents start with random weights and keep them throughout. ELO changes show relative strength, but models don't improve.

2. **Simple Move Selection**: Agents use greedy best-move selection without search algorithms like MCTS (Monte Carlo Tree Search).

3. **No Position Features**: Board encoding only includes piece positions, not advanced features like:
   - Castling rights
   - En passant availability
   - Move history
   - Repetition tracking

4. **Basic Neural Network**: Current architecture is relatively simple compared to state-of-the-art chess engines.

5. **No Model Persistence**: Trained models aren't saved between sessions.

### Future Enhancements

- [ ] Implement reinforcement learning (policy gradient, actor-critic)
- [ ] Add Monte Carlo Tree Search (MCTS)
- [ ] Include game phase detection (opening/middlegame/endgame)
- [ ] Add opening book and endgame tablebases
- [ ] Implement model checkpointing and loading
- [ ] Add human vs AI mode
- [ ] Multi-tournament bracket system
- [ ] Detailed move analysis and suggestions
- [ ] Export games in PGN format
- [ ] Performance metrics dashboard
- [ ] Distributed training across multiple machines

## 🤝 Contributing

Contributions are welcome! Here are some ways to contribute:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Describe new functionality
3. **Submit Pull Requests**: Fix bugs or add features
4. **Improve Documentation**: Clarify or expand README

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Open a Pull Request


## 🎯 Project Roadmap

### Phase 1: Core Functionality ✅
- [x] Multi-agent system
- [x] Real-time WebSocket communication
- [x] ELO rating system
- [x] Beautiful UI with animations
- [x] Training session management

### Phase 2: Intelligence 🚧
- [ ] Implement actual reinforcement learning
- [ ] Add MCTS for better move selection
- [ ] Experience replay buffer
- [ ] Model checkpointing

### Phase 3: Advanced Features 📋
- [ ] Human vs AI mode
- [ ] Tournament brackets
- [ ] Opening books
- [ ] Endgame tablebases
- [ ] PGN export/import

### Phase 4: Scale 🎯
- [ ] Distributed training
- [ ] Cloud deployment
- [ ] Performance optimizations
- [ ] Mobile app

---

**Made with ♟️ and 🤖 by AI enthusiasts**

*Star ⭐ this repo if you found it helpful!*
