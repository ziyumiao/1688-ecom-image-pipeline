"""Install bundled companion skills beside this skill without overwriting existing ones."""

from __future__ import annotations

import shutil
from pathlib import Path


def main() -> None:
    skill_root = Path(__file__).resolve().parents[1]
    skills_root = skill_root.parent
    bundle_root = skill_root / "companion-skills"

    for name in ("codesonline-image", "ecom-details-image"):
        source = bundle_root / name
        target = skills_root / name
        if not (source / "SKILL.md").is_file():
            raise FileNotFoundError(f"Missing bundled skill source: {source}")
        if target.exists():
            print(f"Already installed; left unchanged: {target}")
            continue
        shutil.copytree(source, target)
        print(f"Installed: {target}")


if __name__ == "__main__":
    main()
