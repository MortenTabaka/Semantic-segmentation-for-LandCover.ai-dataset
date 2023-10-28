Semantic segmentation of LandCover.ai dataset
==============================

The LandCover dataset consists of aerial images of urban and rural areas of Poland. The project focuses on the application of various neural networks for semantic segmentation, including the reconstruction of the neural network implemented by the authors of the dataset. 

The dataset used in this project is the [Landcover.ai Dataset](https://landcover.ai.linuxpolska.com/), 
which was originally published with [LandCover.ai: Dataset for Automatic Mapping of Buildings, Woodlands, Water and Roads from Aerial Imagery paper](https://arxiv.org/abs/2005.02264)
also accessible on [PapersWithCode](https://paperswithcode.com/paper/landcover-ai-dataset-for-automatic-mapping-of).

**Please note that I am not the author or owner of this dataset, and I am using it under the terms of the license specified by the original author. 
All credits for the dataset go to the original author and contributors.**

## Make predictions on custom images

After installing the necessary dependencies, execute the following scripts.

Add project root to the Python path:
```commandline
python3 models/scripts/add_project_root_to_the_python_path.py
```

Run prediction on images in `models/custom_data/input`:
```commandline
python3 models/scripts/run_prediction_on_folder.py
```
This script allows you to make predictions using the DeepLabv3+ model on a folder containing custom input images. You can use the following parameters to customize the prediction process:

* model_revision: This optional parameter allows you to choose which model revision to use for making predictions. 
The default is "deeplabv3plus_v5.10.2", but you can select a different revision from list of availabe ones (`--help`).

* input_folder: This optional parameter specifies the folder containing the input images that you want to make predictions on. 
The default folder is `models/custom_data/input`. Accepted image formats are **JPG, PNG and TIFF**.

* output_folder: This optional parameter specifies the folder where the output predictions will be saved. 
The default folder is `models/custom_data/output`.

To get more information on how to use the script, execute the following command:
```
python3 models/scripts/run_prediction_on_folder.py --help
```

## Sample result
The image used in this sample is a high-resolution TIFF orthophotomap covering an area of approximately 3.5 km². The image has a resolution of 25453x13176, and it is not part of the project dataset. Similar images for Poland regions can be obtained free of charge from the Head Office of Geodesy and Cartography through their [service](https://www.geoportal.gov.pl/dane/ortofotomapa).

To facilitate analysis, the image is split into tiles, and predictions are made on each tile. The outputs are then concatenated to the original size to produce the final result.

### Legend
- ![#000000](https://via.placeholder.com/15/000000/000000?text=+) `Background`
- ![#FF0000](https://via.placeholder.com/15/FF0000/000000?text=+) `Buildings`
- ![#008000](https://via.placeholder.com/15/008000/000000?text=+) `Woodland`
- ![#0000FF](https://via.placeholder.com/15/0000FF/000000?text=+) `Water`
- ![#FFFFFF](https://via.placeholder.com/15/FFFFFF/000000?text=+) `Roads`


![prediction.png](reports%2Ffigures%2Fprediction.png)
![orthophotomap.png](reports%2Ffigures%2Forthophotomap.png)

# Installation
There are two ways to run this project: installing the environment via Anaconda or running a Docker container (recommended).

## Docker
[Installation guide - Docker](https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset/blob/main/INSTALLATION-DOCKER.md)

## Anaconda Environment (legacy)
[Installation guide - Conda](https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset/blob/main/INSTALLATION-CONDA.md)

# Jupyter Notebooks

## [Development notebooks](https://drive.google.com/drive/folders/105HjfaU6_3NHRozYWXR9IjKiKKJRW5ez?usp=sharing)
Jupyter notebooks used in early-stage development.

## [Templates](https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset/tree/main/notebooks/templates)
Jupyter notebook templates for machine learning operations in the project.
### Available templates
   * [Training a new model.](https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset/blob/main/notebooks/templates/Model_training.ipynb)
   * [*LEGACY* - Predict and plot masks, generated by model with downloaded best weights.](https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset/blob/main/notebooks/templates/Plot_predictions.ipynb)

## DeepLabv3+ Architecture - Legacy Revisions

[Developemnt notebooks](https://drive.google.com/drive/folders/105HjfaU6_3NHRozYWXR9IjKiKKJRW5ez?usp=sharing)

| Ver. | Backbone                     | Weights    | Frozen convolution base | Loss function | Data augmentation | Train dataset size | Loss weights | mIoU on test dataset |
| --- |------------------------------|------------| --- | --- | --- | --- | --- | --- |
| 5.1 | Tensorflow Xception          | Imagenet   | Yes | Sparse Categorical Crossentropy | No | 7470 | No | 0.587 | 
| 5.2 | Tensorflow Xception | Imagenet   | Yes | Sparse Categorical Crossentropy | Yes | 14940 | No | 0.423 |
| 5.3 | Tensorflow Xception          | Imagenet   | Yes | Sparse Categorical Crossentropy | No | 7470 | Yes | 0.542 |
| 5.4 | Modified Xception            | Cityscapes | Yes | Sparse Categorical Crossentropy | No | 7470 | No | 0.549 |
| 5.4 | Modified Xception            | Cityscapes | Yes | Sparse Categorical Crossentropy | No | 7470 | Yes | 0.562 |
| 5.5 | Modified Xception            | Cityscapes | Yes | Sparse Categorical Crossentropy | No | 7470 | Yes | 0.567 |
| 5.6 | Modified Xception            | Cityscapes | Yes | Sparse Categorical Crossentropy | No | 7470 | Yes | 0.536 |
| 5.7 | Modified Xception            | Cityscapes | No | Sparse Categorical Crossentropy | No | 7470 | Yes | 0.359 |
| 5.8 | Modified Xception            | Cityscapes | Yes | Soft Dice Loss | No | 7470 | No | 0.559 |
| 5.9 | Modified Xception            | Pascal VOC | Partially | Soft Dice Loss | No | 7470 | No | 0.607 |
| **5.10** | Modified Xception            | Cityscapes | Partially | Soft Dice Loss | No | 7470 | No | **0.718** |
| 5.11 | Modified Xception            | Cityscapes | Partially | Soft Dice Loss | Yes | 14940 | No | 0.659 |
| 5.12 | Modified Xception            | Cityscapes | Partially | Soft Dice Loss | Yes | 7470 | No | 0.652 |

## Currently best mIoU score

![alt text](https://github.com/MortenTabaka/Semantic-segmentation-for-LandCover.ai-dataset/blob/main/reports/figures/Currently_best_classes_iou.png)

**Notebook v.5.10** with **meanIoU = 0.718**.

Notebooks are available [**on Google Drive**](https://drive.google.com/drive/folders/105HjfaU6_3NHRozYWXR9IjKiKKJRW5ez?usp=sharing).

## References
<a id="1">[1]</a> 
Boguszewski, Adrian and Batorski, Dominik and Ziemba-Jankowska, Natalia and Dziedzic, Tomasz and Zambrzycka, Anna (2021). ["LandCover.ai: Dataset for Automatic Mapping of Buildings, Woodlands, Water and Roads from Aerial Imagery"](https://arxiv.org/abs/2005.02264v2)

<a id="2">[2]</a> 
A. Abdollahi, B. Pradhan, G. Sharma, K. N. A. Maulud and A. Alamri, ["Improving Road Semantic Segmentation Using Generative Adversarial Network,"](https://ieeexplore.ieee.org/document/9416669) in IEEE Access, vol. 9, pp. 64381-64392, 2021, doi: 10.1109/ACCESS.2021.3075951.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    |   |   ├── architectures      <- Model architectures available for training
    │   │   ├── predict_model.py   
    │   │   └── model_builder.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

## Citation
If you use this software, please cite it using these metadata.
```
@software{Tabaka_Semantic_segmentation_of_2021,
author = {Tabaka, Marcin Jarosław},
license = {Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)},
month = {11},
title = {{Semantic segmentation of LandCover.ai dataset}},
url = {https://github.com/MortenTabaka/Semantic-segmentation-of-LandCover.ai-dataset},
year = {2021}
}
```

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
