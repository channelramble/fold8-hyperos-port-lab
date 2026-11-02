November 2 update: the upstream OneOS kit now contains a HyperOS option.
See [the current showcase guide](SHOWCASE-GUIDE.txt) and
[verified package findings](UPSTREAM-SHOWCASE.md). HyperOS, ColorOS and Pixel
images have been downloaded and verified locally. OriginOS/Flyme/MagicOS remain
research leads. The October 25 snapshot below is historical.

# Chinese-skin sources

Research snapshot from October 25, 2026; this is not a compatibility guarantee.

| Skin | Source | Preparation state |
| --- | --- | --- |
| HyperOS 17 | [AxisGSI](https://sourceforge.net/projects/axisgsiupdates/files/hyperos/) | Download/hash verification and offline patch builds completed; no phone boot |
| ColorOS 17 | [OneOS v0.4.13](https://github.com/fahadalijaved23/OneOS/releases/tag/v0.4.13), [maintainer files](https://gofile.io/d/A2PSsxv8) | Fold-oriented OneOS candidate identified; no completed local download/test |
| OriginOS | [MysticGSI](https://sourceforge.net/projects/mystic-gsi-updates/files/OriginOS/) | Community GSI source identified; not downloaded or ported |
| Flyme | [MysticGSI](https://sourceforge.net/projects/mystic-gsi-updates/files/Flyme/) | Community GSI source identified; not downloaded or ported |
| MagicOS | [AxisGSI](https://sourceforge.net/projects/axisgsiupdates/files/magicos/) | Community GSI source identified; not downloaded or ported |

HyperOS was explicitly prioritized. The other rows are research leads, not ready
images for this Fold. Android version matching alone does not establish device,
vendor HAL, Binder, display or carrier compatibility.

The identified OneOS ColorOS filename was OneOS_ColorOS17_FindN6_ZFold8.img.gz,
with published expected SHA-256
`4d371cbeb5da0b7c4b67ff44ce437ca56a244b0e3a93e1a696099ab6071d1809`.
That hash was not verified against a completed local ColorOS file. The live file
folder showed later APK versions than the pinned GitHub source; their behavior
was not audited. Do not substitute them silently in this reproducible build.
