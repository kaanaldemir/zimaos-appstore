# Kaan Aldemir Apps

Personal community app store for ZimaOS. Add this URL under App Store → Community store → Add:

`https://kaanaldemir.github.io/zimaos-appstore/store.json`

Legacy ZIP fallback: `https://kaanaldemir.github.io/zimaos-appstore/store/main.zip`

The catalog contains Paperkeep, Smart Control, Piano Studio, Project Zomboid, Shinobi and Headplane. Paperkeep is included while its GHCR image is publicly downloadable. Only amd64 is advertised because these personal images are built for the mini PC architecture.

## Updates

GitHub Actions refreshes the catalog every six hours, on source changes and on manual dispatch. It resolves publicly available image manifests, pins image digests, and updates an app's package version only when its image set or source definition changes. ZimaOS handles installation and applying updates. This does not automatically install software or restart existing apps.

Existing custom app installations are not automatically adopted by a new store entry. Keep their configuration and data; review any migration separately. New entries use separate data directories and may have ports already occupied by an existing app. Edit the installation settings before installing.

## Adding another application

Add `Apps/AppName/docker-compose.yml` and an icon, using standard Compose plus the official top-level `x-casaos` metadata. Register it in `catalog.json`. Use a public Linux container image and keep secrets out of the repository. A successful catalog build validates packaging and image architecture; it does not claim that every application's configuration has been runtime-tested.

Paperkeep's source repository remains private. Its image contains application code but no writing or private configuration. Windows desktop tools, Android apps, undeployed Python experiments, and the static personal website are excluded because they do not currently provide a suitable server image. New compatible apps can be packaged here later.

## Sources

- [Official ZimaOS store creation guide](https://github.com/IceWhaleTech/CasaOS-AppStore/blob/main/docs/quick-start/overview.md)
- [Official build action](https://github.com/IceWhaleTech/build-appstore-action)

Each app retains its upstream developer and repository attribution. Store recipes do not change upstream licensing.
