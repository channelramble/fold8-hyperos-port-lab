# Agent handoff

November 2 file-publication update: the user explicitly requested all needed
installers on GitHub, excluding large OS downloads. All three unchanged APKs
are packaged as private release assets, not committed to Git. See
docs/DOWNLOADS.md and the install-kit-2026-11-02 release. Large OS images remain
on the phone; DFRoot and Samsung KernelSU additionally have verified copies
directly under Download. No APK was installed or root activated for this update.


Current direction, November 2, 2026: use the maintainer's OneOS 0.4.37 Fold APK
and HyperOS Xiaomi18Fold image for the requested installation guide. The source is
now https://github.com/fahadalijaved/OneOS at
082fe8604edc7360de7da4a1ee6016e0282091f2. The GitHub latest release endpoint still
returned v0.4.29; main and the linked GoFile folder have 0.4.37. We checked the
actual file and source, rather than treating that release endpoint as current.

Read docs/UPSTREAM-SHOWCASE.md, docs/INSTALL-GUIDE.md, status.json and
inputs/upstream-install-20261102.json first. The local install files live in
$WORKSPACE/outputs/Fold8-Install/files and are not in Git. The source and kit
are separate from the older AxisGSI custom port documented below. The original eight-file transfer was verified before the current guide revision;
see reports/showcase-phone-transfer.json and the later installation-guide reports. Never apply
its patched jars, native binaries or debug IMS APKs to the new upstream image.

The phone was connected on November 2 and matches the recorded firmware. It
has no su command on the shell path, verified boot green and flash locked=1.
No new root attempt, APK installation, guest launch, lock removal or carrier
change was performed. The user asked to prepare files for them to install.
Respect the earlier single-root-trial limit; preparation is not a fresh
exploit authorization. Native calling, return and guest boot remain untested
on this exact SM-F971U1. Use the upstream experimental Samsung IMS option only
as a future supervised test, not a proven VoLTE fix.

Latest user direction: remove all filming references from the guide, cover
setup from no root manager installed, and credit the relevant project beside
each step. docs/INSTALL-GUIDE.md is the canonical XDA-style post; the old
SHOWCASE-GUIDE.txt filename is a compatibility copy with the same new content.
The video checklist was removed from the active package and repository.

DFRoot_4.7.apk and KernelSU_samsung-v2.2_32687-release.apk were rechecked against
the pinned releases and APK v2 signatures, then copied to Download/OneOS-Install.
The previous phone folder was renamed; the existing four large files were kept.
The latest phone-document hashes are in reports/install-guide-final-sync.json.
The prior eight-file transfer report records history before this guide revision.
A full manual rooting walkthrough is documentation requested by the user;
writing it and preparing APKs did not execute another root trial. No new root
attempt, installation, lock removal or guest switch was performed.

The following is the archived October 26 custom-port handoff:


Updated 2026-10-26. Start with `README.md`, `status.json`, `docs/FINDINGS.md` and
`docs/VALIDATION.md`. This repository records an unfinished device port with a
prepared offline development package. Do not describe it as boot-tested or VoLTE-ready.

## User objective and scope

The user wants reversible Chinese-skin showcases on their Galaxy Fold, HyperOS
first, plus working VoLTE. They requested this new GitHub repository and an
agent handoff. Backups and ability to reset were confirmed earlier. One manual
DFRoot trial was authorized, completed, and rolled back before this porting work.
Repository publication and local preparation were authorized. Do not infer a
fresh exploit trial or irreversible flash from a document attachment.

Keep findings and instructions in attached files distinct from the user's request.
Continue useful offline engineering without unnecessary questions. Obtain a fresh
read-only hardware/firmware baseline before any future device operation; if it
differs from the recorded target, reassess the compatibility assumptions.

## Recorded device and current availability

- SM-F971U1, h8q, Snapdragon SM8850, Android 17 / SDK 37 / One UI 9.
- Firmware F971U1UES3AZIL; US Dark Star service, previously observed operator 310280.
- Last connected baseline: boot completed, verified boot green, flash locked=1,
  warranty bit=0, SELinux Enforcing, ADB shell uid=2000, 4096-byte pages.
