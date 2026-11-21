"""Génère le site statique (./site) à partir de data/company.json et data/team.json.
Pour ajouter quelqu'un : modifier data/team.json + mettre sa photo dans photos/<slug>.jpg,
puis pousser sur GitHub. Le site se reconstruit et se redéploie tout seul."""
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')

with open(os.path.join(ROOT, 'data', 'company.json'), encoding='utf-8') as f:
    CO = json.load(f)
with open(os.path.join(ROOT, 'data', 'team.json'), encoding='utf-8') as f:
    TEAM = json.load(f)

ICON = {
    'tel': '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/>',
    'mail': '<path d="M3 5h18c.6 0 1 .4 1 1v12c0 .6-.4 1-1 1H3a1 1 0 0 1-1-1V6c0-.6.4-1 1-1zm9 7.2L4 7.3V17h16V7.3l-8 4.9zM5 7l7 4.3L19 7H5z"/>',
    'web': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-3a15.6 15.6 0 0 0-1.3-3.9A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h3c.3 1.4.8 2.7 1.3 3.9A8 8 0 0 1 5.1 16zm3-8h-3a8 8 0 0 1 4.3-3.9C8.9 5.3 8.4 6.6 8.1 8zM12 20c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.9c.5-1.2 1-2.5 1.3-3.9h3a8 8 0 0 1-4.3 3.9zm1.7-5.9a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z"/>',
    'wa': '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.8 14.1c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-2.9-1-5-3.6-5.4-4.1-.3-.5-1.2-1.6-1.2-3s.8-2.1 1-2.4c.3-.3.6-.4.8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.5.7c-.2.2-.3.4-.1.7.7 1.2 1.6 2 2.8 2.6.3.1.5.1.7-.1l.8-1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.4.1.1.1.6-.1 1.2z"/>',
    'pin': '<path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    'add': '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0 2c-3 0-8 1.5-8 4.5V21h10.5a6 6 0 0 1 3.4-6.4C16.4 14.2 14.2 14 12 14zm7 1v3h-3v2h3v3h2v-3h3v-2h-3v-3z"/>',
    'drill': '<path d="M10 2h4v3h3v4h-2l-1 9-2 4-2-4-1-9H7V5h3V2zm1 9 .6 6h.8l.6-6h-2z"/>',
    'leaf': '<path d="M20 3c-9 0-15 4-15 11 0 1.8.5 3.4 1.3 4.7L4 21l1.4 1.4 2.3-2.3C9 20.7 10.4 21 12 21c6 0 9-6 8-18zM8.5 17.9C10 13 13 10 17 8c-3 2.6-5 5.6-6.3 10.3-.8 0-1.6-.2-2.2-.4z"/>',
    'drop': '<path d="M12 2s-7 7.6-7 12.5A7 7 0 0 0 19 14.5C19 9.6 12 2 12 2zm-3.5 13h2a2 2 0 0 0 2 2v2a4 4 0 0 1-4-4z"/>',
    'cap': '<path d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3zM5 13.2V17l7 4 7-4v-3.8l-7 3.8-7-3.8z"/>',
    'people': '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM9 13c-3.3 0-7 1.6-7 4v3h14v-3c0-2.4-3.7-4-7-4zm8 0c-.5 0-1 0-1.5.1 1.5 1 2.5 2.3 2.5 3.9v3h5v-3c0-2.4-3.2-4-6-4z"/>',
}


