# Use Alpine because it's more secure, more performant and more size friendly
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG MINECRAFT_VERSION=1.20.1
ARG FORGE_VERSION=47.4.23

# Core Dungeons Mods
ARG DUNGEONS_CONTENT_MODRINTH_ID=J5Mq5eIb
ARG DUNGEONS_CONTENT_TWO_MODRINTH_ID=o97IEL9y
ARG L_ENDERS_CATACLYSM_MODRINTH_ID=C3H0azzB
ARG ENCHANTWITHMOB_MODRINTH_ID=1UcKN8Qz
ARG GOETY_MODRINTH_ID=jVtlXH2H
ARG ECHOVOIDS_MODRINTH_ID=B7luDqgf
ARG VALHELSIA_STRUCTURES_MODRINTH_ID=9bGpLPl7
ARG ILLAGE_SPILLAGE_MODRINTH_ID=90YOIp4K
ARG ARTHYS_RPG_ARMS_MODRINTH_ID=QCFWRk8k
ARG DUNGEONS_AND_TAVERNS_MODRINTH_ID=ojHpWOrz

# Combat Mods
ARG BETTER_COMBAT_MODRINTH_ID=rnhiaw3t
ARG COMBAT_ROLL_MODRINTH_ID=532t65Zz
ARG AITK_MODRINTH_ID=peO41ivl

# Visual / QoL (subtle-effects is server-optional, rest are client-only in the mrpack)
ARG SUBTLE_EFFECTS_MODRINTH_ID=41iwVxX9

# Performance (server-side)
ARG MODERNFIX_MODRINTH_ID=uuWZXSci
ARG FERRITECORE_MODRINTH_ID=DG5Fn9Sz
ARG CANARY_MODRINTH_ID=lauzXB0n

# Server-side Dependencies
ARG GECKOLIB_MODRINTH_ID=aC5KMoNg
ARG FORMATIONS_MODRINTH_ID=5zgQmLP4
ARG CURIOS_MODRINTH_ID=IPQlZkz1
ARG LIONFISH_API_MODRINTH_ID=CPftDBcY
ARG BAGUS_LIB_MODRINTH_ID=EutpppUn
ARG PATCHOULI_MODRINTH_ID=94dtOLgZ
ARG VALHELSIA_CORE_MODRINTH_ID=eP3L8E7C
ARG PLAYER_ANIMATOR_MODRINTH_ID=xe2EVE6q
ARG CLOTH_CONFIG_MODRINTH_ID=t8TXrZvZ
ARG FZZY_CONFIG_MODRINTH_ID=7MmXhjWs
ARG KOTLIN_FOR_FORGE_MODRINTH_ID=Zsh14XeQ

# Additional Dependencies (used server-side, classified as client deps by some mods)
ARG IMMERSIVE_MESSAGES_API_MODRINTH_ID=4JWF2yfv
ARG TXNILIB_MODRINTH_ID=kQ8qnDHA
ARG ARCHITECTURY_API_MODRINTH_ID=1MKTLiiG
ARG OCTOLIB_MODRINTH_ID=HZ7KmyXp

# Install everything we need
RUN apk add --no-cache \
    openjdk17-jre \
    jq \
    rcon

# Create a user and usergroup with high UID and GID to not overlap with an existing host user or usergroup
RUN addgroup -g 10001 minecraft && \
    adduser -D -u 10000 -G minecraft minecraft

# Set working directory
WORKDIR /home/minecraft

# Create server directories
RUN mkdir -p /home/minecraft/server/mods

# Download and install Forge server
RUN wget -O /tmp/forge-installer.jar \
    "https://maven.minecraftforge.net/net/minecraftforge/forge/${MINECRAFT_VERSION}-${FORGE_VERSION}/forge-${MINECRAFT_VERSION}-${FORGE_VERSION}-installer.jar" && \
    cd /home/minecraft/server && \
    java -jar /tmp/forge-installer.jar --installServer && \
    rm /tmp/forge-installer.jar /home/minecraft/server/forge-installer.jar.log

