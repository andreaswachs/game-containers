# Use Alpine because it's more secure, more performant and more size friendly
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG MINECRAFT_VERSION=1.21.1
ARG FABRIC_LOADER_VERSION=0.19.3
ARG FABRIC_INSTALLER_VERSION=1.1.1
ARG FABRIC_API_VERSION=0.116.8

# Core
ARG FABRIC_API_MODRINTH_ID=3wZtvzew

# Weapons
ARG SIMPLY_SWORDS_MODRINTH_ID=gcFhYOoT
ARG BETTER_COMBAT_MODRINTH_ID=JJQpBecL

# Magic
ARG SPELL_ENGINE_MODRINTH_ID=AzuZrwDk
ARG SPELL_POWER_MODRINTH_ID=IyVyrKj8
ARG WIZARDS_MODRINTH_ID=IhFI6pgc
ARG PALADINS_MODRINTH_ID=I8fuG8YJ

# Equipment & Accessories
ARG TRINKETS_MODRINTH_ID=JagCscwi
ARG ELYTRA_SLOT_MODRINTH_ID=jxx2pc4h
ARG CHARM_OF_UNDYING_MODRINTH_ID=RX60LMvX
ARG TRAVELERS_BACKPACK_MODRINTH_ID=5I4utX2T
ARG IMMERSIVE_ARMORS_MODRINTH_ID=4m0lwLNO

# Quality of Life
ARG VEINMINER_MODRINTH_ID=XJrQXP5u
ARG ENCHANTING_INFUSER_MODRINTH_ID=lBRm6Aii
ARG EASY_ANVILS_MODRINTH_ID=znaWBlgU

# World & Adventure
ARG TERRALITH_MODRINTH_ID=eWDLFabb
ARG DUNGEONS_AND_TAVERNS_MODRINTH_ID=EUlNXs9V
ARG WHEN_DUNGEONS_ARISE_MODRINTH_ID=g8oglmT0

# Navigation
ARG NATURES_COMPASS_MODRINTH_ID=dtrDpgsF
ARG EXPLORERS_COMPASS_MODRINTH_ID=qSRKiE4D
ARG WAYSTONES_MODRINTH_ID=qtRSzbaZ
ARG XAEROS_MINIMAP_MODRINTH_ID=Tx54V6kI
ARG XAEROS_WORLD_MAP_MODRINTH_ID=L2nO7ZYD

# Visual & Fun
ARG DANCERIZER_MODRINTH_ID=nZTi8Pqd

# Building
ARG CHIPPED_MODRINTH_ID=6h2mVZcb
ARG MACAWS_DOORS_MODRINTH_ID=Zsfvgzu6
ARG MACAWS_BRIDGES_MODRINTH_ID=pl1CA7dW

# Performance (server + client)
ARG LITHIUM_MODRINTH_ID=N08Z8wog
ARG FERRITECORE_MODRINTH_ID=sOzRw3CG
ARG KRYPTON_MODRINTH_ID=Acz3ttTp

# Library Dependencies
ARG ARCHITECTURY_API_MODRINTH_ID=Pzc2FP5K
ARG FZZY_CONFIG_MODRINTH_ID=kOmySYD4
ARG SIMPLY_TOOLTIPS_MODRINTH_ID=jrFEfRpA
ARG PLAYER_ANIMATOR_MODRINTH_ID=CkedfDp3
ARG CLOTH_CONFIG_MODRINTH_ID=HpMb5wGb
ARG CARDINAL_COMPONENTS_API_MODRINTH_ID=nLsCe2VD
ARG BALM_MODRINTH_ID=VynBiUHt
ARG PUZZLES_LIB_MODRINTH_ID=pqCNhF6A
ARG FORGE_CONFIG_API_PORT_MODRINTH_ID=N5qzq0XV
ARG FABRIC_LANGUAGE_KOTLIN_MODRINTH_ID=bdhiINYC
ARG STRUCTURE_POOL_API_MODRINTH_ID=Y6aBoKEl
ARG RUNES_MODRINTH_ID=PfNFbP8u
ARG AZURELIB_ARMOR_MODRINTH_ID=ECrTfeJS
ARG RESOURCEFUL_LIB_MODRINTH_ID=Hf91FuVF
ARG ATHENA_MODRINTH_ID=JfyYsWKP

# Install everything we need
RUN apk add --no-cache \
    openjdk21-jre \
    jq \
    rcon

