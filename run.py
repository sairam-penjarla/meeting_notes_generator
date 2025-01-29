from src.utils import Utilities
from custom_logger import logger
from flask import jsonify
import os
import traceback
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)
utils = Utilities()

@app.route("/")
def landing_page():
    try:
        previous_session_meta_data = utils.session_utils.get_session_meta_data()
        return render_template("index.html", previous_session_meta_data=previous_session_meta_data)
    except Exception:
        print("Error in landing_page function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/get_random_session_icon', methods=['POST'])
def get_random_session_icon():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        return jsonify({"relavant_schema": utils.get_session_icon(session_id)})
    except Exception:
        print("Error in get_random_session_icon function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/get_session_data', methods=['POST'])
def get_session_data():
    try:
        data = request.get_json()
        session_id = data.get('sessionId')
        session_data = utils.session_utils.get_session_data(session_id)
        return jsonify({'session_data': session_data})
    except Exception:
        print("Error in get_session_data function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/delete_session', methods=['POST'])
def delete_session():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        if not session_id:
            return jsonify({"error": "Session ID is required."}), 400
        response, status_code = utils.session_utils.delete_session(session_id)
        return jsonify(response), status_code
    except Exception:
        print("Error in delete_session function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/delete_all_sessions', methods=['POST'])
def delete_all_sessions():
    try:
        response, status_code = utils.session_utils.delete_all_sessions()
        return jsonify(response), status_code
    except Exception:
        print("Error in delete_all_sessions function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/update_session', methods=['POST'])
def update_session():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        session_icon = data.get('session_icon')
        transcript = data.get('transcript')
        participants = data.get('participants')
        summary = data.get('summary')
        notes = data.get('notes')
        action_items = data.get('action_items')
        session_name = data.get('session_name')
        utils.session_utils.add_data(session_id, session_icon, transcript, participants, summary, notes, action_items, session_name)
        return jsonify({"success": True})
    except Exception:
        print("Error in update_session function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/read_transcript', methods=['POST'])
def read_transcript():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400
    try:
        file_content = file.read()
        file_type = os.path.splitext(file.filename)[1]
        transcript = utils.extract_text(file_content, file_type)
        return jsonify({"transcript": transcript}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Error in read_transcript function:")
        print(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

@app.route('/get_session_name', methods=['POST'])
def get_session_name():
    try:
        data = request.get_json()
        transcript = data.get('transcript')
        messages = utils.get_previous_messages("session_name")
        msg = {"role": "user", "content": transcript}
        llm_output = utils.invoke_llm(messages=messages+[msg])
        return jsonify({"session_name": llm_output}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Error in read_transcript function:")
        print(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
    
@app.route('/invoke_agent', methods=['POST'])
def invoke_agent():
    try:
        data = request.get_json()
        transcript = data.get('transcript')
        component = data.get('component')
        messages = utils.get_previous_messages(component)
        msg = {"role": "user", "content": transcript}
        agent_output = utils.invoke_llm_stream(messages=messages + [msg])
        return Response(agent_output, content_type='text/event-stream')
    except Exception:
        print("Error in invoke_agent function:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
