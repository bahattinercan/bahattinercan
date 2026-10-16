"""Vitrin repolarina MIT lisansi ekler.

Kapsam disi birakilanlar:
- russia-plague-website, doner-website : zaten MIT
- local-ai-news, beauty-salon          : ticari urun olabilir, karar kullaniciya ait
- arsivlenmis repolar                  : read-only
"""
import base64
import json
import os
import subprocess

OWNER = "bahattinercan"
YEAR = "2026"
HOLDER = "Bahattin Ercan"

MIT = """MIT License

Copyright (c) {year} {holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(year=YEAR, holder=HOLDER)

REPOS = [
    "unity-prototypes-archive", "steam-layout", "tiktok_frontend",
    "flutter-responsive-ui", "flutter-neumorphism-design", "b2b-site",
    "b2b-site-angular", "toggle-crm-api", "barber_shops", "barber-shops-api",
    "e-commerce-backend", "e-commerce-frontend", "e-commerce-admin",
    "smart_home_design", "amazon-clone", "edusity", "instagram_frontend",
]

MSG = (
    "chore: MIT lisansı ekle\n\n"
    "Public repoların hiçbirinde lisans yoktu; lisanssız bir repo hukuken\n"
    "\"tüm hakları saklı\" demektir, yani okuyan biri kodu örnek alamaz.\n"
    "Vitrin niteliğindeki repolara MIT eklendi.\n"
)


def main():
    ok = fail = 0
    for repo in REPOS:
        payload = {"message": MSG,
                   "content": base64.b64encode(MIT.encode("utf-8")).decode("ascii")}
        tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "licpayload.json")
        open(tmp, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False))
        r = subprocess.run(
            ["gh", "api", "-X", "PUT", f"repos/{OWNER}/{repo}/contents/LICENSE",
             "--input", tmp],
            capture_output=True, text=True, encoding="utf-8")
        good = '"content"' in (r.stdout or "")
        print(f"{'ok  ' if good else 'HATA'} {repo}")
        if not good:
            print("      ", (r.stdout or r.stderr).strip()[:160])
        ok += good
        fail += (not good)
    print(f"\n{ok} repo, {fail} sorun")


if __name__ == "__main__":
    main()
