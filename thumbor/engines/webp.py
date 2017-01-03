#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com
import os
from io import BytesIO
from tempfile import NamedTemporaryFile

import subprocess
from PIL import Image

from thumbor.engines.pil import Engine as PILEngine
from thumbor.utils import logger





class Engine(PILEngine):
    @property
    def size(self):
        return self.image_size


    def run_webp(self):
        buffer = self.buffer
        logger.warn(len(buffer))
        ifile = NamedTemporaryFile(suffix=".webp", delete=False)
        ofile = NamedTemporaryFile(suffix=".webp", delete=False)
        try:
            ifile.write(buffer)
            ifile.close()
            ofile.close()
            command = [
                self.context.config.WEBPCONV_PATH,
                ifile,
                self.height,
                self.width,
                ofile,
            ]
            logger.warn(command)
            with open(os.devnull) as null:
                subprocess.call(command, stdin=null)
            with open(ofile.name, 'rb') as f:  # reopen with file thats been changed with the optimizer
              return f.read()

        finally:
            os.unlink(ifile.name)
            os.unlink(ofile.name)






    def update_image_info(self):
        pass

    def load(self, buffer, extension):
        self.extension = extension
        self.buffer = buffer
        self.image = ''
        self.update_image_info()
        self.width='144'
        self.height ='176'
        self.image_size = (144,176)

    def draw_rectangle(self, x, y, width, height):
        raise NotImplementedError()

    def resize(self, width, height):
        self.width=str(width)
        self.height=str(height)
        self.image_size=(self.width,self.height)

    def crop(self, left, top, right, bottom):
        raise NotImplementedError()

    def rotate(self, degrees):
        raise NotImplementedError()

    def flip_vertically(self):
        raise NotImplementedError()

    def flip_horizontally(self):
        raise NotImplementedError()



    def flush_operations(self):
        self.buffer = self.run_webp()
       # self.image_size=len(self.buffer)

    def read(self, extension=None, quality=None):
        self.flush_operations()
        logger.warn(len(self.buffer))
        return self.buffer

    def convert_to_grayscale(self):
        pass
