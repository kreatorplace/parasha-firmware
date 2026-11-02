# Parasha Display · firmware updates

Software for the Kreator Place Parasha Display (Seeed XIAO ESP32-C3 with a 4.2" or 7.5" e-paper panel).

- **Install by USB (new units):** https://kreatorplace.github.io/parasha-firmware/
- **Updates over WiFi:** each display checks this repository's **Releases** when it's plugged in and every day at 6 AM.
  It installs a release only if it's newer than what's running and signed with the Kreator Place key.

## Publishing an update

1. Open the [release tool](https://kreatorplace.github.io/parasha-firmware/release-tool.html), load the signing key file and the new `.bin` files.
2. Click **Sign and create release files** and download the 3 files.
3. **Releases → Draft a new release**, tag `v<version>`, drag in the 3 files.
   - **Test first:** tick *Set as a pre-release*. Only displays switched to the test channel (Demo page) install it.
   - **Everyone:** keep *Set as the latest release* ticked.
4. **Publish release.**

To move a test release to everyone: **Edit** the release, untick *pre-release*, tick *latest*, **Update release**.

## What's in a release

| File | What it is |
|---|---|
| `parasha-4.2in.bin` | Firmware for the 4.2" display |
| `parasha-7.5in.bin` | Firmware for the 7.5" display |
| `manifest.json` | Version, file sizes, SHA-256 and signatures |

The signing key (`parasha-signing-key.pem`) is never stored here.

Calendar data on the displays: [Hebcal.com](https://www.hebcal.com) (CC BY 4.0). City locations: [GeoNames](https://www.geonames.org) (CC BY 4.0).
