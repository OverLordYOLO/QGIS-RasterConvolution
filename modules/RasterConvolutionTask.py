import os
import logging
import time
from osgeo import gdal
from qgis.core import QgsTask

class RasterConvolutionTask(QgsTask):
    def __init__(self, description, input_file, output_file, kernel, kernel_size=3):
        super().__init__(description, QgsTask.CanCancel)
        self.input_file = input_file
        self.output_file = output_file
        self.kernel = kernel
        self.kernel_size = kernel_size
        self.result = None

    def run(self):
        start_time = time.time()
        try:
            logging.info(f"Applying convolution: {self.description()}")

            # Format kernel for gdal.Translate
            kernel_flat = ' '.join(str(v) for v in self.kernel)
            kernel_str = f"KERNEL={self.kernel_size} {self.kernel_size} {kernel_flat}"

            gdal.SetConfigOption('GDAL_CONVOLUTION_FILTER', kernel_str)
            src_ds = gdal.Open(self.input_file)
            if not src_ds:
                raise RuntimeError(f"Failed to open input file: {self.input_file}")

            # Apply the convolution filter using gdal.Translate with config option
            dst_ds = gdal.Translate(self.output_file, src_ds, options=gdal.TranslateOptions())
            dst_ds = None

            time_spent = time.time() - start_time
            self.result = {
                "status": "success",
                "message": None,
                "output_file": self.output_file,
                "time_spent": time_spent
            }
            logging.info(f"Convolution completed in {time_spent:.2f} seconds.")
        except Exception as e:
            self.result = {
                "status": "error",
                "message": str(e),
                "output_file": None,
                "time_spent": time.time() - start_time
            }
            logging.error(f"Convolution failed: {e}")

        self.setProgress(100)
        return self.result["status"] == "success"

    def cancel(self):
        logging.warning(f"Convolution task {self.description()} was canceled.")
        super().cancel()

    def finished(self, success):
        if success:
            logging.info(f"{self.result}")
        else:
            logging.warning(f"{self.result}")

if __name__ == "__main__":
    high_pass = [
        -1, -1, -1,
        -1,  8, -1,
        -1, -1, -1
    ]

    gaussian_blur = [
        1,  2,  1,
        2,  4,  2,
        1,  2,  1
    ]
    # Normalize the kernel
    gaussian_blur = [x / 16 for x in gaussian_blur]

    
    task = RasterConvolutionTask(
        "Edge enhancement",
        input_file="path/to/input.tif",
        output_file="path/to/output.tif",
        kernel=kernel,
        kernel_size=3
    )

    QgsApplication.taskManager().addTask(task)