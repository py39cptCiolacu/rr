import os
import re
import shutil
import subprocess
from build_scripts.build_constants import RPYTHON_BIN_PATH, C_FUNCTION_FILE_MODIFIED, C_FUNCTION_FILE_ORIGINAL, TARGET_FILE_NAME, TARGET_PYTHON_FUNCTION_NAME, IMPORTS

def run_pypy():
    print("RUNNING RPYTHON BUILD....")
    result = subprocess.run([RPYTHON_BIN_PATH, TARGET_FILE_NAME], capture_output=True, encoding="utf-8")

    output = result.stdout + result.stderr

    match = re.search(r"written:\s*(.*)", output)
    if match:
        file_path = match.group(1).strip()
        folder_path = os.path.dirname(file_path)
        return folder_path
    
    raise FileNotFoundError("path where the build was made was not found")

def find_and_modify_function(c_transcript_dir):
    target_file = os.path.join(c_transcript_dir, C_FUNCTION_FILE_ORIGINAL)
    if not os.path.exists(target_file):
        raise FileNotFoundError(f"{TARGET_FILE_NAME} not found in: {c_transcript_dir}")
    if not os.path.exists(C_FUNCTION_FILE_MODIFIED):
        raise FileNotFoundError(f"source file {C_FUNCTION_FILE_MODIFIED} not found")

    with open(target_file, "r", encoding="utf-8") as f:
        target_code = f.read()

    with open(C_FUNCTION_FILE_MODIFIED, "r", encoding="utf-8") as f:
        modified_code = f.read()

    sig_match_src = re.search(fr"(pypy_g_{TARGET_PYTHON_FUNCTION_NAME}\s*\(([^)]*)\))", target_code)
    if not sig_match_src:
        raise ValueError(fr"mentioned function - pypy_g_{TARGET_PYTHON_FUNCTION_NAME} not found in source code")

    param_src = sig_match_src.group(2).strip()

    start_brace_src = modified_code.find("{")
    if start_brace_src == -1:
        raise ValueError("modified code - function structure is broken")
    brace_count = 0
    i = start_brace_src
    while i < len(modified_code):
        if modified_code[i] == "{":
            brace_count += 1
        elif modified_code[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end_brace_src = i
                break
        i += 1
    else:
        raise ValueError("modified code - function structure is broken")
    

    source_body = modified_code[start_brace_src+1:end_brace_src].strip()

    sig_match_tgt = re.search(fr"(pypy_g_{TARGET_PYTHON_FUNCTION_NAME}\s*\(([^)]*)\))", target_code)
    if not sig_match_tgt:
        raise ValueError("modified function structure is broken")

    signature_tgt = sig_match_tgt.group(1)
    param_tgt = sig_match_tgt.group(2).strip()
    param_tgt_name = param_tgt.split()[-1].replace("*","").strip()

    param_src_name = param_src.split()[-1].replace("*","").strip()
    new_body = source_body.replace(param_src_name, param_tgt_name)

    new_function = f"{signature_tgt} {{\n{new_body}\n}}"

    start_brace_tgt = target_code.find("{", sig_match_tgt.end())
    brace_count = 0
    i = start_brace_tgt
    while i < len(target_code):
        if target_code[i] == "{":
            brace_count += 1
        elif target_code[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                end_brace_tgt = i
                break
        i += 1
    else:
        raise ValueError("modified function structure is broken")

    patched_code = target_code[:sig_match_tgt.start()] + new_function + target_code[end_brace_tgt+1:]

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(patched_code)

    return target_file

def add_imports(c_transcript_dir):
    target_file = os.path.join(c_transcript_dir, C_FUNCTION_FILE_ORIGINAL)
    if not os.path.exists(target_file):
        raise FileNotFoundError(f"{C_FUNCTION_FILE_ORIGINAL} not found in: {c_transcript_dir}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    imports_text = "\n".join(IMPORTS) + "\n"

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(imports_text + content)

    return target_file

def make(c_transcipt_dir):
    if not os.path.isdir(c_transcipt_dir):
        raise NotADirectoryError(f"invalid folder: {c_transcipt_dir}")

    commands = [
        ["make", "clean"],
        ["make"]
    ]

    for cmd in commands:
        print(f"\nRunning: {' '.join(cmd)} in {c_transcipt_dir}")
        process = subprocess.Popen(
            cmd,
            cwd=c_transcipt_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # afișare output live
        for line in process.stdout:
            print(line, end="")
        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"command {' '.join(cmd)} failed with code {process.returncode}")

def copy_executable(source_folder):
    source_file = os.path.join(source_folder, "rr-source")
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"rr-source not found in : {source_folder}")

    dest_file = os.path.join(os.getcwd(), "rr-source-py")

    shutil.copy2(source_file, dest_file)
    os.chmod(dest_file, 0o755)

    print(f"executable copied to: {dest_file}")
    return dest_file

if __name__ == "__main__":
    # c_transcript_dir = run_pypy()
    c_transcript_dir = "/tmp/usession-main-5/testing_1"
    find_and_modify_function(c_transcript_dir)

    add_imports(c_transcript_dir)
    make(c_transcript_dir)
    copy_executable(c_transcript_dir)
    print("DONE!")