from ultralytics import YOLO
from supervision import Detections

class AadharCardDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.id2label = self.model.names
        self.required_classes = {'AADHAR_NUMBER', 'NAME'}
    
    def is_aadhar_card(self, image_path):
        # Perform Inference
        detections = Detections.from_ultralytics(self.model.predict(image_path)[0])
        
        # Extract detected class names from detections
        detected_classes = set(detections.data['class_name'])
        
        # Check if any of the required classes are detected
        is_aadhar_card = any(cls in detected_classes for cls in self.required_classes)
        
        print("Detected classes:", detected_classes)
        return is_aadhar_card