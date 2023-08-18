from .direction import Direction

from contextlib import contextmanager
from threading import Thread, Event
from typing import Optional, Tuple
from queue import Queue, Empty
from io import BytesIO
from PIL import Image
from time import time, sleep

import numpy as np
import functools
import tempfile
import requests
import cv2
import re
import os

STREAM_EXPR = re.compile(r"#EXT-X-STREAM-INF:BANDWIDTH=(\d+)(?:,CODECS=\"(.*?)\")?(?:,RESOLUTION=(\d+)x(\d+))?")
VERSION_EXPR = re.compile(r"#EXT-X-VERSION:(\d)")
DURATION_EXPR = re.compile(r"#EXTINF:(\d+.\d+),")

def get_info(playlist_url):
    response = requests.get(playlist_url, timeout = 0.1)
    content = response.content.decode().strip().split('\n')
    
    version = int(re.search(VERSION_EXPR, content[1]).group(1))
    results = re.search(STREAM_EXPR, content[2])
    
    bandwidth = int(results.group(1))
    codec = results.group(2)
    width = int(results.group(3))
    height = int(results.group(4))
    path = content[3]

    return version, bandwidth, codec, width, height, path

def get_blocks(playlist_url):
    version, bandwidth, codec, width, height, path = get_info(playlist_url)
    
    url = playlist_url[:-13] + path
    response = requests.get(url)
    content = response.content.decode()

    stream_id = path.split('.')[0].split('_')[1]
    durations = list(map(float, re.findall(DURATION_EXPR, content)))
    expr = re.compile(r"media_%s_(\d+).ts" % stream_id)
    blocks = re.findall(expr, content)
    
    return stream_id, durations, list(map(int, blocks))

def inforequired(func):
    @functools.wraps(func)
    def wrapper(self):
        if self._info is None:
            self._info = get_info(self.video_url)
        return func(self)
    return wrapper

def stream(playlist_url, image_queue, delay_queue, exit_event):
    last_block = None
    
    while True:
        if exit_event.is_set():
            break

        try:
            stream_id, durations, blocks = get_blocks(playlist_url)
            
            for block, duration in zip(blocks, durations):
                if last_block is None or block > last_block:
                    last_block = block
                    filename = "media_%s_%s.ts" % (stream_id, block)
                    stream_id = filename.split('_')[1]
                    url = playlist_url[:-13] + filename
                    response = requests.get(url, stream = True)
                    
                    if response.status_code == 200:
                        with tempfile.NamedTemporaryFile("ab", suffix = ".mpeg", delete = False) as file:
                            for chunk in response.iter_content(chunk_size = 1024):
                                file.write(chunk)
                        
                        video = cv2.VideoCapture(file.name)
                        count = 0
                        
                        while video.isOpened():
                            success, frame = video.read()
                            
                            if not success:
                                break

                            image_queue.put(frame)
                            count += 1
                        
                        framerate = duration / count
                        
                        for _ in range(count):
                            delay_queue.put(framerate)
                            
                        os.remove(file.name)
        except:
            exit_event.set()
            break
                
class Stream:
    def __init__(self, video_url):
        self.video_url = video_url
        
    def begin(self):
        self.image_queue = Queue()
        self.delay_queue = Queue()
        self.exit_event = Event()
        
        self.streamer = Thread(target = stream, args = (self.video_url, self.image_queue, self.delay_queue, self.exit_event))
        self.streamer.start()
        
        self.next_time = None
        
    def end(self, *args):
        self.exit_event.set()
        
    @property
    def streaming(self):
        return not self.exit_event.is_set()
        
    def __next__(self):
        while True:
            try:
                if self.streaming:
                    image = self.image_queue.get_nowait()
                    delay = self.delay_queue.get_nowait()
                    
                    if self.next_time is None:
                        self.next_time = time()
                    
                    self.next_time += delay
                    
                    while time() < self.next_time:
                        pass
                    
                    return image
                else:
                    raise StopIteration
            except Empty:
                pass
        
    def __iter__(self):
        return self
    
class Camera:
    def __init__(
        self,
        id: str,
        name: str,
        direction: str,
        roadway: str,
        image_url: str,
        video_url: str,
        disabled: str,
        blocked: str,
        latitude: str,
        longitude: str,
    ):
        self.id = id
        self.name = name
        self.direction = Direction(direction)
        self.roadway = roadway
        self.image_url = image_url
        self.video_url = video_url
        self.disabled = disabled == "true"
        self.blocked = blocked == "true"
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
        self._info = None
        
    def get_preview_image(self) -> np.ndarray:
        response = requests.get(self.image_url)
        image = Image.open(BytesIO(response.content))
        return np.asarray(image)
    
    @contextmanager
    def get_stream(self):
        try:
            stream = Stream(self.video_url)
            stream.begin()
            yield stream
        finally:
            stream.end()
    
    @property
    @inforequired
    def version(self) -> int:
        return self._info["version"]
    
    @property
    @inforequired
    def bandwidth(self) -> int:
        return self._info["bandwidth"]
    
    @property
    @inforequired
    def codec(self) -> Optional[str]:
        return self._info["codec"]
    
    @property
    @inforequired
    def width(self) -> Optional[int]:
        return self._info["width"]
    
    @property
    @inforequired
    def height(self) -> Optional[int]:
        return self._info["height"]
    
    @property
    @inforequired
    def resolution(self) -> Optional[Tuple[int, int]]:
        return self.width, self.height
    
    @property
    @inforequired
    def path(self) -> str:
        return self._info["path"]