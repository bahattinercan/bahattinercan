"""readmes/ klasorundeki dosyalari ilgili repolara README.md olarak push eder."""
import base64
import io
import json
import os
import subprocess

OWNER = "bahattinercan"
STAGE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "readmes")

MESSAGE = (
    "docs: kök README ekle\n\n"
    "Repo'nun açıklaması vardı ama giriş noktası yoktu: ziyaretçi ne olduğunu,\n"
    "nasıl çalıştırılacağını ve nerede bittiğini okuyamıyordu. Her README\n"
    "yapıyı, çalıştırma adımlarını ve bilinen sınırları açıkça yazıyor.\n"
)


def push(repo, path):
    body = io.open(path, encoding="utf-8").read()
    payload = {
        "message": MESSAGE,
        "content": base64.b64encode(body.encode("utf-8")).decode("ascii"),
    }
    tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "ghpayload.json")
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False))
    r = subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{OWNER}/{repo}/contents/README.md",
         "--input", tmp],
        capture_output=True, text=True, encoding="utf-8",
    )
    ok = '"content"' in (r.stdout or "")
    if not ok:
        # Var olan README varsa sha gerekiyor
        return False, (r.stdout or r.stderr).strip()[:220]
    return True, ""


def main():
    files = sorted(f for f in os.listdir(STAGE) if f.endswith(".md"))
    ok = fail = 0
    for f in files:
        repo = f[:-3]
        good, err = push(repo, os.path.join(STAGE, f))
        print(f"{'ok  ' if good else 'HATA'} {repo}")
        if good:
            ok += 1
        else:
            fail += 1
            print("      ", err)
    print(f"\n{ok} repo guncellendi, {fail} sorun")


if __name__ == "__main__":
    main()
