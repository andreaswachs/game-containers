# Use Alpine because it's more secure, more performant and more size friendly
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG COBBLEMON_VERSION=1.7.3
ARG MINECRAFT_VERSION=1.21.1
ARG FABRIC_LOADER_VERSION=0.19.3
ARG FABRIC_INSTALLER_VERSION=1.1.1
ARG FABRIC_API_VERSION=0.116.8
ARG FABRIC_API_MODRINTH_ID=3wZtvzew
ARG COBBLEMON_MODRINTH_ID=kF7CvxTo

# Mega Evolution
ARG MEGA_SHOWDOWN_MODRINTH_ID=5GXFsZw0
ARG NAVAS_ZAMEGA_MODRINTH_ID=9DB6eyaV
ARG MEGA_SHOWDOWN_ITEM_PACK_MODRINTH_ID=UKP9CyH2

# Missing Pokemon / Legendaries
ARG MYTHS_AND_LEGENDS_MODRINTH_ID=eg83qtSQ
ARG LEGENDARY_MONUMENTS_MODRINTH_ID=6nvO1cvI
ARG LEGENDS_MYTHS_MODRINTH_ID=ffm34Mmj
ARG COMPLETE_COBBLEMON_COLLECTION_MODRINTH_ID=Azf9qoT6

# Gyms + Elite Four / Trainers
ARG RADICAL_TRAINERS_MODRINTH_ID=gQx1F1dx
ARG RCT_API_MODRINTH_ID=9OZx0coL
ARG RAD_GYMS_MODRINTH_ID=2AR7EuiZ

# Library Dependencies
ARG ARCHITECTURY_API_MODRINTH_ID=Wto0RchG
ARG ACCESSORIES_MODRINTH_ID=Xlt4eWBe
ARG OWO_LIB_MODRINTH_ID=JB1fLQnc
ARG LITHOSTITCHED_MODRINTH_ID=JWtSqSeY
ARG CHIPPED_MODRINTH_ID=6h2mVZcb
ARG FORGE_CONFIG_API_PORT_MODRINTH_ID=N5qzq0XV
ARG RESOURCEFUL_LIB_MODRINTH_ID=Hf91FuVF
ARG ATHENA_MODRINTH_ID=JfyYsWKP

# Install everything we need
RUN apk add --no-cache \
    openjdk21-jre \
    jq \
    rcon

# Create a user and usergroup with high UID and GID to not overlap with an existing host user or usergroup
RUN addgroup -g 10001 cobblemon && \
    adduser -D -u 10000 -G cobblemon cobblemon

# Set working directory
WORKDIR /home/cobblemon

# Create server directories
RUN mkdir -p /home/cobblemon/server/mods

# Download Fabric server launcher
RUN wget -O /home/cobblemon/server/fabric-server-launcher.jar \
    "https://meta.fabricmc.net/v2/versions/loader/${MINECRAFT_VERSION}/${FABRIC_LOADER_VERSION}/${FABRIC_INSTALLER_VERSION}/server/jar"

# Download Fabric API mod
RUN wget -O /home/cobblemon/server/mods/fabric-api.jar \
    "https://cdn.modrinth.com/data/P7dR8mSH/versions/${FABRIC_API_MODRINTH_ID}/fabric-api-${FABRIC_API_VERSION}%2B${MINECRAFT_VERSION}.jar"

# Download Cobblemon mod
RUN wget -O /home/cobblemon/server/mods/cobblemon.jar \
    "https://cdn.modrinth.com/data/MdwFAVRL/versions/${COBBLEMON_MODRINTH_ID}/Cobblemon-fabric-${COBBLEMON_VERSION}%2B${MINECRAFT_VERSION}.jar"

# Download library dependencies (required by addon mods below)
RUN wget -O /home/cobblemon/server/mods/architectury-api.jar \
    "https://cdn.modrinth.com/data/lhGA9TYQ/versions/${ARCHITECTURY_API_MODRINTH_ID}/architectury-13.0.8-fabric.jar" && \
    wget -O /home/cobblemon/server/mods/accessories.jar \
    "https://cdn.modrinth.com/data/jtmvUHXj/versions/${ACCESSORIES_MODRINTH_ID}/accessories-fabric-1.1.0-beta.53%2B1.21.1.jar" && \
    wget -O /home/cobblemon/server/mods/owo-lib.jar \
    "https://cdn.modrinth.com/data/ccKDOlHs/versions/${OWO_LIB_MODRINTH_ID}/owo-lib-0.12.15.4%2B1.21.jar" && \
    wget -O /home/cobblemon/server/mods/lithostitched.jar \
    "https://cdn.modrinth.com/data/XaDC71GB/versions/${LITHOSTITCHED_MODRINTH_ID}/lithostitched-1.7.13-fabric-21.1.jar" && \
    wget -O /home/cobblemon/server/mods/chipped.jar \
    "https://cdn.modrinth.com/data/BAscRYKm/versions/${CHIPPED_MODRINTH_ID}/chipped-fabric-1.21.1-4.0.2.jar" && \
    wget -O /home/cobblemon/server/mods/forge-config-api-port.jar \
    "https://cdn.modrinth.com/data/ohNO6lps/versions/${FORGE_CONFIG_API_PORT_MODRINTH_ID}/ForgeConfigAPIPort-v21.1.6-1.21.1-Fabric.jar" && \
    wget -O /home/cobblemon/server/mods/resourceful-lib.jar \
    "https://cdn.modrinth.com/data/G1hIVOrD/versions/${RESOURCEFUL_LIB_MODRINTH_ID}/resourcefullib-fabric-1.21-3.0.12.jar" && \
    wget -O /home/cobblemon/server/mods/athena.jar \
    "https://cdn.modrinth.com/data/b1ZV3DIJ/versions/${ATHENA_MODRINTH_ID}/athena-fabric-1.21.1-4.0.6.jar"

