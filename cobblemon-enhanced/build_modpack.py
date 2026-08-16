import json, os, hashlib, urllib.request, zipfile, tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

VERSIONS = {}
with open(os.path.join(SCRIPT_DIR, "versions.env")) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        VERSIONS[key.strip()] = value.strip()

with open(os.path.join(SCRIPT_DIR, "image.yaml")) as f:
    for line in f:
        if line.startswith("tag:"):
            IMAGE_VERSION = line.split(":", 1)[1].strip()
            break
USER_AGENT = f"andreaswachs/cobblemon-enhanced/{IMAGE_VERSION}"

WORK = tempfile.mkdtemp(prefix="modpack_")
MODS_DIR = os.path.join(WORK, "mods")
os.makedirs(MODS_DIR, exist_ok=True)

OVERRIDES_DIR = os.path.join(WORK, "overrides")
os.makedirs(OVERRIDES_DIR, exist_ok=True)

# Xaero's World Map defaults to M for opening the map, which shadows Cobblemon's M keybind
# (starter selection + Pokemon management). Remap to N via options.txt override.
with open(os.path.join(OVERRIDES_DIR, "options.txt"), "w") as f:
    f.write("key_gui.xaero_open_map:key.keyboard.n\n")

# All mods: (project_id, version_id, filename, url, env_client, env_server)
# env_client/server: "required", "optional", or "unsupported"
MODS = [
    # Core
    ("P7dR8mSH", "3wZtvzew", "fabric-api-0.116.8+1.21.1.jar",
     "https://cdn.modrinth.com/data/P7dR8mSH/versions/3wZtvzew/fabric-api-0.116.8%2B1.21.1.jar",
     "required", "required"),
    ("MdwFAVRL", "kF7CvxTo", "Cobblemon-fabric-1.7.3+1.21.1.jar",
     "https://cdn.modrinth.com/data/MdwFAVRL/versions/kF7CvxTo/Cobblemon-fabric-1.7.3%2B1.21.1.jar",
     "required", "required"),
    # Mega Evolution
    ("SszvX85I", "5GXFsZw0", "mega_showdown-fabric-1.9.0+1.7.3+1.21.1-hotfix-v3.jar",
     "https://cdn.modrinth.com/data/SszvX85I/versions/5GXFsZw0/mega_showdown-fabric-1.9.0%2B1.7.3%2B1.21.1-hotfix-v3.jar",
     "required", "required"),
    ("2V1Y86sc", "9DB6eyaV", "zamega-fabric-1.7.4-hotfix-hotfix.jar",
     "https://cdn.modrinth.com/data/2V1Y86sc/versions/9DB6eyaV/zamega-fabric-1.7.4-hotfix-hotfix.jar",
     "optional", "required"),
    ("ldNeqFqN", "UKP9CyH2", "mega-showdown-item-pack-1.4.2.jar",
     "https://cdn.modrinth.com/data/ldNeqFqN/versions/UKP9CyH2/mega-showdown-item-pack-1.4.2.jar",
     "optional", "required"),
    # Legendaries
    ("CaOWby9K", "eg83qtSQ", "MythsAndLegends-fabric-1.9.0.jar",
     "https://cdn.modrinth.com/data/CaOWby9K/versions/eg83qtSQ/MythsAndLegends-fabric-1.9.0.jar",
     "required", "required"),
    ("m6RyHSbV", "6nvO1cvI", "legendarymonuments-fabric-1.21.1-8.0.3.jar",
     "https://cdn.modrinth.com/data/m6RyHSbV/versions/6nvO1cvI/legendarymonuments-fabric-1.21.1-8.0.3.jar",
     "required", "required"),
    ("5EMX10qI", "ffm34Mmj", "legends-myths-3.jar",
     "https://cdn.modrinth.com/data/5EMX10qI/versions/ffm34Mmj/legends-myths-3.jar",
     "optional", "required"),
    ("qoL4kNxC", "Azf9qoT6", "complete-cobblemon-collection-myths-and-legends-compat-2.1.0.jar",
     "https://cdn.modrinth.com/data/qoL4kNxC/versions/Azf9qoT6/complete-cobblemon-collection-myths-and-legends-compat-2.1.0.jar",
     "optional", "required"),
    ("88hsodcW", "z8KI8Mom", "baby-legends-cobblemon-2.3.jar",
     "https://cdn.modrinth.com/data/88hsodcW/versions/z8KI8Mom/baby-legends-cobblemon-2.3.jar",
     "optional", "required"),
    # Gyms / Trainers
    ("lRwTUnD7", "gQx1F1dx", "rctmod-fabric-1.21.1-0.18.1-beta.jar",
     "https://cdn.modrinth.com/data/lRwTUnD7/versions/gQx1F1dx/rctmod-fabric-1.21.1-0.18.1-beta.jar",
     "required", "required"),
    ("CBfM2yw7", "9OZx0coL", "rctapi-fabric-1.21.1-0.15.2-beta.jar",
     "https://cdn.modrinth.com/data/CBfM2yw7/versions/9OZx0coL/rctapi-fabric-1.21.1-0.15.2-beta.jar",
     "optional", "optional"),
    ("eF8kqlHd", "2AR7EuiZ", "rad-gyms-fabric-0.4.4.jar",
     "https://cdn.modrinth.com/data/eF8kqlHd/versions/2AR7EuiZ/rad-gyms-fabric-0.4.4.jar",
     "required", "required"),
    ("3sLJoaQH", "mk1teRxf", "Radical Gyms & Structures - RGS.jar",
     "https://cdn.modrinth.com/data/3sLJoaQH/versions/mk1teRxf/Radical%20Gyms%20%26%20Structures%20-%20RGS.jar",
     "optional", "required"),
    ("RV1qfVQ8", "qSRKiE4D", "ExplorersCompass-1.21.1-2.6.0-fabric.jar",
     "https://cdn.modrinth.com/data/RV1qfVQ8/versions/qSRKiE4D/ExplorersCompass-1.21.1-2.6.0-fabric.jar",
     "required", "required"),
    # Navigation
    ("1bokaNcj", "Tx54V6kI", "xaerominimap-fabric-1.21.1-26.4.2.jar",
     "https://cdn.modrinth.com/data/1bokaNcj/versions/Tx54V6kI/xaerominimap-fabric-1.21.1-26.4.2.jar",
     "required", "unsupported"),
    ("NcUtCpym", "L2nO7ZYD", "xaeroworldmap-fabric-1.21.1-1.44.2.jar",
     "https://cdn.modrinth.com/data/NcUtCpym/versions/L2nO7ZYD/xaeroworldmap-fabric-1.21.1-1.44.2.jar",
     "required", "unsupported"),
    ("V7BPfphg", "izoTezRT", "compasstomapxaeros-0.1.1.jar",
     "https://cdn.modrinth.com/data/V7BPfphg/versions/izoTezRT/compasstomapxaeros-0.1.1.jar",
     "required", "required"),
    # Libraries
    ("lhGA9TYQ", "Wto0RchG", "architectury-13.0.8-fabric.jar",
     "https://cdn.modrinth.com/data/lhGA9TYQ/versions/Wto0RchG/architectury-13.0.8-fabric.jar",
     "required", "required"),
    ("jtmvUHXj", "Xlt4eWBe", "accessories-fabric-1.1.0-beta.53+1.21.1.jar",
     "https://cdn.modrinth.com/data/jtmvUHXj/versions/Xlt4eWBe/accessories-fabric-1.1.0-beta.53%2B1.21.1.jar",
     "required", "required"),
    ("ccKDOlHs", "JB1fLQnc", "owo-lib-0.12.15.4+1.21.jar",
     "https://cdn.modrinth.com/data/ccKDOlHs/versions/JB1fLQnc/owo-lib-0.12.15.4%2B1.21.jar",
     "required", "required"),
    ("XaDC71GB", "JWtSqSeY", "lithostitched-1.7.13-fabric-21.1.jar",
     "https://cdn.modrinth.com/data/XaDC71GB/versions/JWtSqSeY/lithostitched-1.7.13-fabric-21.1.jar",
     "required", "required"),
    ("BAscRYKm", "6h2mVZcb", "chipped-fabric-1.21.1-4.0.2.jar",
     "https://cdn.modrinth.com/data/BAscRYKm/versions/6h2mVZcb/chipped-fabric-1.21.1-4.0.2.jar",
     "required", "required"),
    ("ohNO6lps", "N5qzq0XV", "ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar",
     "https://cdn.modrinth.com/data/ohNO6lps/versions/N5qzq0XV/ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar",
     "optional", "optional"),
    ("G1hIVOrD", "Hf91FuVF", "resourcefullib-fabric-1.21-3.0.12.jar",
     "https://cdn.modrinth.com/data/G1hIVOrD/versions/Hf91FuVF/resourcefullib-fabric-1.21-3.0.12.jar",
     "required", "required"),
    ("b1ZV3DIJ", "JfyYsWKP", "athena-fabric-1.21.1-4.0.6.jar",
     "https://cdn.modrinth.com/data/b1ZV3DIJ/versions/JfyYsWKP/athena-fabric-1.21.1-4.0.6.jar",
     "required", "optional"),
    ("AXY1OO9m", "54k31lEX", "CobbleFurnies-fabric-1.2.jar",
     "https://cdn.modrinth.com/data/AXY1OO9m/versions/54k31lEX/CobbleFurnies-fabric-1.2.jar",
     "required", "required"),
    # Performance (server + client)
    ("gvQqBUqZ", "N08Z8wog", "lithium-fabric-0.15.4+mc1.21.1.jar",
     "https://cdn.modrinth.com/data/gvQqBUqZ/versions/N08Z8wog/lithium-fabric-0.15.4%2Bmc1.21.1.jar",
     "required", "required"),
    ("uXXizFIs", "sOzRw3CG", "ferritecore-7.0.3-fabric.jar",
     "https://cdn.modrinth.com/data/uXXizFIs/versions/sOzRw3CG/ferritecore-7.0.3-fabric.jar",
     "required", "required"),
    ("fQEb0iXm", "Acz3ttTp", "krypton-0.2.8.jar",
     "https://cdn.modrinth.com/data/fQEb0iXm/versions/Acz3ttTp/krypton-0.2.8.jar",
     "required", "required"),
    # Performance (client only)
    ("AANobbMI", "KIRFiWG4", "sodium-fabric-0.8.12+mc1.21.1.jar",
     "https://cdn.modrinth.com/data/AANobbMI/versions/KIRFiWG4/sodium-fabric-0.8.12%2Bmc1.21.1.jar",
     "required", "unsupported"),
    ("Orvt0mRa", "Z8VpxxGh", "indium-1.0.35+mc1.21.jar",
     "https://cdn.modrinth.com/data/Orvt0mRa/versions/Z8VpxxGh/indium-1.0.35%2Bmc1.21.jar",
     "required", "unsupported"),
    ("NNAgCjsB", "hsWvcyFJ", "entityculling-fabric-1.10.5-mc1.21.1.jar",
     "https://cdn.modrinth.com/data/NNAgCjsB/versions/hsWvcyFJ/entityculling-fabric-1.10.5-mc1.21.1.jar",
     "required", "unsupported"),
]

