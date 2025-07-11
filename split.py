import os, random, shutil

SRC = "dataset/raw_images"
DST_IMG = "dataset/images"
DST_LBL = "dataset/labels"

# poměr 0.8 = 80 % train, 0.2 = 20 % val
split_ratio = {"train": 0.8, "val": 0.2}

files = [f for f in os.listdir(SRC) if f.endswith(".jpg")]
random.shuffle(files)
n_train = int(len(files) * split_ratio["train"])

for idx, fname in enumerate(files):
    split = "train" if idx < n_train else "val"
    # vytvoření složek je již hotové
    shutil.move(os.path.join(SRC, fname),
                os.path.join(DST_IMG, split, fname))
print("Hotovo: rozděleno na train/val.")