# Download Mega Evolution mods
RUN wget -O /home/cobblemon/server/mods/mega-showdown.jar \
    "https://cdn.modrinth.com/data/SszvX85I/versions/${MEGA_SHOWDOWN_MODRINTH_ID}/mega_showdown-fabric-1.9.0%2B1.7.3%2B1.21.1-hotfix-v3.jar" && \
    wget -O /home/cobblemon/server/mods/navas-zamega.jar \
    "https://cdn.modrinth.com/data/2V1Y86sc/versions/${NAVAS_ZAMEGA_MODRINTH_ID}/zamega-fabric-1.7.4-hotfix-hotfix.jar" && \
    wget -O /home/cobblemon/server/mods/mega-showdown-item-pack.jar \
    "https://cdn.modrinth.com/data/ldNeqFqN/versions/${MEGA_SHOWDOWN_ITEM_PACK_MODRINTH_ID}/mega-showdown-item-pack-1.4.2.jar"

# Download Missing Pokemon / Legendary mods
RUN wget -O /home/cobblemon/server/mods/myths-and-legends.jar \
    "https://cdn.modrinth.com/data/CaOWby9K/versions/${MYTHS_AND_LEGENDS_MODRINTH_ID}/MythsAndLegends-fabric-1.9.0.jar" && \
    wget -O /home/cobblemon/server/mods/legendary-monuments.jar \
    "https://cdn.modrinth.com/data/m6RyHSbV/versions/${LEGENDARY_MONUMENTS_MODRINTH_ID}/legendarymonuments-fabric-1.21.1-8.0.3.jar" && \
    wget -O /home/cobblemon/server/mods/legends-myths.jar \
    "https://cdn.modrinth.com/data/5EMX10qI/versions/${LEGENDS_MYTHS_MODRINTH_ID}/legends-myths-3.jar" && \
    wget -O /home/cobblemon/server/mods/complete-cobblemon-collection.jar \
    "https://cdn.modrinth.com/data/qoL4kNxC/versions/${COMPLETE_COBBLEMON_COLLECTION_MODRINTH_ID}/complete-cobblemon-collection-myths-and-legends-compat-2.1.0.jar"

# Download Gym / Trainer mods
RUN wget -O /home/cobblemon/server/mods/radical-cobblemon-trainers.jar \
    "https://cdn.modrinth.com/data/lRwTUnD7/versions/${RADICAL_TRAINERS_MODRINTH_ID}/rctmod-fabric-1.21.1-0.18.1-beta.jar" && \
    wget -O /home/cobblemon/server/mods/rct-api.jar \
    "https://cdn.modrinth.com/data/CBfM2yw7/versions/${RCT_API_MODRINTH_ID}/rctapi-fabric-1.21.1-0.15.2-beta.jar" && \
    wget -O /home/cobblemon/server/mods/rad-gyms.jar \
    "https://cdn.modrinth.com/data/eF8kqlHd/versions/${RAD_GYMS_MODRINTH_ID}/rad-gyms-fabric-0.4.4.jar"

# Copy the entrypoint script
COPY cobblemon.sh ./

# Fix permissions
RUN chown -R cobblemon:cobblemon /home/cobblemon && \
    chmod +x cobblemon.sh

# Store version info for runtime reference
RUN echo "COBBLEMON_VERSION=${COBBLEMON_VERSION}" > /home/cobblemon/version.txt && \
    echo "MINECRAFT_VERSION=${MINECRAFT_VERSION}" >> /home/cobblemon/version.txt

# USER is not being used, but we are actually running the server as the cobblemon user inside the entrypoint
# The reason is conflicts with volumes permissions while wanting to have this streamlined as much as possible

# Launch entrypoint script to run the server
ENTRYPOINT ["/home/cobblemon/cobblemon.sh"]
