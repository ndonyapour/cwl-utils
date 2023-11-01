# SPDX-License-Identifier: Apache-2.0
"""Classes for docker-extract."""
import logging
import os
import subprocess  # nosec
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from .singularity import get_version as get_singularity_version
from .singularity import is_version_2_6 as is_singularity_version_2_6
from .singularity import is_version_3_or_newer as is_singularity_version_3_or_newer

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


class ImageBuilder(ABC):
    def __init__(
        self,
        req_dockerfile: str,
        req_dockerimageid: str,
        save_directory: Optional[Union[str, Path]],
        cmd: str,
        force_pull: bool,
    ) -> None:
        """Create an ImageBuilder."""
        self.req_dockerfile = req_dockerfile
        self.req_dockerimageid = req_dockerimageid
        self.save_directory = save_directory
        self.cmd = cmd
        self.force_pull = force_pull

    @abstractmethod
    def build_docker_image(self) -> None:
        """Build and save the image to disk."""

    @staticmethod
    def _run_command(cmd_pull: List[str]) -> None:
        try:
            subprocess.run(  # nosec
                cmd_pull, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as err:
            if err.output:
                raise subprocess.SubprocessError(err.output) from err
            raise err


class DockerImageBuilder(ImagePuller):
    """Build docker image with Docker."""

    def save_docker_image(self) -> None:
        """Download and save the software container image to disk as a docker tarball."""
        _LOGGER.info(f"Building {self.req_dockerimageid} with {self.cmd}...")
        dockerfile_dir = create_tmp_dir(args.dir)
            with open(os.path.join(dockerfile_dir, "Dockerfile"), "w") as dfile:
                    dfile.write(req.dockerFile)
            cmd = [
                "spython",
                "recipe",
                os.path.join(dockerfile_dir, "Dockerfile"),
                os.path.join(dockerfile_dir, "Singularity.def"),
            ]
            print("Do conversion")
        cmd_docker_build = 
    
        ImagePuller._run_command_pull(cmd_pull)
        _LOGGER.info(f"Image successfully pulled: {self.req}")
        # if self.save_directory:
        #     dest = os.path.join(self.save_directory, self.get_image_name())
        #     if self.save_directory and self.force_pull:
        #         os.remove(dest)
        #     cmd_save = [
        #         self.cmd,
        #         "save",
        #         "-o",
        #         dest,
        #         self.req,
        #     ]
        #     subprocess.run(cmd_save, check=True)  # nosec
        #     _LOGGER.info(f"Image successfully saved: {dest!r}.")
        #     print(self.generate_udocker_loading_command())


class SingularityImagePuller(ImagePuller):
    """Pull docker image with Singularity."""

    CHARS_TO_REPLACE = ["/"]
    NEW_CHAR = "_"

    def get_image_name(self) -> str:
        """Determine the file name appropriate to the installed version of Singularity."""
        image_name = self.req
        for char in self.CHARS_TO_REPLACE:
            image_name = image_name.replace(char, self.NEW_CHAR)
        if is_singularity_version_2_6():
            suffix = ".img"
        elif is_singularity_version_3_or_newer():
            suffix = ".sif"
        else:
            raise Exception(
                f"Don't know how to handle this version of singularity: {get_singularity_version()}."
            )
        return f"{image_name}{suffix}"

    def save_docker_image(self) -> None:
        """Pull down the Docker software container image and save it in the Singularity image format."""
        save_directory: Union[str, Path]
        if self.save_directory:
            save_directory = self.save_directory
        if (
            os.path.exists(os.path.join(save_directory, self.get_image_name()))
            and not self.force_pull
        ):
            _LOGGER.info(f"Already cached {self.req} with Singularity.")
            return
        _LOGGER.info(f"Pulling {self.req} with Singularity...")
        cmd_pull = [
            self.cmd,
            "pull",
        ]
        if self.force_pull:
            cmd_pull.append("--force")
        cmd_pull.extend(
            [
                "--name",
                os.path.join(save_directory, self.get_image_name()),
                f"docker://{self.req}",
            ]
        )
        ImagePuller._run_command_pull(cmd_pull)
        _LOGGER.info(
            f"Image successfully pulled: {save_directory}/{self.get_image_name()}"
        )
