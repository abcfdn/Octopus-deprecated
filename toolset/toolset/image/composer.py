# -*- encoding: UTF-8 -*-

import os
import sys

from PIL import ImageFont, ImageDraw, Image
import numpy as np

FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')


class ImageComposer:
    def __init__(self, pieces):
        self.imgs = [p.get_img() for p in pieces]

    def vertical_combine(self):
        stacked = np.vstack((np.asarray(img) for img in self.imgs))
        self.comb = Image.fromarray(stacked)

    def save(self, filename):
        self.comb.save(filename)


class ImagePiece:
    def __init__(self, filename):
        self.img = Image.open(filename)

    def get_font(self, font_setting):
        font_path = os.path.join(FONT_PATH, '%s.ttf' % font_setting['type'])
        return ImageFont.truetype(font_path, font_setting['size'])

    def word_size(self, font, word):
        width = 0
        for c in word:
            w, h = font.getsize(c)
            width += w
        return width, h

    def draw_text(self, text, settings):
        x_pos = settings['x_pos']
        y_pos = settings['y_pos']
        x_max = settings['x_max']
        font = self.get_font(settings['font'])
        gap = settings['gap']
        fill = tuple(settings['fill'])

        draw = ImageDraw.Draw(self.img)
        for word in text.split(' '):
            ww, wh = self.word_size(font, word)
            if x_pos + ww >= x_max:
                x_pos = settings['x_pos']
                y_pos += wh

            for c in (word + ' '):
                if c == '\n' or c == '\r':
                    x_pos = settings['x_pos']
                    y_pos += wh
                    continue

                w, h = font.getsize(c)
                draw.text((x_pos, y_pos), c, font=font, fill=fill)
                x_pos += (w + gap)


    def draw_img(self, img, setting):
        pass

    def get_img(self):
        return self.img

    def save(self, filename):
        self.img.save(filename)
