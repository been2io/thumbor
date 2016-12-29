#!/usr/bin/python
import os
from subprocess import Popen, PIPE

import subprocess
from tempfile import NamedTemporaryFile

from thumbor.optimizers import BaseOptimizer
from thumbor.utils import logger


class Optimizer(BaseOptimizer):

    def should_run(self, image_extension, buffer):
        return image_extension in ['.webp']
    def run_optimizer(self, image_extension, buffer):
        if not self.should_run(image_extension, buffer):
            return buffer

        ifile = NamedTemporaryFile(delete=False)
        ofile = NamedTemporaryFile(suffix="webp",delete=False)
        try:
            ifile.write(buffer)
            ifile.close()
            ofile.close()

            self.optimize(buffer, ifile.name, ofile.name)

            with open(ofile.name, 'rb') as f:  # reopen with file thats been changed with the optimizer
                return f.read()

        finally:
            os.unlink(ifile.name)
            os.unlink(ofile.name)
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