# Download server-side dependencies (required by mods below)
RUN wget -O /home/minecraft/server/mods/geckolib.jar \
    "https://cdn.modrinth.com/data/8BmcQJ2H/versions/${GECKOLIB_MODRINTH_ID}/geckolib-forge-1.20.1-4.8.4.jar" && \
    wget -O /home/minecraft/server/mods/formations.jar \
    "https://cdn.modrinth.com/data/tPe4xnPd/versions/${FORMATIONS_MODRINTH_ID}/formations-1.0.4-forge-mc1.20.2.jar" && \
    wget -O /home/minecraft/server/mods/curios.jar \
    "https://cdn.modrinth.com/data/vvuO3ImH/versions/${CURIOS_MODRINTH_ID}/curios-forge-5.14.1%2B1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/lionfish-api.jar \
    "https://cdn.modrinth.com/data/FoVacERa/versions/${LIONFISH_API_MODRINTH_ID}/lionfishapi-3.0.jar" && \
    wget -O /home/minecraft/server/mods/bagus-lib.jar \
    "https://cdn.modrinth.com/data/95nSN4Rd/versions/${BAGUS_LIB_MODRINTH_ID}/bagus_lib-1.20.1-5.6.1.jar" && \
    wget -O /home/minecraft/server/mods/patchouli.jar \
    "https://cdn.modrinth.com/data/nU0bVIaL/versions/${PATCHOULI_MODRINTH_ID}/Patchouli-1.20.1-85-FORGE.jar" && \
    wget -O /home/minecraft/server/mods/valhelsia-core.jar \
    "https://cdn.modrinth.com/data/HsdNFinx/versions/${VALHELSIA_CORE_MODRINTH_ID}/valhelsia_core-forge-1.20.1-1.1.2.jar" && \
    wget -O /home/minecraft/server/mods/player-animator.jar \
    "https://cdn.modrinth.com/data/gedNE4y2/versions/${PLAYER_ANIMATOR_MODRINTH_ID}/player-animation-lib-forge-1.0.2-rc1%2B1.20.jar" && \
    wget -O /home/minecraft/server/mods/cloth-config.jar \
    "https://cdn.modrinth.com/data/9s6osm5g/versions/${CLOTH_CONFIG_MODRINTH_ID}/cloth-config-11.1.136-forge.jar" && \
    wget -O /home/minecraft/server/mods/fzzy-config.jar \
    "https://cdn.modrinth.com/data/hYykXjDp/versions/${FZZY_CONFIG_MODRINTH_ID}/fzzy_config-0.7.6%2B1.20.1%2Bforge.jar" && \
    wget -O /home/minecraft/server/mods/kotlin-for-forge.jar \
    "https://cdn.modrinth.com/data/ordsPcFz/versions/${KOTLIN_FOR_FORGE_MODRINTH_ID}/kotlinforforge-4.12.0-all.jar" && \
    wget -O /home/minecraft/server/mods/immersive-messages-api.jar \
    "https://cdn.modrinth.com/data/6xvrmbjn/versions/${IMMERSIVE_MESSAGES_API_MODRINTH_ID}/immersivemessages-forge-1.0.18-1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/txnilib.jar \
    "https://cdn.modrinth.com/data/vBbPDuOs/versions/${TXNILIB_MODRINTH_ID}/txnilib-forge-1.0.24-1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/architectury-api.jar \
    "https://cdn.modrinth.com/data/lhGA9TYQ/versions/${ARCHITECTURY_API_MODRINTH_ID}/architectury-9.2.14-forge.jar" && \
    wget -O /home/minecraft/server/mods/octolib.jar \
    "https://cdn.modrinth.com/data/RH2KUdKJ/versions/${OCTOLIB_MODRINTH_ID}/OctoLib-FORGE-0.5.0.1%2B1.20.1.jar"

