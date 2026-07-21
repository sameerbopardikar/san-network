#!/usr/bin/env bash
# Checksum-pinned Gitleaks install; arch- and destination-aware.
set -euo pipefail

VERSION="8.30.1"
INSTALL_DIR="${GITLEAKS_INSTALL_DIR:-${HOME}/.local/bin}"
ARCH_RAW="$(uname -m)"
case "${ARCH_RAW}" in
  x86_64|amd64) ARCH="x64" ;;
  aarch64|arm64) ARCH="arm64" ;;
  *)
    echo "unsupported architecture: ${ARCH_RAW}" >&2
    exit 1
    ;;
esac

# Published asset checksums for v8.30.1 (linux).
case "${ARCH}" in
  x64)
    ASSET="gitleaks_${VERSION}_linux_x64.tar.gz"
    SHA256="551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
    ;;
  arm64)
    ASSET="gitleaks_${VERSION}_linux_arm64.tar.gz"
    SHA256="e4a487ee7ccd7d3a7f7ec08657610aa3606637dab924210b3aee62570fb4b080"
    ;;
esac

WORKDIR="$(mktemp -d)"
cleanup() { rm -rf "${WORKDIR}"; }
trap cleanup EXIT

curl --fail --location --silent --show-error \
  --output "${WORKDIR}/${ASSET}" \
  "https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/${ASSET}"
echo "${SHA256}  ${WORKDIR}/${ASSET}" | sha256sum --check
tar --extract --gzip --file "${WORKDIR}/${ASSET}" --directory "${WORKDIR}" gitleaks
mkdir -p "${INSTALL_DIR}"
install --mode 0755 "${WORKDIR}/gitleaks" "${INSTALL_DIR}/gitleaks"
echo "installed ${INSTALL_DIR}/gitleaks (${ARCH})"
