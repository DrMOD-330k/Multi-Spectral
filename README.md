# Introduction
DrMOD, a large-scale challenging multispectral dataset. This dataset consists of 14,041 multispectral images, each with eight spectral channels and a spatial resolution of 1200 x 900. It spans eight object categories and includes 330,191 rotated bounding boxes. DrMOD dataset covers a diverse range of urban scenes from drone perspectives, addressing challenges such as small-sized objects and complex backgrounds.

# Dataset
Visualization examples of the annotation:
![DrMOD](https://github.com/DrMOD-330k/Multi-Spectral/blob/main/resources/DrMOD.png)

Data statistics and attribute analysis:
![statistic](https://github.com/DrMOD-330k/Multi-Spectral/blob/main/resources/statistic.png)

# Download
Download links of the whole dataset will be posted here later.

# Baseline Models
We utilize a ResNet50 backbone pretrained on the ImageNet dataset for initialization. For MSI input, it’s obtained from ResNet50 based on wavelength interpolation ([425, 490, 550, 600, 660, 725, 780, 880] nm). The interpolated weights file will be posted here later. **Note:** When using the multispectral baseline models, you need to modify the number of input channels in the first layer of the network to 8 to match the 8-channel multispectral pretrained weights.

# Code
The proposed methods are implemented based on pytorch, and the evaluation code has been open source. For details, please see [MMRotate](https://github.com/open-mmlab/mmrotate).

# Acknowledgement
We express our sincere gratitude to the contributors of the [MMRotate](https://github.com/open-mmlab/mmrotate) project. The MMRotate codebase provided a solid foundation for our work in multispectral rotated object detection, and its modular design and comprehensive documentation significantly facilitated our research and development process.
