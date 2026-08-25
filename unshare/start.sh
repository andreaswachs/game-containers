#!/bin/ash
set -e

# Check if EULA has been accepted
if [ -z "$EULA" ]; then
    echo "Variable EULA not defined, see docs to know how to accept EULA."
    exit 1
fi

# Default the allocated RAM to 2G if not set (this is an old, lightweight version)
ALLOCATED_RAM="${ALLOCATED_RAM:-2G}"

# Server files are pre-downloaded in /home/minecraft/server during image build
# The world directory is used for persistent data (mounted as volume)
WORLD_DIR="/home/minecraft/world"
SERVER_DIR="/home/minecraft/server"

# Create world directory structure
mkdir -p "$WORLD_DIR/mods"

# Copy server files to world directory (allows volume persistence and custom mods)
cp -n "$SERVER_DIR/server.jar" "$WORLD_DIR/" 2>/dev/null || true
cp -rn "$SERVER_DIR/libs" "$WORLD_DIR/" 2>/dev/null || true
cp -n "$SERVER_DIR/mods/"*.jar "$WORLD_DIR/mods/" 2>/dev/null || true

# Set up EULA
echo "eula=${EULA}" > "$WORLD_DIR/eula.txt"

# Fix permissions
chown -R minecraft:minecraft "$WORLD_DIR"

# Print version info
if [ -f /home/minecraft/version.txt ]; then
    echo "=== Minecraft Unshare Server ==="
    cat /home/minecraft/version.txt
    echo "ALLOCATED_RAM=${ALLOCATED_RAM}"
    echo "================================"
fi

# Start the server via fabric's KnotServer
cd "$WORLD_DIR"
exec su -c "java -Xmx${ALLOCATED_RAM} -Dfabric.gameJarPath=server.jar -cp 'libs/*' net.fabricmc.loader.impl.launch.knot.KnotServer nogui" minecraft
