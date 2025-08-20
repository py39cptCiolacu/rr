import sys

# from rpython.jit.codewriter.policy import JitPolicy
from rr.main import main

def target(driver, args):
    driver.exe_name = "rr-source"
    return main, None

# def jitpolicy(driver):
#     return JitPolicy()

if __name__ == "__main__":
    main(sys.argv)


