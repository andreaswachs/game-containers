# Prerequisite

You need to accept EULA to run this server, you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - EULA=true
```

# Increasing RAM Allocation

If you need to increase the RAM (by default it's 6G), you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - ALLOCATED_RAM=8G
```

# Example

```yaml
services:
  minecraft:
    image: ghcr.io/andreaswachs/dungeons-like
    container_name: dungeons-like
    ports:
      - "25565:25565/tcp"
    volumes:
      - ./world:/home/minecraft/world
    restart: 'unless-stopped'
    environment:
      - ALLOCATED_RAM=8G
      - EULA=true
```

# Sending commands to the server console

If you want to send commands to the console you can leverage minecraft official rcon support, you would need to generate all server files by starting the server at least once and edit the `server.properties` rcon related fields 
```txt
enable-rcon=true
rcon.port=25575
rcon.password=<rcon_password>
```

Then you can send any command with the following syntax
```bash
docker exec -it dungeons-like sh -c "rcon -H localhost -p 25575 -P <rcon_password> <command>"
```

# Included Mods

This server is a Minecraft Forge 1.20.1 server packed with mods that recreate the Minecraft Dungeons experience.

## Core Dungeons Mods

- **Dungeons Content** - Adds Minecraft Dungeons weapons, armor, artifacts, and enemies into the game
- **Dungeons Content 2** - Expands on Dungeons Content with additional items, mobs, and features
- **L_Ender's Cataclysm** - Adds challenging boss fights with unique mechanics and rewards
- **EnchantWithMob** - Adds the enchanting mechanic from Minecraft Dungeons where mobs can be enchanted
- **Goety - The Dark Arts** - Adds a dark magic system with spells, rituals, and summoning
- **Echovoids** - Adds void-themed dimensions, bosses, and items
- **Valhelsia Structures** - Adds naturally generating structures including dungeons, castles, and ruins
- **Illage and Spillage: Respillaged** - Adds illager raids and boss encounters
- **Arthys' RPG Armory** - Adds RPG-style weapons, shields, and armor with unique abilities
- **Dungeons and Taverns** - Adds dungeons, taverns, and other structures to discover while exploring

## Combat Mods

- **Better Combat** - Spectacular melee combat system inspired by Minecraft Dungeons with sweep attacks and combo chains
- **Combat Roll** - Adds a combat roll ability for dodging attacks
- **Arrow In The Knee** - Adds arrow mechanics where mobs can be staggered by arrow hits

## Visual & QoL

- **Subtle Effects** - Subtle particle and visual effects that enhance the atmosphere (client optional on server)
- **Immersive Damage Indicators** - Shows damage numbers floating above mobs when hit (client only)
- **Perception** - Adds visual feedback for combat and status effects (client only)
- **Accessible Step** - Automatically step up full blocks without jumping (client only)
- **MobEffectsVFX** - Visual effects for mob status effects (client only)
- **Legendary Tooltips** - Enhanced tooltip styling for items (client only)
- **Equipment Compare** - Compare equipment stats side by side (client only)
- **Explosive Enhancement: Reforged** - Improved explosion visuals (client only)
- **Physics Mod** - Physics-based mob death animations and item physics (client only)

## Resource Packs & Shaders (in client modpack only)

- **Dungeons Style** - Resource pack that reskins the game to match Minecraft Dungeons aesthetics
- **Fresh Moves** - Player animation overhaul with animated eyes
- **Rethinking Voxels** - Shader pack with volumetric lighting and voxel-based rendering

## Library Dependencies

The following library mods are included as required by the mods above:

Curios API, Lionfish API, Bagus Lib, Patchouli, Valhelsia Core, Player Animator, Cloth Config, Fzzy Config, Kotlin for Forge, Iceberg, Prism, Immersive Messages API, TxniLib, Architectury API, OctoLib

# Client Modpack

A prebuilt client modpack is available as `dungeons-like.mrpack`. Import it into the Modrinth launcher via "Add instance from file". To rebuild it, run:

```bash
python3 build_modpack.py
```
