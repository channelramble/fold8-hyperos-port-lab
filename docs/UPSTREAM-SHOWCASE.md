# Prepared upstream showcase kit — November 2, 2026

The recommended install path is now **OneOS 0.4.37 Fold edition**, with the
maintainer's HyperOS Xiaomi18Fold image. This is a different image from the
older AxisGSI `dada` custom port in this repository. None of our old framework
patches, native binaries or IMS debug APKs are included in the showcase kit.

The maintainer repository moved to [fahadalijaved/OneOS](https://github.com/fahadalijaved/OneOS).
We inspected source commit `082fe8604edc7360de7da4a1ee6016e0282091f2`.
The `releases/latest` endpoint returned v0.4.29, while source and the
[maintainer-linked download folder](https://gofile.io/d/A2PSsxv8) contained
0.4.37. The actual downloaded APK identifies itself as `com.fahadali.oneos`,
versionCode 54, versionName `0.4.37-fold`.

## Files prepared locally

- `OneOS-0.4.37-fold.apk`
- `OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz`
- `OneOS_ColorOS17_FindN6_ZFold8.img.gz`
- `OneOS_Pixel11Fold_Full_ZFold8.img.gz`

They live under `$WORKSPACE/outputs/Fold8-Showcase/files`. Binary files are not
committed or redistributed through this GitHub repository.

The [manifest](../inputs/upstream-showcase-20261102.json) records exact sizes and
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

All four install files, both guides, the manifest and checksums were copied to
`/sdcard/Download/OneOS-Showcase` and independently SHA-256 verified on the phone.
See [the transfer report](../reports/showcase-phone-transfer.json). Boot, return,
calls, camera and both screens remain untested on this exact device.

## Simple recording flow

Use [SHOWCASE-GUIDE.txt](SHOWCASE-GUIDE.txt) for the five-step phone guide and
[VIDEO-CHECKLIST.txt](VIDEO-CHECKLIST.txt) for a short filming plan. Root and the
upstream lock-removal prerequisite must be satisfied before switching. The
guide leaves the lock bypass and experimental IMS option off for the first
visual demo. HyperOS's return may reboot; temporary root may not survive.

## VoLTE

Current upstream exposes **Advanced > Use One UI's calling service (VoLTE)**.
It stages the phone's own Samsung IMS service into the guest. This is more
relevant to the showcase package than installing our older PhhIms debug APK.
It remains experimental; neither source code nor a toggle proves registration,
carrier voice support, call audio or cleanup on this phone. The
[upstream IMS design](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/docs/samsung-ims-in-guest.md)
includes older status statements; current UI/source/package lists establish
availability of the option, not success of its runtime behavior.

Only after guest boot and return work should a separate supervised ordinary
call test evaluate registration, incoming/outgoing calls, two-way audio, DTMF,
hang-up and recovery in One UI. Do not test emergency numbers. No VoLTE claim
is made for the user's carrier.
