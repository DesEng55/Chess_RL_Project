from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import threading

from agents import MultiAgentChessSystem

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

system = MultiAgentChessSystem(population_size=4)
training_in_progress = False

@app.route("/api/play-match", methods=["POST"])
def play_match():
    """Play a single match between two random agents"""
    global training_in_progress
    
    if training_in_progress:
        return jsonify({"error": "Training in progress"}), 400
    
    try:
        # Run match in background thread to allow real-time updates
        def run_match():
            system.play_match(socketio)
        
        thread = threading.Thread(target=run_match)
        thread.start()
        
        return jsonify({"status": "match_started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/start-training", methods=["POST"])
def start_training():
    """Start a training session with multiple matches"""
    global training_in_progress
    
    if training_in_progress:
        return jsonify({"error": "Training already in progress"}), 400
    
    try:
        data = request.get_json()
        num_matches = data.get("num_matches", 10)
        
        # Run training in background thread
        def run_training():
            global training_in_progress
            training_in_progress = True
            try:
                system.train(num_matches, socketio)
            finally:
                training_in_progress = False
        
        thread = threading.Thread(target=run_training)
        thread.start()
        
        return jsonify({
            "status": "training_started",
            "num_matches": num_matches
        })
    except Exception as e:
        training_in_progress = False
        return jsonify({"error": str(e)}), 500

@app.route("/api/reset", methods=["POST"])
def reset():
    """Reset the system with new agents"""
    global system, training_in_progress
    
    if training_in_progress:
        return jsonify({"error": "Cannot reset during training"}), 400
    
    try:
        system = MultiAgentChessSystem(population_size=4)
        
        # Emit updated agent list
        socketio.emit("agents_update", {
            "agents": system.get_agents_stats()
        })
        
        return jsonify({"status": "reset"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/agents", methods=["GET"])
def get_agents():
    """Get current agent statistics"""
    try:
        return jsonify({
            "agents": system.get_agents_stats()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print("Client connected")
    # Send initial agent data
    socketio.emit("agents_update", {
        "agents": system.get_agents_stats()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print("Client disconnected")

@socketio.on('request_agents')
def handle_request_agents():
    """Handle request for agent statistics"""
    try:
        socketio.emit("agents_update", {
            "agents": system.get_agents_stats()
        })
    except Exception as e:
        print(f"Error sending agent data: {e}")

if __name__ == "__main__":
    print("♟️ Chess RL Backend Running on http://localhost:5000")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🤖 Population size: 4 agents")
    print("⚡ WebSocket connections enabled")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)