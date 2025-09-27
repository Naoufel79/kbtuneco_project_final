from pathlib import Path
import sys
import polib


def compile_all(locale_dir: str = "locale") -> int:
    base = Path(locale_dir)
    if not base.exists():
        print(f"[compile_translations] Locale directory not found: {base}")
        return 1

    total = 0
    for po_path in base.rglob("*.po"):
        mo_path = po_path.with_suffix(".mo")
        try:
            po = polib.pofile(str(po_path))
            mo_path.parent.mkdir(parents=True, exist_ok=True)
            po.save_as_mofile(str(mo_path))
            print(f"[compile_translations] Compiled {po_path} -> {mo_path}")
            total += 1
        except Exception as e:
            print(f"[compile_translations] ERROR compiling {po_path}: {e}")
            return 2

    print(f"[compile_translations] Compiled {total} translation file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(compile_all())
