import os
import subprocess

from setuptools import find_packages, setup
from wheel.bdist_wheel import bdist_wheel


def get_long_description():
    with open("../README.md", "r", encoding="utf-8") as f:
        return f.read()


def get_data_files():
    os = subprocess.check_output(["go", "env", "GOOS"]).strip().decode("utf-8")
    return [("Scripts", ["../fml.exe"])] if os == "windows" else [("bin", ["../fml"])]


def get_version():
    version = os.environ.get("VERSION")
    return version.replace("-", "+", 1)


def get_platform():
    os = subprocess.check_output(["go", "env", "GOOS"]).strip().decode("utf-8")
    arch = subprocess.check_output(["go", "env", "GOARCH"]).strip().decode("utf-8")
    plat = f"{os}_{arch}"
    if plat == "darwin_amd64":
        return "macosx_10_13_x86_64"
    elif plat == "darwin_arm64":
        return "macosx_11_0_arm64"
    elif plat == "linux_amd64":
        return "manylinux_2_17_x86_64.manylinux2014_x86_64.musllinux_1_1_x86_64"
    elif plat == "linux_arm64":
        return "manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64"
    elif plat == "windows_amd64":
        return "win_amd64"
    else:
        raise ValueError("not supported platform.")


class custom_bdist_wheel(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        # Mark us as not a pure python package
        self.root_is_pure = False

    def get_tag(self):
        return "py3", "none", get_platform()


setup(
    name="fasttrackml",
    version=get_version(),
    description="Rewrite of the MLFlow tracking server with a focus on scalability.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    data_files=get_data_files(),
    python_requires=">=3.6",
    zip_safe=False,
    ext_modules=[],
    cmdclass=dict(
        bdist_wheel=custom_bdist_wheel,
    ),
)
