
import logging
import os
from dacapo.store.create_store import create_config_store, create_weights_store
from dacapo.experiments.run import Run
from dacapo import validate
import sys

logger = logging.getLogger(__name__)

folder_pattern = "/groups/cellmap/cellmap/zouinkhim/c-elegen/dacapo_files/{run_name}/checkpoints/iterations"

def process(run_name):
    config_store = create_config_store()
    run_config = config_store.retrieve_run_config(run_name)

    run = Run(run_config,load_starter_model=False)
    weights_store = create_weights_store()

    checkpoints = [int(x) for x in os.listdir(folder_pattern.format(run_name=run_name)) if x.isdigit()]

    for iteration in checkpoints:
        try:
            logger.info(f"Processing iteration {iteration}")
            # load weights
            run.model.load_state_dict(
                weights_store.retrieve_weights(run_name, iteration).model
            )
            logger.error(f"Loaded weights for iteration {iteration}")
            validate(run, iteration)
        except Exception as e:
            logger.error(f"Error processing iteration {iteration}: {e}")

if __name__ == "__main__":
    # get run_name from command line
    if len(sys.argv) > 1:
        run_name = sys.argv[1]
    else:
        print("Please provide a run_name as a command line argument.")
        sys.exit(1)
    process(run_name)



# run_name = "20240722_bw_op50_mito_setup04_0"