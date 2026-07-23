# Prerequisite

You need to accept EULA to run this server, you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - EULA=true
```

# Increasing RAM Allocation

If you need to increase the RAM (by default it's 4GB), you can do so by adding the following environment variable to the service configuration:

```yaml
environment:
  - ALLOCATED_RAM=8G
```

# Example

```yaml
services:
  cobblemon-enhanced:
    image: ghcr.io/andreaswachs/cobblemon-enhanced
    container_name: cobblemon-enhanced
    ports:
      - "25565:25565/tcp"
    volumes:
      - ./world:/home/cobblemon/world
    restart: 'unless-stopped'
    environment:
      - ALLOCATED_RAM=12G
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
docker exec -it cobblemon-enhanced sh -c "rcon -H localhost -p 25575 -P <rcon_password> <command>"
```

# Included Addon Mods

This server goes beyond vanilla Cobblemon with the following addon mods:

## Mega Evolution

- **Mega Showdown** - Adds Mega Evolution, Z-Moves, Terastallization, Dynamax, Ultra Burst, and Fusions
- **Navas ZA Megas** - Adds all Mega Evolutions from Pokemon Legends Z-A
- **Mega Showdown Item Pack** - Adds recipes and loot tables for Mega Stones and related items

## Missing Pokemon / Legendaries

- **Myths and Legends** - Adds key items and spawning conditions for Legendary and Mythical Pokemon encounters
- **Legendary Monuments** - Adds special monument structures that spawn Legendaries (Zacian, Zamazenta, Reshiram, Zekrom, Kyurem, Hoopa, Cosmog, Keldeo, Regigigas, all Regis, Swords of Justice, Legendary Birds, and more)
- **Legends & Myths** - Adds legendary and mythical Pokemon with new structures to explore
- **Complete Cobblemon Collection** - Adds models, spawns, and animations for Pokemon not yet in vanilla Cobblemon

## Gyms + Elite Four / Trainers

- **Radical Cobblemon Trainers** - Over 1500 unique trainers from Radical Red, Unbound, and Brilliant Diamond/Shining Pearl that spawn naturally in the world
- **Radical Cobblemon Trainers API** - Trainer management and battle API (required by RCT)
- **Rad Gyms** - Roguelike gym battles built on the RCT API

## Library Dependencies

The following library mods are included as required by the addon mods above:

- Architectury API, Accessories, owo-lib, Lithostitched, Chipped, Forge Config API Port, Resourceful Lib, Athena

# Client Modpack

A prebuilt client modpack is available as `cobblemon-enhanced.mrpack`. Import it into the Modrinth launcher via "Add instance from file". To rebuild it, run:

```bash
python3 build_modpack.py
```
