# Validation and release gates

## Passed offline

- HyperOS published ZIP SHA-256, ZIP CRC and extracted image hash verified.
- Host installd mapping: all 85 entries matched the pinned OneOS table.
- Framework/native candidate build completed with exact-input checks.
- Structural DEX checker rejects failed tools, empty output, missing DEX and
  invalid result/exception-range sequences; this is not full ART verification.
- Python regression suite passed; see reports/unit-tests.txt.
- Platform and guest IMS flavors assembled. Guest manifest has no sharedUserId
  and requests MODIFY_PHONE_STATE. APK v2 signature verified.
- Compile-only Android framework classes were not packaged in the initial IMS
  build; both final variants were also checked in reports/ims-variants.json.

## Required before a working-port claim

1. Review remaining direct calls, control strings, reflective lock access, native
   operations and Binder dispatch. Rebuild after every necessary change.
2. Verify every mapped guest overlay and APEX alias is mounted and hash-matched.
   Validate package signatures, dependencies and host/guest Binder ownership.
3. With the correct connected phone, capture a fresh minimal stock baseline and
   confirm the user has a concrete rollback path and current backup.
4. Boot the candidate under supervision; verify inner/outer display, rotation,
   touch, Wi-Fi, audio, charging, storage access and telephony without exposing
   lock/profile creation or factory-reset flows.
5. Return to One UI; verify storage, lock unlock, Wi-Fi, eSIM/subscriptions and
   normal calls. Repeat only when failures or changes justify another trial.
6. IMS: prove bearer/P-CSCF/SIM authentication, registration and voice capability,
   ordinary incoming/outgoing calls, two-way audio, DTMF, hang-up, idle recovery
   and cleanup on return. Record carrier, firmware and test conditions.

No runtime gates above have passed for HyperOS. On October 26 ADB showed zero
connected devices. Emergency calling remains unverified; never call emergency
numbers as a test. Root status or a VoLTE icon is not a substitute for these tests.
