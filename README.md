# Fold8 HyperOS port lab

**November 2 update: the installation kit now includes the missing root-tool
and root-manager APKs.** Start with the complete
[step-by-step installation guide](docs/INSTALL-GUIDE.md). It covers DFRoot 4.7,
Samsung KernelSU 2.2, OneOS 0.4.37 Fold, HyperOS, ColorOS and Pixel, with project
credits and source links beside each step.

Files and the guide are on the connected phone under **Download/OneOS-Install**.
The root APKs are prepared only; neither was installed or run again. Working
root remains a launch prerequisite. Guest boot, return and VoLTE remain
unverified on this SM-F971U1. See [package findings](docs/UPSTREAM-SHOWCASE.md)
and [current input manifest](inputs/upstream-install-20261102.json).

The remainder of this README describes the **older custom AxisGSI development
port**. Do not mix its images, patches or IMS debug APKs with the upstream kit.


Reproducible HyperOS 17 and IMS development work for the Samsung SM-F971U1.

**The offline development package is prepared. This is not an install-ready ROM.**
HyperOS boot, return to One UI, VoLTE and emergency calling have not been verified.
No phone was connected at the October 26, 2026 runtime-test preflight.

## Available

- Exact-input HyperOS framework and native storage-service candidate builder.
- Sixteen Xiaomi/recovery/diagnostic method guards, plus the upstream OneOS guards.
- Android 17 IMS platform-UID and dedicated-UID development variants.
- Privileged-permission integration template and guest overlay map.
- Regression tests, structural DEX checks, input/output hashes and audit evidence.
- Source patches against pinned upstream commits and an automated checkout helper.
- [AGENT.md](AGENT.md), the development handoff, with the remaining work spelled out.

```sh
python3 -m unittest discover -s oneos/scripts -p 'test_*py'
python3 -m unittest discover -s tests -p 'test_*py'
python3 tools/verify_repository.py
```

Follow [BUILD.md](docs/BUILD.md) for the offline builds. Read
[FINDINGS.md](docs/FINDINGS.md), [INTEGRATION.md](docs/INTEGRATION.md) and
[VALIDATION.md](docs/VALIDATION.md) before preparing any device trial.
Other Chinese skin sources are listed in [SKINS.md](docs/SKINS.md).

## Status

Compilation and structural checks are development evidence, not a successful boot
or carrier test. The dedicated-UID IMS variant removes the shared-system-UID
signature conflict at packaging time; privileged permission grants, hidden APIs,
Samsung modem integration and carrier provisioning remain unverified.

**CI:** All 15 local tests passed. GitHub Actions also passed for showcase
commit `409dfce` on November 2. The earlier account-billing block is historical;
see [CI status](docs/CI_STATUS.md). These are offline checks, not phone tests.

`status.json` is the current status. `reports/artifacts.json` identifies the local
build products. There is no flash installer, automatic root activation or enabled
HyperOS launcher profile in this repository. Original ROM images, proprietary
framework binaries, APK build products, signing keys and private phone dumps are
not committed.

## Provenance and license scope

OneOS source is pinned at `73c3be36c35462742503380e1f025fead3cea48c`;
Samsung-Galaxy-A05/vendor_phhims at `2bc8c93a4918f4b06c423406f27b4f3b29c44715`.
See [inputs/manifest.json](inputs/manifest.json) and [THIRD_PARTY.md](THIRD_PARTY.md).
This is independent development, not an official Samsung, Xiaomi or OneOS release.
