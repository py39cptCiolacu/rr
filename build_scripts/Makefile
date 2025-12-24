# automatically generated makefile with Python embedding
RPYDIR = "/home/pypy/rpython"
PYTHON_INCLUDE = /usr/include/python3.12
PYTHON_LIBDIR = /usr/lib/x86_64-linux-gnu
PYTHON_LIB = -lpython3.12 -lpthread -ldl -lm

TARGET = rr-source
DEFAULT_TARGET = rr-source

SOURCES = testing_1.c \
          data_rpython_flowspace.c \
          data_rpython_memory_gc.c \
          data_rpython_memory_gctransform.c \
          data_rpython_rlib.c \
          data_rpython_rlib_parsing.c \
          data_rpython_rtyper.c \
          data_rpython_rtyper_lltypesystem.c \
          data_rr_backend.c \
          data_rr_compiler.c \
          data_rr_frontend.c \
          data_rr_main.c \
          data_rr_utils.c \
          nonfuncnodes.c \
          data_rpython_memory_gc_1.c \
          data_rpython_rlib_1.c \
          data_rpython_rtyper_lltypesystem_1.c \
          implement.c \
          rpython_flowspace.c \
          rpython_memory.c \
          rpython_memory_gc.c \
          rpython_memory_gctransform.c \
          rpython_rlib.c \
          rpython_rlib_parsing.c \
          rpython_rtyper.c \
          rpython_rtyper_lltypesystem.c \
          rpython_translator.c \
          rpython_translator_c.c \
          rr_backend.c \
          rr_compiler.c \
          rr_frontend.c \
          rr_main.c \
          rr_utils.c \
          thread.c \
          entrypoint.c \
          mem.c \
          exception.c \
          rtyper.c \
          support.c \
          profiling.c \
          debug_print.c \
          debug_traceback.c \
          asm.c \
          instrument.c \
          int.c \
          stack.c \
          threadlocal.c \
          ../module_cache/module_0.c \
          ../module_cache/module_1.c

OBJECTS = $(SOURCES:.c=.o)

LIBS = -lutil -lm -lrt $(PYTHON_LIB)
LIBDIRS = -L$(PYTHON_LIBDIR)
INCLUDEDIRS = -I$(RPYDIR)/translator/c -I$(PYTHON_INCLUDE)

CFLAGS = -O3 \
         -pthread \
         -fomit-frame-pointer \
         -Wall \
         -Wno-unused \
         -Wno-address \
         -Wno-discarded-qualifiers \
         -Wno-duplicate-decl-specifier

CFLAGSEXTRA = -DPYPY_MAKEFILE

LDFLAGS = -pthread -Wl,--export-dynamic
LDFLAGS_LINK = -pthread
LDFLAGSEXTRA =

CC = gcc
CC_LINK = $(CC)
LINKFILES =

RPATH_FLAGS = -Wl,-rpath='$$ORIGIN/'

PRECOMPILEDHEADERS = singleheader.h.gch

all: $(DEFAULT_TARGET)

$(TARGET): $(OBJECTS)
	$(CC_LINK) $(LDFLAGSEXTRA) -o $@ $(OBJECTS) $(LIBDIRS) $(LIBS) $(LINKFILES) $(LDFLAGS)
	$(MAKE) postcompile BIN=$(TARGET)

%.o: %.c singleheader.h.gch
	$(CC) $(CFLAGS) $(CFLAGSEXTRA) -o $@ -c $< $(INCLUDEDIRS)

%.o: %.s
	$(CC) $(CFLAGS) $(CFLAGSEXTRA) -o $@ -c $< $(INCLUDEDIRS)

%.o: %.cxx
	$(CXX) $(CFLAGS) $(CFLAGSEXTRA) -o $@ -c $< $(INCLUDEDIRS)

singleheader.h.gch: singleheader.h
	$(CC) $(CFLAGS) $(CFLAGSEXTRA) -o $@ -c $< $(INCLUDEDIRS)

postcompile:
	true

debug:
	$(MAKE) CFLAGS="$(DEBUGFLAGS) -DRPY_ASSERT" debug_target

debug_exc:
	$(MAKE) CFLAGS="$(DEBUGFLAGS) -DRPY_ASSERT -DDO_LOG_EXC" debug_target

debug_mem:
	$(MAKE) CFLAGS="$(DEBUGFLAGS) -DRPY_ASSERT -DPYPY_USE_TRIVIAL_MALLOC" debug_target

llsafer:
	$(MAKE) CFLAGS="-O2 -DRPY_LL_ASSERT" $(DEFAULT_TARGET)

lldebug:
	$(MAKE) CFLAGS="$(DEBUGFLAGS) -DRPY_ASSERT -DRPY_LL_ASSERT" debug_target

profile:
	$(MAKE) CFLAGS="-g -O1 -pg $(CFLAGS) -fno-omit-frame-pointer" LDFLAGS="-pg $(LDFLAGS)" $(DEFAULT_TARGET)

lldebug0:
	$(MAKE) CFLAGS="$(DEBUGFLAGS) -O0 -DMAX_STACK_SIZE=8192000 -DRPY_ASSERT -DRPY_LL_ASSERT" debug_target

clean:
	rm -f $(OBJECTS) $(DEFAULT_TARGET) $(TARGET) $(ASMFILES) $(PRECOMPILEDHEADERS) *.gc?? ../module_cache/*.gc??

clean_noprof:
	rm -f $(OBJECTS) $(DEFAULT_TARGET) $(TARGET) $(ASMFILES)

DEBUGFLAGS = -O1 -g

debug_target: $(DEFAULT_TARGET)
	#
