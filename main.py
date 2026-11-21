"""news-image-20261121 entrypoint.

Copies the pre-rendered front page (image.jpg, committed in this repo)
to the grader's output path. Standard library only: the grading runtime
installs nothing, so this file imports nothing beyond os and shutil.
The output file is always named entry.png, whatever the source format
(RULES.txt: "The file is a PNG or a JPEG, told apart by its first bytes;
the name stays entry.png either way").
"""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "image.jpg")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