# Create a user and usergroup with high UID and GID to not overlap with an existing host user or usergroup
RUN addgroup -g 10001 minecraft && \
    adduser -D -u 10000 -G minecraft minecraft

# Set working directory
WORKDIR /home/minecraft

# Create server directories
RUN mkdir -p /home/minecraft/server/mods

# Download Fabric server launcher
RUN wget -O /home/minecraft/server/fabric-server-launcher.jar \
    "https://meta.fabricmc.net/v2/versions/loader/${MINECRAFT_VERSION}/${FABRIC_LOADER_VERSION}/${FABRIC_INSTALLER_VERSION}/server/jar"

# Download Fabric API mod
RUN wget -O /home/minecraft/server/mods/fabric-api.jar \
    "https://cdn.modrinth.com/data/P7dR8mSH/versions/${FABRIC_API_MODRINTH_ID}/fabric-api-${FABRIC_API_VERSION}%2B${MINECRAFT_VERSION}.jar"

# Download library dependencies (required by addon mods below)
RUN wget -O /home/minecraft/server/mods/architectury-api.jar \
    "https://cdn.modrinth.com/data/lhGA9TYQ/versions/${ARCHITECTURY_API_MODRINTH_ID}/architectury-13.0.11-fabric.jar" && \
    wget -O /home/minecraft/server/mods/fzzy-config.jar \
    "https://cdn.modrinth.com/data/hYykXjDp/versions/${FZZY_CONFIG_MODRINTH_ID}/fzzy_config-0.7.6%2B1.21.jar" && \
    wget -O /home/minecraft/server/mods/simply-tooltips.jar \
    "https://cdn.modrinth.com/data/6avVoBVB/versions/${SIMPLY_TOOLTIPS_MODRINTH_ID}/SimplyTooltips-fabric-0.1.3.jar" && \
    wget -O /home/minecraft/server/mods/player-animator.jar \
    "https://cdn.modrinth.com/data/gedNE4y2/versions/${PLAYER_ANIMATOR_MODRINTH_ID}/player-animation-lib-fabric-2.0.4%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/cloth-config.jar \
    "https://cdn.modrinth.com/data/9s6osm5g/versions/${CLOTH_CONFIG_MODRINTH_ID}/cloth-config-15.0.140-fabric.jar" && \
    wget -O /home/minecraft/server/mods/cardinal-components-api.jar \
    "https://cdn.modrinth.com/data/K01OU20C/versions/${CARDINAL_COMPONENTS_API_MODRINTH_ID}/cardinal-components-api-6.1.3.jar" && \
    wget -O /home/minecraft/server/mods/balm.jar \
    "https://cdn.modrinth.com/data/MBAkmtvl/versions/${BALM_MODRINTH_ID}/balm-fabric-1.21.1-21.0.65.jar" && \
    wget -O /home/minecraft/server/mods/puzzles-lib.jar \
    "https://cdn.modrinth.com/data/QAGBst4M/versions/${PUZZLES_LIB_MODRINTH_ID}/PuzzlesLib-v21.1.52-1.21.1-Fabric.jar" && \
    wget -O /home/minecraft/server/mods/forge-config-api-port.jar \
    "https://cdn.modrinth.com/data/ohNO6lps/versions/${FORGE_CONFIG_API_PORT_MODRINTH_ID}/ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar" && \
    wget -O /home/minecraft/server/mods/fabric-language-kotlin.jar \
    "https://cdn.modrinth.com/data/Ha28R6CL/versions/${FABRIC_LANGUAGE_KOTLIN_MODRINTH_ID}/fabric-language-kotlin-1.13.13%2Bkotlin.2.4.10.jar" && \
    wget -O /home/minecraft/server/mods/structure-pool-api.jar \
    "https://cdn.modrinth.com/data/LrYZi08Q/versions/${STRUCTURE_POOL_API_MODRINTH_ID}/structure_pool_api-fabric-1.2.1%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/runes.jar \
    "https://cdn.modrinth.com/data/lP9Yrr1E/versions/${RUNES_MODRINTH_ID}/runes-fabric-1.3.1%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/azurelib-armor.jar \
    "https://cdn.modrinth.com/data/pduQXSbl/versions/${AZURELIB_ARMOR_MODRINTH_ID}/azurelibarmor-fabric-1.21.1-3.1.3.jar" && \
    wget -O /home/minecraft/server/mods/resourceful-lib.jar \
    "https://cdn.modrinth.com/data/G1hIVOrD/versions/${RESOURCEFUL_LIB_MODRINTH_ID}/resourcefullib-fabric-1.21-3.0.12.jar" && \
    wget -O /home/minecraft/server/mods/athena.jar \
    "https://cdn.modrinth.com/data/b1ZV3DIJ/versions/${ATHENA_MODRINTH_ID}/athena-fabric-1.21.1-4.0.6.jar"

