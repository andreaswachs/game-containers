#!/bin/ash
set -e

# Check if EULA has been accepted
if [ -z "$EULA" ]; then
    echo "Variable EULA not defined, see docs to know how to accept EULA."
    exit 1
fi

# Default the allocated RAM to 4G if not set
ALLOCATED_RAM="${ALLOCATED_RAM:-4G}"

WORLD_DIR="/home/minecraft/world"
SERVER_DIR="/home/minecraft/server"

# Create world directory structure
mkdir -p "$WORLD_DIR/mods" "$WORLD_DIR/config"

# Copy mods to world directory (allows volume persistence and custom mods)
cp -n "$SERVER_DIR/mods/"*.jar "$WORLD_DIR/mods/" 2>/dev/null || true

# Copy configs to world directory (allows persistence and customization)
find "$SERVER_DIR/config/" -type f | while IFS= read -r srcfile; do
    relpath="${srcfile#$SERVER_DIR/config/}"
    dstfile="$WORLD_DIR/config/$relpath"
    mkdir -p "$(dirname "$dstfile")"
    cp -n "$srcfile" "$dstfile" 2>/dev/null || true
done

# Symlink Forge libraries to world directory (avoid copying 150+ MB on each start)
ln -sfn "$SERVER_DIR/libraries" "$WORLD_DIR/libraries"

# Copy Forge launch script (always overwrite to match installed Forge version)
cp -f "$SERVER_DIR/run.sh" "$WORLD_DIR/run.sh" 2>/dev/null || true

# Write JVM arguments (memory allocation)
echo "-Xmx${ALLOCATED_RAM}" > "$WORLD_DIR/user_jvm_args.txt"

# Set up EULA
echo "eula=${EULA}" > "$WORLD_DIR/eula.txt"

# Fix permissions
chown -R minecraft:minecraft "$WORLD_DIR"
chmod +x "$WORLD_DIR/run.sh"

# Print version info
if [ -f /home/minecraft/version.txt ]; then
    echo "=== MZA Server ==="
    cat /home/minecraft/version.txt
    echo "ALLOCATED_RAM=${ALLOCATED_RAM}"
    echo "================="
fi

# Start the server
cd "$WORLD_DIR"
exec su -c "sh run.sh nogui" minecraft
