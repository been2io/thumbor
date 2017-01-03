
import os
from tempfile import NamedTemporaryFile

import subprocess

from thumbor.engines.pil import Engine as PILEngine





class Engine(PILEngine):
    @property
    def size(self):
        return self.image_size


    def run_webp(self):
        buffer = self.buffer
        ifile = NamedTemporaryFile(suffix=".webp", delete=False)
        ofile = NamedTemporaryFile(suffix=".webp", delete=False)
        try:
            ifile.write(buffer)
            ifile.close()
            ofile.close()
            command = [
                self.context.config.WEBPCONV_PATH,
                ifile.name,
                self.height,
                self.width,
                ofile.name,
            ]
            with open(os.devnull) as null:
                subprocess.call(command, stdin=null,stdout=null,stderr=null)
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
        pass

    def resize(self, width, height):
        self.width=str(width)
        self.height=str(height)
        self.image_size=(self.width,self.height)

    def crop(self, left, top, right, bottom):
        pass

    def rotate(self, degrees):
        pass
    def flip_vertically(self):
        pass
    def flip_horizontally(self):
        pass


    def flush_operations(self):
        self.buffer = self.run_webp()
       # self.image_size=len(self.buffer)

    def read(self, extension=None, quality=None):
        self.flush_operations()
        return self.buffer

    def convert_to_grayscale(self):
        pass
