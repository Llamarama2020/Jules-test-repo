import os
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageDraw

class SiteGenerator:
    def __init__(self, config):
        self.config = config
        self.dist_dir = Path("dist")
        self.images_dir = self.dist_dir / "images"
        self.pages_dir = self.dist_dir / "pages"

    def create_directories(self):
        for folder in [self.dist_dir, self.images_dir, self.pages_dir]:
            folder.mkdir(parents=True, exist_ok=True)

    def generate_placeholder_image(self, filename, size, text, bg_color, text_color):
        img = Image.new('RGB', size, color=bg_color)
        d = ImageDraw.Draw(img)
        # Using default font
        d.text((10, size[1]//2 - 5), text, fill=text_color)
        filepath = self.images_dir / filename
        img.save(filepath, "GIF")

    def get_nav_html(self, current_page_depth):
        prefix = "" if current_page_depth == 0 else "../"

        # Paths for navigation
        home_path = f"{prefix}index.html"
        about_path = f"{prefix}pages/about.html" if current_page_depth == 0 else "about.html"
        links_path = f"{prefix}pages/links.html" if current_page_depth == 0 else "links.html"

        return f"""
        <table border="1" cellpadding="5" cellspacing="0" width="150" bgcolor="#000000">
            <tr>
                <td>
                    <font face="Arial, Helvetica, sans-serif" color="#FFFFFF">
                        <b>NAVIGATION</b>
                    </font>
                </td>
            </tr>
            <tr>
                <td>
                    <a href="{home_path}"><font color="#FFFFFF">Home</font></a>
                </td>
            </tr>
            <tr>
                <td>
                    <a href="{about_path}"><font color="#FFFFFF">About Me</font></a>
                </td>
            </tr>
            <tr>
                <td>
                    <a href="{links_path}"><font color="#FFFFFF">Links</font></a>
                </td>
            </tr>
        </table>
        """

    def generate_page(self, filename, title, content, depth=0):
        img_prefix = "images/" if depth == 0 else "../images/"
        cfg = self.config

        html = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
<head>
    <title>{title}</title>
</head>
<body bgcolor="{cfg['bgcolor']}" text="{cfg['text']}" link="{cfg['link']}" vlink="{cfg['vlink']}" alink="{cfg['alink']}">

    <!-- Header Table -->
    <table border="0" width="100%" cellpadding="10" cellspacing="0">
        <tr bgcolor="#000000">
            <td align="center">
                <h1><font face="Courier New, Courier, mono" color="{cfg['text']}">{title}</font></h1>
            </td>
        </tr>
    </table>

    <br>

    <!-- Main Content Table -->
    <table border="0" width="100%" cellpadding="10" cellspacing="0">
        <tr valign="top">
            <!-- Sidebar -->
            <td width="150">
                {self.get_nav_html(depth)}
                <br><br>
                <img src="{img_prefix}button.gif" alt="88x31 Button" width="88" height="31" border="0">
            </td>

            <!-- Main Area -->
            <td>
                <table border="3" cellpadding="15" cellspacing="0" width="100%" bgcolor="#000000">
                    <tr>
                        <td>
                            <font face="Times New Roman, Times, serif" color="{cfg['text']}">
                                {content}
                            </font>
                        </td>
                    </tr>
                </table>
                <br>
                <div align="center">
                    <img src="{img_prefix}profile.gif" alt="Profile Image" width="100" height="100" border="5">
                    <p><i>Best viewed in Netscape Navigator 4.0</i></p>
                    <img src="http://www.cuteline.net/images/counter.gif" alt="Hit Counter" border="0">
                </div>
            </td>
        </tr>
    </table>

    <hr noshade size="2">
    <div align="right">
        <font size="2">Created with Web 1.0 Site Generator &copy; 1997</font>
    </div>

</body>
</html>
"""
        filepath = (self.dist_dir / filename) if depth == 0 else (self.pages_dir / filename)
        with open(filepath, "w") as f:
            f.write(html)

    def generate(self):
        self.create_directories()

        # Colors for images - use text color for foreground
        txt_col = self.config['text']
        bg_col = self.config['bgcolor']

        self.generate_placeholder_image("button.gif", (88, 31), "COOL SITE", txt_col, bg_col)
        self.generate_placeholder_image("profile.gif", (100, 100), "ME", bg_col, txt_col)

        self.generate_page("index.html", self.config['site_title'], self.config['home_content'], depth=0)
        self.generate_page("about.html", "About Me", self.config['about_content'], depth=1)
        self.generate_page("links.html", "Webrings & Links", self.config['links_content'], depth=1)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web 1.0 Site Generator")
        self.geometry("600x700")

        self.presets = {
            "Hot Dog Stand": {
                "bgcolor": "#FF0000", "text": "#FFFF00", "link": "#FFFFFF", "vlink": "#000000", "alink": "#FFFF00"
            },
            "Classic Blue": {
                "bgcolor": "#000080", "text": "#FFFFFF", "link": "#00FFFF", "vlink": "#C0C0C0", "alink": "#FFFFFF"
            },
            "Cyberpunk": {
                "bgcolor": "#000000", "text": "#00FF00", "link": "#FF00FF", "vlink": "#00FFFF", "alink": "#00FF00"
            }
        }

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Site Info
        ttk.Label(main_frame, text="Site Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=50)
        self.title_entry.insert(0, "My Awesome 1997 Page")
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        # Color Preset
        ttk.Label(main_frame, text="Color Scheme:").grid(row=1, column=0, sticky=tk.W)
        self.preset_var = tk.StringVar(value="Hot Dog Stand")
        self.preset_combo = ttk.Combobox(main_frame, textvariable=self.preset_var, values=list(self.presets.keys()))
        self.preset_combo.grid(row=1, column=1, sticky=tk.W)
        self.preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)

        # Colors
        color_frame = ttk.LabelFrame(main_frame, text="Colors", padding="5")
        color_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.color_vars = {}
        for i, (label, key) in enumerate([("Background:", "bgcolor"), ("Text:", "text"), ("Link:", "link"), ("Visited Link:", "vlink"), ("Active Link:", "alink")]):
            ttk.Label(color_frame, text=label).grid(row=i, column=0, sticky=tk.W)
            var = tk.StringVar()
            self.color_vars[key] = var
            ttk.Entry(color_frame, textvariable=var, width=15).grid(row=i, column=1, sticky=tk.W)

        self.apply_preset()

        # Content
        content_frame = ttk.LabelFrame(main_frame, text="Page Content (HTML allowed)", padding="5")
        content_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), expand=True)

        ttk.Label(content_frame, text="Home Page:").pack(anchor=tk.W)
        self.home_text = tk.Text(content_frame, height=5)
        self.home_text.pack(fill=tk.X)
        self.home_text.insert(tk.END, "<h2>Welcome!</h2>\n<p>This is my new homepage!</p>\n<marquee>Surfing the web!</marquee>")

        ttk.Label(content_frame, text="About Page:").pack(anchor=tk.W)
        self.about_text = tk.Text(content_frame, height=5)
        self.about_text.pack(fill=tk.X)
        self.about_text.insert(tk.END, "<h2>About Me</h2>\n<p>I am a web traveler.</p>")

        ttk.Label(content_frame, text="Links Page:").pack(anchor=tk.W)
        self.links_text = tk.Text(content_frame, height=5)
        self.links_text.pack(fill=tk.X)
        self.links_text.insert(tk.END, "<h2>My Links</h2>\n<ul>\n<li><a href='http://www.google.com'>Google</a></li>\n</ul>")

        # Generate Button
        self.gen_btn = ttk.Button(main_frame, text="GENERATE SITE", command=self.generate_site)
        self.gen_btn.grid(row=4, column=0, columnspan=3, pady=20)

    def apply_preset(self, event=None):
        preset = self.presets[self.preset_var.get()]
        for key, value in preset.items():
            self.color_vars[key].set(value)

    def generate_site(self):
        config = {
            "site_title": self.title_entry.get(),
            "bgcolor": self.color_vars["bgcolor"].get(),
            "text": self.color_vars["text"].get(),
            "link": self.color_vars["link"].get(),
            "vlink": self.color_vars["vlink"].get(),
            "alink": self.color_vars["alink"].get(),
            "home_content": self.home_text.get("1.0", tk.END),
            "about_content": self.about_text.get("1.0", tk.END),
            "links_content": self.links_text.get("1.0", tk.END),
        }

        try:
            generator = SiteGenerator(config)
            generator.generate()
            messagebox.showinfo("Success", f"Site generated in {os.path.abspath('dist')}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--headless":
        # Fallback for verification in headless environment
        default_config = {
            "site_title": "Headless Test",
            "bgcolor": "#FF0000", "text": "#FFFF00", "link": "#FFFFFF", "vlink": "#000000", "alink": "#FFFF00",
            "home_content": "Home", "about_content": "About", "links_content": "Links"
        }
        gen = SiteGenerator(default_config)
        gen.generate()
        print("Generated in headless mode.")
    else:
        app = App()
        app.mainloop()
