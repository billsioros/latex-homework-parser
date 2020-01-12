
# MIT License
#
# Copyright (c) 2019 Vasileios Sioros
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

import os

import time

import json

import argparse

from tika import parser

from pylatexenc.latexencode import UnicodeToLatexConversionRule, UnicodeToLatexEncoder, RULE_REGEX


encoder = UnicodeToLatexEncoder(conversion_rules=[
    UnicodeToLatexConversionRule(RULE_REGEX, [
    ]),
    'defaults'
])

config_path = os.path.join(os.getcwd(), ".config.json")

config_template = {
    "title": {
    },
    "authors": [
    ],
    "packages": [
    ],
    "commands": {
    },
    "environments": {
    }
}

tex_project_template = \
"""
\\documentclass[12pt]{{article}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[greek, english]{{babel}}

% Packages
{packages}

% Commands
{commands}

% Environments
{environments}

% Python Syntax Highlighting
\\definecolor{{string_color}}{{RGB}}{{0, 161, 13}}
\\definecolor{{comment_color}}{{RGB}}{{46, 46, 46}}
\\definecolor{{keyword_color}}{{RGB}}{{0, 112, 191}}
\\definecolor{{background_color}}{{RGB}}{{250, 250, 250}}

\\lstset{{
    framesep=15pt,
    xleftmargin=15pt,
    xrightmargin=15pt,
    language=Python,
    captionpos=b,
    numbers=right,
    numberstyle=\\small\\ttfamily,
    frame=lines,
    showspaces=false,
    showtabs=false,
    breaklines=true,
    showstringspaces=false,
    breakatwhitespace=true,
    commentstyle=\\color{{comment_color}}\\textit,
    keywordstyle=\\bfseries\\color{{keyword_color}}\\textbf,
    stringstyle=\\color{{string_color}}\\textit,
    morekeywords={{self, lambda, __init__, __del__, __name__, for, in, not, and, or, :}},
    basicstyle=\\small\\ttfamily,
    tabsize=4,
    keepspaces=true,
    columns=flexible,
    backgroundcolor=\\color{{background_color}}
}}

% Links
\\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
}}

% Lengths
\\setlength{{\\parindent}}{{0in}}
\\setlength{{\\oddsidemargin}}{{0in}}
\\setlength{{\\textwidth}}{{6.5in}}
\\setlength{{\\textheight}}{{10in}}
\\setlength{{\\topmargin}}{{-1.0in}}
\\setlength{{\\headheight}}{{18pt}}

\\titlespacing*{{\\subsection}}
{{0pt}}{{5.5ex plus 1ex minus .2ex}}{{4.3ex plus .2ex}}

\\title{{\\huge {primary_title}\\\\{secondary_title}}}
\\author{{{authors}}}
\\date{{{date}}}

\\begin{{document}}

\\maketitle

\\pagenumbering{{gobble}}

\\pagebreak

{subsections}

\\end{{document}}
"""


def parse_package(package):

    return f"\\usepackage{{{package}}}"


def parse_command(command, args_count_rgx=r"#[1-9][0-9]*"):

    signature, body = command

    args_count = len(re.findall(args_count_rgx, body, flags=re.UNICODE))

    args_str = f"[{args_count}]" if args_count > 0 else ""

    return f"\\newcommand{{\\{signature}}}{args_str}{{{body}}}"


def parse_environment(environment):

    signature, body = environment

    begin, end = body["begin"], body["end"]

    return f"\\newenvironment{{{signature}}}\n\t{{{begin}}}\n\t{{{end}}}"


def parse_section(section):

    section = section.strip()

    section = re.sub(r"\n\n+", "\n", section, flags=re.UNICODE)

    section = re.sub(r"[^\S\n]+", " ", section, flags=re.UNICODE)

    return f"\n\\subsection*{{{section}}}\n\n\\vspace{{2in}}\n\n\\pagebreak"


def parse_seed(seed, section_rgx=r"([1-9][0-9]*\.[^\S\n]*?.+?[\?\.]\n\n+)(?=([1-9][0-9]*\.[^\S\n]*?.+?[\?\.]\n\n+)|($)|(.*))"):

    sections = parser.from_file(seed)['content']

    sections = encoder.unicode_to_latex(sections)

    sections = sections.encode('utf8', 'strict').decode('ascii', 'ignore')

    sections = re.findall(section_rgx, sections, flags=re.UNICODE | re.DOTALL)

    sections = map(lambda section: section[0], sections)

    return map(parse_section, sections)


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description="LaTeX Homework Parser")

    argparser.add_argument("-l", "--load",  help="specify the input file")
    argparser.add_argument("-s", "--save",  help="specify the output file",          required=True)
    argparser.add_argument("-f", "--force", help="do not prompt before overwriting", action="store_true")

    args = argparser.parse_args()


    if os.path.exists(args.save) and not args.force:

        answer = input(f"Would you like to overwrite '{args.save}': ")

        if not re.fullmatch(r"y|Y|yes|YES|", answer):

            exit(1)

    else:

        path = os.path.dirname(args.save)

        if len(path) > 0 and not os.path.isdir(path):

            os.makedirs(path)


    if not os.path.exists(config_path):

        with open(config_path, "w", encoding="utf8") as config_file:

            json.dump(config_template, config_file, indent=4, sort_keys=True)

            config = config_template

    else:

        with open(config_path, "r", encoding="utf8") as config_file:

            config = json.load(config_file)


    with open(args.save, "w", encoding="utf8") as tex_file:

        tex_file.write(
            tex_project_template.format(
                packages="\n".join(map(parse_package, sorted(config["packages"]))),
                commands='\n'.join(map(parse_command, sorted(config["commands"].items()))),
                environments="\n\n".join(map(parse_environment, sorted(config["environments"].items()))),
                primary_title=config["title"].get("primary", ""),
                secondary_title=config["title"].get("secondary", ""),
                authors="\\\\".join(config["authors"]),
                date=time.strftime("%B %Y"),
                subsections='\n'.join(parse_seed(args.load)) if args.load else ""
            )
        )

