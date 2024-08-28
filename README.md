# Introduction
We introduce a large-scale challenging multispectral dataset, named DrMOD. This dataset consists of 14,041 multispectral images, each with eight spectral channels and a spatial resolution of 1200 x 900. It spans eight object categories and includes 330,191 rotated bounding boxes. DrMOD covers a diverse range of urban scenes from drone perspectives, addressing challenges such as small-sized objects and complex backgrounds.

# Links
Download links of the dataset will be posted here later.

# Model Weights
We utilize a ResNet50 backbone pre-trained on the ImageNet dataset for initialization to accelerate model convergence. For MSI input, it’s obtained from ResNet50 based on wavelength interpolation ([425, 490, 550, 600, 660, 725, 780, 880] nm). The interpolated weights file will be posted here later.

# Visualization and Attribute Analysis
Some examples of the annotation:
![DrMOD_annotation](https://github.com/DrMOD-330k/Multi-Spectral/blob/main/resources/DrMOD_annotation.png)

Data statistics and attribute analysis:
![statistic](https://github.com/DrMOD-330k/Multi-Spectral/blob/main/resources/statistic.png)

# Acknowledgement
We express our sincere gratitude to the contributors of the [MMRotate](https://github.com/open-mmlab/mmrotate) project. The MMRotate codebase provided a solid foundation for our work in multispectral rotated object detection, and its modular design and comprehensive documentation significantly facilitated our research and development process.
