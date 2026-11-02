# [GUIDE] HyperOS, ColorOS and Pixel through OneOS on Galaxy Z Fold8 SM-F971U1

**Updated: November 2, 2026.** This guide starts with no root manager installed.
It uses **DFRoot 4.7**, **Samsung KernelSU 2.2** and **OneOS 0.4.37 Fold**.
It is an independent installation guide, not an official XDA or project release.

OneOS runs another Android environment using the Samsung kernel while One UI
remains installed. DFRoot supplies temporary root; Samsung KernelSU manages
which apps may use it. Installing a root-manager APK alone does not root a phone.

**What has actually been verified:** these exact root-tool versions obtained
root on this particular phone/build on October 25, then were removed and the
phone rebooted. The prepared OneOS APK and images passed integrity checks.
The guest systems, their return paths and VoLTE have not been tested on this
SM-F971U1. Root success on one build does not establish support for other builds.

## 1. Check the phone and prepare a backup

1. Open **Settings > About phone** and confirm **SM-F971U1**.
2. Under **Software information**, confirm Android **17**, One UI **9** and
   build ending **F971U1UES3AZIL**. The recorded full build is
   `CP2A.260605.016.F971U1UES3AZIL`; the kernel is
   `6.12.58-android16-6-p47945c2-abogkiF971USQS3AZIL-4k`.
3. If the model, firmware or kernel differs, stop and reassess the root route.
   Do not downgrade or flash a different boot image to force a match.
4. Back up important files, accounts and recovery codes somewhere other than
   this phone. Keep access to another phone for calls during guest testing.
5. Charge above 30%, let the phone cool below 42 C and check free storage.
   The downloaded files total about 14.8 GB; extracting HyperOS adds about
   7.75 GB, ColorOS 10.28 GB, or Pixel 6.56 GB, before overlays and guest data.
   Set up one system first and respect OneOS's free-space check.

This is experimental software with a risk of data loss. No full stock-firmware
reflash package has been validated in this kit. A restart is not a guaranteed
recovery from every failure; severe failure may require Samsung service.

