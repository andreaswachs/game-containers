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
USER_AGENT = f"andreaswachs/dungeons-like/{IMAGE_VERSION}"

WORK = tempfile.mkdtemp(prefix="modpack_")
MODS_DIR = os.path.join(WORK, "mods")
os.makedirs(MODS_DIR, exist_ok=True)

OVERRIDES_DIR = os.path.join(WORK, "overrides")
os.makedirs(OVERRIDES_DIR, exist_ok=True)

# All mods: (project_id, version_id, filename, url, env_client, env_server)
# env_client/server: "required", "optional", or "unsupported"
MODS = [
    # === Core Dungeons Mods (server + client) ===
    ("R0ToJjk1", VERSIONS["DUNGEONS_CONTENT_MODRINTH_ID"], "dungeons_1.19_mc1.20.1.jar",
     "https://cdn.modrinth.com/data/R0ToJjk1/versions/" + VERSIONS["DUNGEONS_CONTENT_MODRINTH_ID"] + "/dungeons_1.19_mc1.20.1.jar",
     "required", "required"),
    ("dVxU9eTq", VERSIONS["DUNGEONS_CONTENT_TWO_MODRINTH_ID"], "dungeons_content_two-1.0.2-alpha-forge-1.20.1.jar",
     "https://cdn.modrinth.com/data/dVxU9eTq/versions/" + VERSIONS["DUNGEONS_CONTENT_TWO_MODRINTH_ID"] + "/dungeons_content_two-1.0.2-alpha-forge-1.20.1.jar",
     "required", "required"),
    ("46KJle7n", VERSIONS["L_ENDERS_CATACLYSM_MODRINTH_ID"], "L_Enders_Cataclysm-3.31.jar",
     "https://cdn.modrinth.com/data/46KJle7n/versions/" + VERSIONS["L_ENDERS_CATACLYSM_MODRINTH_ID"] + "/L_Enders_Cataclysm-3.31.jar",
     "required", "required"),
    ("SwDIbBHh", VERSIONS["ENCHANTWITHMOB_MODRINTH_ID"], "enchantwithmob-1.20.1-11.17.1.jar",
     "https://cdn.modrinth.com/data/SwDIbBHh/versions/" + VERSIONS["ENCHANTWITHMOB_MODRINTH_ID"] + "/enchantwithmob-1.20.1-11.17.1.jar",
     "required", "required"),
    ("4ZVIxU8x", VERSIONS["GOETY_MODRINTH_ID"], "goety-2.5.57.3.jar",
     "https://cdn.modrinth.com/data/4ZVIxU8x/versions/" + VERSIONS["GOETY_MODRINTH_ID"] + "/goety-2.5.57.3.jar",
     "required", "required"),
    ("pBrtNB24", VERSIONS["ECHOVOIDS_MODRINTH_ID"], "echovoids-2.0.3b-forge-1.20.1.jar",
     "https://cdn.modrinth.com/data/pBrtNB24/versions/" + VERSIONS["ECHOVOIDS_MODRINTH_ID"] + "/echovoids-2.0.3b-forge-1.20.1.jar",
     "required", "required"),
    ("T21szC0a", VERSIONS["VALHELSIA_STRUCTURES_MODRINTH_ID"], "valhelsia_structures-forge-1.20.1-1.1.2.jar",
     "https://cdn.modrinth.com/data/T21szC0a/versions/" + VERSIONS["VALHELSIA_STRUCTURES_MODRINTH_ID"] + "/valhelsia_structures-forge-1.20.1-1.1.2.jar",
     "required", "required"),
    ("kLoMCc4b", VERSIONS["ILLAGE_SPILLAGE_MODRINTH_ID"], "illageandspillagerespillaged-1.2.8.jar",
     "https://cdn.modrinth.com/data/kLoMCc4b/versions/" + VERSIONS["ILLAGE_SPILLAGE_MODRINTH_ID"] + "/illageandspillagerespillaged-1.2.8.jar",
     "required", "required"),
    ("Ivn6yJvS", VERSIONS["ARTHYS_RPG_ARMS_MODRINTH_ID"], "arthys_rpg_arms-2.1.4-forge-1.20.1.jar",
     "https://cdn.modrinth.com/data/Ivn6yJvS/versions/" + VERSIONS["ARTHYS_RPG_ARMS_MODRINTH_ID"] + "/arthys_rpg_arms-2.1.4-forge-1.20.1.jar",
     "required", "required"),
    ("tpehi7ww", VERSIONS["DUNGEONS_AND_TAVERNS_MODRINTH_ID"], "dungeons-and-taverns-3.0.3.f.jar",
     "https://cdn.modrinth.com/data/tpehi7ww/versions/" + VERSIONS["DUNGEONS_AND_TAVERNS_MODRINTH_ID"] + "/dungeons-and-taverns-3.0.3.f.jar",
     "optional", "required"),
    # === Combat Mods ===
    ("5sy6g3kz", VERSIONS["BETTER_COMBAT_MODRINTH_ID"], "bettercombat-forge-1.9.0+1.20.1.jar",
     "https://cdn.modrinth.com/data/5sy6g3kz/versions/" + VERSIONS["BETTER_COMBAT_MODRINTH_ID"] + "/bettercombat-forge-1.9.0%2B1.20.1.jar",
     "required", "required"),
    ("wGKYL7st", VERSIONS["COMBAT_ROLL_MODRINTH_ID"], "combatroll-forge-1.3.3+1.20.1.jar",
     "https://cdn.modrinth.com/data/wGKYL7st/versions/" + VERSIONS["COMBAT_ROLL_MODRINTH_ID"] + "/combatroll-forge-1.3.3%2B1.20.1.jar",
     "required", "required"),
    ("A0W9tMly", VERSIONS["AITK_MODRINTH_ID"], "aitk-1.2.1-forge+1.20.1.jar",
     "https://cdn.modrinth.com/data/A0W9tMly/versions/" + VERSIONS["AITK_MODRINTH_ID"] + "/aitk-1.2.1-forge%2B1.20.1.jar",
     "required", "required"),
    # === Visual / QoL (client-side) ===
    ("4q8UOK1d", VERSIONS["SUBTLE_EFFECTS_MODRINTH_ID"], "SubtleEffects-forge-1.20.1-1.14.3.jar",
     "https://cdn.modrinth.com/data/4q8UOK1d/versions/" + VERSIONS["SUBTLE_EFFECTS_MODRINTH_ID"] + "/SubtleEffects-forge-1.20.1-1.14.3.jar",
     "required", "optional"),
    ("tTKSJOdG", VERSIONS["IMMERSIVE_DAMAGE_INDICATORS_MODRINTH_ID"], "immersivedamageindicators-forge-1.0.0-1.20.1.jar",
     "https://cdn.modrinth.com/data/tTKSJOdG/versions/" + VERSIONS["IMMERSIVE_DAMAGE_INDICATORS_MODRINTH_ID"] + "/immersivedamageindicators-forge-1.0.0-1.20.1.jar",
     "required", "unsupported"),
    ("P8STLvzB", VERSIONS["PERCEPTION_MODRINTH_ID"], "Perception-FORGE-0.1.4+1.20.1.jar",
     "https://cdn.modrinth.com/data/P8STLvzB/versions/" + VERSIONS["PERCEPTION_MODRINTH_ID"] + "/Perception-FORGE-0.1.4%2B1.20.1.jar",
     "required", "unsupported"),
    ("z6d6n7ve", VERSIONS["ACCESSIBLE_STEP_MODRINTH_ID"], "accessible-step-forge-mc1.20.1-2.1.1+1.20.1.jar",
     "https://cdn.modrinth.com/data/z6d6n7ve/versions/" + VERSIONS["ACCESSIBLE_STEP_MODRINTH_ID"] + "/accessible-step-forge-mc1.20.1-2.1.1%2B1.20.1.jar",
     "required", "unsupported"),
    ("lq1wGfHO", VERSIONS["MOBEFFECTSVFX_MODRINTH_ID"], "mob_effects_vfx-0.8.jar",
     "https://cdn.modrinth.com/data/lq1wGfHO/versions/" + VERSIONS["MOBEFFECTSVFX_MODRINTH_ID"] + "/mob_effects_vfx-0.8.jar",
     "required", "unsupported"),
    ("atHH8NyV", VERSIONS["LEGENDARY_TOOLTIPS_MODRINTH_ID"], "LegendaryTooltips-1.20.1-forge-1.4.5.jar",
     "https://cdn.modrinth.com/data/atHH8NyV/versions/" + VERSIONS["LEGENDARY_TOOLTIPS_MODRINTH_ID"] + "/LegendaryTooltips-1.20.1-forge-1.4.5.jar",
     "required", "unsupported"),
    ("CYSUVOdj", VERSIONS["EQUIPMENT_COMPARE_MODRINTH_ID"], "EquipmentCompare-1.20.1-forge-1.3.7.jar",
     "https://cdn.modrinth.com/data/CYSUVOdj/versions/" + VERSIONS["EQUIPMENT_COMPARE_MODRINTH_ID"] + "/EquipmentCompare-1.20.1-forge-1.3.7.jar",
     "required", "unsupported"),
    ("r0camchr", VERSIONS["EXPLOSIVE_ENHANCEMENT_MODRINTH_ID"], "explosiveenhancement-forge-1.20.1-1.1.0-client.jar",
     "https://cdn.modrinth.com/data/r0camchr/versions/" + VERSIONS["EXPLOSIVE_ENHANCEMENT_MODRINTH_ID"] + "/explosiveenhancement-forge-1.20.1-1.1.0-client.jar",
     "required", "unsupported"),
     ("Xy8aRQKS", VERSIONS["PHYSICS_MOD_MODRINTH_ID"], "physics-mod-3.0.20-mc-1.20.1-forge.jar",
     "https://cdn.modrinth.com/data/Xy8aRQKS/versions/" + VERSIONS["PHYSICS_MOD_MODRINTH_ID"] + "/physics-mod-3.0.20-mc-1.20.1-forge.jar",
     "required", "unsupported"),
    # === Performance (server + client) ===
    ("nmDcB62a", VERSIONS["MODERNFIX_MODRINTH_ID"], "modernfix-forge-5.27.79+mc1.20.1.jar",
     "https://cdn.modrinth.com/data/nmDcB62a/versions/" + VERSIONS["MODERNFIX_MODRINTH_ID"] + "/modernfix-forge-5.27.79%2Bmc1.20.1.jar",
     "optional", "optional"),
    ("uXXizFIs", VERSIONS["FERRITECORE_MODRINTH_ID"], "ferritecore-6.0.1-forge.jar",
     "https://cdn.modrinth.com/data/uXXizFIs/versions/" + VERSIONS["FERRITECORE_MODRINTH_ID"] + "/ferritecore-6.0.1-forge.jar",
     "optional", "optional"),
    ("qa2H4BS9", VERSIONS["CANARY_MODRINTH_ID"], "canary-mc1.20.1-0.3.3.jar",
     "https://cdn.modrinth.com/data/qa2H4BS9/versions/" + VERSIONS["CANARY_MODRINTH_ID"] + "/canary-mc1.20.1-0.3.3.jar",
     "optional", "optional"),
    # === Performance (client only) ===
    ("sk9rgfiA", VERSIONS["EMBEDDIUM_MODRINTH_ID"], "embeddium-0.3.31+mc1.20.1.jar",
     "https://cdn.modrinth.com/data/sk9rgfiA/versions/" + VERSIONS["EMBEDDIUM_MODRINTH_ID"] + "/embeddium-0.3.31%2Bmc1.20.1.jar",
     "required", "unsupported"),
    ("GchcoXML", VERSIONS["OCULUS_MODRINTH_ID"], "oculus-mc1.20.1-1.8.0.jar",
     "https://cdn.modrinth.com/data/GchcoXML/versions/" + VERSIONS["OCULUS_MODRINTH_ID"] + "/oculus-mc1.20.1-1.8.0.jar",
     "optional", "unsupported"),
    ("NNAgCjsB", VERSIONS["ENTITY_CULLING_MODRINTH_ID"], "entityculling-forge-1.10.5-mc1.20.1.jar",
     "https://cdn.modrinth.com/data/NNAgCjsB/versions/" + VERSIONS["ENTITY_CULLING_MODRINTH_ID"] + "/entityculling-forge-1.10.5-mc1.20.1.jar",
     "required", "unsupported"),
    # === Server-side Dependencies ===
    ("8BmcQJ2H", VERSIONS["GECKOLIB_MODRINTH_ID"], "geckolib-forge-1.20.1-4.8.4.jar",
     "https://cdn.modrinth.com/data/8BmcQJ2H/versions/" + VERSIONS["GECKOLIB_MODRINTH_ID"] + "/geckolib-forge-1.20.1-4.8.4.jar",
     "required", "required"),
    ("tPe4xnPd", VERSIONS["FORMATIONS_MODRINTH_ID"], "formations-1.0.4-forge-mc1.20.2.jar",
     "https://cdn.modrinth.com/data/tPe4xnPd/versions/" + VERSIONS["FORMATIONS_MODRINTH_ID"] + "/formations-1.0.4-forge-mc1.20.2.jar",
     "unsupported", "required"),
    ("vvuO3ImH", VERSIONS["CURIOS_MODRINTH_ID"], "curios-forge-5.14.1+1.20.1.jar",
     "https://cdn.modrinth.com/data/vvuO3ImH/versions/" + VERSIONS["CURIOS_MODRINTH_ID"] + "/curios-forge-5.14.1%2B1.20.1.jar",
     "required", "required"),
    ("FoVacERa", VERSIONS["LIONFISH_API_MODRINTH_ID"], "lionfishapi-3.0.jar",
     "https://cdn.modrinth.com/data/FoVacERa/versions/" + VERSIONS["LIONFISH_API_MODRINTH_ID"] + "/lionfishapi-3.0.jar",
     "required", "required"),
    ("95nSN4Rd", VERSIONS["BAGUS_LIB_MODRINTH_ID"], "bagus_lib-1.20.1-5.6.1.jar",
     "https://cdn.modrinth.com/data/95nSN4Rd/versions/" + VERSIONS["BAGUS_LIB_MODRINTH_ID"] + "/bagus_lib-1.20.1-5.6.1.jar",
     "required", "required"),
    ("nU0bVIaL", VERSIONS["PATCHOULI_MODRINTH_ID"], "Patchouli-1.20.1-85-FORGE.jar",
     "https://cdn.modrinth.com/data/nU0bVIaL/versions/" + VERSIONS["PATCHOULI_MODRINTH_ID"] + "/Patchouli-1.20.1-85-FORGE.jar",
     "required", "required"),
    ("HsdNFinx", VERSIONS["VALHELSIA_CORE_MODRINTH_ID"], "valhelsia_core-forge-1.20.1-1.1.2.jar",
     "https://cdn.modrinth.com/data/HsdNFinx/versions/" + VERSIONS["VALHELSIA_CORE_MODRINTH_ID"] + "/valhelsia_core-forge-1.20.1-1.1.2.jar",
     "required", "required"),
    ("gedNE4y2", VERSIONS["PLAYER_ANIMATOR_MODRINTH_ID"], "player-animation-lib-forge-1.0.2-rc1+1.20.jar",
     "https://cdn.modrinth.com/data/gedNE4y2/versions/" + VERSIONS["PLAYER_ANIMATOR_MODRINTH_ID"] + "/player-animation-lib-forge-1.0.2-rc1%2B1.20.jar",
     "required", "required"),
    ("9s6osm5g", VERSIONS["CLOTH_CONFIG_MODRINTH_ID"], "cloth-config-11.1.136-forge.jar",
     "https://cdn.modrinth.com/data/9s6osm5g/versions/" + VERSIONS["CLOTH_CONFIG_MODRINTH_ID"] + "/cloth-config-11.1.136-forge.jar",
     "required", "required"),
    ("hYykXjDp", VERSIONS["FZZY_CONFIG_MODRINTH_ID"], "fzzy_config-0.7.6+1.20.1+forge.jar",
     "https://cdn.modrinth.com/data/hYykXjDp/versions/" + VERSIONS["FZZY_CONFIG_MODRINTH_ID"] + "/fzzy_config-0.7.6%2B1.20.1%2Bforge.jar",
     "required", "required"),
    ("ordsPcFz", VERSIONS["KOTLIN_FOR_FORGE_MODRINTH_ID"], "kotlinforforge-4.12.0-all.jar",
     "https://cdn.modrinth.com/data/ordsPcFz/versions/" + VERSIONS["KOTLIN_FOR_FORGE_MODRINTH_ID"] + "/kotlinforforge-4.12.0-all.jar",
     "required", "required"),
    # === Client-side Dependencies ===
    ("5faXoLqX", VERSIONS["ICEBERG_MODRINTH_ID"], "Iceberg-1.20.1-forge-1.1.25.jar",
     "https://cdn.modrinth.com/data/5faXoLqX/versions/" + VERSIONS["ICEBERG_MODRINTH_ID"] + "/Iceberg-1.20.1-forge-1.1.25.jar",
     "required", "unsupported"),
    ("1OE8wbN0", VERSIONS["PRISM_MODRINTH_ID"], "Prism-1.20.1-forge-1.0.5.jar",
     "https://cdn.modrinth.com/data/1OE8wbN0/versions/" + VERSIONS["PRISM_MODRINTH_ID"] + "/Prism-1.20.1-forge-1.0.5.jar",
     "required", "unsupported"),
    ("6xvrmbjn", VERSIONS["IMMERSIVE_MESSAGES_API_MODRINTH_ID"], "immersivemessages-forge-1.0.18-1.20.1.jar",
     "https://cdn.modrinth.com/data/6xvrmbjn/versions/" + VERSIONS["IMMERSIVE_MESSAGES_API_MODRINTH_ID"] + "/immersivemessages-forge-1.0.18-1.20.1.jar",
     "required", "required"),
    ("vBbPDuOs", VERSIONS["TXNILIB_MODRINTH_ID"], "txnilib-forge-1.0.24-1.20.1.jar",
     "https://cdn.modrinth.com/data/vBbPDuOs/versions/" + VERSIONS["TXNILIB_MODRINTH_ID"] + "/txnilib-forge-1.0.24-1.20.1.jar",
     "required", "required"),
    ("lhGA9TYQ", VERSIONS["ARCHITECTURY_API_MODRINTH_ID"], "architectury-9.2.14-forge.jar",
     "https://cdn.modrinth.com/data/lhGA9TYQ/versions/" + VERSIONS["ARCHITECTURY_API_MODRINTH_ID"] + "/architectury-9.2.14-forge.jar",
     "required", "required"),
    ("RH2KUdKJ", VERSIONS["OCTOLIB_MODRINTH_ID"], "OctoLib-FORGE-0.5.0.1+1.20.1.jar",
     "https://cdn.modrinth.com/data/RH2KUdKJ/versions/" + VERSIONS["OCTOLIB_MODRINTH_ID"] + "/OctoLib-FORGE-0.5.0.1%2B1.20.1.jar",
     "required", "required"),
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
    if client_side in ("required", "optional", "unsupported"):
        env["client"] = client_side
    if server_side in ("required", "optional", "unsupported"):
        env["server"] = server_side

    files_entry.append({
        "path": f"mods/{filename}",
        "hashes": {"sha1": sha1, "sha512": sha512},
        "downloads": [url],
        "fileSize": size,
        "env": env,
    })

# Download resource packs into overrides/resourcepacks
RESOURCE_PACKS = [
    ("AZaZTrT0", VERSIONS["DUNGEONS_STYLE_MODRINTH_ID"], "Dungeons-Style-1.20.1-0.5.1.zip",
     "https://cdn.modrinth.com/data/AZaZTrT0/versions/" + VERSIONS["DUNGEONS_STYLE_MODRINTH_ID"] + "/Dungeons-Style-1.20.1-0.5.1.zip"),
    ("slufHzC2", VERSIONS["FRESH_MOVES_MODRINTH_ID"], "Fresh-Moves-v3.1.zip",
     "https://cdn.modrinth.com/data/slufHzC2/versions/" + VERSIONS["FRESH_MOVES_MODRINTH_ID"] + "/-1.21.2%20Fresh%20Moves%20v3.1%20%28With%20Animated%20Eyes%29.zip"),
]

OVERRIDES_RP_DIR = os.path.join(OVERRIDES_DIR, "resourcepacks")
os.makedirs(OVERRIDES_RP_DIR, exist_ok=True)

for project_id, version_id, filename, url in RESOURCE_PACKS:
    print(f"Downloading resource pack {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    data = urllib.request.urlopen(req).read()
    filepath = os.path.join(OVERRIDES_RP_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    sha1 = hashlib.sha1(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    size = len(data)

    files_entry.append({
        "path": f"overrides/resourcepacks/{filename}",
        "hashes": {"sha1": sha1, "sha512": sha512},
        "downloads": [url],
        "fileSize": size,
        "env": {"client": "optional", "server": "unsupported"},
    })

# Download shader into overrides/shaderpacks
SHADERS = [
    ("kmwfVOoi", VERSIONS["RETHINKING_VOXELS_MODRINTH_ID"], "rethinking-voxels_r0.1-beta9.zip",
     "https://cdn.modrinth.com/data/kmwfVOoi/versions/" + VERSIONS["RETHINKING_VOXELS_MODRINTH_ID"] + "/rethinking-voxels_r0.1-beta9.zip"),
]

OVERRIDES_SP_DIR = os.path.join(OVERRIDES_DIR, "shaderpacks")
os.makedirs(OVERRIDES_SP_DIR, exist_ok=True)

for project_id, version_id, filename, url in SHADERS:
    print(f"Downloading shader {filename}...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    data = urllib.request.urlopen(req).read()
    filepath = os.path.join(OVERRIDES_SP_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(data)
    sha1 = hashlib.sha1(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()
    size = len(data)

    files_entry.append({
        "path": f"overrides/shaderpacks/{filename}",
        "hashes": {"sha1": sha1, "sha512": sha512},
        "downloads": [url],
        "fileSize": size,
        "env": {"client": "optional", "server": "unsupported"},
    })

index = {
    "formatVersion": 1,
    "game": "minecraft",
    "versionId": IMAGE_VERSION,
    "name": "Dungeons-like",
    "files": files_entry,
    "dependencies": {
        "minecraft": VERSIONS["MINECRAFT_VERSION"],
        "forge": VERSIONS["FORGE_VERSION"],
    },
}

with open(os.path.join(WORK, "modrinth.index.json"), "w") as f:
    json.dump(index, f, indent=2)

print(f"\nDownloaded {len(MODS)} mods + {len(RESOURCE_PACKS)} resource packs + {len(SHADERS)} shaders")
print("Creating .mrpack...")

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dungeons-like.mrpack")
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
