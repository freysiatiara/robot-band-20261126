import os

LINE = "The Captchas \u2014 hit single 'Prove You're Human' is the only number one no robot has ever been allowed to stream."


def resolve_output_path():
    if os.environ.get("ENTRY_OUTPUT"):
        return os.environ["ENTRY_OUTPUT"]
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def main():
    line = LINE
    if not line or not line.strip():
        raise SystemExit("entry text must not be blank")
    if not 1 <= len(line) <= 200:
        raise SystemExit("entry text must be 1..200 characters, got %d" % len(line))
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    os.chmod(path, 0o644)
    # Read-back verification guard: the bytes on disk must equal the
    # intended line exactly and stay within the 1..200 char gate.
    with open(path, "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        raise SystemExit("read-back mismatch: output bytes differ from intended entry")
    if not 1 <= len(written.decode("utf-8")) <= 200:
        raise SystemExit("read-back length out of range: %d chars" % len(written.decode("utf-8")))


if __name__ == "__main__":
    main()
