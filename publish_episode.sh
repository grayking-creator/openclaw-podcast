#!/bin/bash
# Retired: this old publisher copied originals and committed unrelated website work.
# The approved orchestrator uploads public media first and delegates WebP imports to DGX.
set -euo pipefail
printf '%s\n' 'Use scripts/launch_approved_release.py with the verified episode approval record.' >&2
printf '%s\n' 'The legacy publisher is disabled; it cannot copy full-size images into websiteBuilder.' >&2
exit 2
