import os
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def load_settings():
    if os.path.exists("settings.yml"):
        with open("settings.yml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise FileNotFoundError("settings.yml 파일이 없습니다.")

def make_output_dir_if_not_exists(settings):
    output_dir = settings["go"]["out_dir"]
    os.makedirs(output_dir, exist_ok=True)

def refers_fonts(settings):
    fonts = settings['fonts']
    var_font = settings['var']['font']

    for fname, ref in var_font.items():
        var_font[fname] = fonts[ref]['cssValue']

def main():
    settings = load_settings()
    make_output_dir_if_not_exists(settings)

    env = Environment(loader=FileSystemLoader("src"))

    refers_fonts(settings)

    settings['meta']['version_s'] = datetime.now().strftime("%y-%m-%d")
    settings['meta']['version_l'] = datetime.now().strftime("%y-%m-%d-%H%M%S")

    for targetFilePath in settings["go"]["targets"]:
        template = env.get_template(targetFilePath)
        result = template.render({
            'settings' : settings['skin'],
            'var'      : settings['var'],
            'fonts'    : settings['fonts'],
            'meta'     : settings['meta'],
        })

        with open(settings["go"]["out_dir"] + '/' + targetFilePath, "w", encoding="utf-8") as f:
            f.write(result)

        print("내보냄: " + targetFilePath)

main()
