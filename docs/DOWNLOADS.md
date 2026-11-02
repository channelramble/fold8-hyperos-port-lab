# Installation downloads and project credits

The three installer APKs are attached to the [GitHub release](https://github.com/channelramble/fold8-hyperos-port-lab/releases/tag/install-kit-2026-11-02).
This repository remains private; sign in with repository access to download them.
Open the [step-by-step guide](INSTALL-GUIDE.md) first. These are original,
unchanged upstream files; this kit is not an official project release.

## Installer APKs

| Download | Size | Original project / credit |
| --- | ---: | --- |
| [OneOS-0.4.37-fold.apk](https://github.com/channelramble/fold8-hyperos-port-lab/releases/download/install-kit-2026-11-02/OneOS-0.4.37-fold.apk) | 1,512,993,289 bytes | [fahadalijaved / OneOS](https://github.com/fahadalijaved/OneOS) |
| [DFRoot_4.7.apk](https://github.com/channelramble/fold8-hyperos-port-lab/releases/download/install-kit-2026-11-02/DFRoot_4.7.apk) | 84,071 bytes | [diabl0w / DFRoot 4.7](https://github.com/diabl0w/DFRoot/releases/tag/v4.7) |
| [KernelSU_samsung-v2.2_32687-release.apk](https://github.com/channelramble/fold8-hyperos-port-lab/releases/download/install-kit-2026-11-02/KernelSU_samsung-v2.2_32687-release.apk) | 7,607,475 bytes | [diabl0w / Samsung KernelSU 2.2](https://github.com/diabl0w/KernelSU/releases/tag/samsung-v2.2), based on [KernelSU](https://github.com/tiann/KernelSU) |

Download the named assets from the release; the automatic source-code ZIP does
not contain APKs. Installing a manager alone does not activate root.

## Large OS images — external downloads only

These three images remain in **My Files > Internal storage > Download >
OneOS-Install** on the prepared phone. They are not uploaded to GitHub.
Each link opens the maintainer's download folder; select the exact filename.
Keep `.img.gz` files compressed for OneOS.

| Image to select in the folder | Size |
| --- | ---: |
| [OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz](https://gofile.io/d/A2PSsxv8) | 4,666,011,150 bytes |
| [OneOS_ColorOS17_FindN6_ZFold8.img.gz](https://gofile.io/d/A2PSsxv8) | 5,285,345,619 bytes |
| [OneOS_Pixel11Fold_Full_ZFold8.img.gz](https://gofile.io/d/A2PSsxv8) | 3,288,346,862 bytes |

Image integration: [OneOS](https://github.com/fahadalijaved/OneOS), using
[MysticGSI](https://github.com/MysticGSI/mysticgsi) and its credited
[TrebleDroid](https://github.com/TrebleDroid) work. Underlying software is from
Xiaomi, OPPO and Google. Additional architecture and Fold8 contributor credits
are linked at the relevant steps in the installation guide.

## SHA-256 checks

The release's `SHA256SUMS` covers its APKs and guide. The phone folder's
`SHA256SUMS` additionally covers the large images, manifest and local documents.
On a Mac, run `shasum -a 256 -c SHA256SUMS` from the matching downloaded folder.

| File | SHA-256 |
| --- | --- |
| `OneOS-0.4.37-fold.apk` | `bd70190031ceaf3b1108825036cf59fe594aaa5bdf3eb1efa7aa955838e2775e` |
| `OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz` | `745e43c2d116c4277af06b65c5d8fbaefec11731dcc23f0c067631fce04554a3` |
| `OneOS_ColorOS17_FindN6_ZFold8.img.gz` | `4d371cbeb5da0b7c4b67ff44ce437ca56a244b0e3a93e1a696099ab6071d1809` |
| `OneOS_Pixel11Fold_Full_ZFold8.img.gz` | `8fbe950c47629c439af0807fc6bbb2afa29308c65c215849bcfa7a01f6b9290d` |
| `DFRoot_4.7.apk` | `9e193ffdaada8577e14a04fb19403256b3fa4991fae1331c7956e083c098a7b1` |
| `KernelSU_samsung-v2.2_32687-release.apk` | `761dffad54ae080a4977971db7b04e2fc65c2d9b5e2336accca4a85661290a69` |

Checksums establish file integrity, not runtime compatibility. Guest boot,
return and VoLTE remain unverified on this SM-F971U1. The kit does not need
OneLineage installed separately or any older custom-port/debug IMS binaries.
