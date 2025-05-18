import sys
from parser import load_replay_file, reconstruct_all_rounds
from visualizer import render_rounds_as_images_and_gif

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_replay.grbr>")
        sys.exit(1)

    replay_path = sys.argv[1]
    player1_raw, player2_raw = load_replay_file(replay_path)
    round_frames = reconstruct_all_rounds(player1_raw, player2_raw)
    render_rounds_as_images_and_gif(round_frames)

if __name__ == "__main__":
    main()
