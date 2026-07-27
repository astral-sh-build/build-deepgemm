import subprocess
from pathlib import Path

import modal

TEST_DIRECTORY = Path(__file__).parent.resolve()

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("gnupg", "wget")
    .run_commands(
        "wget -q https://developer.download.nvidia.com/compute/cuda/repos/"
        "debian12/x86_64/cuda-keyring_1.1-1_all.deb -O /tmp/cuda-keyring.deb",
        "dpkg -i /tmp/cuda-keyring.deb",
        "apt-get update",
        "apt-get install -y --no-install-recommends "
        "cuda-nvcc-12-9 cuda-cuobjdump-12-9 cuda-cudart-dev-12-9",
    )
    .env({"CUDA_HOME": "/usr/local/cuda-12.9"})
    .uv_sync(uv_project_dir=str(TEST_DIRECTORY))
    .env({"PATH": "/usr/local/bin:/usr/bin:/bin"})
    .add_local_file(
        TEST_DIRECTORY / "test_deepgemm.py",
        remote_path="/gpu-tests/test_deepgemm.py",
    )
)

app = modal.App("astral-build-deepgemm-gpu-tests")


@app.function(image=image, gpu="H100", timeout=900)
def test() -> None:
    subprocess.run(
        ["/.uv/.venv/bin/python", "-m", "pytest", "-v", "/gpu-tests/test_deepgemm.py"],
        check=True,
    )
