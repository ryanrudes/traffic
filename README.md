# New York State Department of Transportation API

[![PyPI download month](https://img.shields.io/pypi/dm/traffic.svg)](https://pypi.python.org/pypi/traffic/)
[![PyPI - Status](https://img.shields.io/pypi/status/traffic)](https://pypi.python.org/pypi/traffic/)
[![PyPI](https://img.shields.io/pypi/v/traffic)](https://pypi.python.org/pypi/traffic/)
![GitHub](https://img.shields.io/github/license/ryanrudes/traffic)

## Installation
```bash
pip install traffic
```

## Authentication
1. Visit the 511 NY [website](https://511ny.org/my511/register) and create a new account
2. Login to your account and request an API key [here](https://511ny.org/developers/help)

## Example
The following code cycles through live feeds of various traffic cameras at random.

```python
from traffic import API

import random
import cv2

api = API("<insert-api-key>")

cameras = api.get_cameras()
print("Cameras:", len(cameras))

while True:
    camera = random.choice(cameras)
    
    try:
        with camera.get_stream() as stream:
            for i in range(100):
                frame = next(stream)
                
                cv2.imshow("LIVE: " + camera.roadway, frame)
                cv2.waitKey(1)
                
            cv2.destroyAllWindows()
    except KeyboardInterrupt:
        raise
    except StopIteration:
        pass
```