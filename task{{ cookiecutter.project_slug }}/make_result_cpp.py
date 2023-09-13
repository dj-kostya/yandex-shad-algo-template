import os
import re
import subprocess
from pathlib import Path

SRC_PATH = Path("src")

MAIN_FILE = SRC_PATH / 'main.cpp'

TMP_FILE = SRC_PATH / 'tmp.cpp'
RESULT_FILE = SRC_PATH / 'result.cpp'
TASK_NAME = '{{ cookiecutter.task_name }}'

HEADERS_FILE = SRC_PATH / f'{TASK_NAME}.h'
CPP_FILE = SRC_PATH / f'{TASK_NAME}.cpp'

INCLUDE_RE = re.compile(r'#include ((<[^>]+>)|(\"[^\"]+\"))')


def build_result() -> str:
    result_content = ""
    with open(HEADERS_FILE, 'r') as headers:
        headers_content = headers.read()
        headers_content = headers_content.replace("#pragma once", "")
        result_content += headers_content
    result_content += "\n"
    with open(CPP_FILE, 'r') as cpp:
        cpp_content = cpp.read()
        cpp_content = cpp_content.replace(f"#include \"{TASK_NAME}.h\"", "")
        result_content += cpp_content
    result_content += "\n"
    with open(MAIN_FILE, 'r') as main_cpp:
        main_cpp_content = main_cpp.read()
        main_cpp_content = main_cpp_content.replace(f"#include \"{TASK_NAME}.h\"", "")
        result_content += main_cpp_content
    return result_content


def move_all_includes_to_top(result_content: str) -> str:
    includes = INCLUDE_RE.findall(result_content)
    all_includes = sorted([f"#include {include[0]}" for include in includes])
    for incl in all_includes:
        result_content = result_content.replace(incl, "")
    includes_content = "\n".join(all_includes)
    return f"{includes_content}\n{result_content}"


def write_content(result_content: str) -> None:
    with open(TMP_FILE, 'w') as result:
        result.write(result_content)


def apply_clang_format():
    with open(RESULT_FILE, 'w') as f:
        res = subprocess.run(["clang-format", str(TMP_FILE.absolute())], stdout=f)


def remove_tmp():
    os.remove(TMP_FILE)


if __name__ == "__main__":
    content = build_result()
    content = move_all_includes_to_top(content)
    write_content(content)
    apply_clang_format()
    remove_tmp()
