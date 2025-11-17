import logging
from control_models.base import ControlModel
from typing import List, Dict

logger = logging.getLogger(__name__)

class PolygonLabelsModel(ControlModel):
    """
    Class representing a PolygonLabels control tag for YOLO model.
    """

    type = "PolygonLabels"
    model_path = "liquimoly-seg.pt"

    def __init__(self, *args, model_score_threshold=0.25, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_score_threshold = model_score_threshold
        logger.info(f"Confidence threshold set to {self.model_score_threshold}")

    @classmethod
    def is_control_matched(cls, control) -> bool:
        if control.objects[0].tag != "Image":
            return False
        return control.tag == cls.type

    def predict_regions(self, path) -> List[Dict]:
        results = self.model.predict(path)
        return self.create_polygons(results, path)

    def create_polygons(self, results, path):
        logger.debug(f"create_polygons: {self.from_name}")
        data = results[0].masks
        if data is None:
            logger.warning(f"No masks returned for {path}")
            return []
        
        model_names = self.model.names
        regions = []

        for i in range(len(data)):
            score = float(results[0].boxes.conf[i])
            points = (data.xyn[i] * 100)
            model_label = model_names[int(results[0].boxes.cls[i])]

            if score < self.model_score_threshold:
                continue

            # Print/log if model_label not in label_map
            if model_label not in self.label_map:
                logger.warning(f"Model label '{model_label}' not found in label_map. Even correct detections are skipped.")
                print(f"Warning: Detected label '{model_label}' not present in label_map — detections skipped.")
                continue

            output_label = self.label_map[model_label]

            region = {
                "from_name": self.from_name,
                "to_name": self.to_name,
                "type": "polygonlabels",
                "value": {
                    "polygonlabels": [output_label],
                    "points": points.tolist(),
                    "closed": True,
                },
                "score": score,
            }
            regions.append(region)
        return regions

# preload and cache default model at startup
PolygonLabelsModel.get_cached_model(PolygonLabelsModel.model_path)
