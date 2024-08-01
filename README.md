
** This repo is a scratch pad of the scripts used for c-elegans analysis. **

Current c-eleganss datasets are :
- jrc_c-elegans-op50-1
- jrc_c-elegans-bw-1
- jrc_c-elegans-comma-1

Current Organelle target is :
- Mitochondria [mito]
- Lipid droplets [ld]

jrc_c-elegans-op50-1 and jrc_c-elegans-bw-1 are a bit similar that's why i am training a model using crops from both datasets. jrc_c-elegans-comma-1 is a bit different and no much crops are available for it yet.
Lipids in jrc_c-elegans-op50-1 and jrc_c-elegans-bw-1 are easy to identify as they are big and round. that's why i am using a scratch small unet for them
