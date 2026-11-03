import re
p = 'boards.py'
s = open(p, encoding='utf-8').read()
start = s.index('DIAMOND = (')
end = s.index('LOGO_W')
new = '''def _svg(bg, fg):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'><rect width='12' height='12' fill='{bg}'/>"
           f"<polygon points='6,1.2 10.8,6 6,10.8 1.2,6' fill='{fg}'/></svg>")
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


DIAMOND = _svg("#FEF102", "#EE1D23")
DIAMOND_INK = _svg("#FFF4DC", "#E4007C")

'''
s = s[:start] + new + s[end:]
s = s.replace('url("{DIAMOND}")', "url('{DIAMOND}')")
open(p, 'w', encoding='utf-8').write(s)
