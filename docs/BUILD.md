# Reproduce the offline builds

## Fast source checks

```sh
python3 -m unittest discover -s oneos/scripts -p 'test_*py'
python3 -m unittest discover -s tests -p 'test_*py'
python3 tools/verify_repository.py
```

## Source checkout

`python3 tools/prepare_upstreams.py` creates new, pinned checkouts beneath
`build/upstreams`, verifies each commit and applies the corresponding patch.
It requires Git/network access, refuses existing checkout destinations and does
not access a phone. It initializes the pinned IMS RNNoise submodule.

## HyperOS inputs

Acquire the ZIP from the URL in `inputs/manifest.json` and check its SHA-256 before
extracting the single `system.img` member. Check the raw image hash as well.
Use `oneos/scripts/inspect-port-image.py` with read-only `debugfs` to extract the
framework and native inputs. Never pass debugfs `-w` for the original image.

The crash-recovery input is nested: `/system/apex/com.android.crashrecovery.capex`
contains `original_apex`; that ZIP contains `apex_payload.img`; its filesystem
contains `/javalib/service-crashrecovery.jar`. Check the CAPEX/JAR hashes in the
manifest. Use Java 21, apktool 3.0.3 and an Android SDK containing dexdump:

```sh
export JAVA_HOME=/absolute/path/to/jdk21
export ANDROID_HOME=/absolute/path/to/android-sdk
python3 oneos/scripts/build-hyperos-candidate.py \
  --extracted /absolute/path/to/extracted \
  --crash-jar /absolute/path/to/service-crashrecovery.jar \
  --host-installd reports/host_installd.txt \
  --output /absolute/path/to/new-output-directory
```

Use the supplied host table only for the recorded firmware; obtain and compare a
fresh one after any firmware change. Output contains four framework jars, two
native binaries, build/audit logs and `candidate-status.json` with launch_ready=false.
It is not a flashable image or a ready-to-launch OneOS package.

## IMS

In the patched IMS checkout, use SDK platform android-37.0, Java 21 and
NDK 26.3.11579264. Verify the full Android platform JAR from the manifest, then:

```sh
python3 prepare-platform-sdk.py --sdk /absolute/path/to/sdk \
  --platform-jar /absolute/path/to/android-all-17.jar \
  --output /absolute/path/to/new-sdk-view
export ANDROID_HOME=/absolute/path/to/new-sdk-view
./gradlew :app:assemblePlatformDebug :app:assembleGuestDebug \
  -PoneosPlatformJar=/absolute/path/to/android-all-17.jar --no-daemon
```

The SDK view changes compile-time inputs only. It is not a framework replacement.
`platformDebug` retains the upstream shared system UID. `guestDebug` removes it
and adds the MODIFY_PHONE_STATE request. Both are debug-signed development APKs.
The latter still requires privileged placement and verification of hidden APIs,
permission grants, overlay policy, modem access and carrier behavior.

The debug certificate is machine-local, so APK hashes vary between independently
signed builds. Framework ZIP metadata can also change hashes; compare DEX content
and source provenance when investigating reproducibility. Published hashes identify
this particular local build, not every possible rebuild.
