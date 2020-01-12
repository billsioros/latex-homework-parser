# LaTeX Homework Parser

## Set Up

    python -m venv env
    pip install -r requirements.txt

## Example Usage

    python generate.py -l example/homework.pdf -s example/solution.tex

## Available Options

    usage: generate.py [-h] [-l LOAD] -s SAVE [-f]

    LaTeX Project Base Generation

    optional arguments:
    -h, --help            show this help message and exit
    -l LOAD, --load LOAD  specify the input file
    -s SAVE, --save SAVE  specify the output file
    -f, --force           do not prompt before overwriting
