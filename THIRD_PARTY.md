# Source attribution and licensing

The candidate builder incorporates OneOS Python guard scripts and build tooling
from https://github.com/fahadalijaved23/OneOS at the commit in inputs/manifest.json.
Their Apache-2.0 license and upstream NOTICE/CREDITS are retained under licenses/.
The modified files and new port tooling are identified by patches/OneOS.patch.

OneOS's NOTICE separately restricts reuse of its OneLineage-derived session
scripts. Those switcher/assets scripts are not vendored here; the checkout helper
retrieves upstream for local development. No independent redistribution permission
for those scripts is asserted by this repository.

The IMS patch applies to https://github.com/Samsung-Galaxy-A05/vendor_phhims.
Its source files use GPL-2.0 SPDX notices and its RNNoise dependency has separate
upstream terms. The complete upstream implementation, native dependency and APK
binaries are not redistributed here. Preserve those notices when building or
redistributing a derivative. IMS-specific additions accompany that GPL-2.0 work.

The Android platform JAR is a compile-only external input. Samsung/Xiaomi ROM
images, framework binaries, proprietary applications, certificates' private keys
and modem firmware are not part of this repository. Source links and checksums
identify locally inspected inputs and do not grant redistribution rights.

Independent Python tooling and documentation added for this lab are provided
under Apache-2.0, except IMS-specific derivatives which follow the IMS source's
GPL-2.0 terms. See licenses/OneOS-LICENSE for the Apache-2.0 text.
