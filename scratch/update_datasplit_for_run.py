
# %%
from dacapo.train import train_run
from dacapo.experiments.run import Run
from dacapo.store.create_store import create_config_store

config_store = create_config_store()

# run = Run(run_config)
# run = Run(config_store.retrieve_run_config("test_mito_run"))
# # we already trained it, so we will just load the weights
# train_run(run)

# %%
config_store
# %%
config_store.retrieve_run_config_names()
# %%
run_config = config_store.retrieve_run_config("20240722_bw_op50_mito_setup04_0_v_using_all")
# %%
run = Run(run_config)
# %%
valite = run.datasplit.validate
# %%
config_store.retrieve_run_config_names()
# %%
config_store.retrieve_datasplit_config_names()
# %%
matches_run_datasplit = {'20240722_all_ld_setup04_0':"20240726_ld_all_8_4nm_semantic_ld_4nm",
 '20240722_all_ld_setup04_1':"20240726_ld_all_8_4nm_semantic_ld_4nm",
 '20240722_all_ld_setup04_2':"20240726_ld_all_8_4nm_semantic_ld_4nm",
 '20240722_bw_op50_4nm_ld_setup04_0':"20240726_ld_op50_bw_8_4nm_semantic_ld_4nm",
 '20240722_bw_op50_4nm_ld_setup04_1':"20240726_ld_op50_bw_8_4nm_semantic_ld_4nm",
 '20240722_bw_op50_4nm_ld_setup04_2':"20240726_ld_op50_bw_8_4nm_semantic_ld_4nm",
 '20240722_bw_op50_8nm_ld_setup04_0':"20240726_ld_op50_bw_16_8nm_semantic_ld_8nm",
 '20240722_bw_op50_8nm_ld_setup04_1':"20240726_ld_op50_bw_16_8nm_semantic_ld_8nm",
 '20240722_bw_op50_8nm_ld_setup04_2':"20240726_ld_op50_bw_16_8nm_semantic_ld_8nm",
 '20240722_bw_op50_mito_setup04_0':"20240726_mito_op50_bw-1_8_4nm_semantic_mito_4nm",
 '20240722_bw_op50_mito_setup04_0_v_using_all':"20240726_mito_all_8_4nm_semantic_mito_4nm",
 '20240722_bw_op50_mito_setup04_1':"20240726_mito_op50_bw-1_8_4nm_semantic_mito_4nm",
 '20240722_bw_op50_mito_setup04_1_v_using_all':"20240726_mito_all_8_4nm_semantic_mito_4nm",
 '20240722_bw_op50_mito_setup04_2':"20240726_mito_op50_bw-1_16_8nm_semantic_mito_8nm",
 '20240722_bw_op50_mito_setup04_2_v_using_all':"20240726_mito_all_16_8nm_semantic_mito_8nm",
#  '20240722_bw_op50_mito_setup04_5_v_using_all':"20240726_mito_all_16_8nm_semantic_mito_8nm",
 }
def update_run_datasplit(run_name,datasplit_name):
    run_config = config_store.retrieve_run_config(run_name)
    datasplit_config = config_store.retrieve_datasplit_config(datasplit_name)
    run_config.datasplit_config = datasplit_config
    config_store.delete_run_config(run_name)
    config_store.store_run_config(run_config)
# %%
for run,datasplit in matches_run_datasplit.items():
    print(run)
    update_run_datasplit(run,datasplit)
# %%
# omport subprocess
runs = matches_run_datasplit.keys()
print(list(runs))
# %%
config_store.path
# %%
