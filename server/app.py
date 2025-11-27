from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import database
from agents import gemini_agent, fallback_agent, analytics_agent, system_agent, planner_agent, resource_agent

app = Flask(__name__)
CORS(app)

# Initialize DB
database.init_db()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    user_id = data.get('user_id', 1) # Default user ID 1 for now

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # 1. Get History
    history = database.get_chat_history(user_id)

    # 2. Try Gemini
    response_text = gemini_agent.generate_response(history, user_input)
    
    # 3. Fallback if Gemini fails
    if not response_text:
        response_text = fallback_agent.get_fallback_response(user_input)
        source = "fallback"
    else:
        source = "gemini"

    # 4. Log Chat
    database.log_chat(user_id, "user", user_input)
    database.log_chat(user_id, "model", response_text)

    # 5. Analyze Sentiment (Background-ish)
    sentiment = analytics_agent.analyze_sentiment(user_input)
    database.log_sentiment(user_id, sentiment['score'], sentiment['magnitude'])

    return jsonify({
        "response": response_text,
        "source": source,
        "sentiment": sentiment
    })

@app.route('/api/agent/planner', methods=['POST'])
def planner():
    # Generate a plan based on time of day (and optional mood if we had it from req)
    plan = planner_agent.generate_plan()
    return jsonify({"response": plan, "source": "planner_agent"})

@app.route('/api/agent/resource', methods=['POST'])
def resource():
    data = request.json
    mood = data.get('mood', 'general')
    strategy = resource_agent.get_strategy(mood)
    return jsonify({"response": strategy, "source": "resource_agent"})

@app.route('/api/analytics', methods=['GET'])
def analytics():
    user_id = request.args.get('user_id', 1)
    history = database.get_sentiment_history(user_id)
    return jsonify(history)

@app.route('/api/export', methods=['GET'])
def export_data():
    user_id = request.args.get('user_id', 1)
    chats = database.get_chat_history(user_id, limit=1000) # Get all chats
    sentiment = database.get_sentiment_history(user_id)
    
    export_data = {
        "user_id": user_id,
        "exported_at": str(datetime.datetime.now()),
        "chats": chats,
        "sentiment_logs": sentiment
    }
    
    return jsonify(export_data)

@app.route('/api/system', methods=['GET'])
def system_status():
    status = system_agent.get_system_status()
    return jsonify(status)

@app.route('/api/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id', 1)
    history = database.get_chat_history(user_id)
    return jsonify(history)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