**Source / credit:** [OneOS requirements](https://github.com/fahadalijaved/OneOS#readme)
and its [Fold8 profile](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/app-android/core/model/src/main/kotlin/com/fahadali/oneos/core/model/Profiles.kt).
The exact prior root result is local testing evidence, not an upstream guarantee.

## 2. Locate the installation files

On the prepared phone, open **My Files > Internal storage > Download > OneOS-Install**.

| File | Purpose / original project |
| --- | --- |
| `DFRoot_4.7.apk` | Temporary root tool — [diabl0w/DFRoot 4.7](https://github.com/diabl0w/DFRoot/releases/tag/v4.7) |
| `KernelSU_samsung-v2.2_32687-release.apk` | Root manager — [diabl0w's Samsung KernelSU 2.2](https://github.com/diabl0w/KernelSU/releases/tag/samsung-v2.2) |
| `OneOS-0.4.37-fold.apk` | Fold-specific guest installer/switcher — [OneOS](https://github.com/fahadalijaved/OneOS) |
| `OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz` | HyperOS image for this OneOS route |
| `OneOS_ColorOS17_FindN6_ZFold8.img.gz` | ColorOS 17, Find N6 image |
| `OneOS_Pixel11Fold_Full_ZFold8.img.gz` | Pixel 11 Fold image |

Keep the image files compressed. OneOS extracts them. Do not use the older
AxisGSI `dada` ZIP, our custom patch candidates or the separate PhhIms debug APKs.

For a fresh download, obtain the root apps from the linked releases and the
OneOS app/images from the [maintainer-linked folder](https://gofile.io/d/A2PSsxv8).
Use the **fold** APK, not **s25** or **s26**. Versions here are deliberately
pinned; a later release needs its own checks. `manifest.json` and `SHA256SUMS`
accompany the prepared files.

**Image credit:** OneOS prepares and integrates these guest images using
[MysticGSI](https://github.com/MysticGSI/mysticgsi), which also credits
[TrebleDroid](https://github.com/TrebleDroid). Xiaomi, OPPO and Google produce
the underlying HyperOS, ColorOS and Pixel software respectively; they do not
endorse these Samsung ports. See [OneOS's credits](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/CREDITS.md).

## 3. Install the root tool and manager

1. Tap `DFRoot_4.7.apk` in My Files and install it.
2. Tap `KernelSU_samsung-v2.2_32687-release.apk` and install it.
3. If Android requests permission for My Files to install unknown apps, grant
   that permission for these verified files. Revoke it after installation.
   If a different security control blocks installation, read its exact message
   before changing settings; this guide does not require disabling protections
   wholesale.
4. Open Samsung KernelSU once. It may show root is unavailable at this point.
   Keep **Auto jailbreak OFF** if that setting is present. Install no modules.
5. Open DFRoot's settings. Keep **Start at Boot OFF** and **Auto Soft Reboot OFF**.

These are the app installations for the temporary-root route previously tested
on this phone. There is no bootloader-unlock, Odin, Magisk boot-patching or
custom-kernel flashing step in this procedure.

**Source / credit:** [DFRoot usage and FAQ, pinned to 4.7](https://github.com/diabl0w/DFRoot/blob/v4.7/README.md)
and [Samsung KernelSU by diabl0w](https://github.com/diabl0w/KernelSU), a fork of
[KernelSU](https://github.com/tiann/KernelSU).

## 4. Activate temporary root manually

1. Return to DFRoot's main screen.
2. In **Select a SU Manager**, choose the installed Samsung KernelSU manager.
3. Tap **Launch Root** once and wait for the result. This is the step that
   changes privileged runtime state; installing the APKs did not do that.
4. Open Samsung KernelSU. The earlier successful run showed
   **Working [Jailbreak mode]**. An APK installed or a DFRoot success toast
   alone is not enough; verify usable root in step 5.
5. If DFRoot reports patch failure, the phone freezes, or the manager never
   becomes working, stop. Use the recovery section rather than repeatedly
   launching root or trying unrelated kernel files.

Keep automatic root activation disabled. Temporary root can disappear after
a full restart. After a successful session followed by a restart, check the
manager before using OneOS again; manual reactivation may be necessary.

**Source / credit:** [DFRoot](https://github.com/diabl0w/DFRoot/blob/v4.7/README.md),
including its [Launch Root interface](https://github.com/diabl0w/DFRoot/blob/v4.7/app/src/main/res/layout/activity_main.xml).
DFRoot implements a DirtyFrag-based root route; its detailed upstream credits
are in that project's README. Root does not unlock the bootloader.

## 5. Install OneOS and give it root access

1. Install `OneOS-0.4.37-fold.apk`, then open OneOS once.
2. Open **Samsung KernelSU > Superuser**, find **OneOS**
   (`com.fahadali.oneos`) and allow superuser access for that app.
3. Return to OneOS's device report and tap **Check root**. It runs `su -c id`;
   continue only if the result confirms root (`uid=0`).
4. Run OneOS's **Run tests** and review compatibility results. Do not bypass a
   failed check. These read-only checks do not prove a guest will boot.

ADB Root is not needed for this app-driven setup. A separate ADB shell may
remain unprivileged even when OneOS has a valid root grant.

**Source / credit:** [OneOS root-check and permission instructions](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/app-android/app/src/main/res/values/strings.xml).

## 6. Prepare One UI before switching

1. Confirm the backup is usable and normal calls work in One UI.
2. Following OneOS's prerequisite, manually set the screen-lock type to
   **None** or **Swipe**, with no PIN, pattern, password, fingerprint or face
   lock. Samsung may remove biometric credentials when you change this.
3. Leave OneOS's **Risky** lock bypass OFF and keep its heat protection enabled.
4. Keep the experimental VoLTE option OFF for the initial boot/return test.

**Source / credit:** [OneOS Getting started](https://github.com/fahadalijaved/OneOS#readme).

## 7. Set up HyperOS

1. In OneOS, open **Systems > HyperOS > I have the file**.
2. Select `OneOS_HyperOS_Xiaomi18Fold_ZFold8.img.gz` from **Download > OneOS-Install**.
3. Tap **Set up**. Keep OneOS open and the phone connected to power; allow
   around 15 minutes, depending on storage speed.
4. Wait for image verification and preparation to complete. If OneOS rejects
   the file, model or available space, resolve the stated problem first.
5. Tap **Switch** and read the displayed compatibility notice. This remains
   an experimental configuration on the SM-F971U1.
6. On first boot, skip optional account sign-in and do not create a guest
   screen lock. Check touch, both displays, folding, Wi-Fi, sound and heat.
   The selected HyperOS and ColorOS images do not include Google apps.

**Source / credit:** [OneOS](https://github.com/fahadalijaved/OneOS) and its
[HyperOS integration notes](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/docs/hyperos.md).
The guest-switching architecture began with
[OneLineage by WeWaffles](https://github.com/WeWaffles/OneLineage).
OneLineage/OneHyper is not an additional app required for this installation.

## 8. Return to One UI and check recovery

1. Open the OneOS app inside the guest and tap **Back to One UI**, or hold
   **Volume Up + Volume Down together for 3 seconds**.
2. Expect HyperOS's return to restart the phone for this image/build. Wait
   for stock One UI and unlock it normally if prompted.
3. Confirm files, Wi-Fi, SIM/subscriptions, audio and ordinary calls still work.
4. Check Samsung KernelSU again. If root was lost, a later guest session needs
   manual root activation first. Do not turn on automatic rooting to skip this.

If stuck on a frozen screen or logo, hold **Side/Power + Volume Down** for
until the phone restarts; Samsung notes this can take up to 60 seconds. If a
maintenance menu appears, select Normal Boot. If startup remains unstable,
DFRoot's FAQ describes holding Volume Down during boot to enter Safe Mode;
uninstall the new root apps there if needed. Do not improvise a firmware flash.

**Source / credit:** [OneOS return instructions](https://github.com/fahadalijaved/OneOS#readme),
[Samsung forced restart](https://www.samsung.com/us/support/troubleshoot/TSG10013330/)
and [DFRoot recovery FAQ](https://github.com/diabl0w/DFRoot/blob/v4.7/README.md).

## 9. Add ColorOS or Pixel

Return to One UI first. With working root, repeat step 7 using the matching
system card and file:

- **ColorOS 17 / Find N6:** `OneOS_ColorOS17_FindN6_ZFold8.img.gz`.
- **Pixel 11 Fold:** `OneOS_Pixel11Fold_Full_ZFold8.img.gz`.

OneOS can retain previous systems as copies. Keep each system's guest data
with that system and check space before adding another. Do not force another
image into an existing system's data directory. Only one guest runs at a time.

**Source / credit:** [OneOS multiple-system support](https://github.com/fahadalijaved/OneOS#readme),
[MysticGSI](https://github.com/MysticGSI/mysticgsi), and
[Josh Skinner's Fold8 work](https://github.com/fahadalijaved/OneOS/pull/1),
credited upstream for Fold8 ColorOS/Pixel display and hinge integration.

## 10. Optional: test VoLTE separately

After a successful guest boot and return, OneOS offers
**Advanced > Use One UI's calling service (VoLTE)** for a subsequent session.
It tries the phone's own Samsung IMS service inside the guest. It is not a
confirmed fix for this device/carrier, and the earlier PhhIms debug APK is not
part of this setup.

If you test it, check ordinary incoming and outgoing calls, two-way audio,
DTMF, hang-up and recovery after returning to One UI. A 4G/5G icon or working
mobile data does not establish VoLTE. Keep another calling device available;
do not call emergency numbers as a test.

**Source / credit:** [OneOS Samsung IMS integration](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/docs/samsung-ims-in-guest.md)
and its [current experimental setting](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/app-android/app/src/full/res/values/strings_advanced.xml).
Samsung supplies the proprietary IMS components; OneOS implements the guest
integration. Some design-note status paragraphs predate the current UI.

## 11. Remove the installation

1. Return to One UI while the apps are still installed.
2. With working root, open **OneOS > Advanced > Remove OneOS data**. Read the
   warning: it removes guest systems, their apps/accounts/data and session logs.
3. After cleanup succeeds, uninstall OneOS. Downloaded image files remain and
   can be deleted separately when no longer needed.
4. Keep DFRoot's startup option and KernelSU's automatic activation OFF.
   Uninstall DFRoot and Samsung KernelSU, then perform a full restart to end
   the temporary-root session.
5. Restore your normal screen lock and verify normal stock operation.

Uninstalling the root apps and restarting is not a claim that every root-created
file is erased. The earlier verified cleanup also removed exact known trial
files; do not blindly delete `/data/adb` or another setup's modules. Knox,
payment apps and integrity attestations are not guaranteed by a green boot
indicator or a successful restart.

**Source / credit:** [OneOS removal instructions](https://github.com/fahadalijaved/OneOS#readme)
and [DFRoot](https://github.com/diabl0w/DFRoot/blob/v4.7/README.md).
The prior root/rollback result applies to the recorded local trial only.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| No root manager | Install the supplied Samsung KernelSU APK; then follow steps 3–5. |
| KernelSU installed but not working | The manager alone does not activate root. Follow step 4 on the matching firmware. |
| DFRoot says patching failed | Stop. A mitigated or different kernel may not support this route; do not downgrade by guesswork. |
| DFRoot manager dropdown is empty | Install/open the specified Samsung KernelSU app, then reopen DFRoot. |
| OneOS root check fails | Verify KernelSU is working and OneOS is allowed in its Superuser list. |
| APK will not install | Check file completeness and the exact Android error; do not uninstall another version without checking its data and signature. |
| Image rejected | Use the matching system card and original verified `.img.gz`, not an extracted or recompressed image. |
| Guest freezes or gets excessively hot | Return to One UI; if unresponsive, use the forced-restart procedure. |
| Root missing after restart | Temporary root may need manual reactivation. |
| Data works but calls fail | Native IMS remains experimental. Return to One UI for reliable calling. |

Full project attribution: [OneOS CREDITS.md](https://github.com/fahadalijaved/OneOS/blob/082fe8604edc7360de7da4a1ee6016e0282091f2/CREDITS.md).
This guide and file verification are separate from the authorship of those projects.
