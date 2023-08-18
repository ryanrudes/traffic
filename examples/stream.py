import sys
sys.path.insert(0, "..")

from traffic import API

import random
import cv2

key = input("Enter your API key: ")
api = API(key)

cameras = api.get_cameras()
print("Cameras:", len(cameras))

while True:
    camera = random.choice(cameras)
    
    try:
        with camera.get_stream() as stream:
            title = "LIVE: " + camera.roadway if camera.roadway else "LIVE"
                
            for i in range(100):
                frame = next(stream)
                
                cv2.imshow(title, frame)
                cv2.waitKey(1)
                
            cv2.destroyAllWindows()
    except KeyboardInterrupt:
        raise
    except StopIteration:
        pass