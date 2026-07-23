# Use Alpine because it's more secure, more performant and more size friendly
FROM alpine:3

# Version ARGs - these are set by CI from versions.env
ARG COBBLEMON_VERSION=1.7.3
ARG MINECRAFT_VERSION=1.21.1
ARG FABRIC_LOADER_VERSION=0.17.2
ARG FABRIC_INSTALLER_VERSION=1.0.1
ARG FABRIC_API_VERSION=0.116.8
ARG FABRIC_API_MODRINTH_ID=3wZtvzew
ARG COBBLEMON_MODRINTH_ID=kF7CvxTo

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
