# Engineering findings

These observations come from the pinned image/source and read-only phone inspection.
The phone was last inspected while connected on October 25. On October 26 ADB
reported zero connected devices. No guest was installed or booted during this work.

## Native storage service separation

The guest and One UI share Binder services. A guest vold registering as `vold`
can replace the host registration. This image's native patch is pinned to the
complete input hashes recorded in `hyperos-native-candidate.py`:

| Binary | Offset | Change / inspected evidence |
| --- | --- | --- |
| vold | 0xf45c | Whole NUL-delimited vold name becomes gvld; start() references 0xf45d |
| vold | 0x6ce00 | TBZ becomes B to 0x6ced4, the vendor service's not-declared return path |
| service.incremental.so | 0x64785 | Whole NUL-delimited lookup name becomes gvld |

The relevant ELF LOAD segments have equal file offsets and virtual addresses.
Debug symbols came from .gnu_debugdata. IncrementalService's two inspected
String16 references are at 0xc005c and 0xc2710/14. Expected original bytes are
checked before writing any candidate. services.jar and two Xiaomi framework
lookups must match the new name; the native patch alone is insufficient.

## Common and OEM guards

The OneOS common guards applied to this Android 17 services.jar, with a Xiaomi
XSpace repair method disabled before the no-new-users graph check. The Fold's
85-entry IInstalld table exactly matched the pinned upstream table. Its source
was read from the connected phone's services.jar; subscriber data was not needed.

The method specification now has sixteen exact-body hashes and replacements:
Xiaomi recovery BCB writes, factory-reset paths, direct power paths, host boot
animation activation, cache-optimizer installd access, XSpace repair, two vold
lookups, the AOSP RescueParty disable decision, three oldcredential HAL mutations,
and two trade-in diagnostic command paths. Unknown method bodies fail the build
before method edits are written.

The expanded audit found oldcredential deletion, timer mutation and file writes
in SecSyntheticPasswordManager. These three methods now return without making
the HAL writes. The original trade-in diagnostic doMain/doTesting methods could
write sys.powerctl, including a testing/wipe path; those command bodies are now
unavailable in the candidate. Their original evidence is retained in
reports/tradein-before-guards.json. The rebuilt tradeinmode.jar must be mounted.

## Remaining review

The candidate direct-call report still includes Binder Weaver dispatch stubs,
Weaver writes behind the service-null guard, and recovery calls behind guarded
paths. These are review findings, not seven observed destructive operations.
The scanner does not prove those paths unreachable; reflective calls and native
code require a separate review. The control-string report likewise records
potential sites even when a method has an early-return guard.

The OEM lock classes use reflective access to base lock-settings methods and
look up vendor.xiaomi.hardware.oldcredential.IOldCredentialService/default.
A missing vendor service on Samsung is not an adequate isolation argument.
Guest namespace ownership, Binder routing and vendor-extension initialization
must be checked before a trial. The candidate builder deliberately leaves
launch_ready=false and does not create an approved launcher package.

## IMS

The original IMS app requests android.uid.system. HyperOS framework-res was signed
by Xiaomi, certificate SHA-256
`c9009d01ebf9f5d0302bc71b2fe9aa9a47a432bba17308a3111b75d7b2149025`.
The development APK is debug-signed, so it cannot simply join that shared UID.

Two flavors now build against Android 17 system APIs. `platformDebug` preserves
upstream integration. `guestDebug` removes sharedUserId in the merged manifest,
requests MODIFY_PHONE_STATE, and comes with a privileged-permission template.
This removes the specific shared-UID signing conflict in the prototype, but it
has not established permission grants, hidden-API access, radio/IMS bearer access,
carrier authorization, audio behavior or emergency calling. Both final APKs were
inspected: neither packages Android platform classes. Their exact hashes and
manifest facts are in reports/ims-variants.json.

The historical stock provider binding was com.sec.imsservice. Read-only
CarrierConfig queries were denied to shell. No provider selection, modem setting
or carrier configuration was changed. A caller ID, registration flag or VoLTE icon
would not establish working incoming/outgoing voice or successful return to One UI.

## Build-check correction

The original structural checker ignored dexdump's exit status and could report
success for a jar with no DEX or an empty failed parse. It now refuses those cases,
checks duplicate DEX entries and recognizes instruction offsets wider than four
hex digits. Regression tests cover these failures. This strengthens the check;
it still does not execute ART's full verifier or prove runtime compatibility.
