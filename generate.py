"""Gera dark_mode.svg (ASCII do avatar + info estilo neofetch). Uso: python generate.py  (precisa de Pillow e gh CLI logado)"""
import io, json, subprocess, urllib.request
from datetime import date
from html import escape
from PIL import Image, ImageOps

USER = "GabrielSouza2006"
BIRTH = date(2006, 9, 16)
RAMP = " .:-=+*#%@"
COLS, ROWS = 38, 26


def gh(*args):
    return json.loads(subprocess.check_output(["gh", "api", *args], text=True))


def ascii_avatar(url):
    img = Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert("L")
    img = ImageOps.equalize(img.crop((60, 0, 340, 400))).resize((COLS, ROWS))
    lines = []
    for y in range(ROWS):
        row = ""
        for x in range(COLS):
            # máscara elíptica para recortar o fundo
            dx, dy = (x - COLS / 2 + 0.5) / (COLS / 2), (y - ROWS / 2 + 0.5) / (ROWS / 2)
            row += RAMP[img.getpixel((x, y)) * (len(RAMP) - 1) // 255] if dx * dx + dy * dy <= 1 else " "
        lines.append(row.rstrip())
    return lines


def uptime():
    t = date.today()
    months = (t.year - BIRTH.year) * 12 + t.month - BIRTH.month - (t.day < BIRTH.day)
    anchor = date(BIRTH.year + (BIRTH.month - 1 + months) // 12, (BIRTH.month - 1 + months) % 12 + 1, BIRTH.day)  # dia 16 existe em todo mês
    return f"{months // 12} years, {months % 12} months, {(t - anchor).days} days"


def main():
    u = gh(f"users/{USER}")
    repos = gh(f"users/{USER}/repos?per_page=100")
    stars = sum(r["stargazers_count"] for r in repos)
    commits = gh(f"search/commits?q=author:{USER}")["total_count"]
    art = ascii_avatar(u["avatar_url"] + "&s=400")

    W = 60  # largura da coluna de info, em caracteres
    def kv(k, v):
        assert len(k) + len(v) + 4 <= W, f"linha longa demais: {k}"
        return [("key", k + ":"), ("dot", " " + "." * (W - len(k) - len(v) - 3) + " "), ("val", v)]
    def head(t):
        return [("cc", "— " + t + " "), ("dot", "—" * (W - len(t) - 3))]

    info = [
        [("key", f"gabriel@{USER.lower()}"), ("dot", " " + "—" * (W - len(USER) - 9))],
        [],
        kv("OS", "Windows, Linux"),
        kv("Uptime", uptime()),
        kv("Host", "Brasil"),
        kv("Kernel", "Engenheiro de Software FullStack"),
        kv("IDE", "VS Code, Eclipse, Claude Code"),
        [],
        head("Tech Stack"),
        kv("Languages", "Python, Java, TypeScript, JavaScript"),
        kv("Languages.Other", "PHP, C#"),
        kv("Backend", "Spring, Flask, CodeIgniter"),
        kv("Frontend", "React, Angular, Next.js, Nuxt"),
        kv("UI", "HTML, CSS, Bootstrap"),
        kv("Mobile", "Expo"),
        kv("Databases", "MySQL, PostgreSQL, SQL Server"),
        kv("Tools", "Git, GitHub, Docker, Linux"),
        kv("Languages.Real", "Português, English"),
        [],
        head("Working On"),
        [("val", "• APIs com Python (Flask)")],
        [("val", "• Arquitetura backend com Java + Spring")],
        [("val", "• Análise de dados e Big Data")],
        [("val", "• Deploy de aplicações e DevOps")],
        [("val", "• Aplicações com automação de IA")],
        [],
        head("Contact"),
        kv("Email", "gabriel.souza16906@gmail.com"),
        kv("LinkedIn", "in/gabriel-santos-0b20a8261"),
        [],
        head("GitHub Stats"),
        kv("Repos", str(u["public_repos"])),
        kv("Stars", str(stars)),
        kv("Commits", str(commits)),
        kv("Followers", str(u["followers"])),
    ]

    lh, top = 20, 30
    height = top + max(len(art), len(info)) * lh + 10
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="{height}px" font-size="16px">',
           "<style>.key{fill:#ffa657}.val{fill:#a5d6ff}.cc,.dot{fill:#616e7f}.art{fill:#c9d1d9}text,tspan{white-space:pre}</style>",
           f'<rect width="985px" height="{height}px" fill="#161b22" rx="15"/>',
           f'<text x="15" y="{top}" class="art">']
    out += [f'<tspan x="15" y="{top + (i + max(0, len(info) - len(art)) // 2) * lh}">{escape(l)}</tspan>' for i, l in enumerate(art)]
    out.append("</text>")
    out.append(f'<text x="390" y="{top}" fill="#c9d1d9">')
    for i, parts in enumerate(info):
        spans = "".join(f'<tspan class="{c}">{escape(t)}</tspan>' for c, t in parts)
        out.append(f'<tspan x="390" y="{top + i * lh}">{spans}</tspan>')
    out += ["</text>", "</svg>"]
    open("dark_mode.svg", "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main()
