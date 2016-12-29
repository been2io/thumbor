#!/usr/bin/python
import os
from subprocess import Popen, PIPE

import subprocess

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger


class Optimizer(BaseOptimizer):

    def should_run(self, image_extension, buffer):
        return image_extension in ['.webp']

    def optimize(self, buffer, input_file, output_file):

        command = [
            self.context.config.WEBM_PATH,
            input_file,
            '144',
            "176",
            output_file,
        ]
        with open(os.devnull) as null:
            subprocess.call(command, stdin=null)