# Download Weapon mods
RUN wget -O /home/minecraft/server/mods/simply-swords.jar \
    "https://cdn.modrinth.com/data/bK3Ubu9p/versions/${SIMPLY_SWORDS_MODRINTH_ID}/simplyswords-fabric-1.63.0-1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/better-combat.jar \
    "https://cdn.modrinth.com/data/5sy6g3kz/versions/${BETTER_COMBAT_MODRINTH_ID}/bettercombat-fabric-2.4.0%2B1.21.1.jar"

# Download Magic mods
RUN wget -O /home/minecraft/server/mods/spell-engine.jar \
    "https://cdn.modrinth.com/data/XvoWJaA2/versions/${SPELL_ENGINE_MODRINTH_ID}/spell_engine-fabric-1.9.16%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/spell-power.jar \
    "https://cdn.modrinth.com/data/8ooWzSQP/versions/${SPELL_POWER_MODRINTH_ID}/spell_power-fabric-1.6.0%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/wizards.jar \
    "https://cdn.modrinth.com/data/NkGaQMDA/versions/${WIZARDS_MODRINTH_ID}/wizards-fabric-3.0.4%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/paladins.jar \
    "https://cdn.modrinth.com/data/FxXkHaLe/versions/${PALADINS_MODRINTH_ID}/paladins-fabric-3.0.5%2B1.21.1.jar"

# Download Equipment & Accessory mods
RUN wget -O /home/minecraft/server/mods/trinkets.jar \
    "https://cdn.modrinth.com/data/5aaWibi9/versions/${TRINKETS_MODRINTH_ID}/trinkets-3.10.0.jar" && \
    wget -O /home/minecraft/server/mods/elytra-slot.jar \
    "https://cdn.modrinth.com/data/mSQF1NpT/versions/${ELYTRA_SLOT_MODRINTH_ID}/elytraslot-fabric-9.0.1%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/charm-of-undying.jar \
    "https://cdn.modrinth.com/data/b5GyyYkp/versions/${CHARM_OF_UNDYING_MODRINTH_ID}/charmofundying-fabric-9.1.0%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/travelers-backpack.jar \
    "https://cdn.modrinth.com/data/rlloIFEV/versions/${TRAVELERS_BACKPACK_MODRINTH_ID}/travelersbackpack-fabric-1.21.1-10.1.38.jar" && \
    wget -O /home/minecraft/server/mods/immersive-armors.jar \
    "https://cdn.modrinth.com/data/eE2Db4YU/versions/${IMMERSIVE_ARMORS_MODRINTH_ID}/immersive_armors-1.7.6%2B1.21.1-fabric.jar"

# Download Quality of Life mods
RUN wget -O /home/minecraft/server/mods/veinminer.jar \
    "https://cdn.modrinth.com/data/OhduvhIc/versions/${VEINMINER_MODRINTH_ID}/veinminer-fabric-2.11.2%2B1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/enchanting-infuser.jar \
    "https://cdn.modrinth.com/data/ePv85y52/versions/${ENCHANTING_INFUSER_MODRINTH_ID}/EnchantingInfuser-v21.1.4-1.21.1-Fabric.jar" && \
    wget -O /home/minecraft/server/mods/easy-anvils.jar \
    "https://cdn.modrinth.com/data/OZBR5JT5/versions/${EASY_ANVILS_MODRINTH_ID}/EasyAnvils-v21.1.0-1.21.1-Fabric.jar"

# Download World & Adventure mods
RUN wget -O /home/minecraft/server/mods/terralith.jar \
    "https://cdn.modrinth.com/data/8oi3bsk5/versions/${TERRALITH_MODRINTH_ID}/Terralith_1.21.x_v2.6.2.jar" && \
    wget -O /home/minecraft/server/mods/dungeons-and-taverns.jar \
    "https://cdn.modrinth.com/data/tpehi7ww/versions/${DUNGEONS_AND_TAVERNS_MODRINTH_ID}/dungeons-and-taverns-v4.4.4.jar" && \
    wget -O /home/minecraft/server/mods/when-dungeons-arise.jar \
    "https://cdn.modrinth.com/data/8DfbfASn/versions/${WHEN_DUNGEONS_ARISE_MODRINTH_ID}/DungeonsArise-1.21.1-2.1.68-fabric-release.jar"

