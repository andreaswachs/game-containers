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

IMAGE_VERSION = VERSIONS["IMAGE_VERSION"]
USER_AGENT = f"andreaswachs/minecraft-enhanced/{IMAGE_VERSION}"

WORK = tempfile.mkdtemp(prefix="modpack_")
MODS_DIR = os.path.join(WORK, "mods")
os.makedirs(MODS_DIR, exist_ok=True)

OVERRIDES_DIR = os.path.join(WORK, "overrides")
os.makedirs(OVERRIDES_DIR, exist_ok=True)

# All mods: (project_id, version_id, filename, url, env_client, env_server)
# env_client/server: "required", "optional", or "unsupported"
MODS = [
    # Core
    ("P7dR8mSH", VERSIONS["FABRIC_API_MODRINTH_ID"], "fabric-api-0.115.6+1.21.1.jar",
     "https://cdn.modrinth.com/data/P7dR8mSH/versions/" + VERSIONS["FABRIC_API_MODRINTH_ID"] + "/fabric-api-0.115.6%2B1.21.1.jar",
     "required", "required"),
    # Weapons
    ("bK3Ubu9p", VERSIONS["SIMPLY_SWORDS_MODRINTH_ID"], "simplyswords-fabric-1.63.0-1.21.1.jar",
     "https://cdn.modrinth.com/data/bK3Ubu9p/versions/" + VERSIONS["SIMPLY_SWORDS_MODRINTH_ID"] + "/simplyswords-fabric-1.63.0-1.21.1.jar",
     "required", "required"),
    ("5sy6g3kz", VERSIONS["BETTER_COMBAT_MODRINTH_ID"], "bettercombat-fabric-2.4.0+1.21.1.jar",
     "https://cdn.modrinth.com/data/5sy6g3kz/versions/" + VERSIONS["BETTER_COMBAT_MODRINTH_ID"] + "/bettercombat-fabric-2.4.0%2B1.21.1.jar",
     "required", "required"),
    # Magic
    ("XvoWJaA2", VERSIONS["SPELL_ENGINE_MODRINTH_ID"], "spell_engine-fabric-1.9.16+1.21.1.jar",
     "https://cdn.modrinth.com/data/XvoWJaA2/versions/" + VERSIONS["SPELL_ENGINE_MODRINTH_ID"] + "/spell_engine-fabric-1.9.16%2B1.21.1.jar",
     "required", "required"),
    ("8ooWzSQP", VERSIONS["SPELL_POWER_MODRINTH_ID"], "spell_power-fabric-1.6.0+1.21.1.jar",
     "https://cdn.modrinth.com/data/8ooWzSQP/versions/" + VERSIONS["SPELL_POWER_MODRINTH_ID"] + "/spell_power-fabric-1.6.0%2B1.21.1.jar",
     "required", "required"),
    ("NkGaQMDA", VERSIONS["WIZARDS_MODRINTH_ID"], "wizards-fabric-3.0.4+1.21.1.jar",
     "https://cdn.modrinth.com/data/NkGaQMDA/versions/" + VERSIONS["WIZARDS_MODRINTH_ID"] + "/wizards-fabric-3.0.4%2B1.21.1.jar",
     "required", "required"),
    ("FxXkHaLe", VERSIONS["PALADINS_MODRINTH_ID"], "paladins-fabric-3.0.5+1.21.1.jar",
     "https://cdn.modrinth.com/data/FxXkHaLe/versions/" + VERSIONS["PALADINS_MODRINTH_ID"] + "/paladins-fabric-3.0.5%2B1.21.1.jar",
     "required", "required"),
    # Equipment & Accessories
    ("5aaWibi9", VERSIONS["TRINKETS_MODRINTH_ID"], "trinkets-3.10.0.jar",
     "https://cdn.modrinth.com/data/5aaWibi9/versions/" + VERSIONS["TRINKETS_MODRINTH_ID"] + "/trinkets-3.10.0.jar",
     "required", "required"),
    ("mSQF1NpT", VERSIONS["ELYTRA_SLOT_MODRINTH_ID"], "elytraslot-fabric-9.0.1+1.21.1.jar",
     "https://cdn.modrinth.com/data/mSQF1NpT/versions/" + VERSIONS["ELYTRA_SLOT_MODRINTH_ID"] + "/elytraslot-fabric-9.0.1%2B1.21.1.jar",
     "required", "required"),
    ("b5GyyYkp", VERSIONS["CHARM_OF_UNDYING_MODRINTH_ID"], "charmofundying-fabric-9.1.0+1.21.1.jar",
     "https://cdn.modrinth.com/data/b5GyyYkp/versions/" + VERSIONS["CHARM_OF_UNDYING_MODRINTH_ID"] + "/charmofundying-fabric-9.1.0%2B1.21.1.jar",
     "required", "required"),
    ("rlloIFEV", VERSIONS["TRAVELERS_BACKPACK_MODRINTH_ID"], "travelersbackpack-fabric-1.21.1-10.1.38.jar",
     "https://cdn.modrinth.com/data/rlloIFEV/versions/" + VERSIONS["TRAVELERS_BACKPACK_MODRINTH_ID"] + "/travelersbackpack-fabric-1.21.1-10.1.38.jar",
     "required", "required"),
    ("eE2Db4YU", VERSIONS["IMMERSIVE_ARMORS_MODRINTH_ID"], "immersive_armors-1.7.6+1.21.1-fabric.jar",
     "https://cdn.modrinth.com/data/eE2Db4YU/versions/" + VERSIONS["IMMERSIVE_ARMORS_MODRINTH_ID"] + "/immersive_armors-1.7.6%2B1.21.1-fabric.jar",
     "required", "required"),
    # Quality of Life
    ("OhduvhIc", VERSIONS["VEINMINER_MODRINTH_ID"], "veinminer-fabric-2.11.2+1.21.1.jar",
     "https://cdn.modrinth.com/data/OhduvhIc/versions/" + VERSIONS["VEINMINER_MODRINTH_ID"] + "/veinminer-fabric-2.11.2%2B1.21.1.jar",
     "optional", "required"),
    ("ePv85y52", VERSIONS["ENCHANTING_INFUSER_MODRINTH_ID"], "EnchantingInfuser-v21.1.4-1.21.1-Fabric.jar",
     "https://cdn.modrinth.com/data/ePv85y52/versions/" + VERSIONS["ENCHANTING_INFUSER_MODRINTH_ID"] + "/EnchantingInfuser-v21.1.4-1.21.1-Fabric.jar",
     "required", "required"),
    ("OZBR5JT5", VERSIONS["EASY_ANVILS_MODRINTH_ID"], "EasyAnvils-v21.1.0-1.21.1-Fabric.jar",
     "https://cdn.modrinth.com/data/OZBR5JT5/versions/" + VERSIONS["EASY_ANVILS_MODRINTH_ID"] + "/EasyAnvils-v21.1.0-1.21.1-Fabric.jar",
     "required", "required"),
    # World & Adventure
    ("8oi3bsk5", VERSIONS["TERRALITH_MODRINTH_ID"], "Terralith_1.21.x_v2.6.2.jar",
     "https://cdn.modrinth.com/data/8oi3bsk5/versions/" + VERSIONS["TERRALITH_MODRINTH_ID"] + "/Terralith_1.21.x_v2.6.2.jar",
     "optional", "required"),
    ("tpehi7ww", VERSIONS["DUNGEONS_AND_TAVERNS_MODRINTH_ID"], "dungeons-and-taverns-v4.4.4.jar",
     "https://cdn.modrinth.com/data/tpehi7ww/versions/" + VERSIONS["DUNGEONS_AND_TAVERNS_MODRINTH_ID"] + "/dungeons-and-taverns-v4.4.4.jar",
     "optional", "required"),
    ("8DfbfASn", VERSIONS["WHEN_DUNGEONS_ARISE_MODRINTH_ID"], "DungeonsArise-1.21.1-2.1.68-fabric-release.jar",
     "https://cdn.modrinth.com/data/8DfbfASn/versions/" + VERSIONS["WHEN_DUNGEONS_ARISE_MODRINTH_ID"] + "/DungeonsArise-1.21.1-2.1.68-fabric-release.jar",
     "unsupported", "required"),
    # Navigation
    ("fPetb5Kh", VERSIONS["NATURES_COMPASS_MODRINTH_ID"], "NaturesCompass-1.21.1-2.6.0-fabric.jar",
     "https://cdn.modrinth.com/data/fPetb5Kh/versions/" + VERSIONS["NATURES_COMPASS_MODRINTH_ID"] + "/NaturesCompass-1.21.1-2.6.0-fabric.jar",
     "required", "required"),
    ("RV1qfVQ8", VERSIONS["EXPLORERS_COMPASS_MODRINTH_ID"], "ExplorersCompass-1.21.1-2.6.0-fabric.jar",
     "https://cdn.modrinth.com/data/RV1qfVQ8/versions/" + VERSIONS["EXPLORERS_COMPASS_MODRINTH_ID"] + "/ExplorersCompass-1.21.1-2.6.0-fabric.jar",
     "required", "required"),
    ("LOpKHB2A", VERSIONS["WAYSTONES_MODRINTH_ID"], "waystones-fabric-1.21.1-21.1.41.jar",
     "https://cdn.modrinth.com/data/LOpKHB2A/versions/" + VERSIONS["WAYSTONES_MODRINTH_ID"] + "/waystones-fabric-1.21.1-21.1.41.jar",
     "required", "required"),
    ("1bokaNcj", VERSIONS["XAEROS_MINIMAP_MODRINTH_ID"], "xaerominimap-fabric-1.21.1-26.4.2.jar",
     "https://cdn.modrinth.com/data/1bokaNcj/versions/" + VERSIONS["XAEROS_MINIMAP_MODRINTH_ID"] + "/xaerominimap-fabric-1.21.1-26.4.2.jar",
     "required", "optional"),
    ("NcUtCpym", VERSIONS["XAEROS_WORLD_MAP_MODRINTH_ID"], "xaeroworldmap-fabric-1.21.1-1.44.2.jar",
     "https://cdn.modrinth.com/data/NcUtCpym/versions/" + VERSIONS["XAEROS_WORLD_MAP_MODRINTH_ID"] + "/xaeroworldmap-fabric-1.21.1-1.44.2.jar",
     "required", "optional"),
    # Visual & Fun
    ("yBW8D80W", VERSIONS["LAMBDYNAMICLIGHTS_MODRINTH_ID"], "lambdynamiclights-4.8.10+1.21.1.jar",
     "https://cdn.modrinth.com/data/yBW8D80W/versions/" + VERSIONS["LAMBDYNAMICLIGHTS_MODRINTH_ID"] + "/lambdynamiclights-4.8.10%2B1.21.1.jar",
     "required", "unsupported"),
    ("hZ4lZ6jX", VERSIONS["DANCERIZER_MODRINTH_ID"], "dancerizer-1.4.1.jar",
     "https://cdn.modrinth.com/data/hZ4lZ6jX/versions/" + VERSIONS["DANCERIZER_MODRINTH_ID"] + "/dancerizer-1.4.1.jar",
     "required", "required"),
    # Building
    ("BAscRYKm", VERSIONS["CHIPPED_MODRINTH_ID"], "chipped-fabric-1.21.1-4.0.2.jar",
     "https://cdn.modrinth.com/data/BAscRYKm/versions/" + VERSIONS["CHIPPED_MODRINTH_ID"] + "/chipped-fabric-1.21.1-4.0.2.jar",
     "required", "required"),
    ("kNxa8z3e", VERSIONS["MACAWS_DOORS_MODRINTH_ID"], "mcw-doors-1.1.5-mc1.21.1fabric.jar",
     "https://cdn.modrinth.com/data/kNxa8z3e/versions/" + VERSIONS["MACAWS_DOORS_MODRINTH_ID"] + "/mcw-doors-1.1.5-mc1.21.1fabric.jar",
     "required", "required"),
    ("GURcjz8O", VERSIONS["MACAWS_BRIDGES_MODRINTH_ID"], "mcw-bridges-3.1.2-mc1.21.1fabric.jar",
     "https://cdn.modrinth.com/data/GURcjz8O/versions/" + VERSIONS["MACAWS_BRIDGES_MODRINTH_ID"] + "/mcw-bridges-3.1.2-mc1.21.1fabric.jar",
     "required", "required"),
    # Performance (server + client)
    ("gvQqBUqZ", VERSIONS["LITHIUM_MODRINTH_ID"], "lithium-fabric-0.15.4+mc1.21.1.jar",
     "https://cdn.modrinth.com/data/gvQqBUqZ/versions/" + VERSIONS["LITHIUM_MODRINTH_ID"] + "/lithium-fabric-0.15.4%2Bmc1.21.1.jar",
     "required", "required"),
    ("uXXizFIs", VERSIONS["FERRITECORE_MODRINTH_ID"], "ferritecore-7.0.3-fabric.jar",
     "https://cdn.modrinth.com/data/uXXizFIs/versions/" + VERSIONS["FERRITECORE_MODRINTH_ID"] + "/ferritecore-7.0.3-fabric.jar",
     "required", "required"),
    ("fQEb0iXm", VERSIONS["KRYPTON_MODRINTH_ID"], "krypton-0.2.8.jar",
     "https://cdn.modrinth.com/data/fQEb0iXm/versions/" + VERSIONS["KRYPTON_MODRINTH_ID"] + "/krypton-0.2.8.jar",
     "required", "required"),
    # Performance (client only)
    ("AANobbMI", VERSIONS["SODIUM_MODRINTH_ID"], "sodium-fabric-0.8.12+mc1.21.1.jar",
     "https://cdn.modrinth.com/data/AANobbMI/versions/" + VERSIONS["SODIUM_MODRINTH_ID"] + "/sodium-fabric-0.8.12%2Bmc1.21.1.jar",
     "required", "unsupported"),
    ("Orvt0mRa", VERSIONS["INDIUM_MODRINTH_ID"], "indium-1.0.35+mc1.21.jar",
     "https://cdn.modrinth.com/data/Orvt0mRa/versions/" + VERSIONS["INDIUM_MODRINTH_ID"] + "/indium-1.0.35%2Bmc1.21.jar",
     "required", "unsupported"),
    ("NNAgCjsB", VERSIONS["ENTITY_CULLING_MODRINTH_ID"], "entityculling-fabric-1.10.5-mc1.21.1.jar",
     "https://cdn.modrinth.com/data/NNAgCjsB/versions/" + VERSIONS["ENTITY_CULLING_MODRINTH_ID"] + "/entityculling-fabric-1.10.5-mc1.21.1.jar",
     "required", "unsupported"),
    # Libraries
    ("XaDC71GB", VERSIONS["LITHOSTITCHED_MODRINTH_ID"], "lithostitched-1.7.13-fabric-21.1.jar",
     "https://cdn.modrinth.com/data/XaDC71GB/versions/" + VERSIONS["LITHOSTITCHED_MODRINTH_ID"] + "/lithostitched-1.7.13-fabric-21.1.jar",
     "required", "required"),
    ("lhGA9TYQ", VERSIONS["ARCHITECTURY_API_MODRINTH_ID"], "architectury-13.0.11-fabric.jar",
     "https://cdn.modrinth.com/data/lhGA9TYQ/versions/" + VERSIONS["ARCHITECTURY_API_MODRINTH_ID"] + "/architectury-13.0.11-fabric.jar",
     "required", "required"),
    ("hYykXjDp", VERSIONS["FZZY_CONFIG_MODRINTH_ID"], "fzzy_config-0.7.6+1.21.jar",
     "https://cdn.modrinth.com/data/hYykXjDp/versions/" + VERSIONS["FZZY_CONFIG_MODRINTH_ID"] + "/fzzy_config-0.7.6%2B1.21.jar",
     "required", "required"),
    ("6avVoBVB", VERSIONS["SIMPLY_TOOLTIPS_MODRINTH_ID"], "SimplyTooltips-fabric-0.1.3.jar",
     "https://cdn.modrinth.com/data/6avVoBVB/versions/" + VERSIONS["SIMPLY_TOOLTIPS_MODRINTH_ID"] + "/SimplyTooltips-fabric-0.1.3.jar",
     "required", "required"),
    ("gedNE4y2", VERSIONS["PLAYER_ANIMATOR_MODRINTH_ID"], "player-animation-lib-fabric-2.0.4+1.21.1.jar",
     "https://cdn.modrinth.com/data/gedNE4y2/versions/" + VERSIONS["PLAYER_ANIMATOR_MODRINTH_ID"] + "/player-animation-lib-fabric-2.0.4%2B1.21.1.jar",
     "required", "required"),
    ("9s6osm5g", VERSIONS["CLOTH_CONFIG_MODRINTH_ID"], "cloth-config-15.0.140-fabric.jar",
     "https://cdn.modrinth.com/data/9s6osm5g/versions/" + VERSIONS["CLOTH_CONFIG_MODRINTH_ID"] + "/cloth-config-15.0.140-fabric.jar",
     "required", "required"),
    ("K01OU20C", VERSIONS["CARDINAL_COMPONENTS_API_MODRINTH_ID"], "cardinal-components-api-6.1.3.jar",
     "https://cdn.modrinth.com/data/K01OU20C/versions/" + VERSIONS["CARDINAL_COMPONENTS_API_MODRINTH_ID"] + "/cardinal-components-api-6.1.3.jar",
     "required", "required"),
    ("MBAkmtvl", VERSIONS["BALM_MODRINTH_ID"], "balm-fabric-1.21.1-21.0.65.jar",
     "https://cdn.modrinth.com/data/MBAkmtvl/versions/" + VERSIONS["BALM_MODRINTH_ID"] + "/balm-fabric-1.21.1-21.0.65.jar",
     "required", "required"),
    ("QAGBst4M", VERSIONS["PUZZLES_LIB_MODRINTH_ID"], "PuzzlesLib-v21.1.52-1.21.1-Fabric.jar",
     "https://cdn.modrinth.com/data/QAGBst4M/versions/" + VERSIONS["PUZZLES_LIB_MODRINTH_ID"] + "/PuzzlesLib-v21.1.52-1.21.1-Fabric.jar",
     "required", "required"),
    ("ohNO6lps", VERSIONS["FORGE_CONFIG_API_PORT_MODRINTH_ID"], "ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar",
     "https://cdn.modrinth.com/data/ohNO6lps/versions/" + VERSIONS["FORGE_CONFIG_API_PORT_MODRINTH_ID"] + "/ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar",
     "required", "required"),
    ("Ha28R6CL", VERSIONS["FABRIC_LANGUAGE_KOTLIN_MODRINTH_ID"], "fabric-language-kotlin-1.13.13+kotlin.2.4.10.jar",
     "https://cdn.modrinth.com/data/Ha28R6CL/versions/" + VERSIONS["FABRIC_LANGUAGE_KOTLIN_MODRINTH_ID"] + "/fabric-language-kotlin-1.13.13%2Bkotlin.2.4.10.jar",
     "required", "required"),
    ("LrYZi08Q", VERSIONS["STRUCTURE_POOL_API_MODRINTH_ID"], "structure_pool_api-fabric-1.2.1+1.21.1.jar",
     "https://cdn.modrinth.com/data/LrYZi08Q/versions/" + VERSIONS["STRUCTURE_POOL_API_MODRINTH_ID"] + "/structure_pool_api-fabric-1.2.1%2B1.21.1.jar",
     "required", "required"),
    ("lP9Yrr1E", VERSIONS["RUNES_MODRINTH_ID"], "runes-fabric-1.3.1+1.21.1.jar",
     "https://cdn.modrinth.com/data/lP9Yrr1E/versions/" + VERSIONS["RUNES_MODRINTH_ID"] + "/runes-fabric-1.3.1%2B1.21.1.jar",
     "required", "required"),
    ("pduQXSbl", VERSIONS["AZURELIB_ARMOR_MODRINTH_ID"], "azurelibarmor-fabric-1.21.1-3.1.3.jar",
     "https://cdn.modrinth.com/data/pduQXSbl/versions/" + VERSIONS["AZURELIB_ARMOR_MODRINTH_ID"] + "/azurelibarmor-fabric-1.21.1-3.1.3.jar",
     "required", "required"),
    ("G1hIVOrD", VERSIONS["RESOURCEFUL_LIB_MODRINTH_ID"], "resourcefullib-fabric-1.21-3.0.12.jar",
     "https://cdn.modrinth.com/data/G1hIVOrD/versions/" + VERSIONS["RESOURCEFUL_LIB_MODRINTH_ID"] + "/resourcefullib-fabric-1.21-3.0.12.jar",
     "required", "required"),
    ("b1ZV3DIJ", VERSIONS["ATHENA_MODRINTH_ID"], "athena-fabric-1.21.1-4.0.6.jar",
     "https://cdn.modrinth.com/data/b1ZV3DIJ/versions/" + VERSIONS["ATHENA_MODRINTH_ID"] + "/athena-fabric-1.21.1-4.0.6.jar",
     "required", "optional"),
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

index = {
    "formatVersion": 1,
    "game": "minecraft",
    "versionId": IMAGE_VERSION,
    "name": "Minecraft Enhanced",
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

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minecraft-enhanced.mrpack")
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
