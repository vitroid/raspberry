from PIL import ImageFont, ImageDraw
import unicornhathd
from PIL import Image
import time
import colorsys

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

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def clockface(now):
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

    hue = (time.time() / 60) % 1.0

    # hour
    font = ImageFont.truetype("/home/pi/github/raspberry/unicorn-clock/MyriadPro-Regular.otf", 10)
    msg = f"{now.tm_hour:02d}"
    w, h = draw.textsize(msg, font=font)
    # draw.text((0, -1), msg, font=font, fill=(255,64,64))
    draw.text((0, -1), msg, font=font, fill=hsv2rgb(hue, 0.0, 1.0))

    # minute
    font = ImageFont.truetype("/home/pi/github/raspberry/unicorn-clock/MyriadPro-Regular.otf", 14)
    msg = f"{now.tm_min:02d}"
    w, h = draw.textsize(msg, font=font)
    # draw.text((16-w, 16-h), msg, font=font, fill=(255,128,128), stroke_width=1, stroke_fill=(0,0,0))
    draw.text((16-w, 16-h), msg, font=font, fill=hsv2rgb(hue, 0.8, 1.0), stroke_width=1, stroke_fill=(0,0,0))

    return img

# timezone = pytz.timezone('Asia/Tokyo')
output = DisplayOutput()
last = time.localtime()
while True:
    now = time.localtime()
    if now.tm_sec != last.tm_sec:
        img = clockface(now)
        output.write(img)
    time.sleep(0.1)
    last = now
