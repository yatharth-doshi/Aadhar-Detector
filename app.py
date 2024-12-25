from flask import Flask, request, jsonify
from aadhar_card_detector import AadharCardDetector
from PIL import Image
import os

app = Flask(__name__)

model_path = "./models/model.pt"  # Update with your actual path
detector = AadharCardDetector(model_path)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/validate', methods=['POST'])
def detect_aadhar():
    if 'doc' not in request.files:
        return jsonify({'msg': "error", 'content': 'No file part in the request'}), 400

    file = request.files['doc']
    if file.filename == '':
        return jsonify({'msg': "error", 'content': 'No selected file'}), 400

    try:
        # Save uploaded file to temporary folder
        temp_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(temp_image_path)

        image = Image.open(temp_image_path)
        
        # Check if it's an Aadhaar card
        is_aadhar = detector.is_aadhar_card(image)
        data = {}
        if is_aadhar:
            data['msg'] = "success"
            data['content'] = True
        else:
            data['msg'] = "success"
            data['content'] = False
        
        os.remove(temp_image_path)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({'msg': "error", 'content': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000, debug=True)
