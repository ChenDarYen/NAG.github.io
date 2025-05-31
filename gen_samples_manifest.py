import os
import json


def main():
    # Base directory containing all sample subfolders
    base_dir = os.path.join(os.path.dirname(__file__), "assets", "samples")

    # Map HTML grid IDs to their corresponding sample subfolders
    grids = {
        "gridFluxSchnell": "flux-schnell_4-step",
        "gridLargeTurbo":  "sd3.5-large-turbo_8-step",
        "gridFluxDev":     "flux-dev_25-step",
        "gridLarge":       "sd3.5-large_25-step",
        "gridWanT2V":      "wan21-t2v_25-step",
        "gridWanI2V":      "wan21-i2v_25-step",
    }

    manifest = {}

    for grid_id, subfolder in grids.items():
        dirpath = os.path.join(base_dir, subfolder)
        if not os.path.isdir(dirpath):
            print(f"Warning: directory not found: {dirpath}")
            manifest[grid_id] = {"images": [], "videos": []}
            continue

        files = os.listdir(dirpath)
        # Collect numeric indexes (e.g. "0", "1", …)
        idx_set = set()
        for fname in files:
            name = fname.split('.', 1)[0]
            idx = name.split('_')[0]
            if idx.isdigit():
                idx_set.add(idx)
        indexes = sorted(idx_set, key=lambda x: int(x))

        images_list = []
        videos_list = []

        for idx in indexes:
            # Read prompt files
            prompt_path = os.path.join(dirpath, f"{idx}.txt")
            neg_path = os.path.join(dirpath, f"{idx}_neg.txt")
            cfg_neg_path = os.path.join(dirpath, f"{idx}_neg_cfg.txt")
            prompt = open(prompt_path, encoding="utf-8").read().strip() if os.path.isfile(prompt_path) else ""
            neg_prompt = open(neg_path, encoding="utf-8").read().strip() if os.path.isfile(neg_path) else ""
            cfg_neg_prompt = open(cfg_neg_path, encoding="utf-8").read().strip() if os.path.isfile(cfg_neg_path) else ""

            # Image sample
            img_main = next(
                (f for f in files
                 if f.startswith(idx) and not f.startswith(f"{idx}_nag")
                 and f.lower().endswith((".png", ".jpg", ".jpeg"))),
                None
            )
            img_neg = next(
                (f for f in files
                 if f.startswith(f"{idx}_nag")
                 and f.lower().endswith((".png", ".jpg", ".jpeg"))),
                None
            )
            if img_main:
                images_list.append({
                    "sample":         f"./assets/samples/{subfolder}/{img_main}",
                    "sample_nag":     f"./assets/samples/{subfolder}/{img_neg}" if img_neg else "",
                    "prompt":         prompt,
                    "negative_prompt": neg_prompt,
                    "cfg_negative_prompt": cfg_neg_prompt,
                })

            # Video sample
            vid_main = next(
                (f for f in files
                 if f.startswith(idx) and not f.startswith(f"{idx}_nag")
                 and f.lower().endswith(".mp4")),
                None
            )
            vid_neg = next(
                (f for f in files
                 if f.startswith(f"{idx}_nag")
                 and f.lower().endswith(".mp4")),
                None
            )
            if vid_main:
                videos_list.append({
                    "sample":         f"./assets/samples/{subfolder}/{vid_main}",
                    "sample_nag":     f"./assets/samples/{subfolder}/{vid_neg}" if vid_neg else "",
                    "prompt":         prompt,
                    "negative_prompt": neg_prompt,
                    "cfg_negative_prompt": cfg_neg_prompt,
                })

        manifest[grid_id] = {
            "images": images_list,
            "videos": videos_list,
        }

    # Write out the JSON manifest
    out_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "samples.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✔ Generated manifest: {out_file}")


if __name__ == '__main__':
    main()
