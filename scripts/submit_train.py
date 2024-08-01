

import subprocess

# runs = [
#     "c_elegen_bw_op50_ld_scratch_0_v",
#     "c_elegen_bw_op50_ld_scratch_1_v",
# ]
# runs = [
#     "c_elegen_bw_op50_mito_setup04_0_v_using_all",
#     "c_elegen_bw_op50_mito_setup04_1_v_using_all"
# ]
# runs = ["bw_op50_mito_setup04_0_v_using_all","bw_op50_mito_setup04_1_v_using_all","bw_op50_mito_setup04_2_v_using_all"]
# runs = [
#     "c_elegen_bw_op50_mito_setup04_0_v",
#     "c_elegen_bw_op50_mito_setup04_1_v",
# ]


# runs = [
#     "20240722_bw_op50_mito_setup04_0_v_using_all",
#     "20240722_bw_op50_mito_setup04_1_v_using_all",
#     "20240722_bw_op50_mito_setup04_2_v_using_all",
#     "20240722_bw_op50_mito_setup04_0",
#     "20240722_bw_op50_mito_setup04_1",
#     "20240722_bw_op50_mito_setup04_2",
# ]
runs = [
    '20240722_all_ld_setup04_0',
 '20240722_all_ld_setup04_1', 
 '20240722_all_ld_setup04_2', 
#  '20240722_bw_op50_4nm_ld_setup04_0', 
#  '20240722_bw_op50_4nm_ld_setup04_1', 
#  '20240722_bw_op50_4nm_ld_setup04_2', 
#  '20240722_bw_op50_8nm_ld_setup04_0', 
#  '20240722_bw_op50_8nm_ld_setup04_1', 
#  '20240722_bw_op50_8nm_ld_setup04_2', 
#  '20240722_bw_op50_mito_setup04_0', 
 '20240722_bw_op50_mito_setup04_0_v_using_all', 
#  '20240722_bw_op50_mito_setup04_1', 
 '20240722_bw_op50_mito_setup04_1_v_using_all', 
#  '20240722_bw_op50_mito_setup04_2', 
 '20240722_bw_op50_mito_setup04_2_v_using_all', 
#  '20240722_bw_op50_mito_setup04_5_v_using_all'
]

# runs = [
# # "20240722_all_ld_setup04_0",
# # "20240722_all_ld_setup04_1",
# # # "20240722_all_ld_setup04_2",
# # "20240722_bw_op50_4nm_ld_setup04_0",
# # "20240722_bw_op50_4nm_ld_setup04_1",
# # "20240722_bw_op50_4nm_ld_setup04_2",
# "20240722_bw_op50_8nm_ld_setup04_0",
# "20240722_bw_op50_8nm_ld_setup04_1",
# # "20240722_bw_op50_8nm_ld_setup04_2"
# ]
for run_name in runs:
    command = [
        "bsub",
        "-P",
        "cellmap",
        "-We",
        "72:00",
        "-J",
        run_name,
        "-q",
        "gpu_tesla",
        "-n",
        f"20",
        "-gpu",
        "num=1",
        "-o",
        f"run_logs/{run_name}/logs/1.out",
        "-e",
        f"run_logs/{run_name}/logs/1.err",
        "dacapo",
        "train",
        "-r",
        run_name,
    ]

    subprocess.run(command)