# LaTeX Homework Parser

## Set Up

    python -m venv env
    pip install -r requirements.txt

## Example

    python parse.py -l example/homework.pdf -s example/solution.tex

The script is expecting a  **PDF** file containing distinctly numbered sections, such as [this](example/homework.pdf).

The script can be run with no input file, in which case it will create
a non assignment-specific LaTeX template.

## Available Options

    usage: parse.py [-h] [-l LOAD] -s SAVE [-f]

    LaTeX Project Base Generation

    optional arguments:
    -h, --help            show this help message and exit
    -l LOAD, --load LOAD  specify the input file
    -s SAVE, --save SAVE  specify the output file
    -f, --force           do not prompt before overwriting

## Configuration

Configuration can be achieved through a JSON configuration file,
by the name of **.config.json**.

An example of such a file' s contents can be seen below.

```json
{
    "title": {
        "primary": "Lorem Ipsum",
        "secondary": "Consectetur adipiscing elit"
    },
    "authors": [
        "Nullam lacinia"
    ],
    "packages": [
        "alphabeta",
        "amsmath",
        "amsthm",
        "caption",
        "color",
        "fullpage",
        "graphicx",
        "latexsym",
        "listings",
        "pxfonts",
        "stackrel",
        "titlesec",
        "subfig",
        "tikz",
        "float",
        "hyperref"
    ],
    "commands": {
        "R": "\\mathbb{R}",
        "N": "\\mathbb{N}",
        "norm": "\\left\\lVert#1\\right\\rVert",
        "abs": "\\left\\lvert#1\\right\\rvert",
        "margin": "\\hspace{4pt}",
        "code": "\\lstinputlisting[caption={#2}]{#1}"
    },
    "environments": {
        "rcases": {
            "begin": "\\left.\\begin{aligned}",
            "end": "\\end{aligned}\\right\\rbrace"
        },
        "matlab": {
            "begin": "\\begin{figure}[hp]\\centering\\captionsetup{justification=centering}",
            "end": "\\end{figure}"
        }
    }
}
```
