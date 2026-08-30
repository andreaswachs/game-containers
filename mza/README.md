# Prerequisite

You need to accept EULA to run this server, you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - EULA=true
```

# Increasing RAM Allocation

If you need to increase the RAM (by default it's 4G), you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - ALLOCATED_RAM=4G
```

# Example

```yaml
services:
  minecraft:
    image: ghcr.io/andreaswachs/mza
    container_name: mza
    ports:
      - "25565:25565/tcp"
    volumes:
      - ./world:/home/minecraft/world
    restart: 'unless-stopped'
    environment:
      - ALLOCATED_RAM=4G
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
docker exec -it mza sh -c "rcon -H localhost -p 25575 -P <rcon_password> <command>"
```

# About

This server hosts the [MZA (Minecraft Zombie Apocalypse)](https://modrinth.com/modpack/mza) modpack. It is a Minecraft 1.20.1 modpack built on Forge where you use the Create mod to build defenses, gear up with powerful weapons, and survive in a post-apocalyptic world.

## Technical Details

- **Minecraft**: 1.20.1
- **Forge**: 47.3.0
- **Java**: 17
- **Modpack version**: MZA 1.2.0

Client-only mods (rendering, shaders, visual) are excluded from the server image to prevent crashes. The following mods are included on the server:

- **Create** - Core machinery and automation mod
- **Create Additions** - Adds electricity and energy systems to Create
- **Steam 'n' Rails** - Create addon for trains and railways
- **PointBlank** - Guns and weapons mod
- **PointBlank Recipe Gunpacks** - Gun recipe pack for PointBlank
- **Easy Villagers** - Villager trading and breeding
- **JEI** - Recipe viewer (server-side support)
- **Jade** - Block/entity information display (server-side data sync)
- **TerraBlender** - Biome generation support
- **GeckoLib** - Animation library
- **Cloth Config** - Configuration library
- **Searchables** - Search library (required by JEI)
