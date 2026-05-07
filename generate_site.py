import os
from pathlib import Path
from PIL import Image, ImageDraw

# Constants
DIST_DIR = Path("dist")
IMAGES_DIR = DIST_DIR / "images"
PAGES_DIR = DIST_DIR / "pages"

# Hot Dog Stand Color Scheme
BGCOLOR = "#FF0000"  # Red
TEXT_COLOR = "#FFFF00"  # Yellow
LINK_COLOR = "#FFFFFF"  # White
VLINK_COLOR = "#000000"  # Black
ALINK_COLOR = "#FFFF00"  # Yellow

def create_directories():
    """Creates the necessary directory structure."""
    for folder in [DIST_DIR, IMAGES_DIR, PAGES_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
    print(f"Created directory structure in {DIST_DIR}")

def generate_placeholder_image(filename, size, text, bg_color, text_color):
    """Generates a placeholder GIF image."""
    img = Image.new('RGB', size, color=bg_color)
    d = ImageDraw.Draw(img)
    # Using default font as we can't rely on specific ttf files being present
    d.text((10, size[1]//2 - 5), text, fill=text_color)

    filepath = IMAGES_DIR / filename
    img.save(filepath, "GIF")
    print(f"Generated image: {filepath}")

def get_nav_html(current_page_depth):
    """Generates the navigation sidebar HTML."""
    prefix = "" if current_page_depth == 0 else "../"
    pages_prefix = "pages/" if current_page_depth == 0 else ""

    # If we are already in pages/, we don't need the pages_prefix for pages within the same folder
    about_path = f"{prefix}{pages_prefix}about.html" if current_page_depth == 0 else "about.html"
    links_path = f"{prefix}{pages_prefix}links.html" if current_page_depth == 0 else "links.html"

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
                <a href="{prefix}index.html"><font color="#FFFFFF">Home</font></a>
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

def generate_page(filename, title, content, depth=0):
    """Generates an HTML page with the table-based layout."""
    img_prefix = "images/" if depth == 0 else "../images/"

    html = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
<head>
    <title>{title}</title>
</head>
<body bgcolor="{BGCOLOR}" text="{TEXT_COLOR}" link="{LINK_COLOR}" vlink="{VLINK_COLOR}" alink="{ALINK_COLOR}">

    <!-- Header Table -->
    <table border="0" width="100%" cellpadding="10" cellspacing="0">
        <tr bgcolor="#000000">
            <td align="center">
                <h1><font face="Courier New, Courier, mono" color="#FFFF00">{title}</font></h1>
            </td>
        </tr>
    </table>

    <br>

    <!-- Main Content Table -->
    <table border="0" width="100%" cellpadding="10" cellspacing="0">
        <tr valign="top">
            <!-- Sidebar -->
            <td width="150">
                {get_nav_html(depth)}
                <br><br>
                <img src="{img_prefix}button.gif" alt="88x31 Button" width="88" height="31" border="0">
            </td>

            <!-- Main Area -->
            <td>
                <table border="3" cellpadding="15" cellspacing="0" width="100%" bgcolor="#000000">
                    <tr>
                        <td>
                            <font face="Times New Roman, Times, serif">
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
    filepath = (DIST_DIR / filename) if depth == 0 else (PAGES_DIR / filename)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Generated page: {filepath}")

def main():
    create_directories()

    # Generate Assets
    generate_placeholder_image("button.gif", (88, 31), "COOL SITE", (255, 255, 0), (0, 0, 0))
    generate_placeholder_image("profile.gif", (100, 100), "ME", (0, 0, 0), (255, 255, 255))

    # Generate Pages
    home_content = """
    <h2>Welcome to my Homepage!</h2>
    <p>This site is under construction, but feel free to look around.</p>
    <p>I am very excited to share my thoughts with the World Wide Web!</p>
    <p align="center">
        <marquee>Welcome to the Information Superhighway!</marquee>
    </p>
    """
    generate_page("index.html", "My Awesome 1997 Page", home_content, depth=0)

    about_content = """
    <h2>About Me</h2>
    <p>I am a web enthusiast who loves HTML 3.2.</p>
    <p>My hobbies include:</p>
    <ul>
        <li>Surfing the web</li>
        <li>Collecting GIFs</li>
        <li>Writing table-based layouts</li>
    </ul>
    """
    generate_page("about.html", "About Me", about_content, depth=1)

    links_content = """
    <h2>Cool Links</h2>
    <p>Check out these other awesome sites:</p>
    <ul>
        <li><a href="http://www.geocities.com"><font color="#FFFFFF">GeoCities</font></a></li>
        <li><a href="http://www.yahoo.com"><font color="#FFFFFF">Yahoo!</font></a></li>
        <li><a href="http://www.altavista.com"><font color="#FFFFFF">AltaVista</font></a></li>
    </ul>
    <p align="center">
        <img src="../images/button.gif" alt="Link to me" width="88" height="31">
    </p>
    """
    generate_page("links.html", "Webrings & Links", links_content, depth=1)

if __name__ == "__main__":
    main()
