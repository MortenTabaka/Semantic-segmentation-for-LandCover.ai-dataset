import os
from typing import Dict, List, Tuple, Union

from numpy import array, logical_and, stack, uint8, zeros_like
from tensorflow import Tensor, convert_to_tensor, expand_dims, keras
from tensorflow import uint8 as tf_uint8
from tensorflow.keras.preprocessing.image import array_to_img
from yaml import dump, safe_load

from src.features.utils import get_absolute_path_to_project_location


def revision_a_model(
    model_name: str,
    revision: str,
    batch_size: int,
    input_image_height: int,
    input_image_width: int,
    number_of_classes: int,
    model_build_params: Dict[str, Union[int, Tuple[int, int, int], str, None, float]],
    optimizer: keras.optimizers.Optimizer,
    loss_function: keras.losses.Loss,
    initial_learning_rate: float,
    final_learning_rate: Union[float, None],
    metrics: Union[keras.metrics.Metric, str, List[Union[keras.metrics.Metric, str]]],
):
    """
    Utility to create yaml file for model revisions
    Args:
        model_name: name of model got with model.name
            e.g. deeplabv3plus or modified_v2_deeplabv3plus
        revision: version of model during training, e.g. 10.0.1
        batch_size: size of single batch
        input_image_width:
        input_image_height:
        model_build_params: params needed to build model with
            e.g. src.models.architectures.deeplabv3plus
        optimizer:
        loss_function:
        initial_learning_rate:
        final_learning_rate: learning rate in decaying scheduler
        number_of_classes:
        metrics:
    Returns:
        model_key: f"{model_architecture}_{revision}"
    """
    config_dict = {
        "model_name": model_name,
        "revision": revision,
        "dataset_parameters": {
            "input_image_height": input_image_height,
            "input_image_width": input_image_width,
            "number_of_classes": number_of_classes,
            "batch_size": batch_size,
        },
        "model_build_parameters": model_build_params,
        "model_compile_parameters": {
            "optimizer": str(optimizer),
            "loss_function": {
                "object": str(loss_function),
                "initial_learning_rate": initial_learning_rate,
                "final_learning_rate": final_learning_rate,
            },
            "metrics": [str(metric) for metric in metrics],
        },
    }

    model_key = f"{model_name}_v{revision}"

    yaml_filepath = get_absolute_path_to_project_location(
        "models/models_revisions.yaml"
    )

    if not os.path.exists(yaml_filepath):
        # create empty file if it doesn't exist
        with open(yaml_filepath, "w") as f:
            f.write("")

    update_yaml_revision(model_key, config_dict)

    return model_key


def get_model_build_params_for_revision(model_key) -> List:
    data = load_data_for_revision(model_key)

    try:
        pretrained_weights = data["model_build_parameters"]["pretrained_weights"]
        second_input = data["model_build_parameters"]["second_input"]
        input_shape = (
            data["model_build_parameters"]["input_shape"]["input_image_height"],
            data["model_build_parameters"]["input_shape"]["input_image_width"],
            data["model_build_parameters"]["input_shape"]["channels"],
        )
        num_classes = data["model_build_parameters"]["num_classes"]
        backbone = data["model_build_parameters"]["backbone"]
        output_stride = data["model_build_parameters"]["output_stride"]
        alpha = data["model_build_parameters"]["alpha"]
        activation = data["model_build_parameters"]["activation"]

        model_build_parameters = [
            pretrained_weights,
            second_input,
            input_shape,
            num_classes,
            backbone,
            output_stride,
            alpha,
            activation,
        ]
    except KeyError as e:
        raise ValueError(f"YAML file does not contain expected data: {e}")

    return model_build_parameters


def get_revision_model_architecture(model_key: str):
    data = load_data_for_revision(model_key)
    return data["model_name"]


def load_data_for_revision(model_key):
    yaml_filepath = get_absolute_path_to_project_location(
        "models/models_revisions.yaml"
    )
    if not os.path.exists(yaml_filepath):
        raise ValueError(f"YAML file {yaml_filepath} does not exist")

    with open(yaml_filepath, "r") as f:
        existing_models_revisions = safe_load(f)

    data = existing_models_revisions.get(model_key, {})

    if not data:
        raise ValueError(f"YAML file {yaml_filepath} does not contain expected data.")
    return data


def decode_segmentation_mask_to_rgb(
    mask, custom_colormap: List[int], num_classes: int = 5, return_numpy: bool = False
) -> array:
    """
    Transforms Landcover dataset's masks to RGB image.

    Args:
        custom_colormap:
        mask: prediction;
        num_classes: number of classes;
    """
    mask = mask[0]

    if len(custom_colormap) != num_classes:
        raise AttributeError("")

    r = zeros_like(mask).astype(uint8)
    g = zeros_like(mask).astype(uint8)
    b = zeros_like(mask).astype(uint8)

    if return_numpy:
        first_channel, second_channel, third_channel = 2, 1, 0
    else:
        first_channel, second_channel, third_channel = 0, 1, 2

    for i in range(0, num_classes):
        idx = mask == i
        r[idx] = custom_colormap[i][first_channel]
        g[idx] = custom_colormap[i][second_channel]
        b[idx] = custom_colormap[i][third_channel]

    rgb = stack([r, g, b], axis=2)

    if return_numpy:
        return rgb

    image = array_to_img(rgb)
    return image


def encode_segmentation_mask_to_logits(rgb_mask, custom_colormap: List[int]) -> Tensor:
    # Extract the R, G, B channels
    r = rgb_mask[:, :, 0]
    g = rgb_mask[:, :, 1]
    b = rgb_mask[:, :, 2]

    # Determine the class labels using the custom color map
    num_classes = len(custom_colormap)
    mask = zeros_like(r)
    for i in range(num_classes):
        idx = logical_and(
            r == custom_colormap[i][0],
            logical_and(g == custom_colormap[i][1], b == custom_colormap[i][2]),
        )
        mask[idx] = i

    mask_tensor = convert_to_tensor(mask, dtype=tf_uint8)
    mask_tensor = expand_dims(mask_tensor, axis=0)
    return mask_tensor


def update_yaml_revision(model_revision: str, to_add: dict):
    yaml_filepath = get_absolute_path_to_project_location(
        "models/models_revisions.yaml"
    )
    with open(yaml_filepath, "r") as f:
        existing_models_revisions = safe_load(f)

    if existing_models_revisions is None:
        existing_models_revisions = {}

    if model_revision in existing_models_revisions:
        existing_models_revisions[model_revision].update(to_add)
    else:
        existing_models_revisions[model_revision] = to_add

    with open(yaml_filepath, "w") as f:
        dump(existing_models_revisions, f, default_flow_style=False, sort_keys=False)
