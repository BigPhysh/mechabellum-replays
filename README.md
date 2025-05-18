# Mechabellum Replay Viewer

This tool visualizes Mechabellum replay files (`.grbr`) by reconstructing unit positions at the end of each round using only action records and round snapshots.

## Features
- Supports `.grbr` files with up to 6 rounds
- Accurately detects unit movement, buying, selling, and reinforcements
- Produces static plots for each round
- Exports a GIF animation of the full match

## Usage

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the viewer:
```
python main.py path/to/your_replay.grbr
```

3. Outputs:
- A GIF animation of the match
- Static images for each round


---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
