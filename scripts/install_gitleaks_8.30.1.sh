#!/usr/bin/env bash
# Checksum-pinned Gitleaks install for local/CI hosts that lack workflow-scope pushes.
set -euo pipefail
curl --fail --location --silent --show-error \
  --output gitleaks.tar.gz \
  https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz
echo "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb  gitleaks.tar.gz" | sha256sum --check
tar --extract --gzip --file gitleaks.tar.gz gitleaks
install --mode 0755 gitleaks /usr/local/bin/gitleaks
rm -f gitleaks.tar.gz gitleaks
