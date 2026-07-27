import importlib
from importlib.metadata import version

import pytest
import torch


@pytest.fixture(scope="module")
def device() -> torch.device:
    assert torch.cuda.is_available(), "The tests must run on a CUDA GPU"
    device = torch.device("cuda")
    assert torch.cuda.get_device_capability(device)[0] >= 9
    return device


def test_published_cuda_wheel(device: torch.device) -> None:
    assert version("deep-gemm") == "2.1.1+cu.12.8.torch.2.7"
    assert torch.__version__ == "2.7.1+cu128"
    assert torch.version.cuda == "12.8"
    assert torch.cuda.get_device_name(device)


@pytest.mark.parametrize("module_name", ["deep_gemm", "deep_gemm_cpp"])
def test_native_module(device: torch.device, module_name: str) -> None:
    assert importlib.import_module(module_name) is not None


def test_hopper_native_gemm_configuration(device: torch.device) -> None:
    import deep_gemm

    assert deep_gemm.get_num_sms() > 0
    assert callable(deep_gemm.bf16_gemm_nt)
    assert callable(deep_gemm.cublaslt_gemm_nt)


def test_hopper_bfloat16_gemm(device: torch.device) -> None:
    import deep_gemm

    torch.manual_seed(0)
    left = torch.randn((128, 128), device=device, dtype=torch.bfloat16)
    right = torch.randn((128, 128), device=device, dtype=torch.bfloat16)
    actual = torch.empty((128, 128), device=device, dtype=torch.bfloat16)
    deep_gemm.bf16_gemm_nt(left, right, actual)
    expected = left.float() @ right.float().t()
    torch.testing.assert_close(actual.float(), expected, atol=0.25, rtol=0.05)
