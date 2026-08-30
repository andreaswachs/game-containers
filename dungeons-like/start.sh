#!/bin/ash
set -e

# Check if EULA has been accepted
if [ -z "$EULA" ]; then
    echo "Variable EULA not defined, see docs to know how to accept EULA."
    exit 1
fi

# Default the allocated RAM to 6G if not set
ALLOCATED_RAM="${ALLOCATED_RAM:-6G}"

# Server files are pre-downloaded in /home/minecraft/server during image build
# The world directory is used for persistent data (mounted as volume)
WORLD_DIR="/home/minecraft/world"
SERVER_DIR="/home/minecraft/server"

# Fix ownership of the world directory first — the volume may be mounted
# with host UID/GID that differs from the container user (UID 10000)
chown -R minecraft:minecraft "$WORLD_DIR"

# Create world directory structure
mkdir -p "$WORLD_DIR/mods"

# Copy mods to world directory (allows volume persistence and custom mods)
cp -n "$SERVER_DIR/mods/"*.jar "$WORLD_DIR/mods/" 2>/dev/null || true

# Copy Forge launch script (always overwrite to ensure latest)
cp -f "$SERVER_DIR/run.sh" "$WORLD_DIR/run.sh"

# Write JVM args
echo "-Xmx${ALLOCATED_RAM}" > "$WORLD_DIR/user_jvm_args.txt"

# Set up EULA
echo "eula=${EULA}" > "$WORLD_DIR/eula.txt"

chmod +x "$WORLD_DIR/run.sh"

# Symlink Forge libraries to world dir (avoids copying 150+ MB)
# Remove any existing entry first — ln -sfn on BusyBox creates the symlink
# inside an existing directory instead of replacing it
rm -rf "$WORLD_DIR/libraries"
ln -s "$SERVER_DIR/libraries" "$WORLD_DIR/libraries"

# Print version info
if [ -f /home/minecraft/version.txt ]; then
    echo "=== Dungeons-like Server ==="
    cat /home/minecraft/version.txt
    echo "ALLOCATED_RAM=${ALLOCATED_RAM}"
    echo "==========================="
fi

# Start the server
cd "$WORLD_DIR"
exec su -c "sh run.sh nogui" minecraft
