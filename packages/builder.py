import pathlib
import hashlib
import subprocess
import shutil
from setuptools_scm import get_version

root = pathlib.Path(__file__).parent.parent
static = root / "rest_pandas" / "static" / "app"


def get_hash_path():
    return static / ".sha256"


def get_stored_hash():
    return get_hash_path().read_text()


def set_stored_hash(value):
    return get_hash_path().write_text(value)


def compute_hash():
    hashes = []
    for path in sorted(static.rglob("*.*")):
        rel_path = str(path.relative_to(static))
        if path.name.startswith(".") or path.name.endswith(".map"):
            continue
        sha = hashlib.sha256()
        data = path.read_bytes()
        if path.name == "analyst.js":
            data = data.replace(get_version().encode(), b"__WQ_VERSION__")
            rel_path += "'"
        sha.update(data)
        hashes.append(f"{sha.hexdigest()}  {rel_path}\n")

    return "".join(hashes)


def build(update_hash=False):
    old_hash = get_stored_hash()
    print("Building analyst.js and chart.js...")
    subprocess.check_call(["npm", "install"])
    subprocess.check_call(["npm", "run", "rollup-all"])

    new_hash = compute_hash()

    if new_hash != old_hash:
        print("Old Hash:")
        print("  " + old_hash.replace("\n", "\n  "))
        print("New Hash:")
        print("  " + new_hash.replace("\n", "\n  "))
        if update_hash or ".dev" in get_version():
            set_stored_hash(new_hash)
            return True
        else:
            return False
    else:
        print("Hash unchanged since last build.")
        return True


if __name__ == "__main__":
    build(update_hash=True)