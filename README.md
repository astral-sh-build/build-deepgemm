# build-deepgemm

Pre-built Linux wheels for [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM), across Python,
PyTorch, CUDA, and CPU architectures.

## Installation

Following the PyTorch convention, artifacts are published to a separate index for each CUDA
version. Each wheel has a local version suffix that identifies the CUDA, PyTorch, and C++ ABI it
was built against, such as `deep-gemm==2.1.1+cu12.8torch2.10.0cxx11abiTRUE`, and requires the
matching PyTorch release.

Pre-built wheels are available on [Astral's GPU indexes](https://wheels.astralshosted.com/index.html).
For example, to install a CUDA 12.8 build:

```console
$ uv add deep-gemm --index astral-cu128=https://wheels.astralshosted.com/simple/cu128/
```

This configures the index and uses it as the source for `deep-gemm`:

```toml
[tool.uv.sources]
deep-gemm = { index = "astral-cu128" }

[[tool.uv.index]]
name = "astral-cu128"
url = "https://wheels.astralshosted.com/simple/cu128/"
```

Or, with `uv pip`:

```console
$ uv pip install --index https://wheels.astralshosted.com/simple/cu128/ deep-gemm
```

## Supported versions

Wheels are available for the following `deep-gemm` versions:

- [`2.1.1`](https://github.com/astral-sh-build/build-deepgemm/releases/tag/v2.1.1.post3-r1)

The latest release, DeepGEMM 2.1.1, supports the following combinations:

| PyTorch | Python    | `x86_64` CUDA    | `aarch64` CUDA   |
| ------- | --------- | ---------------- | ---------------- |
| 2.7.1   | 3.9–3.13  | 12.8             | 12.8             |
| 2.8.0   | 3.9–3.13  | 12.8, 12.9       | 12.9             |
| 2.9.0   | 3.10–3.14 | 12.8, 12.9, 13.0 | 12.8, 12.9, 13.0 |
| 2.10.0  | 3.10–3.14 | 12.8, 12.9, 13.0 | 12.8, 12.9, 13.0 |

## License

build-deepgemm is licensed under the [Apache License, Version 2.0](LICENSE).

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/ruff/main/assets/svg/Astral.svg" alt="Made by Astral">
  </a>
</div>
