
# Raster Convolution Tools

## Overview

This documentation describes the functionality and usage of two utility components used for applying convolution operations to raster data:

- `KernelSelector`: A utility class to retrieve predefined or generated convolution kernels.
- `RasterConvolutionTask`: A QGIS task that applies a convolution kernel to a raster file using GDAL.

---

## KernelSelector

### Description
Utility class for selecting commonly used convolution kernels by name.
Supports both static (e.g., Sobel, Prewitt) and dynamically generated kernels (identity, uniform blur).

### Key Methods

```python
KernelSelector.get_kernel(name: str) -> list[float]
```
Retrieves a named kernel. Raises `ValueError` if the kernel is not found.

```python
KernelSelector.get_description(name: str) -> str
```
Returns a textual description of the selected kernel.

```python
KernelSelector.generate_identity_kernel(size: int) -> list[float]
```
Generates an identity kernel of any odd size.

```python
KernelSelector.generate_uniform_blur_kernel(size: int) -> list[float]
```
Generates a uniform blur (box filter) kernel of the specified size.

### Example Usage

```python
from KernelSelector import KernelSelector

kernel = KernelSelector.get_kernel("sobel_horizontal")
description = KernelSelector.get_description("sobel_horizontal")
print(description)

identity = KernelSelector.generate_identity_kernel(3)
blur = KernelSelector.generate_uniform_blur_kernel(5)
```

---

## RasterConvolutionTask

### Description
A QGIS background task (`QgsTask`) that applies a convolution kernel to a raster image using GDAL filters.

### Constructor

```python
RasterConvolutionTask(
    description: str,
    input_file: str,
    output_file: str,
    kernel: list[float],
    kernel_size: int = 3
)
```

### Example Usage

```python
from RasterConvolutionTask import RasterConvolutionTask

high_pass_kernel = [
    -1, -1, -1,
    -1,  8, -1,
    -1, -1, -1
]

task = RasterConvolutionTask(
    description="Edge detection",
    input_file="input.tif",
    output_file="output.tif",
    kernel=high_pass_kernel,
    kernel_size=3
)

QgsApplication.taskManager().addTask(task)
```

---

## Environment Setup

Run this code in the QGIS Python environment to access `qgis.core` and `gdal`.

### Debugging in VSCode

- The `.env` file points to your QGIS installation.
- Update `OSGEO4W_ROOT` and Python version accordingly.
- `.vscode/settings.json` ensures VSCode uses the correct environment variables.
