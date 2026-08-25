# Minecraft Unshare

A dedicated Minecraft server running **3D Shareware v1.34** (the April Fools 2019 version) with the [unshare](https://github.com/torzod/unshare) mod — a remake of tildejustin's shareware-multiplayer that makes the joke version pleasant to play for extended periods (removes the forced anaglyph 3D shader, disables demo mode, etc.).

## Running

```sh
docker run -d --name minecraft-unshare \
  -e EULA=true \
  -p 25565:25565 \
  -v ./world:/home/minecraft/world \
  ghcr.io/andreaswachs/minecraft-unshare:latest
```

Or with `docker compose up -d` (set `EULA=true` in the environment first).

Environment variables:

| Variable        | Default | Description                     |
|-----------------|---------|---------------------------------|
| `EULA`          | —       | Must be `true` to accept the [Minecraft EULA](https://aka.ms/MinecraftEULA) |
| `ALLOCATED_RAM` | `2G`    | Heap size for the server        |

This version officially requires Java 8, but runs fine on modern Java — the image defaults to **OpenJDK 21**. Pin `JAVA_PACKAGE=openjdk8-jre` at build time if you want era-correct Java.

The vanilla server jar bundles a 2017-era log4j vulnerable to log4shell (CVE-2021-44228) with no runtime mitigation flag, so `JndiLookup` is stripped from the jar at image build time.

## Client

Import `minecraft-unshare.mrpack` into the Modrinth App to create a matching client. The pack contains the unshare mod via overrides; no other mods are needed (the mod only depends on Fabric Loader).

Rebuild the pack after updating the jar: `python3 build_modpack.py`

## How the server is assembled

The fabric meta/installer "server" flow crashes on this version (`URISyntaxException`: it builds meta URLs from the raw version id `3D Shareware v1.34`, which contains spaces). The Dockerfile therefore assembles the server manually:

1. Vanilla `server.jar` downloaded directly from Mojang's piston-data CDN
2. Fabric runtime libraries (loader, mixin, ASM, intermediary) from maven.fabricmc.net
3. Launched via `net.fabricmc.loader.impl.launch.knot.KnotServer` with `-Dfabric.gameJarPath=server.jar`

## How the mod jar is built

Upstream publishes no releases, so `mods/unshare-1.0.1.jar` is built from source and committed here. To rebuild:

```sh
git clone https://github.com/torzod/unshare && cd unshare
```

Three patches are needed (upstream builds against a yarn mappings version that only exists in the author's local maven):

1. In `build.gradle`, add jitpack and point mappings at the published custom yarn:
   ```gradle
   repositories {
       mavenLocal()
       maven { url "https://jitpack.io" }
   }
   dependencies {
       mappings "dev.tildejustin:yarn:3d-shareware-v2:v2@jar"
   }
   ```
2. Plant the intermediary artifact locally — loom double-URL-encodes the spaces in the version name when resolving `net.fabricmc:intermediary:3D%20Shareware%20v1.34`. Download it once from the single-encoded URL and place all three path variants under `.gradle/loom-cache/minecraftMaven/net/fabricmc/intermediary/`:
   ```sh
   BASE=".gradle/loom-cache/minecraftMaven/net/fabricmc/intermediary"
   mkdir -p "$BASE/3D Shareware v1.34" "$BASE/3D%20Shareware%20v1.34" "$BASE/3D%2520Shareware%2520v1.34"
   curl -so "$BASE/3D Shareware v1.34/intermediary-3D Shareware v1.34.pom" \
     "https://maven.fabricmc.net/net/fabricmc/intermediary/3D%20Shareware%20v1.34/intermediary-3D%20Shareware%20v1.34.pom"
   curl -so "$BASE/3D Shareware v1.34/intermediary-3D Shareware v1.34-v2.jar" \
     "https://maven.fabricmc.net/net/fabricmc/intermediary/3D%20Shareware%20v1.34/intermediary-3D%20Shareware%20v1.34-v2.jar"
   # then copy+rename into the %20 and %2520 variants
   ```
   (The pom's `<version>` must match whichever variant resolves.)
3. Build with **Java 21** (`JAVA_HOME=$(/usr/libexec/java_home -v 21)`): `./gradlew build`

The remapped mod jar lands in `build/libs/unshare-<version>.jar`.
