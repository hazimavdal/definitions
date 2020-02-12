import json
import glob
import os

WORD = "word"
OVERVIEW = "overview"
IPA = "ipa"

SENSES = "senses"
DESC = "desc"
EXAMPLES = "examples"


def examples(ex):
    return "".join([f"<dd><q>{e}</q></dd>" for e in ex])


def sense(s):
    return f"<dl><dt>{s[DESC]}</dt>{examples(s[EXAMPLES])}</dl>"


def senses(gn, g):
    S = [f"<li id='{gn}{str(i)}'>{sense(s)}</li>" for i, s in enumerate(g)]
    return f"<ol>{''.join(S)}</ol>"


def group(name, S):
    return f"<dev><i>{name}</i><dev>{senses(name, S)}</dev></dev>"


def sense_groups(d):
    return "".join([f"<dev>{group(name, S)}</dev>" for (name, S) in d.items()])


def replaceAll(s, d):
    for k, v in d.items():
        s = s.replace(k, v)

    return s


def render(man):
    word = man[WORD]
    ipa = man[IPA]
    overview = man[OVERVIEW]
    senses = sense_groups(man[SENSES])

    with open("templates/main.html", "r") as f:
        html = f.read()
        m = {
            "@title": word.title(),
            "@word": word.title(),
            "@ipa": ipa,
            "@overview": overview,
            "@senses": senses
        }

        html = replaceAll(html, m)

        with open(f"build/{word}.html", "w+") as f:
            f.write(html)


def renderAll():

    if not os.path.exists("build"):
        os.makedirs("build")

    for word in glob.glob('./words/*.json'):
        with open(word, "r") as f:
            man = json.load(f)
            render(man)


if __name__ == "__main__":
    renderAll()
