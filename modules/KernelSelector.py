class KernelSelector:
    """
    Utility class for selecting commonly used convolution kernels by name.
    Supports both static and dynamically generated kernels.
    """

    kernel_descriptions = {
        "sobel_horizontal": "Detects horizontal edges by computing intensity gradient along the Y-axis.",
        "sobel_vertical": "Detects vertical edges by computing intensity gradient along the X-axis.",
        "prewitt_horizontal": "Alternative to Sobel; emphasizes horizontal transitions.",
        "prewitt_vertical": "Alternative to Sobel; emphasizes vertical transitions.",
        "laplacian": "Highlights regions of rapid intensity change in all directions.",
        "sharpen": "Sharpens image by increasing contrast around edges.",
        "high_pass": "Strong edge detector that emphasizes fine detail.",
        "gaussian_blur": "Smooths image and reduces noise using a 3x3 Gaussian kernel.",
        "gaussian_blur_5x5": "Stronger smoothing using a 5x5 Gaussian kernel.",
        "tall_grass_enhancer": "Enhances localized texture variation, useful for spotting tall grass or clumps."
    }

    @staticmethod
    def get_kernel(name: str):
        name = name.lower()

        kernels = {
            "sobel_horizontal": [
                -1, -2, -1,
                 0,  0,  0,
                 1,  2,  1
            ],
            "sobel_vertical": [
                -1,  0,  1,
                -2,  0,  2,
                -1,  0,  1
            ],
            "prewitt_horizontal": [
                -1, -1, -1,
                 0,  0,  0,
                 1,  1,  1
            ],
            "prewitt_vertical": [
                -1,  0,  1,
                -1,  0,  1,
                -1,  0,  1
            ],
            "laplacian": [
                 0, -1,  0,
                -1,  4, -1,
                 0, -1,  0
            ],
            "sharpen": [
                 0, -1,  0,
                -1,  5, -1,
                 0, -1,  0
            ],
            "high_pass": [
                -1, -1, -1,
                -1,  8, -1,
                -1, -1, -1
            ],
            "gaussian_blur": [x / 16 for x in [
                1, 2, 1,
                2, 4, 2,
                1, 2, 1
            ]],
            "gaussian_blur_5x5": [x / 273 for x in [
                1,  4,  7,  4, 1,
                4, 16, 26, 16, 4,
                7, 26, 41, 26, 7,
                4, 16, 26, 16, 4,
                1,  4,  7,  4, 1
            ]],
            "tall_grass_enhancer": [
                -0.5, -0.5, -0.5,
                -0.5,  4.0, -0.5,
                -0.5, -0.5, -0.5
            ]
        }

        if name not in kernels:
            raise ValueError(f"Kernel '{name}' not found. Available kernels: {list(kernels.keys())}")

        return kernels[name]

    @staticmethod
    def get_description(name: str):
        """Retrieve the description of a given kernel."""
        return KernelSelector.kernel_descriptions.get(name.lower(), "No description available.")

    @staticmethod
    def generate_identity_kernel(size: int):
        """
        Generate an identity kernel of any odd size (center value is 1, others 0)
        """
        if size % 2 == 0:
            raise ValueError("Kernel size must be odd.")
        kernel = [0] * (size * size)
        center = (size * size) // 2
        kernel[center] = 1
        return kernel

    @staticmethod
    def generate_uniform_blur_kernel(size: int):
        """
        Generate a uniform blur kernel (box filter) of given size
        """
        if size <= 0:
            raise ValueError("Kernel size must be positive.")
        value = 1.0 / (size * size)
        return [value] * (size * size)