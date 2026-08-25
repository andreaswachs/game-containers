import json, os, hashlib, zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_NAME = "Minecraft Unshare"

# Versions kept in sync with versions.env
DEPENDENCIES = {
    "minecraft": "3D Shareware v1.34",
    "fabric-loader": "0.16.5",
}

MOD_JAR = os.path.join(SCRIPT_DIR, "mods", "unshare-1.0.1.jar")
OUTPUT = os.path.join(SCRIPT_DIR, "minecraft-unshare.mrpack")

with open(IMAGE_YAML := os.path.join(SCRIPT_DIR, "image.yaml")) as f:
    VERSION_ID = next(line.split(":", 1)[1].strip() for line in f if line.startswith("tag:"))

data = open(MOD_JAR, "rb").read()
overrides_mods = os.path.join(SCRIPT_DIR, ".mrpack-work", "overrides", "mods")
os.makedirs(overrides_mods, exist_ok=True)
jar_name = os.path.basename(MOD_JAR)
with open(os.path.join(overrides_mods, jar_name), "wb") as f:
    f.write(data)

index = {
    "formatVersion": 1,
    "game": "minecraft",
    "versionId": VERSION_ID,
    "name": MOD_NAME,
    "summary": "3D Shareware v1.34 server-friendly pack with the unshare mod",
    "files": [],
    "dependencies": DEPENDENCIES,
}
index_path = os.path.join(SCRIPT_DIR, ".mrpack-work", "modrinth.index.json")
with open(index_path, "w") as f:
    json.dump(index, f, indent=2)

with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(index_path, "modrinth.index.json")
    zf.write(MOD_JAR, f"overrides/mods/{jar_name}")

print(f"Created {OUTPUT}")
print(f"Size: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
