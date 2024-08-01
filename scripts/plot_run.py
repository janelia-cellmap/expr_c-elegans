# # %%

run_name = "20240722_bw_op50_mito_setup04_0"
from dacapo.plot import plot_runs
plot_runs([run_name],validation_scores=["mito__f1_score"],plot_losses=[True] )
# %%