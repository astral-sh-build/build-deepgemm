#!/bin/bash
# Script to prepare the build environment for Grouped GEMM.
#
# Example usage:
#   ./prepare_for_build.sh v0.3.0

set -euxo pipefail

export ROOT=`pwd`

if [ $# -ne 1 ]; then
    echo "Usage: $0 <grouped_gemm_version>"
    echo "Example: $0 v0.3.0"
    exit 1
fi

GROUPED_GEMM_VERSION=$1

# Ensure that the Grouped GEMM version is supported.
if [ ! -d "${ROOT}/build_scripts/patches/${GROUPED_GEMM_VERSION}" ]; then
    echo "Error: patches/${GROUPED_GEMM_VERSION} directory does not exist"
    exit 1
fi

# Apply patches.
for patch in "${ROOT}/build_scripts/patches/${GROUPED_GEMM_VERSION}"/*.patch; do
    patch -p1 -d ${ROOT} -i ${patch}
done
