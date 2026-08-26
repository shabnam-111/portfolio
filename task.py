import cv2
import os
from pathlib import Path


def get_sorted_videos(folder):
    videos = [f for f in os.listdir(folder) if f.lower().endswith(".mp4")]

    def sort_key(name):
        try:
            return int(Path(name).stem)
        except:
            return name

    return sorted(videos, key=sort_key)


def extract_frames_from_videos(video_folder, output_folder, target_fps=60):
    os.makedirs(output_folder, exist_ok=True)

    videos = get_sorted_videos(video_folder)

    frame_number = 1

    print(f"\nProcessing folder: {video_folder}")

    for video in videos:
        video_path = os.path.join(video_folder, video)

        print(f"Reading: {video}")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Could not open {video}")
            continue

        original_fps = cap.get(cv2.CAP_PROP_FPS)

        if original_fps <= 0:
            original_fps = target_fps

        frame_step = max(1, round(original_fps / target_fps))

        current_frame = 0

        while True:
            success, frame = cap.read()

            if not success:
                break

            if current_frame % frame_step == 0:
                filename = os.path.join(
                    output_folder,
                    f"{frame_number:03d}.png"
                )

                cv2.imwrite(filename, frame)
                frame_number += 1

            current_frame += 1

        cap.release()

    print(f"Saved {frame_number - 1} frames to {output_folder}")


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(__file__))

    day_folder = os.path.join(base_dir, "frames", "day")
    night_folder = os.path.join(base_dir, "frames", "night")

    day_output = os.path.join(base_dir, "day_frames")
    night_output = os.path.join(base_dir, "night_frames")

    extract_frames_from_videos(day_folder, day_output, 60)
    extract_frames_from_videos(night_folder, night_output, 60)

    print("\nDone!")