"""Unity prototip repolarindan vitrin icin ham veri toplar.

Her repo icin: README, gorsel URL'leri, klasor yapisi ve script adlari.
Script adlari mekanikleri en dogru sekilde anlatan veri (PlayerController,
Spawner, GameManager ...).
"""
import json
import subprocess
import base64
import re

REPOS = [
    "2d-platformer", "audio-virtualization", "basketball-master", "basket-time",
    "beauty-saloon-fever", "candy-explosion", "crazy-cube", "crush-it",
    "cube-mountain", "mario-clone", "rhythm-surfer", "run-and-avoid",
    "stack-box", "zelda-like", "protect-base", "catch-rhythm", "shot-merger",
    "climb-the-stair", "match_2_blast", "math-vr", "spawning-system",
    "plant-a-tree", "word-of-the-war", "weapon-craft-run-clone",
]

SKIP = re.compile(r"^$", re.M)


def gh(args):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def readme(repo):
    raw = gh(["api", f"repos/bahattinercan/{repo}/readme", "--jq", ".content"])
    if not raw.strip():
        return ""
    try:
        return base64.b64decode(raw).decode("utf-8", "replace")
    except Exception:
        return ""


def tree(repo):
    raw = gh(["api", f"repos/bahattinercan/{repo}/git/trees/HEAD?recursive=1"])
    try:
        d = json.loads(raw)
    except Exception:
        return [], []
    paths = [t["path"] for t in d.get("tree", []) if t["type"] == "blob"]
    scripts = sorted({p.split("/")[-1] for p in paths if p.lower().endswith(".cs")})
    images = sorted({p for p in paths
                     if re.search(r"\.(png|jpg|jpeg|gif|webp)$", p, re.I)})
    return scripts, images


def image_urls(text):
    urls = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    urls += re.findall(r'<img[^>]+src="([^"]+)"', text)
    return urls


def main():
    out = {}
    for repo in REPOS:
        rd = readme(repo)
        scripts, images = tree(repo)
        out[repo] = {
            "readme_len": len(rd),
            "readme_head": rd[:900],
            "readme_images": image_urls(rd),
            "repo_images": images[:25],
            "scripts": scripts[:60],
            "script_count": len(scripts),
        }
        print(f"{repo:26s} script={len(scripts):3d} img={len(images):2d} readme={len(rd)}")
    with open("tools/unity_repos.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n-> tools/unity_repos.json")


if __name__ == "__main__":
    main()
