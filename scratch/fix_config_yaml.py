import yaml
from yaml.loader import SafeLoader
from yaml.dumper import SafeDumper

def tuple_constructor(loader, node):
    return tuple(loader.construct_sequence(node))

def tuple_representer(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:python/tuple', data)

def replace_mito(data, to_change, new_value):
    """
    Recursively replace all instances of ['mito'] with mito in the data.
    """
    if isinstance(data, dict):
        return {key: replace_mito(value,to_change, new_value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_mito(item,to_change, new_value) for item in data]
    elif isinstance(data, tuple):
        return tuple(replace_mito(item,to_change, new_value) for item in data)
    elif isinstance(data, str) and data == to_change:
        return new_value
    else:
        return data

def read_and_modify_yaml(input_file, output_file, to_change, new_value, overwrite=False):
    """
    Read a YAML file, replace ['mito'] with mito, and write the result to another YAML file.
    """
    with open(input_file, 'r') as infile:
        data = yaml.load(infile, Loader=SafeLoader)

    modified_data = replace_mito(data, to_change, new_value)

    if overwrite:
        output_file = input_file

    with open(output_file, 'w') as outfile:
        yaml.dump(modified_data, outfile, Dumper=SafeDumper)

if __name__ == "__main__":
    yaml.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor, Loader=SafeLoader)
    yaml.add_representer(tuple, tuple_representer, Dumper=SafeDumper)
    
    input_file = '/groups/cellmap/cellmap/zouinkhim/c-elegen/dacapo_files/configs/runs/20240722_bw_op50_mito_setup04_0_v_using_all.yaml'  # Replace with your input file name
    output_file = '/groups/cellmap/cellmap/zouinkhim/c-elegen/dacapo_files/configs/runs/20240722_bw_op50_mito_setup04_0_v_using_all.yaml' # Replace with your output file name
    to_change = "['mito']"
    new_value = "mito"

    read_and_modify_yaml(input_file, output_file, to_change, new_value,overwrite=True)
