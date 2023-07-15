import colorgram
import tkinter as tk
from tkinter import filedialog
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect, url_for, flash, request
import pyperclip

app = Flask(__name__)
app.config['SECRET_KEY'] = "1095093f5jq9846535609467dzn486h"
Bootstrap5(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/hex_colors/<int:color_format>', methods=["GET", "POST"])
def upload_image(color_format):
    if request.method == "POST":

        # Create a tKinter window
        window = tk.Tk()
        # Hide the window and show only the filedialog
        window.withdraw()
        # Bring the filedialog in front of all the windows
        window.wm_attributes('-topmost', 1)

        try:
            file_name = filedialog.askopenfilename(parent=window,
                                                   initialdir="",
                                                   title="Select A File",
                                                   filetypes=([("png", ".png"),
                                                               ("gif", ".gif"),
                                                               ("bitmap", "bmp"),
                                                               ("jpeg", ".jpg")]
                                                   )
                                                   )
        except RuntimeError:
            flash("Your previous pdf file is still reading!")
            return redirect(url_for("voice_reader"))

        try:

            rgb_list = []
            hex_list = []
            colors_list = []

            # Extract the maximum number of colors from an image, estimated to 1000000.
            colors = colorgram.extract(file_name, 1000000)  # 'static/img/a.png'

            for color in colors:
                rgb = color.rgb

                # converting color codes to hex codes
                hex_value = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
                hex_list.append(hex_value)

                # converting color codes to rgb codes
                rgb = hex_value.lstrip('#')
                lv = len(rgb)
                rgb = tuple(int(rgb[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                rgb_list.append(f'rgb{rgb}')

            # colors_list = []
            if color_format == 1:
                colors_list = hex_list
            if color_format == 2:
                colors_list = rgb_list

            length = len(hex_list)

            return render_template("index.html", colors=colors_list, length=length)
        except AttributeError:
            return render_template("index.html")
    return render_template("index.html")


@app.route('/copy/<copied>', methods=["GET", "POST"])
def copy(copied):
    if request.method == "POST":
        spam = pyperclip.copy(copied)
        print(copied)
        print(spam)

        return render_template("selected_color.html", color=copied)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
