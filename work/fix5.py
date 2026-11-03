import re
s = open('build.py', encoding='utf-8').read()
s = s.replace("<li><b>Own a colour</b> nobody around you owns (Jamun, Gulaal).</li>", "<li><b>Own a look</b> nobody around you owns: white space or a dark board (Quiet, Ink).</li>")
s = s.replace("<li><b>Say it in Hindi</b> and write the name in both scripts.</li>", "<li><b>Say it plainly</b>: short English lines, the name large.</li>")
s = s.replace("<li>Violet or purple</li><li>Rani or magenta pink</li><li>Warm ivory with a heavy black frame</li><li>White space</li><li>A symbol other than a monogram or a house icon</li><li>Hindi as the main language of the headline, except SHD</li>",
              "<li>Generous empty space</li><li>Charcoal or near-black boards</li><li>A thin frame and one rule instead of stamps and badges</li><li>A symbol other than a monogram or a house icon</li><li>Boards with only the name and phone numbers</li>")
s = s.replace("A 10 inch", "A 10 inch")
open('build.py', 'w', encoding='utf-8').write(s)
print(len(re.findall('Hindi', s)))