# Download Core Dungeons mods
RUN wget -O /home/minecraft/server/mods/dungeons-content.jar \
    "https://cdn.modrinth.com/data/R0ToJjk1/versions/${DUNGEONS_CONTENT_MODRINTH_ID}/dungeons_1.19_mc1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/dungeons-content-two.jar \
    "https://cdn.modrinth.com/data/dVxU9eTq/versions/${DUNGEONS_CONTENT_TWO_MODRINTH_ID}/dungeons_content_two-1.0.2-alpha-forge-1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/l_enders-cataclysm.jar \
    "https://cdn.modrinth.com/data/46KJle7n/versions/${L_ENDERS_CATACLYSM_MODRINTH_ID}/L_Enders_Cataclysm-3.31.jar" && \
    wget -O /home/minecraft/server/mods/enchantwithmob.jar \
    "https://cdn.modrinth.com/data/SwDIbBHh/versions/${ENCHANTWITHMOB_MODRINTH_ID}/enchantwithmob-1.20.1-11.17.1.jar" && \
    wget -O /home/minecraft/server/mods/goety.jar \
    "https://cdn.modrinth.com/data/4ZVIxU8x/versions/${GOETY_MODRINTH_ID}/goety-2.5.57.3.jar" && \
    wget -O /home/minecraft/server/mods/echovoids.jar \
    "https://cdn.modrinth.com/data/pBrtNB24/versions/${ECHOVOIDS_MODRINTH_ID}/echovoids-2.0.3b-forge-1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/valhelsia-structures.jar \
    "https://cdn.modrinth.com/data/T21szC0a/versions/${VALHELSIA_STRUCTURES_MODRINTH_ID}/valhelsia_structures-forge-1.20.1-1.1.2.jar" && \
    wget -O /home/minecraft/server/mods/illage-and-spillage.jar \
    "https://cdn.modrinth.com/data/kLoMCc4b/versions/${ILLAGE_SPILLAGE_MODRINTH_ID}/illageandspillagerespillaged-1.2.8.jar" && \
    wget -O /home/minecraft/server/mods/arthys-rpg-arms.jar \
    "https://cdn.modrinth.com/data/Ivn6yJvS/versions/${ARTHYS_RPG_ARMS_MODRINTH_ID}/arthys_rpg_arms-2.1.4-forge-1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/dungeons-and-taverns.jar \
    "https://cdn.modrinth.com/data/tpehi7ww/versions/${DUNGEONS_AND_TAVERNS_MODRINTH_ID}/dungeons-and-taverns-3.0.3.f.jar"

# Download Combat mods (server-side: Better Combat, Combat Roll, AITK)
RUN wget -O /home/minecraft/server/mods/better-combat.jar \
    "https://cdn.modrinth.com/data/5sy6g3kz/versions/${BETTER_COMBAT_MODRINTH_ID}/bettercombat-forge-1.9.0%2B1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/combat-roll.jar \
    "https://cdn.modrinth.com/data/wGKYL7st/versions/${COMBAT_ROLL_MODRINTH_ID}/combatroll-forge-1.3.3%2B1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/aitk.jar \
    "https://cdn.modrinth.com/data/A0W9tMly/versions/${AITK_MODRINTH_ID}/aitk-1.2.1-forge%2B1.20.1.jar"

# Download Visual / QoL mods (server-side compatible ones only: subtle-effects is server-optional)
RUN wget -O /home/minecraft/server/mods/subtle-effects.jar \
    "https://cdn.modrinth.com/data/4q8UOK1d/versions/${SUBTLE_EFFECTS_MODRINTH_ID}/SubtleEffects-forge-1.20.1-1.14.3.jar"

# Download Performance mods (server-side: ModernFix, FerriteCore, Canary)
RUN wget -O /home/minecraft/server/mods/modernfix.jar \
    "https://cdn.modrinth.com/data/nmDcB62a/versions/${MODERNFIX_MODRINTH_ID}/modernfix-forge-5.27.79%2Bmc1.20.1.jar" && \
    wget -O /home/minecraft/server/mods/ferritecore.jar \
    "https://cdn.modrinth.com/data/uXXizFIs/versions/${FERRITECORE_MODRINTH_ID}/ferritecore-6.0.1-forge.jar" && \
    wget -O /home/minecraft/server/mods/canary.jar \
    "https://cdn.modrinth.com/data/qa2H4BS9/versions/${CANARY_MODRINTH_ID}/canary-mc1.20.1-0.3.3.jar"

# Copy the entrypoint script
COPY start.sh ./

# Fix permissions
RUN chown -R minecraft:minecraft /home/minecraft && \
    chmod +x start.sh

# Store version info for runtime reference
RUN echo "MINECRAFT_VERSION=${MINECRAFT_VERSION}" > /home/minecraft/version.txt && \
    echo "FORGE_VERSION=${FORGE_VERSION}" >> /home/minecraft/version.txt && \
    echo "MODPACK=Dungeons-like" >> /home/minecraft/version.txt

# USER is not being used, but we are actually running the server as the minecraft user inside the entrypoint
# The reason is conflicts with volumes permissions while wanting to have this streamlined as much as possible

# Launch entrypoint script to run the server
ENTRYPOINT ["/home/minecraft/start.sh"]
