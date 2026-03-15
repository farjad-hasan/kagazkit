from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke-test the packaged KagazKit Windows executable."
    )
    parser.add_argument("exe_path", help="Path to KagazKit.exe")
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Seconds to wait for the packaged smoke test to finish",
    )
    args = parser.parse_args()

    exe_path = Path(args.exe_path).resolve()
    if not exe_path.exists():
        raise FileNotFoundError(f"Executable not found: {exe_path}")

    smoke_dir = Path(tempfile.mkdtemp(prefix="kagazkit-smoke-"))
    result_file = smoke_dir / "result.txt"

    env = os.environ.copy()
    env["KAGAZKIT_SMOKE_TEST_FILE"] = str(result_file)

    process = subprocess.Popen([str(exe_path)], env=env)
    try:
        process.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired as exc:
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError("Packaged smoke test did not exit within the timeout") from exc

    if process.returncode != 0:
        raise RuntimeError(
            f"Packaged smoke test exited with code {process.returncode}"
        )
    if not result_file.exists():
        raise RuntimeError("Packaged smoke test did not write a result marker")

    result = result_file.read_text(encoding="utf-8").strip()
    if result != "ok":
        raise RuntimeError(f"Packaged smoke test failed: {result}")

    print("GUI smoke test passed for KagazKit.exe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
