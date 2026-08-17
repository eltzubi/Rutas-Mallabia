#!/usr/bin/env python3
"""Rebuilds index.html from the source templates in this folder.

Architecture:
  - Each page (mallabia = home, trabakua = route) is written as a
    <name>_head.html + <name>_tail.html pair, so they're small enough
    to edit directly even though the final assembled page has huge
    embedded base64 images/fonts.
  - fonts/inline_fonts.css holds the self-hosted @font-face rules
    (Fraunces, Karla, IBM Plex Mono), shared by both pages.
  - Each pair is concatenated into a full standalone HTML document.
  - Both full documents get embedded (with & escaped to &amp;) inside
    <textarea> tags in an outer shell, which reads them out and
    assigns them as srcdoc to two <iframe> elements. Only one iframe
    is visible (class "active") at a time.
  - Navigation between views happens via window.postMessage({view:
    'home'|'trabakua'}) posted from links inside the iframes; the
    outer shell listens and toggles which iframe is active. This
    exists because Claude Artifacts (where this started) block
    navigation between separately published artifacts -- and it was
    kept after moving to GitHub Pages because it already worked.

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


def main():
    home_html = assemble_page("mallabia")
    trabakua_html = assemble_page("trabakua")

    for label, html in [("home", home_html), ("trabakua", trabakua_html)]:
        if "</textarea" in html.lower():
            raise SystemExit(f"{label} page contains a literal </textarea> -- would break the outer shell")

    home_esc = home_html.replace("&", "&amp;")
    trabakua_esc = trabakua_html.replace("&", "&amp;")

    shell = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mallabia · Rutas del pueblo</title>
<style>
  html,body{ margin:0; padding:0; height:100%; background:#F5F3EC; }
  @media (prefers-color-scheme: dark){
    html,body{ background:#20261A; }
  }
  .frame{
    position:fixed; inset:0; width:100%; height:100%;
    border:none; display:none;
  }
  .frame.active{ display:block; }
</style>
</head>
<body>
<iframe id="home-frame" class="frame active"></iframe>
<iframe id="trabakua-frame" class="frame"></iframe>

<textarea id="home-src" style="display:none">""" + home_esc + """</textarea>
<textarea id="trabakua-src" style="display:none">""" + trabakua_esc + """</textarea>

<script>
(function(){
  var homeFrame = document.getElementById('home-frame');
  var trabakuaFrame = document.getElementById('trabakua-frame');
  homeFrame.srcdoc = document.getElementById('home-src').value;
  trabakuaFrame.srcdoc = document.getElementById('trabakua-src').value;

  var frames = { home: homeFrame, trabakua: trabakuaFrame };

  function show(view){
    if(!frames[view]) return;
    Object.keys(frames).forEach(function(k){
      frames[k].classList.toggle('active', k === view);
    });
    window.scrollTo(0,0);
  }

  window.addEventListener('message', function(e){
    if(e.data && e.data.view){ show(e.data.view); }
  });
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
