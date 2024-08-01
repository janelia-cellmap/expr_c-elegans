# %%
import dacapo

# %%
from dacapo.store.create_store import create_config_store
# %%
config_store = create_config_store()
# %%
from dacapo.experiments.datasplits import DataSplitGenerator
from funlib.geometry import Coordinate

input_resolution = Coordinate(16, 16, 16)
output_resolution = Coordinate(16 ,16, 16)
datasplit_config = DataSplitGenerator.generate_from_csv(
    "/groups/cellmap/cellmap/zouinkhim/c-elegen/crops_both_ld_test.csv",
    input_resolution,
    output_resolution,
    targets=["ld"],
    name="ld_distance_task_16nm_test",
).compute()
datasplit = datasplit_config.datasplit_type(datasplit_config)
viewer = datasplit._neuroglancer()
config_store.store_datasplit_config(datasplit_config)
# %%
from dacapo.experiments.tasks import DistanceTaskConfig

task_config = DistanceTaskConfig(
    name="ld_distance_task_4nm",
    channels=["ld"],
    clip_distance=10.0,
    tol_distance=10.0,
    scale_factor=20.0,
)
config_store.store_task_config(task_config)
# %%
from dacapo.experiments.architectures import CNNectomeUNetConfig


architecture_config = CNNectomeUNetConfig(
    name="unet_mini",
    input_shape=Coordinate(216, 216, 216),
    eval_shape_increase=Coordinate(72, 72, 72),
    fmaps_in=1,
    num_fmaps=2,
    fmaps_out=2,
    fmap_inc_factor=2,
    downsample_factors=[(2, 2, 2), (3, 3, 3), (3, 3, 3)],
    constant_upsample=True,
    upsample_factors=[],
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
    name="ld_train_8nm",
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
        GammaAugmentConfig(gamma_range=(0.5, 2.0)),
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
# from dacapo.experiments.starts import CosemStartConfig

# We will now download a pretrained cosem model and finetune from that model. It will only have to download the first time it is used.

# start_config = CosemStartConfig("setup04", "1820500")

# %%
trainer_config = config_store.retrieve_trainer_config("ld_train_8nm")
architecture_config = config_store.retrieve_architecture_config("unet_mini")
task_config = config_store.retrieve_task_config("ld_distance_task_4nm")
# datasplit_config = config_store.retrieve_datasplit_config("ld_distance_task_4nm")
# %%
iterations = 3000
validation_interval = 100
repetitions = 1
for i in range(repetitions):
    run_config = RunConfig(
        name=f"tmp_c_elegen_bw_op50_ld_scratch_{i}_v",
        datasplit_config=datasplit_config,
        task_config=task_config,
        architecture_config=architecture_config,
        trainer_config=trainer_config,
        num_iterations=iterations,
        validation_interval=validation_interval,
        repetition=i,
        # start_config=start_config,
    )

    print(run_config.name)
    config_store.store_run_config(run_config)
# %%
from dacapo.train import train_run
from dacapo.experiments.run import Run
from dacapo.store.create_store import create_config_store

config_store = create_config_store()
# run = Run(run_config)

run = Run(config_store.retrieve_run_config("tmp_c_elegen_bw_op50_ld_scratch_0_v"))
# we already trained it, so we will just load the weights
train_run(run)

# %%
# config_store
# %%
config_store.retrieve_run_config_names()
# %%
