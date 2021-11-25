import numpy as np
import cv2


class MLProcessing:

    def process(image):
        data = image_string.split("base64,")
        nparr = np.fromstring(base64.b64decode(data[1]), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image