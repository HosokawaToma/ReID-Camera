import numpy as np
from ultralytics.engine.results import Boxes
from ultralytics.models.yolo import YOLO

from entities.yolo.bounding_box import EntityYoloBoundingBox
from entities.yolo.detections import EntityYoloDetections


class ApplicationYoloModel:
    def __init__(
        self,
        model_path: str = "resources/models/yolo11n.pt",
        confidence_threshold: float = 0.5,
        iou_threshold: float = 0.3,
        imgsz: tuple[int, int] = (640, 640),
        agnostic_nms: bool = False,
        person_class_id: int = 0,
        verbose: bool = False,
        tracker: str = "bytetrack.yaml",
    ):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.imgsz = imgsz
        self.agnostic_nms = agnostic_nms
        self.person_class_id = person_class_id
        self.verbose = verbose
        self.tracker = tracker

    def extract_person_detections(self, frame: np.ndarray) -> list[EntityYoloDetections]:
        yolo_results = self.model.track(
            frame,
            persist=True,
            classes=[self.person_class_id],
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            imgsz=self.imgsz,
            agnostic_nms=self.agnostic_nms,
            verbose=self.verbose,
            tracker=self.tracker,
        )

        detections = []
        yolo_result = yolo_results[0]

        if yolo_result.boxes is not None:
            for box in yolo_result.boxes:
                box: Boxes
                if box.id is not None:
                    box_id = int(box.id[0].cpu().numpy())
                else:
                    box_id = None
                box_xyxy = box.xyxy[0].cpu().numpy()
                box_x1 = int(box_xyxy[0])
                box_y1 = int(box_xyxy[1])
                box_x2 = int(box_xyxy[2])
                box_y2 = int(box_xyxy[3])
                box_xywh = box.xywh[0].cpu().numpy()
                box_width = int(box_xywh[2])
                box_height = int(box_xywh[3])
                box_conf = box.conf[0].cpu().numpy()
                box_cls = int(box.cls[0].cpu().numpy())
                bounding_box = EntityYoloBoundingBox(
                    box_x1, box_y1, box_x2, box_y2, box_width, box_height)
                detections.append(EntityYoloDetections(
                    box_id, bounding_box, box_conf, box_cls
                ))

        return detections
