import os
from typing import List

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.errors import ConanInvalidConfiguration

required_conan_version = ">=1.57.0"

class VdbfusionConan(ConanFile):
    name = "vdbfusion"
    version = "0.1.6"
    license = "MIT"
    author = "Ignacio Vizzo"
    url = "https://github.com/Flyability/registration"
    description = "C++ library for point cloud registration."
    topics = ("tsdf", "lidar")

    settings = "os", "compiler", "build_type", "arch", "system-configuration"
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
    }

    exports_sources = "**"

    def validate(self):
        if str(self.settings.os) not in ("Linux"):
            raise ConanInvalidConfiguration("OS is not supported")

    def requirements(self):
        self.requires("eigen/system@autonomy/gaston")
        self.requires("lasfile/2.0.4@autonomy/gaston")
        self.requires("onetbb/2020.3")
        self.requires("openvdb/9.1.0@local/gaston")                                

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["RUN_CMAKE_CONAN"] = "OFF"

        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["vdbfusion"]