files_entry = []
for project_id, version_id, filename, url, client_side, server_side in MODS:
    print(f"Downloading {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    data = urllib.request.urlopen(req).read()
    filepath = os.path.join(MODS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    sha1 = hashlib.sha1(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    size = len(data)
    
    env = {}
    if client_side == "required":
        env["client"] = "required"
    elif client_side == "optional":
        env["client"] = "optional"
    elif client_side == "unsupported":
        env["client"] = "unsupported"
    
    if server_side == "required":
        env["server"] = "required"
    elif server_side == "optional":
        env["server"] = "optional"
    elif server_side == "unsupported":
        env["server"] = "unsupported"
    
    files_entry.append({
        "path": f"mods/{filename}",
        "hashes": {"sha1": sha1, "sha512": sha512},
        "downloads": [url],
        "fileSize": size,
        "env": env,
    })

index = {
    "formatVersion": 1,
    "game": "minecraft",
    "versionId": IMAGE_VERSION,
    "name": "Cobblemon Enhanced",
    "files": files_entry,
    "dependencies": {
        "minecraft": VERSIONS["MINECRAFT_VERSION"],
        "fabric-loader": VERSIONS["FABRIC_LOADER_VERSION"],
    },
}

with open(os.path.join(WORK, "modrinth.index.json"), "w") as f:
    json.dump(index, f, indent=2)

print(f"\nDownloaded {len(MODS)} mods")
print("Creating .mrpack...")

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cobblemon-enhanced.mrpack")
with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(WORK, "modrinth.index.json"), "modrinth.index.json")
    for filename in os.listdir(MODS_DIR):
        filepath = os.path.join(MODS_DIR, filename)
        zf.write(filepath, f"mods/{filename}")
    for root, _, files in os.walk(OVERRIDES_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            arcname = os.path.relpath(fpath, WORK)
            zf.write(fpath, arcname)

print(f"Created {output_path}")
print(f"Size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
