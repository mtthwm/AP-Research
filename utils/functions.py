import shutil
import os
from PIL import Image
import requests
from memory_profiler import profile
from time import time
from datetime import datetime

def download_url_image (url, filename):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    with open(filename, 'wb') as file:
        shutil.copyfileobj(r.raw, file)
        return filename

def check_image_downloaded_previously(filename):
    return os.path.exists(filename)

def arnold_cat_map (filename:str, outname:str, retain_final:bool, image_key:str, sequence_id:int, append_to_text_file=None):
    start_time = time()
    bits_generated = 0

    p = 1
    q = 1

    original = Image.open(filename).convert('1')
    size = min((original.height, original.width))
    top = 0
    bottom = size - (size % 4)
    left = 0
    right = size - (size % 4)
    original = original.crop((left, top, right, bottom))

    new = Image.new('1', (original.width, original.height))

    for y in range(original.height):
        for x in range(original.width):
            px = original.getpixel((x, y))
            N = original.width
            newX = (x + y * p) % N
            newY = (x * q + y * (p * q + 1)) % N
            new.putpixel((newX, newY), px)

    count_width = int(original.width / 4)
    count_height = int(original.height / 4)

    count = Image.new('1', (count_width, count_height))

    for y in range(0, new.height, 4):
        for x in range(0, new.width, 4):
            pix_sum = 0
            for i in range(16):
                coords = (x + (i % 4), y + int(i / 4))
                add = new.getpixel(coords)
                pix_sum += add
            count.putpixel((int(x / 4), int(y / 4)),
                           1 if pix_sum % 2 == 0 else 0)

    if retain_final:
        zag = Image.new('1', (count.height, count.width))

    x = 0
    y = 0
    xDir = 1
    yDir = 1
    passedCorner = False
    file = None
    if append_to_text_file:
        file = open(append_to_text_file, "a")
    for i in range(count.width*count.height):
        pix = count.getpixel((x, y))
        bits_generated += 1
        if file:
            file.write(str(pix))
        if retain_final:
            zag.putpixel((i % count.width, int(i / count.width)), pix)

        doSwapY = y - yDir < 0 or y - yDir >= count.height
        doSwapX = x + xDir >= count.width or x + xDir < 0

        if doSwapX and doSwapY:
            passedCorner = True
            x -= xDir

        if not doSwapX:
            if passedCorner and doSwapY:
                x -= xDir
            else:
                x += xDir
        if not doSwapY:
            if passedCorner and doSwapX:
                y += yDir
            else:
                y -= yDir

        if doSwapX or doSwapY:
            yDir *= -1
            xDir *= -1

    if file:
        file.close()
    if retain_final:
        zag.save(outname)

    seq = GeneratedSequence(outname=outname, length=bits_generated, generation_time=time() - start_time, image_key=image_key, sequence_id=sequence_id)
    print(f"Generated {seq.outname} ({len(seq)} bits) in {seq.generation_time} ms. {seq.bit_rate} bit/sec")
    return seq


class GeneratedSequence:
    def __init__(self, outname, length, generation_time, image_key, sequence_id):
        self.outname = outname
        self._length = length
        self.generation_time = generation_time
        self.bit_rate = len(self) / generation_time
        self.image_key = image_key
        self.sequence_id = sequence_id
        self.time_generated = datetime.now()

    def __len__(self):
        return self._length
