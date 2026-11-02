# Current CI result

GitHub Actions passed on November 2, 2026 for showcase commit
`409dfce7060be26faab000264302e29460630227`.
[Run 41418365056](https://github.com/channelramble/fold8-hyperos-port-lab/actions/runs/41418365056)
completed successfully (`offline-checks`). This validates offline repository
checks; it does not test a phone, guest boot, rollback or VoLTE.

The earlier billing-blocked run below is historical:

# GitHub Actions status

The initial run for commit bc926a593c582b7df1d492015b537d41491a271c did not start
any test steps. GitHub reported that recent account payments failed or the
spending limit needs to be increased. No billing settings were changed.

Run: https://github.com/channelramble/fold8-hyperos-port-lab/actions/runs/40286746250

Local validation passed 12 port regression tests plus 3 repository tests. The
source checkout/patch application, final Android builds, DEX structural checks
and repository inventory were also verified locally. This is not a hosted-CI pass.

Once the account restriction is resolved, run the included workflow manually
from Actions, or push a source change. It runs Python-only checks and does not
fetch ROM images, invoke ADB, deploy software or change a phone.
