from pathlib import Path
import argparse
import re

def make_folder(folder: str):
    """Test to see if the given folder already exists, and if not, it will create the folder.

    Args:
        folder (str): Folder path to be checked and be created.
    """    
    path = Path(folder)
    
    if not path.exists():
        path.mkdir()

def get_data_from_file(path: str) -> str:
    """Function to get a string of the content of the file in a path.

    Args:
        path (str): Path of the file to be read

    Returns:
        str: Contents of the file as a string.
    """
    file = Path(path)
    assert file.is_file() and file.exists(), f"File {path} could not be found."
    
    with file.open("r") as input_file:
        data = input_file.read()
        
    return data

def write_file(output_file : Path, file_data : str) -> None:
    """Write contents to a file. If the file does not exists yet, the file will be created. All previous content in the file will be overwritten!

    Args:
        output_file (Path): Path object of the output file.
        file_data (str): Data that should be written to the sile
    """    
    if not output_file.exists():
        output_file.touch()
        
    with output_file.open("w") as filewriter:
        filewriter.write(file_data)
        

def parse_file(input_file_path: Path) -> str:
    """Parses the input file in order to remove all the \input statements from the file.

    Args:
        input_file_path (Path): Input LaTeX file to parse.

    Returns:
        str: Output content of the new LaTeX file.
    """
    assert input_file_path.exists(), "Input file does not exist."
    assert input_file_path.is_file(), "Input should be a file, not a folder."
    
    project_folder = input_file_path.parent.absolute()
    
    return_content = get_data_from_file(input_file_path)
    
    while find_amount_of_inputs(return_content) > 0:
        input_statements, splitted_file = find_inputs_in_file(return_content)
        
        output_text = ""
        
        for i, input_statement in enumerate(input_statements):
            output_text += splitted_file[i]
            
            file_path = project_folder / Path(input_statement)
            
            input_data = get_data_from_file(file_path)
            
            output_text += input_data
        
        if i < len(splitted_file) - 1:
            output_text += splitted_file[-1] 
        
        return_content = output_text

    return return_content

def find_amount_of_inputs(input_file: str) -> int:
    """Find the amounts of inputs that are yet to be replaced in the input file.

    Args:
        input_file (str): Content of the input file to be checked.

    Returns:
        int: Number of inputs that should still be replaced.
    """    
    inputs, _ = find_inputs_in_file(input_file)
    
    return len(inputs)

def find_inputs_in_file(input_file: str) -> tuple[list[str], list[str]]:
    """Find a list of input files and splits the output file around the inputs.

    Args:
        input_file (str): Contents of input file where the inputs should be replaced.

    Returns:
        tuple[list[str], list[str]]: tuple of first the list of files that should be included and second a list of the contents of the file around the inputs.
    """    
    input_statements = re.findall("\\\\input{(.*)}", input_file)
    
    splitted_file = re.split("\\\\input{.*}", input_file)
    return input_statements,splitted_file
    
    
def main(input_file: Path, output_folder: Path) -> None:
    make_folder(output_folder)
    
    new_file_data = parse_file(input_file)
    
    output_file = output_folder / Path(input_file.name)
    
    write_file(output_file, new_file_data)


    

def parse_args() -> tuple[Path, Path]:
    arg_parser = argparse.ArgumentParser(prog="LaTeX Preprocessor", description="Simple program to preprocess a complex LaTeX project to a single folder with just a single .tex file with figures.")
    
    arg_parser.add_argument("input_file", type=str, help="Input LaTeX file from where to build the ouput file.")
    arg_parser.add_argument("output_folder", type=str, help="Output folder where all the files should be stored.")
    
    parsed_arguments = arg_parser.parse_args()
    
    return Path(parsed_arguments.input_file), Path(parsed_arguments.output_folder)

if __name__ == "__main__":
    main(*parse_args())