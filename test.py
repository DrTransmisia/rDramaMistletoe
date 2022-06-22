from src.rdramamistletoe.dramarender import *

teststr=\
"""
One day @schizoSQL enters in a bar and sdaf ~~sdaf~~ https://site.dom/img/gussy.png lololo r/againsthatesubs **lol** @schizocel's jeep ded

Some good old html tags <br> dsfajlkò <b>sweaty</b>

dsafkl ~~strikethrough~~ dsfa

```
In the code block number 1, some said u/bardfinn
and even <b>bussy</b>
```

<code>
In the code block number 2, some other said u/bardfinn 
and even <b>bussy</b>
</code>

and finally, out side any codeblock, some other said u/bardfinn

> quote block

>be me
>C\C++ can easly be compiled to WASM
>wating to port mistletoe to C
>???
>fail and revert to mistletoe in py
>gonna load py runtime in WASM
>:marseygenius:
>**bold**
>evilface.jpg

---

another aphradsjklfò

:marseysmile::marseysad:

#fortune

~strike single~

#factcheck

it doesn't work :#marseycrazytrollgun:
bussy

Also ||spoilers ahead! :marseypearlclutch: ciao|| ~strike through~

~ nest maxxing ~~lmao~~ dsf ~ ~~normal strike~~

take a look here https://en.wikipedia.org/Cat fsda
"""

with DramaHTMLRenderer() as renderer:
	renderer.getEmojiPath = lambda name: f"https://rdrama.net/e/{name}.webp"
	rendered = renderer.render(Document(teststr))
	print(rendered)
