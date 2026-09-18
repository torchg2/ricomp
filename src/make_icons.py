# -*- coding: utf-8 -*-
"""Genera le icone dell'app.

    python3 make_icons.py

Il segno sono tre barre che salgono: le misure che si muovono. Resta
leggibile a 40 pixel, che e la dimensione a cui la vedrai davvero sulla
schermata home. Un segno più elaborato li diventa una macchia.

Disegna a 4x e rimpicciolisce, così i bordi restano puliti.
"""
from PIL import Image, ImageDraw

VIOLA = (83, 74, 183)
SC = 4  # sovracampionamento


def mark(size, frazione):
    """Quadrato viola con tre barre che salgono, grandi 'frazione' del lato."""
    S = size * SC
    img = Image.new("RGB", (S, S), VIOLA)
    d = ImageDraw.Draw(img, "RGBA")
    m = S * frazione
    cx = cy = S / 2.0
    x0 = cx - m / 2
    w = m * 0.21            # spessore della barra
    gap = m * 0.315         # distanza fra una barra e l'altra
    for i, (lung, alfa) in enumerate([(0.42, 120), (0.70, 190), (1.0, 255)]):
        y = cy - gap + i * gap
        d.rounded_rectangle([x0, y - w / 2, x0 + m * lung, y + w / 2],
                            radius=w / 2, fill=(255, 255, 255, alfa))
    return img.resize((size, size), Image.LANCZOS)


def main():
    # icone normali: il segno occupa il 58% del lato
    for s in (192, 512):
        mark(s, 0.60).save("../icon-%d.png" % s, optimize=True)
        print("  icon-%d.png" % s)
    # maskable: Android ritaglia fino al 20% per lato, il segno resta piccolo
    mark(512, 0.43).save("../icon-maskable-512.png", optimize=True)
    print("  icon-maskable-512.png")


if __name__ == "__main__":
    main()
