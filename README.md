# cp-merger

A tool to merge Content Patcher mods.

## usage

1. `git clone https://github.com/anotherpillow/cp-merger --recurse-submodules`
2. `pip install -r requirements.txt` (or `python -m pip`, `python3 -m pip`, or `py -m pip`)
3. Place your mods in `input/`, so they're `input/[CP] Mod`, etc.
4. `py main.py --modid CombinedModAuthors.ModID` (or `python`, or `python3`) (or `-i`, or `--id`)
5. Find the merged mod in `output/`
