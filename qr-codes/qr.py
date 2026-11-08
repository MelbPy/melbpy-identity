"""Generate a QR code (SVG + 1000x1000 PNG) with logo.svg in the centre."""

import io
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
import segno

SVG_NS = "http://www.w3.org/2000/svg"
LOGO = Path(__file__).parent / "logo.svg"
SIZE = 1000  # output size in pixels
LOGO_FRACTION = 0.25  # logo width as a fraction of the QR code width
PAD = 1  # white margin around the logo, in modules

ET.register_namespace("", SVG_NS)


def build_svg(url: str) -> bytes:
    # High error correction so the code still scans with the logo covering it.
    qr = segno.make(url, error="h")
    border = 4
    n = qr.symbol_size(border=border)[0]  # width in modules, incl. border

    buf = io.BytesIO()
    qr.save(
        buf,
        kind="svg",
        scale=1,
        border=border,
        dark="black",
        light="white",
        omitsize=True,
        xmldecl=False,
    )
    root = ET.fromstring(buf.getvalue())
    root.set("width", str(SIZE))
    root.set("height", str(SIZE))

    logo = ET.parse(LOGO).getroot()
    _, _, lw, lh = (float(v) for v in logo.get("viewBox").split())
    w = n * LOGO_FRACTION
    h = w * lh / lw
    x = (n - w) / 2
    y = (n - h) / 2

    ET.SubElement(
        root,
        f"{{{SVG_NS}}}rect",
        x=str(x - PAD),
        y=str(y - PAD),
        width=str(w + 2 * PAD),
        height=str(h + 2 * PAD),
        fill="white",
    )
    nested = ET.SubElement(
        root,
        f"{{{SVG_NS}}}svg",
        x=str(x),
        y=str(y),
        width=str(w),
        height=str(h),
        viewBox=logo.get("viewBox"),
    )
    nested.extend(logo)

    return ET.tostring(root, encoding="utf-8")


def main():
    url = input("URL: ").strip()
    out = Path(input("Output file name: ").strip()).with_suffix("")

    svg = build_svg(url)
    out.with_suffix(".svg").write_bytes(svg)
    cairosvg.svg2png(
        bytestring=svg,
        write_to=str(out.with_suffix(".png")),
        output_width=SIZE,
        output_height=SIZE,
    )
    print(f"Wrote {out.with_suffix('.svg')} and {out.with_suffix('.png')}")


if __name__ == "__main__":
    main()
