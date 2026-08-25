# Use Alpine because it's more secure, more performant and more size friendly
# Note: 3D Shareware v1.34 is a 2019-era version that requires Java 8
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG MINECRAFT_VERSION_URL=3D%20Shareware%20v1.34
ARG FABRIC_LOADER_VERSION=0.16.5
ARG MIXIN_VERSION=0.15.3%2Bmixin.0.8.7
# Java 21 works fine for this version; pin to openjdk8-jre if you want era-correct Java
ARG JAVA_PACKAGE=openjdk21-jre

# The fabric meta/installer "server" flow is broken for version ids containing
# spaces (URISyntaxException), so we assemble the server manually:
# vanilla server.jar + fabric libraries + KnotServer entrypoint.
ARG VANILLA_SERVER_URL=https://piston-data.mojang.com/v1/objects/ffd306fc2aaa884755c5a6bf9fbd87aed26dd78f/server.jar
ARG FABRIC_MAVEN=https://maven.fabricmc.net

RUN apk add --no-cache "$JAVA_PACKAGE" zip

# Create a user and usergroup with high UID and GID to not overlap with an existing host user or usergroup
RUN addgroup -g 10001 minecraft && \
    adduser -D -u 10000 -G minecraft minecraft

# Set working directory
WORKDIR /home/minecraft

# Create server directories
RUN mkdir -p /home/minecraft/server/mods /home/minecraft/server/libs

# Download vanilla 3D Shareware v1.34 server jar from Mojang
# and remove JndiLookup (this era of log4j predates the CVE-2021-44228 fix,
# and has no runtime flag to disable it)
RUN wget -O /home/minecraft/server/server.jar "$VANILLA_SERVER_URL" && \
    zip -q -d /home/minecraft/server/server.jar 'org/apache/logging/log4j/core/lookup/JndiLookup.class'

# Download fabric loader runtime libraries
RUN cd /home/minecraft/server/libs && \
    wget -q "${FABRIC_MAVEN}/org/ow2/asm/asm/9.6/asm-9.6.jar" && \
    wget -q "${FABRIC_MAVEN}/org/ow2/asm/asm-analysis/9.6/asm-analysis-9.6.jar" && \
    wget -q "${FABRIC_MAVEN}/org/ow2/asm/asm-commons/9.6/asm-commons-9.6.jar" && \
    wget -q "${FABRIC_MAVEN}/org/ow2/asm/asm-tree/9.6/asm-tree-9.6.jar" && \
    wget -q "${FABRIC_MAVEN}/org/ow2/asm/asm-util/9.6/asm-util-9.6.jar" && \
    wget -q -O sponge-mixin.jar "${FABRIC_MAVEN}/net/fabricmc/sponge-mixin/${MIXIN_VERSION}/sponge-mixin-${MIXIN_VERSION}.jar" && \
    wget -q -O intermediary.jar "${FABRIC_MAVEN}/net/fabricmc/intermediary/${MINECRAFT_VERSION_URL}/intermediary-${MINECRAFT_VERSION_URL}.jar" && \
    wget -q -O fabric-loader.jar "${FABRIC_MAVEN}/net/fabricmc/fabric-loader/${FABRIC_LOADER_VERSION}/fabric-loader-${FABRIC_LOADER_VERSION}.jar"

# The unshare mod has no upstream releases, so the jar is built from source and committed here.
# Build instructions: see README.md
COPY mods/unshare-1.0.1.jar /home/minecraft/server/mods/unshare.jar

# Copy the entrypoint script
COPY start.sh ./

# Fix permissions
RUN chown -R minecraft:minecraft /home/minecraft && \
    chmod +x start.sh

# Store version info for runtime reference
RUN echo "MINECRAFT_VERSION=3D Shareware v1.34 (unshare)" > /home/minecraft/version.txt

# Launch entrypoint script to run the server
ENTRYPOINT ["/home/minecraft/start.sh"]
