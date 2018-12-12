import csv
from PIL import ImageFont, ImageDraw, Image

FONT_FILL = (90, 90, 90, 255)

def parse_input(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the header
        for row in reader:
            yield row

def format_tel(num):
    return '(' + num[0:3] + ') ' + num[3:6] + '-' + num[6:10]

def draw_text_with_gap(x, y, gap, font, text):
    x_pos = x
    for c in text:
        draw.text((x_pos, y), c, font=font, fill=FONT_FILL)
        w, h = font.getsize(c)
        x_pos += (w + gap)

def write_name(name):
    font = ImageFont.truetype('./fonts/arial-bold.ttf', 200)
    draw_text_with_gap(265, 775, 10, font, name)

def write_title(title):
    font = ImageFont.truetype('./fonts/arial-bold.ttf', 120)
    draw_text_with_gap(275, 1070, 10, font, title)

def write_tel(tel):
    font = ImageFont.truetype('./fonts/arial.ttf', 100)
    draw_text_with_gap(2204, 1245, 10, font, tel)

def write_email(email):
    font = ImageFont.truetype('./fonts/arial.ttf', 100)
    draw_text_with_gap(2217, 1530, 10, font, email)

def write_text(name, title, tel, email):
    write_name(name)
    write_title(title)
    write_tel(format_tel(tel))
    write_email(email)

for row in parse_input('input.csv'):
    img = Image.open('./images/template.png')
    draw = ImageDraw.Draw(img)
    write_text(row[0], row[1], row[2], row[3]);
    img.save('./images/' + row[0] + '.png')