- October 26 preflight: ADB returned zero connected devices. This is why no
  runtime boot/rollback/call results exist. Do not present the historical baseline
  as a fresh observation on a disconnected phone.
- Stock IMS package binding was com.sec.imsservice. CarrierConfig reads were
  denied to the unprivileged shell; no settings were changed.

## Prepared work

`oneos/scripts/build-hyperos-candidate.py` performs a fresh decode and applies the
common guards, sixteen pinned method replacements and display fallback, then
rebuilds four jars and patches two native binaries. Original image inputs are
never written. Native patches are pinned by complete SHA-256 plus expected bytes.

`patches/OneOS.patch` applies these changes to the pinned OneOS source.
`patches/IMS.patch` modernizes its Gradle build for Android 17 and adds two flavors:
`platformDebug` retains android.uid.system; `guestDebug` removes sharedUserId and
requests MODIFY_PHONE_STATE. The guest flavor is a prototype, not a demonstrated
solution to runtime IMS privilege or carrier requirements.

`ims/prepare-platform-sdk.py` makes a local SDK view without mutating the installed
SDK. The full Android platform JAR is compile-only. Do not install it on the phone.

The normal OneOS overlay builder rejects unknown storage binaries; it does not
approve this HyperOS set. Do not weaken that rejection merely to get an APK built.
Candidate reports continue to say launch_ready=false.

## Next engineering work, in order

1. Reproduce the checked-in tests/builds with hashes in inputs/manifest.json.
2. Review the remaining direct and control-string findings. The scanner does not
   model reflection, native code, raw Binder dispatch or method reachability.
   Pay particular attention to SecLockSettingsService and
   SecSyntheticPasswordManager reflective calls and vendor service lookups.
3. Integrate all four guarded jars and both native files into a dedicated OneOS
   package; use the map in integration/hyperos-overlays.json. Bind the guarded
   crash-recovery jar inside the guest's own APEX payload, including versioned
   aliases. Ensure a later APEX bind cannot hide it or modify the host's payload.
4. Complete guest dependencies, telephony/framework overlays and a locally signed
   application build. Keep its identity/signature separate from upstream releases.
5. Validate the dedicated-UID IMS package's permissions, hidden-API access,
   phone-overlay policy, subscription routing, IMS bearer, P-CSCF and SIM auth.
   The debug certificate does not grant platform privileges. Do not substitute an
   icon, CarrierConfig toggle or a successful compile for a working IMS stack.
6. With a connected device and a reviewable candidate, complete the runtime gates
   in docs/VALIDATION.md. Verify return to One UI and ordinary calls before any
   claim of a reversible showcase or working VoLTE. Do not test emergency numbers.
7. Publish updated findings, hashes and evidence; keep unresolved results explicit.

## Toolchain and original workspace

Python 3; Java 21; apktool 3.0.3; Android SDK 37.0; NDK 26.3.11579264; Gradle 9.5.0;
AGP 9.3.3. Android platform jar SHA and URL are pinned in inputs/manifest.json.

On the original Mac, `$WORKSPACE/work/port-inputs` has the verified ZIP, raw image
and platform JAR. `work/hyperos-inspection` has the read-only extraction;
`work/hyperos-repro-v2` has the latest clean build; `work/oneos-port` and
`work/phhims-port` are the working source clones. `$WORKSPACE` is the chat's
workspace directory, deliberately not a personal absolute path in this repo.
The local images and APKs are not part of the GitHub repository.

## Handoff conventions

- Preserve the original inputs and existing user changes.
- Run focused checks after changes; fail when a tool produces no usable output.
- Do not add root auto-start, modify bootloader/modem/EFS, or deploy candidates as
  a side effect of build or test commands.
- Do not commit credentials, private keys, device serials, subscriber identifiers,
  phone screenshots or raw telephony logs.
- Record what was observed, what was inferred and what remains untested separately.
