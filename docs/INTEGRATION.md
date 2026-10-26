# Guest integration work

`integration/hyperos-overlays.json` records the intended guest-only mount targets.
It is a specification, not an executable deployment plan or launch approval.

The existing guest_prepare.sh handles services.jar and OPPO's framework but has
no validated HyperOS package. Its APEX phase mounts crashrecovery_payload.img
under `/apex/com.android.crashrecovery` and versioned aliases. The patched
service-crashrecovery.jar must be visible in each guest path after those mounts;
no bind may land in One UI's live APEX namespace or be hidden by a later mount.
All required overlay hashes must be verified before the session changes state.

The native vold must register gvld, omit the vendor IVold/default registration,
and match the gvld lookups in services.jar, miui-services.jar and incremental.so.
The trade-in diagnostic jar must also be guarded. A services.jar-only overlay is
insufficient for this image.

Add a complete package manifest, matching local signing identity, correct guest
APEX payloads and host-specific telephony/framework overlays before enabling a
launcher entry. Preserve the upstream return, shared-data, lock, eSIM and
storage-service protections and validate them on the actual Fold.

## Dedicated-UID IMS prototype

The guest flavor of PhhIms intentionally has no sharedUserId. Its initial
privileged-permission allowlist is in `ims/guest-integration`. Place that XML on
the same guest partition as the eventual privileged APK. Android's requested
runtime phone/microphone permissions must also be granted through a validated
guest setup flow before calls. Neither an allowlist nor a debug signature alone
proves hidden-API or modem access.

Upstream's RRO targets `com.android.phone` and sets `config_ims_mmtel_package` to
`me.phh.ims`. Validate the target package/resource and overlay authorization in
this HyperOS image before compiling/staging it. CarrierConfig may select a
carrier-specific provider instead. Do not override One UI's live IMS provider
as a shortcut for guest integration.

A host-to-guest IMS bridge is not implemented. The guest must not fight the host
for an IMS bearer or registration. Establish ownership and cleanup behavior,
including modem/audio recovery on return, before enabling the provider.
