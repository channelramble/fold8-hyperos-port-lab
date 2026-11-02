# Prepared upstream installation kit — November 2, 2026

The recommended install path is now **OneOS 0.4.37 Fold edition**, with the
maintainer's HyperOS Xiaomi18Fold image. This is a different image from the
older AxisGSI `dada` custom port in this repository. None of our old framework
patches, native binaries or IMS debug APKs are included in the installation kit.

The maintainer repository moved to [fahadalijaved/OneOS](https://github.com/fahadalijaved/OneOS).
We inspected source commit `082fe8604edc7360de7da4a1ee6016e0282091f2`.
The `releases/latest` endpoint returned v0.4.29, while source and the
[maintainer-linked download folder](https://gofile.io/d/A2PSsxv8) contained
0.4.37. The actual downloaded APK identifies itself as `com.fahadali.oneos`,
versionCode 54, versionName `0.4.37-fold`.

## Files prepared locally

The kit now also includes DFRoot 4.7 and Samsung KernelSU 2.2. Their exact
release SHA-256 values and successful APK v2 signature checks are recorded in
[the root-installer report](../reports/root-installers-20261102.json). These
are installers only; no new root activation was performed.


- `OneOS-0.4.37-fold.apk`
- `OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz`
- `OneOS_ColorOS17_FindN6_ZFold8.img.gz`
- `OneOS_Pixel11Fold_Full_ZFold8.img.gz`

They live under `$WORKSPACE/outputs/Fold8-Install/files`. Binary files are not
committed or redistributed through this GitHub repository.

The [manifest](../inputs/upstream-install-20261102.json) records exact sizes and
image hashes from upstream `Images.kt`. All three compressed SHA-256 hashes,
decompressed sizes and decompressed SHA-256 hashes were verified. Decompression
was streamed through a hash, also checking gzip integrity. Safari automatically
expanded the two new image downloads; their original compressed archives were
recovered through Finder and verified, not recompressed.

The APK matches the download folder's size and MD5. MD5 is a publisher
cross-check, not a modern cryptographic authenticity guarantee. Its locally
computed SHA-256 is
`bd70190031ceaf3b1108825036cf59fe594aaa5bdf3eb1efa7aa955838e2775e`.
Android's APK v2 signature verifies; signer certificate SHA-256 is
`37560f7ba9e82a7977c239b77a47c7fa6df0f381cdad44810ffdcab12295f83a`.
The signer has not been independently authenticated against a separately
published certificate fingerprint.

All seven packaged system-file lists match the current source entries after
normalizing their ordering. All 188 unique content-addressed assets match their
packaged hashes. Fourteen session files match the source byte-for-byte; two
(`guest_prepare.sh`, `oneos_switch.sh`) differ only in reviewed comment text
that anonymizes historical examples. This is artifact integrity and source
comparison evidence, not a full reproducible APK build or a runtime audit.

## Phone and installation status

The connected phone is SM-F971U1 / h8q / SM8850, Android 17 SDK 37, build
`CP2A.260605.016.F971U1UES3AZIL`. It matches upstream's Fold8 profile inputs.
Profile acceptance does not demonstrate compatibility on the US U1 variant.
The fresh baseline is in [the device preflight](../reports/device-preflight-20261102.json).

No `su` command was available on the ADB shell path. Verified boot was green,
flash locked=1, SELinux Enforcing and the shell UID was 2000. Working root is
still required before a guest can run. No new root trial, APK installation,
guest launch, lock change or carrier modification was performed.

The four large install files were transferred and verified as recorded in
[the original transfer report](../reports/showcase-phone-transfer.json).
The folder is now `/sdcard/Download/OneOS-Install`; two verified root installers
were added, and the old guides were replaced by installation-only instructions.
See [the update report](../reports/install-guide-phone-update.json) and
[the final document sync](../reports/install-guide-final-sync.json).
Boot, return, calls, camera and both screens remain untested on this exact phone.

## Installation instructions

[INSTALL-GUIDE.md](INSTALL-GUIDE.md) starts with no root manager and includes
manual activation, OneOS's root check, image setup, return, troubleshooting and
removal. Every numbered stage has project/source credit. Root and the upstream
lock-removal prerequisite must be satisfied before switching. The guide keeps
automatic rooting, the lock bypass and experimental IMS off for initial tests.

## VoLTE

Current upstream exposes **Advanced > Use One UI's calling service (VoLTE)**.
It stages the phone's own Samsung IMS service into the guest. This is more
relevant to the installation package than installing our older PhhIms debug APK.
It remains experimental; neither source code nor a toggle proves registration,
carrier voice support, call audio or cleanup on this phone. The
[upstream IMS design](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/docs/samsung-ims-in-guest.md)
includes older status statements; current UI/source/package lists establish
availability of the option, not success of its runtime behavior.

Only after guest boot and return work should a separate supervised ordinary
call test evaluate registration, incoming/outgoing calls, two-way audio, DTMF,
hang-up and recovery in One UI. Do not test emergency numbers. No VoLTE claim
is made for the user's carrier.
