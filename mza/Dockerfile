# Use Alpine because it's more secure, more performant and more size friendly
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG MINECRAFT_VERSION=1.20.1
ARG FORGE_VERSION=47.3.0
ARG MODPACK_VERSION=1.2.0
ARG MODPACK_VERSION_ID=ULJVFOE8

# Install everything we need
RUN apk add --no-cache \
    openjdk17-jre \
    jq \
    rcon \
    unzip

# Create a user and usergroup with high UID and GID to not overlap with an existing host user or usergroup
RUN addgroup -g 10001 minecraft && \
    adduser -D -u 10000 -G minecraft minecraft

# Set working directory
WORKDIR /home/minecraft

# Create server directories
RUN mkdir -p /home/minecraft/server/mods /home/minecraft/server/config

# Download and extract the MZA modpack from Modrinth
RUN wget -O /tmp/mza.mrpack \
    "https://cdn.modrinth.com/data/ygSxrow7/versions/${MODPACK_VERSION_ID}/MZA%20${MODPACK_VERSION}.mrpack" && \
    unzip -o /tmp/mza.mrpack -d /tmp/mza_extracted/ && \
    rm /tmp/mza.mrpack && \
    chmod -R 755 /tmp/mza_extracted/

# Download server-compatible mods from the modpack index
# Excludes client-only rendering/visual mods that would crash on a dedicated server:
#   embeddium, oculus, entity_model_features, entity_texture_features, essential
RUN set -eo pipefail; jq -r '.files[] | select(.path | startswith("mods/")) | .downloads[0]' \
    /tmp/mza_extracted/modrinth.index.json | \
    grep -v -i -E 'embeddium|oculus|entity_model_features|entity_texture_features|essential' | \
    while IFS= read -r url; do \
        wget -q -P /home/minecraft/server/mods/ "$url" || { echo "Failed to download: $url" >&2; exit 1; }; \
    done

# Copy bundled mod from overrides (easy-villagers is not on Modrinth CDN)
RUN cp /tmp/mza_extracted/overrides/mods/*.jar /home/minecraft/server/mods/ 2>/dev/null || true

# Copy config overrides and remove client-only config files
RUN cp -r /tmp/mza_extracted/overrides/config/* /home/minecraft/server/config/ 2>/dev/null || true && \
    find /home/minecraft/server/config \( \
        -name "*-client.*" -o \
        -name "embeddium*" -o \
        -name "oculus*" -o \
        -name "entityculling*" -o \
        -name "entity_model*" -o \
        -name "entity_texture*" -o \
        -name "etf_*" -o \
        -name "notenoughanimations*" -o \
        -name "MouseTweaks*" \
    \) -exec rm -f {} \; 2>/dev/null || true

# Download and install Forge server
RUN wget -O /tmp/forge-installer.jar \
    "https://maven.minecraftforge.net/net/minecraftforge/forge/${MINECRAFT_VERSION}-${FORGE_VERSION}/forge-${MINECRAFT_VERSION}-${FORGE_VERSION}-installer.jar" && \
    cd /home/minecraft/server && \
    java -jar /tmp/forge-installer.jar --installServer && \
    rm /tmp/forge-installer.jar /home/minecraft/server/forge-installer.jar.log

# Clean up extracted modpack
RUN rm -rf /tmp/mza_extracted

# Copy the entrypoint script
COPY start.sh ./

# Fix permissions
RUN chown -R minecraft:minecraft /home/minecraft && \
    chmod +x start.sh

# Store version info for runtime reference
RUN echo "MINECRAFT_VERSION=${MINECRAFT_VERSION}" > /home/minecraft/version.txt && \
    echo "FORGE_VERSION=${FORGE_VERSION}" >> /home/minecraft/version.txt && \
    echo "MODPACK=MZA ${MODPACK_VERSION}" >> /home/minecraft/version.txt

# USER is not being used, but we are actually running the server as the minecraft user inside the entrypoint
# The reason is conflicts with volumes permissions while wanting to have this streamlined as much as possible

# Launch entrypoint script to run the server
ENTRYPOINT ["/home/minecraft/start.sh"]
