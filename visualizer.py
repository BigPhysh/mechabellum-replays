import matplotlib.pyplot as plt
import matplotlib.animation as animation

def render_rounds_as_images_and_gif(frames):
    for round_number, p1_units, p2_units in frames:
        fig, ax = plt.subplots(figsize=(10, 8))
        for key, data in p1_units.items():
            label = f'{data["unit_id"]}:{key}'
            ax.scatter(data["x"], data["y"], color="blue")
            ax.text(data["x"], data["y"], label, color="blue", fontsize=8, ha='right')
        for key, data in p2_units.items():
            label = f'{data["unit_id"]}:{key}'
            ax.scatter(data["x"], data["y"], color="red")
            ax.text(data["x"], data["y"], label, color="red", fontsize=8, ha='left')
        ax.set_title(f"Unit Positions – End of Round {round_number}")
        ax.set_xlim(-250, 250)
        ax.set_ylim(-300, 300)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(f"round_{round_number}.png")
        plt.close()

    fig, ax = plt.subplots(figsize=(10, 8))
    def update(frame_data):
        round_number, p1_units, p2_units = frame_data
        ax.clear()
        for key, data in p1_units.items():
            label = f'{data["unit_id"]}:{key}'
            ax.scatter(data["x"], data["y"], color="blue")
            ax.text(data["x"], data["y"], label, color="blue", fontsize=8, ha='right')
        for key, data in p2_units.items():
            label = f'{data["unit_id"]}:{key}'
            ax.scatter(data["x"], data["y"], color="red")
            ax.text(data["x"], data["y"], label, color="red", fontsize=8, ha='left')
        ax.set_title(f"Unit Positions – End of Round {round_number}")
        ax.set_xlim(-250, 250)
        ax.set_ylim(-300, 300)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False)
    ani.save("mechabellum_replay.gif", writer='pillow', fps=1)
    plt.close()
