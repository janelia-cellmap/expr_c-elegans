# %%
import os
import zarr
path = "/nrs/cellmap/zubovy/temp/cma_test"

os.listdir(path)
# %%
for f in os.listdir(path):
    print(f)
    z = zarr.open(f"{path}/{f}")
    print(z.tree(level=1))
# %%


inputs = [
    "jrc_c-elegans-bw-1/crop541",
    "jrc_c-elegans-bw-1/crop540",
    "jrc_c-elegans-comma-1/crop496",
    "jrc_c-elegans-op50-1/crop521",
    "jrc_c-elegans-op50-1/crop528",
    "jrc_c-elegans-op50-1/crop532",
    "jrc_c-elegans-op50-1/crop535",
    "jrc_c-elegans-bw-1/crop527",
    "jrc_c-elegans-bw-1/crop538",
    "jrc_c-elegans-bw-1/crop536",
    "jrc_c-elegans-bw-1/crop526",
    "jrc_c-elegans-op50-1/crop533",
    "jrc_c-elegans-comma-1/crop515",
    "jrc_c-elegans-bw-1/crop519"]

inputs_match = {"jrc_c-elegans-op50-1":"-f /nrs/cellmap/data/jrc_c-elegans-op50-1/jrc_celegans-op50-1_normalized.zarr -d recon-1/em/fibsem-uint8/",
"jrc_c-elegans-bw-1":"-f /nrs/cellmap/data/jrc_c-elegans-bw-1/jrc_c-elegans-bw-1_normalized.zarr -d recon-1/em/fibsem-uint8/",
"jrc_c-elegans-comma-1":"-f /nrs/cellmap/data/jrc_c-elegans-comma-1/jrc_c-elegans-comma-1.zarr -d recon-1/em/fibsem-uint8"}
# %%
result = {}
for i in inputs:
    key = i.split("/")[0]
    if key not in result:
        result[key] = []
    result[key].append(i.split("/")[1])
result
    
# %%
commands = []
for key in result:
    command = []
    command.append(f"neuroglancer {inputs_match[key]}")

    for crop in result[key]:
        command.append(f" -f {path}/{crop}.zarr -d all")
    commands.append("".join(command))


# %%
import subprocess
subprocess.run(commands[2], shell=True)
# %%

crops_label = {"mito": [541,519,515,521,532,535,533],
"ld": [540,527,538,536,526,496,528]}
# %%
inputs_match = {"jrc_c-elegans-op50-1":["/nrs/cellmap/data/jrc_c-elegans-op50-1/jrc_celegans-op50-1_normalized.zarr","recon-1/em/fibsem-uint8/"],
"jrc_c-elegans-bw-1":["/nrs/cellmap/data/jrc_c-elegans-bw-1/jrc_c-elegans-bw-1_normalized.zarr","recon-1/em/fibsem-uint8/"],
"jrc_c-elegans-comma-1":["/nrs/cellmap/data/jrc_c-elegans-comma-1/jrc_c-elegans-comma-1.zarr","recon-1/em/fibsem-uint8"]}
# %%
#  generate csv
output_path = "/groups/cellmap/cellmap/zouinkhim/c-elegen/20240722_ld_all.csv"
# %%
import csv

label = "ld"
with open(output_path, mode='w') as file:
    writer = csv.writer(file)
    #  get dataset for crop
    dataset = result
    crops_ids = crops_label[label]
    
    for crop in crops_ids:
        # get the key that have the crop id in result
        crop_key = f"crop{crop}"
        dataset_key = [key for key in dataset if crop_key in dataset[key]][0]
        print(dataset_key)

        input_container = inputs_match[dataset_key][0]
        input_dataset = inputs_match[dataset_key][1]
        print(input_container)
        print(input_dataset)
        crop_container = f"{path}/{crop_key}.zarr"
        crop_dataset = label
        writer.writerow(["train",input_container,input_dataset,crop_container,crop_dataset])
        
# %%
os.listdir("/nrs/cellmap/data/jrc_c-elegans-bw-1/staging/groundtruth.zarr/crop519/ld/s0")
 # %%


datasets = ["jrc_c-elegans-op50-1","jrc_c-elegans-bw-1","jrc_c-elegans-comma-1"]

gt_pattern = "/nrs/cellmap/data/{dataset}/staging/groundtruth.zarr/crop{crop_id}/{organelle}/"
# %%
organelles = ["mito","ld"]

    