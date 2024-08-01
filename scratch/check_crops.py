

# %%
paths = ["/nrs/cellmap/data/empiar_c-elegans/empiar_c-elegans_upscaled.zarr",
"/nrs/cellmap/data/empiar_fly-brain/empiar_fly-brain_upscaled.zarr",
"/nrs/cellmap/data/empiar_glycolytic-muscle/empiar_glycolytic-muscle_upscaled.zarr",
"/nrs/cellmap/data/empiar_hela-cell/empiar_hela-cell_upscaled.zarr",
"/nrs/cellmap/data/empiar_lucchi-pp/empiar_lucchi-pp_upscaled.zarr",
"/nrs/cellmap/data/empiar_salivary-gland/empiar_salivary-gland_upscaled.zarr"]
import zarr
for p in paths:
    z = zarr.open(p)
    print(p, z.tree())

# %%
