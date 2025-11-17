import logging
from control_models.base import ControlModel
from typing import List, Dict
from ultralytics import YOLO 

logger = logging.getLogger(__name__)

class CustomModel(ControlModel):
    """
    Control model for the custom YOLOv8 Cupra model using rectangle labels.
    """

    type = "RectangleLabels"  
    model_path = "team_chambe_3L_fine_tune.pt"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info(f"CupraModel loading weights from path: {self.model_path}")
        self.model = self.get_cached_model(self.model_path)             

    @classmethod
    def is_control_matched(cls, control) -> bool:
        if control.objects[0].tag != "Image":
            return False
        return control.tag == cls.type

    def predict_regions(self, path) -> List[Dict]:
        results = self.model.predict(path)
        self.debug_plot(results[0].plot())  # Optional: to visualize prediction

        return self.create_rectangles(results, path)

    def create_rectangles(self, results, path):
        logger.debug(f"create_rectangles: {self.from_name}")
        data = results[0].boxes  # take bounding boxes from first frame
        model_names = self.model.names
        regions = []

        for i in range(data.shape[0]):  # iterate detections
            score = float(data.conf[i])
            x, y, w, h = data.xywhn[i].tolist()  # normalized xywh (center x,y, width, height)
            model_label = model_names[int(data.cls[i])]

            logger.debug(
                "----------------------\n"
                f"task id > {path}\n"
                f"type: {self.control}\n"
                f"x, y, w, h > {x, y, w, h}\n"
                f"model label > {model_label}\n"
                f"score > {score}\n"
            )

            if score < self.model_score_threshold:
                continue

            if model_label not in self.label_map:
                continue
            output_label = self.label_map[model_label]

            region = {
                "from_name": self.from_name,
                "to_name": self.to_name,
                "type": "rectanglelabels",
                "value": {
                    "rectanglelabels": [output_label],
                    "x": (x - w / 2) * 100,
                    "y": (y - h / 2) * 100,
                    "width": w * 100,
                    "height": h * 100,
                },
                "score": score,
            }
            regions.append(region)
        return regions

# Preload your model at startup
CustomModel.get_cached_model(CustomModel.model_path)
