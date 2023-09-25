from PIL import Image, ImageDraw, ImageFont
import io


def create_image(caption: str):
    size = (400, 300)
    W, H = size
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 50
    )
    font_color = "gray"
    bg_color = "white"
    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), caption, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), caption, font=font, fill=font_color)
    image_stream = io.BytesIO()
    image.save(image_stream, format="PNG")
    image_stream.seek(0)

    return image_stream


def create_path(old_path, folder_name) -> str:
    split_path = old_path.split("/")
    split_path[-2] = folder_name
    new_path = "/".join(split_path)
    return new_path
