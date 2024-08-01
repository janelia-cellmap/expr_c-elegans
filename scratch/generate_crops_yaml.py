# %%
inputs_match = {"jrc_c-elegans-op50-1":["/nrs/cellmap/data/jrc_c-elegans-op50-1/jrc_celegans-op50-1_normalized.zarr","recon-1/em/fibsem-uint8/"],
"jrc_c-elegans-bw-1":["/nrs/cellmap/data/jrc_c-elegans-bw-1/jrc_c-elegans-bw-1_normalized.zarr","recon-1/em/fibsem-uint8/"],
"jrc_c-elegans-comma-1":["/nrs/cellmap/data/jrc_c-elegans-comma-1/jrc_c-elegans-comma-1.zarr","recon-1/em/fibsem-uint8"]}
# %%

datasets = ["jrc_c-elegans-op50-1","jrc_c-elegans-bw-1","jrc_c-elegans-comma-1"]

gt_pattern = "/nrs/cellmap/data/{dataset}/staging/groundtruth.zarr"
gt_dataset_pattern = "{crop_id}/{organelle}/"
# %%
organelles = ["mito","ld"]

result_crops = {"mito":{},"ld":{}}
for dataset in datasets:
    gt_path = gt_pattern.format(dataset=dataset)
    crops = [c for c in os.listdir(gt_path) if "crop" in c]
    print(crops)
    for crop in crops:
        print(crop)
        for organelle in organelles:
            gt_dataset_path = gt_dataset_pattern.format(crop_id=crop,organelle=organelle)
            if os.path.exists(os.path.join(gt_path,gt_dataset_path)):
                if dataset in result_crops[organelle]:
                    result_crops[organelle][dataset].append(crop)
                else:
                    result_crops[organelle][dataset] = [crop]
                # result_crops[organelle].append({"dataset":dataset,"crop":crop})
            else:
                print(f"{gt_path}/{gt_dataset_path} does not exist")
        

# %%
result_crops
# %%
import csv

groups = {"op50_bw-1":["jrc_c-elegans-op50-1","jrc_c-elegans-bw-1"],
"all":["jrc_c-elegans-op50-1","jrc_c-elegans-bw-1","jrc_c-elegans-comma-1"]}
for group in groups:
    for organelle in organelles:
        output_path = f"/groups/cellmap/cellmap/zouinkhim/c-elegen/csv_datasplit/20240726_{organelle}_{group}.csv"
        with open(output_path, mode='w') as file:
            writer = csv.writer(file)
            for dataset in groups[group]:
                crops = result_crops[organelle][dataset]
                for crop in crops:
                    # crop_container = f"{gt_pattern}/{dataset}/staging/groundtruth.zarr/crop{crop}/{organelle}"
                    gt_container = gt_pattern.format(dataset=dataset)
                    gt_dataset = gt_dataset_pattern.format(crop_id=crop,organelle=organelle)
                    writer.writerow(["train",inputs_match[dataset][0],inputs_match[dataset][1],gt_container,gt_dataset])
# %%
