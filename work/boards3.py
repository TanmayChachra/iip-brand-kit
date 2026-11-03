"""Round 3: Quiet and Ink only. English only. Real phone numbers. Variants: clean (phones) and proof (phones + legal proof lines).
Proof wording comes from the owner and must be checked against documents before print."""
import sys
from playwright.sync_api import sync_playwright
import boards2 as B

ROOT, LOGO = B.ROOT, B.LOGO
OUT = ROOT / "b3"; OUT.mkdir(exist_ok=True)
P1, P2 = "9837057800", "9219549800"
PROOF = ["Section 80 approved", "Map passed by Zila Panchayat"]
PAPER, INK, RED, CHAR, CREAM, YEL = B.PAPER, B.INK, B.RED, B.CHAR, B.IV2, B.YEL


def theme(k):
    if k == "quiet":
        return dict(bg=PAPER, fg=INK, font="Montserrat", frame=f"inset:0;border:.7cqw solid {INK}", line=RED, sub="#6b6a66", line_txt="Room to build.")
    return dict(bg=CHAR, fg=CREAM, font="Manrope", frame=f"inset:2.4cqw;border:.5cqw solid {CREAM}", line=YEL, sub="#b9b4a6", line_txt="Plug in. Build up.")


def pole(k, h, proof):
    t = theme(k)
    lw = {10: (24 if proof else 30), 12: (34 if proof else 40), 14: (42 if proof else 48), 16: (44 if proof else 50), 18: 54}[h]
    big = {10: 10.5, 12: 11.5, 14: 12.5, 16: 14, 18: 14}[h]
    ph = {10: 5.2, 12: 5.8, 14: 6.4, 16: 7, 18: 7}[h]
    pr = {10: 3.1, 12: 3.4, 14: 3.7, 16: 4, 18: 4}[h]
    proof_html = ""
    if proof:
        proof_html = (f'<div style="width:70cqw;height:.3cqw;background:{t["fg"]};opacity:.35;margin:0 0 2.4cqw"></div>'
                      + "".join(f'<div style="font:500 {pr}cqw Inter;letter-spacing:.06em;margin-bottom:.8cqw">{p}</div>' for p in PROOF))
    div = f'<div style="width:14cqw;height:.9cqw;background:{t["line"]};margin:{4 if h>10 else 2.6}cqw 0"></div>'
    return f"""<div class=b style="background:{t['bg']};color:{t['fg']};font-family:{t['font']},sans-serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;{t['frame']}"></div>
 <img src="{LOGO}" style="width:{lw}cqw;margin-top:{9 if h>10 else 6}cqw;display:block">
 <div style="margin-top:{5 if h>10 else 3}cqw;font-weight:800;font-size:{big}cqw;line-height:1;letter-spacing:.015em">ISAPUR</div>
 <div style="margin-top:1.8cqw;font-weight:500;font-size:{4.1 if h>10 else 3.7}cqw;letter-spacing:.4em;padding-left:.4em">INDUSTRIAL PARK</div>
 {div}
 <div style="font-weight:500;font-size:{6.2 if h>10 else 5.4}cqw">{t['line_txt']}</div>
 <div style="flex:1"></div>
 <div style="text-align:center;margin-bottom:{9 if h>10 else 6}cqw">{proof_html}
  <div style="font:700 {ph}cqw Inter;letter-spacing:.1em">{P1}</div><div style="font:700 {ph}cqw Inter;letter-spacing:.1em;margin-top:.6cqw">{P2}</div></div></div>"""


def wide(k, r, proof):
    t = theme(k)
    gate = r >= 3
    phones = "" if gate else (f'<div style="position:absolute;right:12cqh;bottom:11cqh;text-align:right;font:700 7.2cqh Inter;letter-spacing:.1em;line-height:1.3">{P1}<br>{P2}</div>')
    pr = ("" if gate or not proof else f'<div style="position:absolute;right:12cqh;top:11cqh;text-align:right;font:500 5cqh Inter;letter-spacing:.06em;line-height:1.5">{PROOF[0]}<br>{PROOF[1]}</div>')
    return f"""<div class=b style="background:{t['bg']};color:{t['fg']};font-family:{t['font']},sans-serif;display:flex;align-items:center">
 <div style="position:absolute;{t['frame'].replace('cqw','cqh')}"></div>
 <img src="{LOGO}" style="height:62cqh;margin-left:{16 if r<3 else 12}cqh;display:block">
 <div style="margin-left:{11 if r<3 else 9}cqh">
  <div style="font-weight:800;font-size:{27 if r<3 else 32}cqh;line-height:1;white-space:nowrap">ISAPUR</div>
  <div style="margin-top:3cqh;font-weight:500;font-size:{6.2 if r<3 else 7.4}cqh;letter-spacing:.4em;white-space:nowrap">INDUSTRIAL PARK</div>
  <div style="margin-top:5cqh;width:{18 if r<3 else 16}cqh;height:1.6cqh;background:{t['line']}"></div>
  <div style="margin-top:5cqh;font-weight:500;font-size:{10 if r<3 else 11}cqh;white-space:nowrap">{t['line_txt']}</div></div>{phones}{pr}</div>"""


def main():
    with sync_playwright() as p:
        br = p.chromium.launch()
        for k in ("quiet", "ink"):
            for proof in (False, True):
                tag = "proof" if proof else "clean"
                for h in (16, 18):
                    B.shot(br, pole(k, h, proof), 1000, h * 100, OUT / f"{k}-{tag}-20x{h * 2}.png", 2)
                B.shot(br, wide(k, 2.4, proof), 1200, 500, OUT / f"{k}-{tag}-hoarding.png", 2)
            B.shot(br, wide(k, 4.0, False), 2000, 500, OUT / f"{k}-gate.png", 2)
        br.close()


if __name__ == "__main__":
    main()

