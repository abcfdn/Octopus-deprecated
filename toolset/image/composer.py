from PIL import ImageFont, ImageDraw, Image

WHITE = (230, 230, 230, 255)
FONT_FILL = (90, 90, 90, 255)

class ImageComposer:
    def load_template(self, filename):
        self.img = Image.open(filename)
        self.draw = ImageDraw.Draw(img)

    def get_font(font_setting):
        font_type = font_setting['type']
        font_size = font_setting['size']
        return ImageFont.truetype('./fonts/%s.ttf' % font_type, font_size)

    def draw_one_line(self, text, setting):
        x_pos = settings['x_pos']
        y_pos = settings['y_pos']
        font = get_font(settings['font'])
        fill = settings['fill']
        for c in text:
            self.draw.text((x_pos, y_pos), c, font=font, fill=fill)
            w, h = font.getsize(c)
            x_pos += (w + gap)

    def save(filename):
        self.img.save(filename)
