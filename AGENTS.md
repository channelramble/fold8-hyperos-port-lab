# Repository instructions

Read `AGENT.md` for the handoff and `status.json` for verified versus pending work.
Keep all builds offline with respect to the phone. Device operations must be
separate from build/test commands. Preserve exact-input checks and explicit
non-install-ready status until the documented runtime gates have evidence.

Use Python unittest for the included checks. Do not introduce proprietary ROM
images, APKs, signing keys, subscriber information or raw device logs into Git.