def ico(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg>'


e = html.escape

CSS = """
/* VOICE sobre, industriel · IDEA la carte NFC SMS dépliée en site · PICTURE hexagones photo + bandes de forage orange
   COLOUR noir carbone, orange SMS, blanc · TYPE Roboto Condensed (titres) + Roboto · LAYOUT bandes pleine largeur, grille équipe */
:root{--o:#F0811A;--o2:#c9650a;--k:#1b1a17;--k2:#26241f;--ink:#17171a;--mut:#5d5d63;--line:#e7e5e1;--bg:#fff;--soft:#f6f4f0;color-scheme:light}
*{box-sizing:border-box;min-width:0}
html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Roboto,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;overflow-x:clip}
a{color:inherit}
h1,h2,h3,.cond{font-family:"Roboto Condensed",Roboto,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:0 max(5vw,18px)}
.hexclip{clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
header.top{position:sticky;top:0;z-index:20;background:var(--k);color:#fff;border-bottom:3px solid var(--o)}
header.top .wrap{display:flex;align-items:center;gap:14px;min-height:64px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand img{width:38px;height:auto}
.brand b{font-family:"Roboto Condensed",sans-serif;font-weight:700;letter-spacing:.06em;font-size:17px;text-transform:uppercase}
nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
nav a{text-decoration:none;font-size:15px;padding:10px 12px;color:#e9e6e0}
nav a:hover,nav a:focus-visible{color:var(--o)}
.hero{position:relative;background:var(--k);color:#fff;overflow:hidden}
.stripes{position:absolute;inset:auto 0 0 0;height:46%;background:repeating-linear-gradient(-12deg,transparent 0 30px,var(--o) 30px 48px);clip-path:polygon(0 55%,100% 0,100% 100%,0 100%);opacity:.95}
.hero .wrap{position:relative;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:40px;align-items:center;padding-top:clamp(40px,7vw,90px);padding-bottom:clamp(120px,14vw,190px)}
.hero h1{font-size:clamp(34px,5vw,54px);line-height:1.05;margin:0 0 18px;font-weight:700;text-wrap:balance}
.hero p{font-size:17px;color:#d8d4cc;max-width:56ch;margin:0 0 26px}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:12px 22px;background:var(--o);color:#fff;text-decoration:none;font-weight:700;border:0;font-size:16px;cursor:pointer}
.btn:hover{background:var(--o2)}
.btn.ghost{background:transparent;border:2px solid #fff;margin-left:8px}
.btn svg{width:20px;height:20px;fill:currentColor}
.hexlogo{justify-self:center;width:min(300px,70vw);filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}
.stats{position:relative;z-index:2;margin-top:-70px}
.stats .wrap{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;background:#fff;box-shadow:0 12px 40px rgba(0,0,0,.12);padding:0}
.stat{padding:24px 22px;border-left:1px solid var(--line)}
.stat:first-child{border-left:0}
.stat b{display:block;font-family:"Roboto Condensed",sans-serif;font-size:clamp(30px,4vw,42px);line-height:1;color:var(--o);font-weight:700}
.stat span{font-size:14px;color:var(--mut)}
.band{padding:clamp(48px,6vw,84px) 0}
.band.soft{background:var(--soft)}
.band.dark{background:var(--k);color:#fff}
h2{font-size:clamp(30px,3.6vw,42px);line-height:1.05;margin:0 0 10px;font-weight:700}
.lead{color:var(--mut);max-width:62ch;margin:0 0 32px;font-size:17px}
.dark .lead{color:#cfcac1}
.svc{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:18px}
.svc>div{background:#fff;padding:24px 20px;border-bottom:4px solid var(--o)}
.svc .hx{width:52px;height:58px;background:var(--k);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.svc .hx svg{width:26px;height:26px;fill:var(--o)}
.svc h3{margin:0 0 6px;font-size:21px}
.svc p{margin:0;color:var(--mut);font-size:15px}
.time{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:8px}
.time div{border-top:3px solid var(--o);padding-top:12px}
.time b{font-family:"Roboto Condensed",sans-serif;font-size:28px;color:var(--o)}
.time p{margin:4px 0 0;color:#d6d1c8;font-size:15px}
.team{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:22px}
.member{display:block;text-decoration:none;background:#fff;text-align:center;padding:28px 20px 24px;border:1px solid var(--line);transition:transform .2s,box-shadow .2s}
.member:hover,.member:focus-visible{transform:translateY(-4px);box-shadow:0 14px 30px rgba(0,0,0,.1);outline:none}
.ph{position:relative;width:170px;height:196px;margin:0 auto 18px;background:#c8c8c8}
.ph img{position:absolute;inset:7px;width:calc(100% - 14px);height:calc(100% - 14px);object-fit:cover;background:#fff;z-index:1}
.ph::after{content:"";position:absolute;inset:4px;background:#fff;z-index:0;clip-path:inherit}
.member .fn{font-size:17px;color:var(--mut)}
.member .ln{font-family:"Roboto Condensed",sans-serif;font-weight:700;font-size:28px;letter-spacing:.02em;line-height:1.1}
.member .rl{color:var(--o);font-family:"Roboto Condensed",sans-serif;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:14px;margin:8px 0 14px}
.member .go{font-size:14px;font-weight:600;border-top:1px solid var(--line);padding-top:12px;display:block}
.contact{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:22px}
.ci{display:flex;gap:14px;align-items:flex-start}
.hxs{flex:0 0 42px;height:46px;background:var(--o);display:flex;align-items:center;justify-content:center}
.hxs svg{width:20px;height:20px;fill:#fff}
.ci small{display:block;color:#a9a39a;font-size:13px}
.ci a,.ci span{text-decoration:none;font-size:16px;white-space:normal}
.soc{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.soc a{border:1px solid #4a463f;padding:10px 16px;text-decoration:none;font-size:15px}
.soc a:hover{border-color:var(--o);color:var(--o)}
footer{background:#111;color:#8f8a82;font-size:13px;padding:20px 0}
footer .wrap{display:flex;gap:10px;flex-wrap:wrap;justify-content:space-between}
footer a{color:var(--o);text-decoration:none}
.pp{background:var(--k);color:#fff;position:relative;overflow:hidden}
.pp .stripes{height:12%}
.pp .wrap{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(24px,5vw,60px);align-items:center;padding-top:clamp(30px,5vw,60px);padding-bottom:clamp(60px,8vw,100px)}
.pp .ph{width:clamp(190px,26vw,280px);height:clamp(219px,30vw,323px);margin:0}
.pp .fn{font-size:clamp(22px,2.6vw,30px);color:#e2ded6}
.pp h1{font-size:clamp(40px,6vw,64px);line-height:1;margin:2px 0 12px;letter-spacing:.02em}
.pp .rl{display:inline-block;background:var(--o);color:#fff;font-family:"Roboto Condensed",sans-serif;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:7px 14px;font-size:15px}
.pp .co{margin-top:12px;color:#cfcac1}
.back{display:inline-flex;align-items:center;gap:6px;color:#fff;text-decoration:none;font-size:15px;padding:10px 0;margin-left:auto}
.back:hover{color:var(--o)}
.pcard{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:28px;margin-top:-40px;position:relative;z-index:2}
.rows{background:#fff;box-shadow:0 12px 40px rgba(0,0,0,.1);padding:8px 24px}
.row{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid var(--line);text-decoration:none;min-height:64px}
.row:last-child{border-bottom:0}
.row .hxs{flex-basis:46px;height:50px}
.row .hxs.wa{background:#25D366}
.row small{display:block;color:#8a857d;font-size:13px}
.row b{font-size:17px;font-weight:500;overflow-wrap:anywhere}
.row .ar{margin-left:auto;color:#bbb;font-size:22px}
.row:hover b{color:var(--o2)}
.side{display:flex;flex-direction:column;gap:14px}
.side .btn{justify-content:center;width:100%;margin:0}
.side .btn.dark{background:var(--k)}
.side .btn.dark:hover{background:#333}
.side .box{background:var(--soft);padding:20px;font-size:15px;color:var(--mut)}
.side .box b{color:var(--ink);font-family:"Roboto Condensed",sans-serif;font-size:18px;display:block;margin-bottom:4px}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--k);color:#fff;padding:12px 18px;font-size:15px;opacity:0;transition:opacity .25s;pointer-events:none}
.toast.on{opacity:1}
:focus-visible{outline:3px solid var(--o);outline-offset:2px}
@media(max-width:860px){.hero .wrap{grid-template-columns:1fr}.hexlogo{width:180px;order:-1;justify-self:start}.stats .wrap{grid-template-columns:repeat(2,minmax(0,1fr))}.stat:nth-child(3){border-left:0}.stat{border-top:1px solid var(--line)}.stat:nth-child(-n+2){border-top:0}.time{grid-template-columns:repeat(2,minmax(0,1fr))}.pcard{grid-template-columns:1fr}}
@media(max-width:600px){nav{display:none}.brand b{font-size:14px;letter-spacing:.03em}.back{white-space:nowrap;font-size:14px}.pp .stripes{height:12%}.hero .stripes{height:22%}.pp .wrap{grid-template-columns:1fr;text-align:center;justify-items:center}.btn.ghost{margin:10px 0 0}.rows{padding:4px 16px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.member{transition:none}}
"""

HEAD = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{ogimg}"><meta name="theme-color" content="#1b1a17">
<link rel="icon" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css"></head><body>"""

TOP = """<header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="assets/logo.png" alt="Logo SMS" width="38" height="42"><b>{name}</b></a>{nav}</div></header>"""

FOOT = """<footer><div class="wrap"><span>© {name} · Bamako, Mali</span><span>Cartes NFC par <a href="https://www.tiktok.com/@mali_cartini" target="_blank" rel="noopener">Malicartini</a></span></div></footer>"""


def contact_block():
    tels = ''.join(f'<div class="ci"><div class="hxs hexclip">{ico("tel")}</div><div><small>Téléphone</small><a href="tel:{t}">{d}</a></div></div>' for t, d in CO['tel'])
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in CO['social'])
    return f"""<section class="band dark" id="contact"><div class="wrap">
<h2>Nous contacter</h2><p class="lead">Une question, un projet minier ou de BTP ? Appelez-nous ou passez nous voir.</p>
<div class="contact">{tels}
<div class="ci"><div class="hxs hexclip">{ico("mail")}</div><div><small>E-mail</small><a href="mailto:{CO['email']}">{CO['email']}</a></div></div>
<div class="ci"><div class="hxs hexclip">{ico("pin")}</div><div><small>Adresse</small><span>{e(CO['addr'])}</span></div></div>
</div><div class="soc">{soc}</div></div></section>"""


