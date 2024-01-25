import argparse
import zipfile
import subprocess
import sys
from pathlib import Path
import shutil

def generate_requirements(requirements_file_path: Path) -> None:
    """
    Generates a requirements.txt file from the active Poetry environment.

    Args:
    requirements_file_path (Path): Path to the requirements.txt file to be generated.
    """
    subprocess.check_call(['poetry', 'export', '-f', 'requirements.txt', '--output', str(requirements_file_path)])

def create_zip_file_with_lambda_files_and_packages(lambda_zip: Path, lambda_file_path: Path, temp_directory: Path) -> None:
    """
    Create a zip file with the specified lambda file and installed packages.

    Args:
    lambda_zip (Path): Path to the output ZIP file.
    lambda_file_path (Path): Path to the Lambda function file.
    temp_directory (Path): Path to the temporary directory where dependencies are installed.
    """
    with zipfile.ZipFile(lambda_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the specified Lambda function file to the ZIP
        zipf.write(lambda_file_path, lambda_file_path.name)

        # Add the installed packages to the ZIP at root
        for file_path in temp_directory.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(temp_directory))


def install_packages(requirements_file_path: Path, temp_directory: Path) -> None:
    """
    Install packages from the requirements file to the temporary directory.

    Args:
    requirements_file_path (Path): Path to the requirements.txt file.
    temp_directory (Path): Path to the temporary directory.
    """
    if sys.platform == "win32":
        subprocess.check_call(['pip', 'install', '-r', str(requirements_file_path), '-t', str(temp_directory)], shell=True)
    else:
        subprocess.check_call(['pip', 'install', '-r', str(requirements_file_path), '-t', str(temp_directory)])

def create_lambda_zip(input_path: Path, requirements_path: Path, output_path: Path) -> None:
    """
    Create a zip file to deploy Lambda along with its dependencies.

    Args:
    input_path (Path): Path to the Lambda function file.
    requirements_file_path (Path): Path to the requirements.txt file.
    output_path (Path): Path to the output ZIP file.
    """

    # Create a temporary directory to install packages
    temp_directory = Path('../package')
    temp_directory.mkdir(parents=True, exist_ok=True)

    # Install packages to the temporary directory
    install_packages(requirements_path, temp_directory)

    # Create a new ZIP file with Lambda files and installed packages
    create_zip_file_with_lambda_files_and_packages(output_path, input_path, temp_directory)

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_directory)

def main():
    parser = argparse.ArgumentParser(description="Create a Lambda deployment package.")
    parser.add_argument("input_path", type=str, help="Path to the Lambda function directory")
    parser.add_argument("requirements_file", type=str, help="Path to the requirements.txt file")
    parser.add_argument("output_path", type=str, help="Path to the output ZIP file")
    
    args = parser.parse_args()
    
    create_lambda_zip(Path(args.input_path), Path(args.requirements_file), Path(args.output_path))

if __name__ == "__main__":
    main()
