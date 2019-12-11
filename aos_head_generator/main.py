from io import BytesIO
from PIL import Image, ImageDraw
from flask import Flask, request, abort, send_file

def create_head(color):
    head = Image.open("template.png")
    draw = ImageDraw.Draw(head)
    draw.rectangle(((0, 0), (100, 50)), fill=color)

    bio = BytesIO()
    head.save(bio, "PNG")
    bio.seek(0)
    return bio

app = Flask(__name__)

@app.route("/v1/heads/<string>.png")
def send_image(string):
    if len(string) == 6:
        color_str = string[0:2], string[2:4], string[4:6]
    elif len(string) == 3:
        color_str = string[0], string[1], string[2]
        # Double up each char so that /fff.png is the same as /ffffff.png
        color_str = (x+x for x in color_str)
    else:
        abort(400)

    color = tuple(int(i, 16) for i in color_str)

    image_binary = create_head(color)
    resp = send_file(image_binary, mimetype="image/png")
    resp.cache_control.max_age = 60 * 60 * 24
    resp.cache_control.public = True
    return resp