def index():
    nav = '<nav><a href="#services">Services</a><a href="#equipe">Équipe</a><a href="#contact">Contact</a></nav>'
    svc = ''.join(f'<div><div class="hx hexclip">{ico(i)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d, i in CO['services'])
    stats = ''.join(f'<div class="stat"><b>{e(v)}</b><span>{e(l)}</span></div>' for v, l in CO['stats'])
    tl = ''.join(f'<div><b>{e(y)}</b><p>{e(t)}</p></div>' for y, t in CO['timeline'])
    team = ''.join(f'''<a class="member" href="{m['slug']}.html"><div class="ph hexclip"><img class="hexclip" src="photos/{m['photo']}" alt="{e(m['first'])} {e(m['last'].title())}" loading="lazy" width="520" height="600"></div>
<div class="fn">{e(m['first'])}</div><div class="ln">{e(m['last'])}</div><div class="rl">{e(m['role'])}</div><span class="go">Voir sa carte de contact →</span></a>''' for m in TEAM)
    body = f"""{TOP.format(name=e(CO['name']), nav=nav)}
<section class="hero"><div class="stripes"></div><div class="wrap"><div>
<h1>{e(CO['tagline'])}</h1>
<p>{e(CO['intro'])}</p>
<a class="btn" href="#equipe">Rencontrer l'équipe</a><a class="btn ghost" href="#contact">Nous contacter</a></div>
<img class="hexlogo" src="assets/logo.png" alt="" width="200" height="219"></div></section>
<section class="stats"><div class="wrap">{stats}</div></section>
<section class="band" id="services"><div class="wrap"><h2>Nos services</h2>
<p class="lead">Du forage à la remise en état des sites, en passant par la formation des conducteurs d'engins et la fourniture de personnel qualifié.</p>
<div class="svc">{svc}</div></div></section>
<section class="band dark"><div class="wrap"><h2>Notre parcours</h2><div class="time">{tl}</div></div></section>
<section class="band soft" id="equipe"><div class="wrap"><h2>Notre équipe</h2>
<p class="lead">Les femmes et les hommes qui font avancer vos projets. Touchez une carte pour retrouver leurs coordonnées et les enregistrer dans votre téléphone.</p>
<div class="team">{team}</div></div></section>
{contact_block()}{FOOT.format(name=e(CO['name']))}</body></html>"""
    d = f"{CO['name']} : forage, réhabilitation, assainissement, formations et placement de talents au Mali. Rencontrez notre équipe."
    return HEAD.format(title=f"{CO['name']} — Notre équipe", desc=d, ogimg='assets/logo.png') + body


def vcard(m):
    tels = ''.join(f'TEL;TYPE=WORK,VOICE:{t}\r\n' for t, _ in m['tel'])
    return (f"BEGIN:VCARD\r\nVERSION:3.0\r\nN:{m['last'].title()};{m['first']};;;\r\nFN:{m['first']} {m['last'].title()}\r\n"
            f"ORG:{CO['name']} ({CO['short']})\r\nTITLE:{m['role']}\r\n{tels}EMAIL;TYPE=WORK:{m['email']}\r\nURL:{CO['web']}\r\n"
            f"END:VCARD\r\n")


def person(m):
    full = f"{m['first']} {m['last'].title()}"
    rows = ''.join(f'<a class="row" href="tel:{t}"><div class="hxs hexclip">{ico("tel")}</div><div><small>Téléphone</small><b>{d}</b></div><span class="ar">›</span></a>' for t, d in m['tel'])
    rows += f'<a class="row" href="https://wa.me/{m["wa"]}" target="_blank" rel="noopener"><div class="hxs wa hexclip">{ico("wa")}</div><div><small>WhatsApp</small><b>Écrire un message</b></div><span class="ar">›</span></a>'
    rows += f'<a class="row" href="mailto:{m["email"]}"><div class="hxs hexclip">{ico("mail")}</div><div><small>E-mail</small><b>{m["email"]}</b></div><span class="ar">›</span></a>'
    rows += f'<a class="row" href="{CO["web"]}" target="_blank" rel="noopener"><div class="hxs hexclip">{ico("web")}</div><div><small>Site officiel</small><b>www.senomining.com</b></div><span class="ar">›</span></a>'
    nav = f'<a class="back" href="index.html#equipe">← Toute l\'équipe</a>'
    body = f"""{TOP.format(name=e(CO['name']), nav=nav)}
<section class="pp"><div class="stripes"></div><div class="wrap">
<div class="ph hexclip"><img class="hexclip" src="photos/{m['photo']}" alt="{e(full)}" width="520" height="600"></div>
<div><div class="fn">{e(m['first'])}</div><h1>{e(m['last'])}</h1><span class="rl">{e(m['role'])}</span><div class="co">{e(CO['name'])} ({e(CO['short'])})</div></div>
</div></section>
<section class="band" style="padding-top:0"><div class="wrap"><div class="pcard">
<div class="rows">{rows}</div>
<div class="side">
<a class="btn dark" href="{m['slug']}.vcf" download="{m['slug']}.vcf">{ico("add")} Enregistrer le contact</a>
<button class="btn" id="share" type="button">Partager cette carte</button>
<div class="box"><b>{e(CO['name'])}</b>{e(CO['intro'])}<br><a href="index.html" style="color:var(--o2);font-weight:600">Découvrir l'entreprise →</a></div>
</div></div></div></section>
{contact_block()}{FOOT.format(name=e(CO['name']))}<div class="toast" id="toast">Lien copié</div>
<script>{{const b=document.getElementById('share'),t=document.getElementById('toast');
b.addEventListener('click',async()=>{{const u=location.href;try{{if(navigator.share){{await navigator.share({{title:{full!r},url:u}});return}}await navigator.clipboard.writeText(u);t.classList.add('on');setTimeout(()=>t.classList.remove('on'),1800)}}catch(e){{}}}});}}</script>
</body></html>"""
    d = f"{full}, {m['role'].title()} chez {CO['name']}. Téléphone, e-mail, WhatsApp et contact à enregistrer."
    return HEAD.format(title=f"{full} — {CO['name']}", desc=e(d), ogimg=f"photos/{m['photo']}") + body


def resize_photo(src, dst, box=(520, 600)):
    from PIL import Image
    im = Image.open(src).convert('RGB')
    w, h = im.size
    tw, th = box
    s = max(tw / w, th / h)
    im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
    w, h = im.size
    x0, y0 = (w - tw) // 2, max(0, (h - th) // 3)
    im.crop((x0, y0, x0 + tw, y0 + th)).save(dst, quality=87)


def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, 'assets'))
    os.makedirs(os.path.join(SITE, 'photos'))
    open(os.path.join(SITE, 'assets', 'style.css'), 'w').write(CSS)
    shutil.copy(os.path.join(ROOT, 'assets', 'logo.png'), os.path.join(SITE, 'assets', 'logo.png'))
    open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(index())
    for m in TEAM:
        src_photo = os.path.join(ROOT, 'photos', m['photo'])
        resize_photo(src_photo, os.path.join(SITE, 'photos', m['photo']))
        open(os.path.join(SITE, f"{m['slug']}.html"), 'w', encoding='utf-8').write(person(m))
        open(os.path.join(SITE, f"{m['slug']}.vcf"), 'w', newline='', encoding='utf-8').write(vcard(m))
    open(os.path.join(SITE, '_headers'), 'w').write(
        "/*.vcf\n  Content-Type: text/vcard; charset=utf-8\n  Content-Disposition: attachment\n"
        "/photos/*\n  Cache-Control: public, max-age=86400\n")
    print('Site généré dans', SITE)


if __name__ == '__main__':
    main()
