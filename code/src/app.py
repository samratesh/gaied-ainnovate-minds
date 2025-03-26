from flask import Flask, request, jsonify
from main import process_email  

app = Flask(__name__)

@app.route('/process-email', methods=['POST'])
def process_email_api():
    data = request.get_json()
    
    if not data or 'eml_path' not in data:
        return jsonify({"error": "Missing 'eml_path' in request"}), 400

    eml_path = data['eml_path']
    
    try:
        result = process_email(eml_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Runs on http://127.0.0.1:5000