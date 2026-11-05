# Pinned Linux toolchain for local builds and CI (ADR-005).
# Update a pin deliberately: change it here, rebuild, and run every preset.
FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852

# Must match the baseline in vcpkg-configuration.json.
ARG VCPKG_COMMIT=5d68747adeb88f05aac8ca4d18d29e50296509b1

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      autoconf \
      autoconf-archive \
      automake \
      bison \
      build-essential \
      ca-certificates \
      clang-20 \
      clang-format-20 \
      clang-tidy-20 \
      clang-tools-20 \
      cmake \
      curl \
      flex \
      g++-14 \
      gcc-14 \
      git \
      libclang-rt-20-dev \
      libfuzzer-20-dev \
      libtool \
      linux-libc-dev \
      lld-20 \
      m4 \
      make \
      ninja-build \
      pkg-config \
      python3 \
      tar \
      unzip \
      zip \
 && apt-get clean \
 && ln -s /usr/bin/clang-format-20 /usr/local/bin/clang-format \
 && ln -s /usr/bin/clang-tidy-20 /usr/local/bin/clang-tidy

ENV VCPKG_ROOT=/opt/vcpkg \
    VCPKG_DISABLE_METRICS=1 \
    VCPKG_DOWNLOADS=/vcpkg-cache/downloads \
    VCPKG_DEFAULT_BINARY_CACHE=/vcpkg-cache/archives \
    FINCERO_BUILD_ROOT=/build \
    CC=clang-20 \
    CXX=clang++-20

# The bootstrap needs VCPKG_DOWNLOADS to exist already.
RUN mkdir -p /work /build /vcpkg-cache/downloads /vcpkg-cache/archives \
 && git clone https://github.com/microsoft/vcpkg.git "$VCPKG_ROOT" \
 && git -C "$VCPKG_ROOT" checkout --detach "$VCPKG_COMMIT" \
 && "$VCPKG_ROOT/bootstrap-vcpkg.sh" -disableMetrics

# Named volumes inherit this ownership on first use, so the build runs unprivileged.
# ubuntu:24.04 already ships the non-root user `ubuntu` (uid 1000).
RUN chown -R ubuntu:ubuntu "$VCPKG_ROOT" /work /build /vcpkg-cache \
 && git config --system --add safe.directory /work \
 && git config --system --add safe.directory "$VCPKG_ROOT"

USER ubuntu
WORKDIR /work
