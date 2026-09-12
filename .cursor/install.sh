#!/usr/bin/env bash
# Idempotent Cloud Agent setup for the AKWF-FREE repository.
#
# This repo is a data library of single-cycle waveforms (WAV / C / JS / PNG).
# Its tooling is:
#   * sox + gnuplot + hexdump  -> the AKWF-c / AKWF-png convert.sh pipeline
#   * prettier                 -> markdown formatting (built-in markdown support)
#   * markdownlint-cli         -> markdown linting (.markdownlint.json)
set -euo pipefail

# System packages required by the convert.sh waveform pipeline.
# hexdump ships in the base image; sox and gnuplot are added here.
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y sox gnuplot

# Markdown tooling, installed into /usr/local (already on PATH) so it is
# available in every fresh shell without mutating shell profiles.
NPM_BIN="$(command -v npm)"
sudo env "PATH=$PATH" "$NPM_BIN" install -g --prefix /usr/local \
  prettier@3 markdownlint-cli@0.49

# Report the resolved toolchain for quick verification.
echo "----- toolchain -----"
sox --version
gnuplot --version | head -1
hexdump --version | head -1 || true
echo "prettier $(prettier --version)"
echo "markdownlint $(markdownlint --version)"
