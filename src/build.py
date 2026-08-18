#!/usr/bin/env python3
"""Rebuilds index.html from the source templates in this folder.

Architecture:
  - Each page (mallabia = home, trabakua/iturrizuri = routes) is written as
    a <name>_head.html + <name>_tail.html pair, so they're small enough
    to edit directly even though the final assembled page has huge
    embedded base64 images/fonts.
  - fonts/inline_fonts.css holds the self-hosted @font-face rules
    (Fraunces, Karla, IBM Plex Mono), shared by all pages.
  - Each pair is concatenated into a full standalone HTML document.
  - All full documents get embedded (with & escaped to &amp;) inside
    <textarea> tags in an outer shell, which reads them out and
    assigns them as srcdoc to one <iframe> per page. Only one iframe
    is visible (class "active") at a time.
  - Navigation between views happens via window.postMessage({view:
    '<page-name>'}) posted from links inside the iframes; the outer
    shell listens and toggles which iframe is active. This exists
    because Claude Artifacts (where this started) block navigation
    between separately published artifacts -- and it was kept after
    moving to GitHub Pages because it already worked.
  - To add a new route page: create <name>_head.html + <name>_tail.html,
    add "<name>" to PAGES below (home stays first/default-active), and
    link to it from wherever with
    onclick="parent.postMessage({view:'<name>'},'*');return false;".

IMPORTANT: any file with embedded base64 (fonts/inline_fonts.css,
*_tail.html once photos are added) is huge -- do not open these with
a plain text editor or a tool that reads/prints whole files. Use
Python with a line-length filter (e.g. `if len(line) < 300`) to find
line numbers, and edit via string replacement in a script, not by
hand.

Usage:
    python3 src/build.py
Writes ../index.html (the repo root, which GitHub Pages serves).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


def assemble_page(name):
    return read(f"{name}_head.html") + read("fonts", "inline_fonts.css") + read(f"{name}_tail.html")


# First entry is the page shown by default (class "active").
PAGES = ["mallabia", "trabakua", "iturrizuri"]
VIEW_NAME = {"mallabia": "home"}  # page name -> postMessage view name, defaults to itself


def view_of(page):
    return VIEW_NAME.get(page, page)


def main():
    pages_html = {name: assemble_page(name) for name in PAGES}

    for label, html in pages_html.items():
        if "</textarea" in html.lower():
            raise SystemExit(f"{label} page contains a literal </textarea> -- would break the outer shell")

    iframes = "\n".join(
        f'<iframe id="{view_of(name)}-frame" class="frame{" active" if i == 0 else ""}"></iframe>'
        for i, name in enumerate(PAGES)
    )
    textareas = "\n".join(
        f'<textarea id="{view_of(name)}-src" style="display:none">' + pages_html[name].replace("&", "&amp;") + "</textarea>"
        for name in PAGES
    )
    frame_assignments = "\n  ".join(
        f"var {view_of(name)}Frame = document.getElementById('{view_of(name)}-frame');\n  "
        f"{view_of(name)}Frame.srcdoc = document.getElementById('{view_of(name)}-src').value;"
        for name in PAGES
    )
    frames_map = ", ".join(f"{view_of(name)}: {view_of(name)}Frame" for name in PAGES)

    shell = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mallabia · Rutas del pueblo</title>
<style>
  html,body{ margin:0; padding:0; height:100%; background:#0A0F0A; }
  .frame{
    position:fixed; inset:0; width:100%; height:100%;
    border:none; display:none;
  }
  .frame.active{ display:block; }
</style>
</head>
<body>
""" + iframes + """

""" + textareas + """

<script>
(function(){
  """ + frame_assignments + """

  var frames = { """ + frames_map + """ };

  function show(view){
    if(!frames[view]) return;
    Object.keys(frames).forEach(function(k){
      frames[k].classList.toggle('active', k === view);
    });
    window.scrollTo(0,0);
  }

  window.addEventListener('message', function(e){
    if(e.data && e.data.view){ show(e.data.view); }
    if(e.data && (e.data.theme === 'dark' || e.data.theme === 'light')){
      try { localStorage.setItem('rutas-mallabia-theme', e.data.theme); } catch(err){}
      Object.keys(frames).forEach(function(k){
        frames[k].contentWindow.postMessage({ theme: e.data.theme }, '*');
      });
    }
  });

  // Iframes get an opaque (null) origin via srcdoc, so each one's own
  // localStorage is isolated -- theme choice is persisted here in the
  // shell (real origin) instead, and pushed into each iframe once its
  // srcdoc content has finished loading (so its message listener exists).
  var savedTheme = null;
  try { savedTheme = localStorage.getItem('rutas-mallabia-theme'); } catch(err){}
  if (savedTheme === 'dark' || savedTheme === 'light') {
    Object.keys(frames).forEach(function(k){
      frames[k].addEventListener('load', function(){
        frames[k].contentWindow.postMessage({ theme: savedTheme }, '*');
      });
    });
  }
})();
</script>
</body>
</html>
"""

    out_path = os.path.join(ROOT, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(shell)
    print(f"wrote {out_path} ({len(shell)} bytes)")


if __name__ == "__main__":
    main()