# Download Navigation mods
RUN wget -O /home/minecraft/server/mods/natures-compass.jar \
    "https://cdn.modrinth.com/data/fPetb5Kh/versions/${NATURES_COMPASS_MODRINTH_ID}/NaturesCompass-1.21.1-2.6.0-fabric.jar" && \
    wget -O /home/minecraft/server/mods/explorers-compass.jar \
    "https://cdn.modrinth.com/data/RV1qfVQ8/versions/${EXPLORERS_COMPASS_MODRINTH_ID}/ExplorersCompass-1.21.1-2.6.0-fabric.jar" && \
    wget -O /home/minecraft/server/mods/waystones.jar \
    "https://cdn.modrinth.com/data/LOpKHB2A/versions/${WAYSTONES_MODRINTH_ID}/waystones-fabric-1.21.1-21.1.41.jar" && \
    wget -O /home/minecraft/server/mods/xaeros-minimap.jar \
    "https://cdn.modrinth.com/data/1bokaNcj/versions/${XAEROS_MINIMAP_MODRINTH_ID}/xaerominimap-fabric-1.21.1-26.4.2.jar" && \
    wget -O /home/minecraft/server/mods/xaeros-world-map.jar \
    "https://cdn.modrinth.com/data/NcUtCpym/versions/${XAEROS_WORLD_MAP_MODRINTH_ID}/xaeroworldmap-fabric-1.21.1-1.44.2.jar"

# Download Visual & Fun mods
RUN wget -O /home/minecraft/server/mods/dancerizer.jar \
    "https://cdn.modrinth.com/data/hZ4lZ6jX/versions/${DANCERIZER_MODRINTH_ID}/dancerizer-1.4.1.jar"

# Download Building mods
RUN wget -O /home/minecraft/server/mods/chipped.jar \
    "https://cdn.modrinth.com/data/BAscRYKm/versions/${CHIPPED_MODRINTH_ID}/chipped-fabric-1.21.1-4.0.2.jar" && \
    wget -O /home/minecraft/server/mods/macaws-doors.jar \
    "https://cdn.modrinth.com/data/kNxa8z3e/versions/${MACAWS_DOORS_MODRINTH_ID}/mcw-doors-1.1.5-mc1.21.1fabric.jar" && \
    wget -O /home/minecraft/server/mods/macaws-bridges.jar \
    "https://cdn.modrinth.com/data/GURcjz8O/versions/${MACAWS_BRIDGES_MODRINTH_ID}/mcw-bridges-3.1.2-mc1.21.1fabric.jar"

# Download Performance mods (server-side: Lithium, FerriteCore, Krypton)
RUN wget -O /home/minecraft/server/mods/lithium.jar \
    "https://cdn.modrinth.com/data/gvQqBUqZ/versions/${LITHIUM_MODRINTH_ID}/lithium-fabric-0.15.4%2Bmc1.21.1.jar" && \
    wget -O /home/minecraft/server/mods/ferritecore.jar \
    "https://cdn.modrinth.com/data/uXXizFIs/versions/${FERRITECORE_MODRINTH_ID}/ferritecore-7.0.3-fabric.jar" && \
    wget -O /home/minecraft/server/mods/krypton.jar \
    "https://cdn.modrinth.com/data/fQEb0iXm/versions/${KRYPTON_MODRINTH_ID}/krypton-0.2.8.jar"

# Copy the entrypoint script
COPY start.sh ./

# Fix permissions
RUN chown -R minecraft:minecraft /home/minecraft && \
    chmod +x start.sh

# Store version info for runtime reference
RUN echo "MINECRAFT_VERSION=${MINECRAFT_VERSION}" > /home/minecraft/version.txt

# USER is not being used, but we are actually running the server as the minecraft user inside the entrypoint
# The reason is conflicts with volumes permissions while wanting to have this streamlined as much as possible

# Launch entrypoint script to run the server
ENTRYPOINT ["/home/minecraft/start.sh"]
