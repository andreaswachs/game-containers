# Prerequisite

You need to accept EULA to run this server, you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - EULA=true
```

# Increasing RAM Allocation

If you need to increase the RAM (by default it's 8G), you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - ALLOCATED_RAM=8G
```

# Example

```yaml
services:
  minecraft:
    image: ghcr.io/andreaswachs/minecraft-enhanced
    container_name: minecraft-enhanced
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
docker exec -it minecraft-enhanced sh -c "rcon -H localhost -p 25575 -P <rcon_password> <command>"
```

# Included Mods

This server is a vanilla Minecraft Fabric server packed with popular mods focused on powerful items, cool equipment, and fun gameplay for kids.

## Weapons

- **Simply Swords** - Adds Spears, Glaives, Chakrams, Katanas, Greathammers, Greataxes, Rapiers, and many more weapon types with unique abilities
- **Better Combat** - Spectacular and fun melee combat system inspired by Minecraft Dungeons, with sweep attacks, combo chains, and weapon-specific animations

## Magic

- **Spell Engine** - Data-driven magic system that powers all spell mods below
- **Spell Power** - Spell power attributes, status effects, and enchantments
- **Wizards (RPG Series)** - Cast Arcane, Fire, and Frost spells. Become a wizard with spell books and wands
- **Paladins & Priests (RPG Series)** - Holy magic class with healing, buffs, and divine smites

## Equipment & Accessories

- **Trinkets** - Adds accessory slots for wearing rings, belts, and other trinkets
- **Elytra Slot** - Wear your elytra as an accessory so you can fly AND wear chest armor at the same time
- **Charm of Undying** - Place a Totem of Undying in an accessory slot for auto-revive without holding it
- **Traveler's Backpack** - Unique upgradeable backpacks with customization, fluid tanks, and sleeping bag
- **Immersive Armors** - A lot of unique and vanilla-faithful armor sets that look cool and provide distinct stats

## Quality of Life

- **VeinMiner** - Mine an entire ore vein or tree with a single block break. Hold the veinmine key (or sneak-mine) to activate
- **Enchanting Infuser** - Choose your enchantments at fair prices without the randomness of the enchanting table
- **Easy Anvils** - Overhauled anvils with stored enchantment items, fairer costs, and no more frustrating repair penalties

## World & Adventure

- **Terralith** - Massive world generation overhaul with 94 new biomes, towering mountains, canyons, and unique cave systems. All vanilla-friendly, no new blocks needed
- **Dungeons and Taverns** - Adds dungeons, taverns, and other structures to discover while exploring, full of loot and challenges
- **When Dungeons Arise** - Massive naturally-spawning dungeons with multiple rooms, floors, and epic loot

## Navigation

- **Nature's Compass** - Locate any biome anywhere in the world and have your compass point you to it
- **Explorer's Compass** - Search for any structure and have your compass guide you directly to it
- **Waystones** - Teleport from waystone to waystone, or craft magical scrolls to warp back to base
- **Xaero's Minimap** - Clean minimap with entity, waypoint, and cave rendering
- **Xaero's World Map** - Full-screen world map that fills in as you explore

## Visual & Fun

- **Dancerizer** - Perform taunts and whole dances! Equip dance accessories and bust a move with your friends
- **LambDynamicLights** - Dynamic lighting that illuminates the world around held torches, glowing items, and mobs (client only)

## Building

- **Chipped** - Hundreds of new block variants for building: bricks, wood, glass, and more with unique textures
- **Macaw's Doors** - Dozens of new door styles from modern to rustic
- **Macaw's Bridges** - Build bridges of all types: rope, wood, metal, and more

## Performance

- **Lithium** - Optimizes game physics, mob AI, and block ticking (server + client)
- **FerriteCore** - Reduces memory usage by optimizing how the game stores blocks, items, and chunks (server + client)
- **Krypton** - Optimizes the network stack for smoother multiplayer (server + client)
- **Sodium** - Rewrites the rendering engine for massive FPS improvements (client only)
- **Indium** - Provides Fabric Rendering API compatibility for Sodium, so addon mods render correctly (client only)
- **Entity Culling** - Skips rendering of entities that aren't visible to the player (client only)

## Library Dependencies

The following library mods are included as required by the addon mods above:

- Architectury API, Fzzy Config, Simply Tooltips, Player Animator, Cloth Config, Cardinal Components API, Balm, Puzzles Lib, Forge Config API Port, Fabric Language Kotlin, Structure Pool API, Runes, AzureLib Armor, Resourceful Lib, Athena

# Client Modpack

A prebuilt client modpack is available as `minecraft-enhanced.mrpack`. Import it into the Modrinth launcher via "Add instance from file". To rebuild it, run:

```bash
python3 build_modpack.py
```
