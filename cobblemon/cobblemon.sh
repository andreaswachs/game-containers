#!/bin/ash
set -e

# Check if EULA has been accepted
if [ -z "$EULA" ]; then
    echo "Variable EULA not defined, see docs to know how to accept EULA."
    exit 1
fi

# Default the allocated RAM to 8G if not set
ALLOCATED_RAM="${ALLOCATED_RAM:-8G}"

# Server files are pre-downloaded in /home/cobblemon/server during image build
# The world directory is used for persistent data (mounted as volume)
WORLD_DIR="/home/cobblemon/world"
SERVER_DIR="/home/cobblemon/server"

# Create world directory structure
mkdir -p "$WORLD_DIR/mods"

# Copy mods to world directory (allows volume persistence and custom mods)
cp -n "$SERVER_DIR/mods/"*.jar "$WORLD_DIR/mods/" 2>/dev/null || true

# Copy server launcher if not present
cp -n "$SERVER_DIR/fabric-server-launcher.jar" "$WORLD_DIR/" 2>/dev/null || true

# Set up EULA
echo "eula=${EULA}" > "$WORLD_DIR/eula.txt"

# Fix permissions
chown -R cobblemon:cobblemon "$WORLD_DIR"
chmod +x "$WORLD_DIR/fabric-server-launcher.jar"

# Print version info
if [ -f /home/cobblemon/version.txt ]; then
    echo "=== Cobblemon Server ==="
    cat /home/cobblemon/version.txt
    echo "ALLOCATED_RAM=${ALLOCATED_RAM}"
    echo "========================"
fi

# Start the server
cd "$WORLD_DIR"
exec su -c "java -Xmx${ALLOCATED_RAM} -jar fabric-server-launcher.jar nogui" cobblemon
