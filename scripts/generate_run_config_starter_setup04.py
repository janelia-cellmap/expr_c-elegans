# %%
import dacapo

# %%
from dacapo.store.create_store import create_config_store
# %%
config_store = create_config_store()

# %%

# %%
from dacapo.experiments.datasplits import DataSplitGenerator
from funlib.geometry import Coordinate


# input_resolution = Coordinate(16,16,16)
# output_resolution = Coordinate(8,8,8)

input_resolution = Coordinate(8, 8, 8)
output_resolution = Coordinate(4, 4, 4)
datasplit_config = DataSplitGenerator.generate_from_csv(
    "/groups/cellmap/cellmap/zouinkhim/c-elegen/csv_datasplit/20240726_mito_all.csv",
    input_resolution,
    output_resolution,
    targets=["mito"],
    name="20240726_mito_all_8_4nm",
).compute()
# config_store.delete_datasplit_config(datasplit_config.name)
datasplit = datasplit_config.datasplit_type(datasplit_config)
viewer = datasplit._neuroglancer()

config_store.store_datasplit_config(datasplit_config)

# %%
from dacapo.store.create_store import create_config_store
config_store = create_config_store()
new_datasplit_config = config_store.retrieve_datasplit_config("bw_op50_mito_4nm_upscaled_semantic_mito_4nm")

# %%
config_store.retrieve_datasplit_config_names()
# %%
config_store.datasplits


# %%
from dacapo.experiments.tasks import DistanceTaskConfig

task_config = DistanceTaskConfig(
    name="cosem_distance_task_ld_4nm_v2",
    channels=["ld"],
    clip_distance=20.0,
    tol_distance=20.0,
    scale_factor=40.0,
)
config_store.store_task_config(task_config)
# %%
from dacapo.experiments.architectures import CNNectomeUNetConfig

architecture_config = CNNectomeUNetConfig(
    name="upsample_unet",
    input_shape=Coordinate(216, 216, 216),
    eval_shape_increase=Coordinate(72, 72, 72),
    fmaps_in=1,
    num_fmaps=12,
    fmaps_out=72,
    fmap_inc_factor=6,
    downsample_factors=[(2, 2, 2), (3, 3, 3), (3, 3, 3)],
    constant_upsample=True,
    upsample_factors=[(2, 2, 2)],
)
config_store.store_architecture_config(architecture_config)
# %%
from dacapo.experiments.trainers.gp_augments import (
    ElasticAugmentConfig,
    GammaAugmentConfig,
    IntensityAugmentConfig,
    IntensityScaleShiftAugmentConfig,
)
from dacapo.experiments.trainers import GunpowderTrainerConfig

trainer_config = GunpowderTrainerConfig(
    name="mito_train_4nm_simpler",
    batch_size=1,
    learning_rate=0.0001,
    num_data_fetchers=40,
    augments=[
        ElasticAugmentConfig(
            control_point_spacing=[100, 100, 100],
            control_point_displacement_sigma=[10.0, 10.0, 10.0],
            rotation_interval=(0.0, 1.5707963267948966),
            subsample=8,
            uniform_3d_rotation=True,
        ),
        IntensityAugmentConfig(scale=(0.9, 1.2), shift=(-0.5, 0.35), clip=True),
        GammaAugmentConfig(gamma_range=(0.8, 1.2)),
        IntensityScaleShiftAugmentConfig(scale=1.2, shift=-1.0),
    ],
    snapshot_interval=100000,
    # min_masked=0.05,
    clip_raw=False,
)
config_store.store_trainer_config(trainer_config)
# %%
from dacapo.experiments import RunConfig
from dacapo.experiments.run import Run

from dacapo.store.create_store import create_config_store

config_store = create_config_store()
from dacapo.experiments.starts import CosemStartConfig

# We will now download a pretrained cosem model and finetune from that model. It will only have to download the first time it is used.

start_config = CosemStartConfig("setup04", "1820500")
# %%

config_store.retrieve_trainer_config_names()

# %%
config_store.retrieve_datasplit_config_names()
# %%
trainer_config = config_store.retrieve_trainer_config("mito_train_4nm_simpler")
architecture_config = config_store.retrieve_architecture_config("upsample_unet")
task_config = config_store.retrieve_task_config("cosem_distance_task_ld_4nm_v2")
datasplplits = ["20240722_ld_op50_bw_8_4nm_v2_semantic_ld_8nm"]
datasplit_config = config_store.retrieve_datasplit_config(datasplplits[0])
# %%
iterations = 500000
validation_interval = 10000
repetitions = 3
for i in range(repetitions):
    run_config = RunConfig(
        name=f"20240722_bw_op50_8nm_ld_setup04_{i}",
        datasplit_config=datasplit_config,
        task_config=task_config,
        architecture_config=architecture_config,
        trainer_config=trainer_config,
        num_iterations=iterations,
        validation_interval=validation_interval,
        repetition=i,
        start_config=start_config,
    )


    print(run_config.name)
    config_store.delete_run_config(run_config.name)
    config_store.store_run_config(run_config)
# %%