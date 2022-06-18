from PIL import ImageFont, ImageDraw
import unicornhathd
from PIL import Image
import numpy as np
import time
# from datetime import datetime
# import pytz

class DisplayOutput():
    def __init__(self):
        self.hat = unicornhathd
        self.hat.rotation(270)
        self.hat.brightness(0.6)

    # def write(self, buf):
    def write(self, img):
        # img = Image.frombytes('RGB', (64, 64), buf)
        img = img.resize((16, 16), Image.BILINEAR)

        for x in range(16):
            for y in range(16):
                r, g, b = img.getpixel((x, y))
                self.hat.set_pixel(x, 15-y, r, g, b)

        self.hat.show()

def clock(now):
    img = Image.new("RGB", (16,16))
    draw = ImageDraw.Draw(img)

    # second
    sec = now.tm_sec
    if sec < 15:
        x = 15
        y = sec
    elif sec < 30:
        x = 30 - sec
        y = 15
    elif sec < 45:
        x = 0
        y = 45 - sec
    else:
        x = sec - 45
        y = 0
    img.putpixel((x,y), (255,255,255))


    # hour
    font = ImageFont.truetype("/home/pi/github/raspberry/unicorn-clock/MyriadPro-Regular.otf", 12)
    msg = f"{now.tm_hour:02d}"
    w, h = draw.textsize(msg, font=font)
    draw.text((0, -1), msg, font=font, fill=(255,64,64))

    # minute
    font = ImageFont.truetype("/home/pi/github/raspberry/unicorn-clock/MyriadPro-Regular.otf", 14)
    msg = f"{now.tm_min:02d}"
    w, h = draw.textsize(msg, font=font)
    draw.text((16-w, 16-h), msg, font=font, fill=(255,128,128), stroke_width=1, stroke_fill=(0,0,0))

    return img

# timezone = pytz.timezone('Asia/Tokyo')
output = DisplayOutput()
while True:
    now = time.localtime()
    # print(now)
    # now = datetime.now(timezone)
    # print(now)
    img = clock(now)
    output.write(img)
    time.sleep(0.2)
