
runs= ["20240722_bw_op50_mito_setup04_0"]

iteration  = 100000

import subprocess


for run_name in runs:
    command = [
        "bsub",
        "-P",
        "cellmap",
        "-We",
        "72:00",
        "-J",
        f"validate{run_name}",
        "-q",
        "gpu_tesla",
        "-n",
        f"20",
        "-gpu",
        "num=1",
        "-o",
        f"run_logs/validate_{run_name}/logs/1.out",
        "-e",
        f"run_logs/validate_{run_name}/logs/1.err",
        "dacapo",
        "validate",
        "-r",
        run_name,
        "-i",
        str(iteration),
        
    ]

    subprocess.run(command)