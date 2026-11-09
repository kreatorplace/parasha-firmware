# Parasha Display · firmware updates

Software for the Kreator Place Parasha Display (Seeed XIAO ESP32-C3 with a 4.2" or 7.5" e-paper panel).

- **Install by USB (new units):** https://kreatorplace.github.io/parasha-firmware/
- **Updates over WiFi:** each display checks this repository's **Releases** when it's plugged in and every day just after midnight.
  It installs a release only if it's newer than what's running and signed with the Kreator Place key.

## Publishing an update (automatic)

New firmware is pushed to `incoming/` (`parasha-4.2in.bin`, `parasha-7.5in.bin`, `NOTES.md`).
The **Publish release** workflow (Actions tab) then signs it with the `SIGNING_KEY` secret, publishes the
release as **Latest** and updates the install page. Displays install it when plugged in, or just after midnight.

The workflow stops with an error if the secret isn't the key built into the displays (fingerprint BE6C655B).
The [release tool](https://kreatorplace.github.io/parasha-firmware/release-tool.html) still works for
signing by hand.

## What's in a release

| File | What it is |
|---|---|
| `parasha-4.2in.bin` | Firmware for the 4.2" display |
| `parasha-7.5in.bin` | Firmware for the 7.5" display |
| `manifest.json` | Version, file sizes, SHA-256 and signatures |

The signing key (`parasha-signing-key.pem`) is never stored here.

Calendar data on the displays: [Hebcal.com](https://www.hebcal.com) (CC BY 4.0). City locations: [GeoNames](https://www.geonames.org) (CC BY 4.0).
