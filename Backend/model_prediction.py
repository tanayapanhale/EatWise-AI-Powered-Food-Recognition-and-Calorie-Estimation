from ultralytics import YOLO
model = YOLO(r"Model_Training/Model_Exported/best.pt")

def get_model_predictions(file_path):
    results = model.predict(file_path,save=True, project="Results")
    classes = list(results[0].boxes.cls.cpu().numpy())
    detected_items = [results[0].names[c] for c in classes]
    return detected_items

def get_model_recognitions(file_path):
    results = model.predict(file_path,save=True, project="Detects")