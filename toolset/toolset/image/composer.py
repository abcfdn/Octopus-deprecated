# -*- encoding: UTF-8 -*-

import os
import sys
import logging

from PIL import ImageFont, ImageDraw, Image, ImageOps
import numpy as np
import textwrap

logger = logging.getLogger('image_poster')


# box is defined by [x, y, w]
def start_x(box, width, align):
    if align.lower() == 'left':
        return box[0]
    elif align.lower() == 'center':
        return (int)(box[0] + box[2] / 2 - width / 2)
    else:
        logger.error('Unrecognized setting align={}'.format(align))


class ImageComposer:
    def __init__(self, pieces):
        self.imgs = [p.get_img() for p in pieces]

    def vstack(self):
        stacked = np.vstack((np.asarray(img) for img in self.imgs))
        self.comb = Image.fromarray(stacked)

    def zstack(self, box, align):
        if len(self.imgs) != 2:
            logging.error('Only two imgs are supported in zstack')
        [background, foreground] = self.imgs
        [x, y, _] = box
        new_x = start_x(box, foreground.size[0], align)
        foreground.putalpha(255)
        background.paste(foreground, (new_x, y), foreground)
        self.comb = background

    def to_img_piece(self):
        return ImagePiece(self.comb)

    def save(self, filename):
        self.comb.save(filename)


class ImagePiece:
    def __init__(self, img):
        self.img = img

    @classmethod
    def from_file(cls, filename):
        return cls(Image.open(filename))

    def get_font(self, font_dir, font_setting):
        font_path = os.path.join(font_dir, '%s.ttf' % font_setting['type'])
        return ImageFont.truetype(font_path, font_setting['size'])

    def draw_one_line(self, draw, line, font, fill, start, gap):
        (x, y) = start
        for c in line:
            w, h = draw.textsize(c, font=font)
            draw.text((x, y), c, font=font, fill=fill)
            x += (w + gap[0])

    def draw_text(self, lines, font, settings):
        [x_pos, y_pos, width] = settings['box']
        align = settings['align']
        gap = settings['gap']
        fill = tuple(settings['fill'])

        draw = ImageDraw.Draw(self.img)
        c_width = draw.textsize('a', font=font)[0]
        for line in lines:
            for paragraph in line.split('\n'):
                sublines = textwrap.wrap(paragraph, width=(int)(width / c_width))
                for subline in sublines:
                    text_w, h = draw.textsize(subline, font=font)
                    text_w += len(subline) * gap[0]
                    x_pos = start_x(settings['box'], text_w, align)
                    self.draw_one_line(draw,
                                       subline,
                                       font,
                                       fill,
                                       (x_pos, y_pos),
                                       gap)
                    y_pos += (h + gap[1])

    def crop_to_square(self):
        width, height = self.img.size
        new_length = min(width, height)
        left = (width - new_length)/2
        top = (height - new_length)/2
        right = (width + new_length)/2
        bottom = (height + new_length)/2
        self.img.crop((left, top, right, bottom))

    def to_thumbnail(self, size):
        self.img.thumbnail(size, Image.ANTIALIAS)

    def to_circle_thumbnail(self, size):
        bigsize = (size[0] * 3, size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(size, Image.ANTIALIAS)

        self.crop_to_square()
        self.img = self.img.resize(size, Image.ANTIALIAS)
        self.img = ImageOps.fit(
            self.img, size, method=Image.ANTIALIAS, centering=(0.5, 0.5))
        self.img.putalpha(mask)

    def get_img(self):
        return self.img

    def save(self, filename):
        self.img.save(filename)
