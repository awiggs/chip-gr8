INCLUDE=-Iincludes
CC=gcc
FLAGS=-Wall -Werror -pedantic

TARG_DEBUG=target/debug
TARG_RELEASE=target/release
TARG_TESTS=$(TARG_DEBUG)

LINK_FOLDER=-L$(TARG_DEBUG)
LINK_LIBRARIES=-lchip-gr8

NAME=libchip-gr8

DLL=$(NAME)
DLL_OUT_NAME=$(TARG_DEBUG)/$(DLL)

DLL_OUT=$(DLL_OUT_NAME).so
DLL_DLL_OUT=$(DLL_OUT_NAME).dll

OBJ_OUT=$(TARG_DEBUG)/$(NAME).o

TESTS_SRC=tests/test_rom.c
TESTS_EXE=test.exe
TESTS_OUT=$(TARG_TESTS)/$(TESTS_EXE)

all: so dll build_tests 

clean:
	#echo $(TARG_DEBUG)/$(wildcard *)
	#rm $(OBJ_OUT) $(DLL_OUT) $(TESTS_OUT)

test:
	./target/debug/test.exe

build_tests: $(TESTS_OUT)

#dll: $(DLL_OUT)
#	cp $(DLL_OUT) $(DLL_DLL_OUT)
	
so: $(DLL_OUT)

dll:
	$(CC) -shared -o $(DLL_DLL_OUT) $(OBJ_OUT) target/debug/ops.o

$(DLL_OUT): $(OBJ_OUT) target/debug/ops.o
	$(CC) -shared -o $(DLL_OUT) $(OBJ_OUT) target/debug/ops.o

$(OBJ_OUT): src/chip8.c includes/chip8.h includes/instructions.h includes/ops.h src/ops.c
	$(CC) -c $(FLAGS) $(INCLUDE) -o $(OBJ_OUT) -fpic src/chip8.c

target/debug/ops.o: src/chip8.c includes/chip8.h includes/instructions.h includes/ops.h src/ops.c
	$(CC) -c $(FLAGS) $(INCLUDE) -o target/debug/ops.o -fpic src/ops.c

$(TESTS_OUT): $(TESTS_SRC) $(DLL_OUT)
	$(CC) -o $(TESTS_OUT) $(FLAGS) $(LINK_FOLDER) $(LINK_LIBRARIES) $(INCLUDE) -fpic $(TESTS_SRC)
