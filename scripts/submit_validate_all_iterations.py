
# runs= ["20240722_bw_op50_mito_setup04_0"]
runs = [
    # "20240722_bw_op50_4nm_ld_setup04_0",
    # "20240722_bw_op50_4nm_ld_setup04_2",
    # "20240722_bw_op50_8nm_ld_setup04_1",
    # "20240722_bw_op50_mito_setup04_1",
    # "20240722_bw_op50_mito_setup04_2",
    # "20240722_bw_op50_4nm_ld_setup04_1",
    "20240722_bw_op50_8nm_ld_setup04_0",
    # "20240722_bw_op50_8nm_ld_setup04_2"
]
import subprocess


for run_name in runs:
    command = [
        "bsub",
        "-P",
        "cellmap",
        "-We",
        "72:00",
        "-J",
        f"validate_{run_name}",
        "-q",
        "gpu_tesla",
        "-n",
        f"10",
        "-gpu",
        "num=1",
        "-o",
        f"/groups/cellmap/cellmap/zouinkhim/c-elegen/run_logs/validate_{run_name}.out",
        "-e",
        f"/groups/cellmap/cellmap/zouinkhim/c-elegen/run_logs/validate_{run_name}.err",
        "python",
        "validate_all_checkpoints.py",
        run_name,
        
    ]

    subprocess.run(command)