# New York State Department of Transportation API

[![PyPI download month](https://img.shields.io/pypi/dm/nysdotapi.svg)](https://pypi.python.org/pypi/nysdotapi/)
[![PyPI - Status](https://img.shields.io/pypi/status/nysdotapi)](https://pypi.python.org/pypi/nysdotapi/)
[![PyPI](https://img.shields.io/pypi/v/nysdotapi)](https://pypi.python.org/pypi/nysdotapi/)
![GitHub](https://img.shields.io/github/license/ryanrudes/traffic)

## Installation
```bash
pip install nysdotapi
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
```