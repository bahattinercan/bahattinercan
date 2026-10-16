"""Profil denetimi: eksikleri ve kirik baglantilari tek komutta raporlar.

Kullanim:
    python tools/audit_profile.py [kullanici]

Cikis kodu: kritik sorun varsa 1, yoksa 0. CI'a baglanabilir.
Bagimlilik yok (urllib + gh CLI).
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

OWNER = sys.argv[1] if len(sys.argv) > 1 else "bahattinercan"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Bu alan adlari botu engelliyor; 2xx beklenmez, uyari sayilmaz.
ALLOW_NON_2XX = ("linkedin.com", "img.shields.io", "komarev.com")


def gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return r.stdout


def gh_text(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def http(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (profile-audit)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


class Report:
    def __init__(self):
        self.fail = 0
        self.warn = 0

    def ok(self, msg):
        print(f"  \u2713 {msg}")

    def bad(self, msg):
        print(f"  \u2717 {msg}")
        self.fail += 1

    def meh(self, msg):
        print(f"  ! {msg}")
        self.warn += 1

    def head(self, t):
        print(f"\n{t}")


def main():
    rep = Report()
    public = gh(["repo", "list", OWNER, "--limit", "100", "--json",
                 "name,isPrivate,isFork,description,homepageUrl,pushedAt,isArchived"])
    if not public:
        print("repo listesi alinamadi (gh auth?)")
        return 1
    own = [r for r in public if not r["isPrivate"] and not r["isFork"]]
    # Arsivli repolar salt-okunur: eksikleri duzeltilemez, ayri raporlanir.
    live = [r for r in own if not r.get("isArchived")]
    arch = [r for r in own if r.get("isArchived")]

    # 1) Profil README
    rep.head("1) Profil README")
    diff = gh_text(["api", f"repos/{OWNER}/{OWNER}/readme", "--jq", ".name"]).strip()
    if diff:
        rep.ok("profil README var")
    else:
        rep.bad("profil README yok — anasayfada kisisel bolum gorunmez")

    md_path = os.path.join(ROOT, "README.md")
    md = io.open(md_path, encoding="utf-8").read() if os.path.exists(md_path) else ""

    # 2) README baglantilari
    rep.head("2) README baglantilari")
    urls = sorted(set(re.findall(r'https?://[^\s"\'<>\)]+', md)))
    checked = bad = 0
    for u in urls:
        if any(d in u for d in ALLOW_NON_2XX):
            continue
        checked += 1
        code = http(u)
        if not str(code).startswith("2"):
            rep.bad(f"HTTP {code}  {u}")
            bad += 1
    rep.ok(f"{checked} baglanti kontrol edildi" if not bad else f"{checked} baglanti, {bad} kirik")

    # 3) Goreli gorsel referanslari (profil reposu icinde)
    rep.head("3) README gorsel dosyalari")
    refs = [m for m in re.findall(r'src="([^"]+)"', md) if not m.startswith(("http", "data:"))]
    missing = [r for r in refs if not os.path.exists(os.path.join(ROOT, r))]
    if missing:
        for m in missing:
            rep.bad(f"dosya yok: {m}")
    else:
        rep.ok(f"{len(refs)} yerel gorsel referansi gecerli")

    # 4) Repo hijyeni
    rep.head(f"4) Public repo hijyeni ({len(live)} duzenlenebilir, "
             f"{len(arch)} arsivli)")
    no_desc, no_topics, no_readme, no_lic = [], [], [], []
    for r in live:
        name = r["name"]
        if not (r.get("description") or "").strip():
            no_desc.append(name)
        topics = gh(["api", f"repos/{OWNER}/{name}/topics", "--jq", ".names"]) or []
        if not topics:
            no_topics.append(name)
        if not gh_text(["api", f"repos/{OWNER}/{name}/readme", "--jq", ".name"]).strip():
            no_readme.append(name)
        if not gh_text(["api", f"repos/{OWNER}/{name}/license", "--jq", ".license.spdx_id"]).strip():
            no_lic.append(name)

    for label, lst in (("aciklama", no_desc), ("topic", no_topics),
                       ("README", no_readme), ("lisans (bilincli olabilir)", no_lic)):
        if lst:
            rep.meh(f"{label} eksik: {len(lst)} — {', '.join(lst[:6])}"
                    + (" ..." if len(lst) > 6 else ""))
        else:
            rep.ok(f"{label}: tamami dolu")
    if arch:
        print(f"  Not: {len(arch)} arsivli repo (salt-okunur) kapsam disi; "
              f"indeksleri unity-prototypes-archive reposunda.")

    # 5) Demo baglantilari
    rep.head("5) Canli demo baglantilari")
    homes = [(r["name"], r["homepageUrl"]) for r in own
             if r.get("homepageUrl") and not r.get("isArchived")]
    if not homes:
        rep.meh("hicbir repoda canli demo baglantisi yok")
    for name, url in homes:
        code = http(url)
        if str(code).startswith("2"):
            rep.ok(f"{name} -> {url}")
        else:
            rep.bad(f"{name} -> HTTP {code}  {url}")

    # 6) Pinlenen repolar
    rep.head("6) Pinlenen repolar")
    q = ('{user(login:"%s"){pinnedItems(first:6,types:REPOSITORY){nodes{'
         '... on Repository{name description homepageUrl isArchived}}}}}' % OWNER)
    data = gh(["api", "graphql", "-f", f"query={q}"])
    try:
        pins = data["data"]["user"]["pinnedItems"]["nodes"]
    except Exception:
        pins = []
    if not pins:
        rep.meh("pin listesi okunamadi")
    for p in pins:
        note = []
        if not (p.get("description") or "").strip():
            note.append("aciklama YOK")
        if p.get("isArchived"):
            note.append("ARSIVLI")
        if note:
            rep.meh(f"{p['name']}: {', '.join(note)}")
        else:
            rep.ok(f"{p['name']}: aciklama var")
    print("\n  Not: pin secimi GitHub API'sinde yok; 'Customize your pins' arayuzunden yapilir.")

    # 7) Katki dagilimi
    rep.head("7) Katki dagilimi (son 12 ay)")
    try:
        req = urllib.request.Request(f"https://github.com/users/{OWNER}/contributions",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as r:
            html = r.read().decode("utf-8", "replace")
        tips = re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html)
        total = sum(0 if t.startswith("No ") else int(re.match(r"(\d+)", t).group(1))
                    for _, t in tips if re.match(r"(\d+|No) contribution", t))
        rep.ok(f"son 12 ayda {total} katki (ozel repolar dahil)")
        print("  Not: ucuncu parti istatistik kartlari bunu gosteremez; kendi kartimiz gosteriyor.")
    except Exception as e:
        rep.meh(f"katki verisi alinamadi: {e}")

    print(f"\n{'='*58}\nSONUC: {rep.fail} kritik, {rep.warn} uyari")
    return 1 if rep.fail else 0


if __name__ == "__main__":
    sys.exit(main())
