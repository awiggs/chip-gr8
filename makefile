INCLUDE=-Iincludes
CC=gcc
FLAGS=-Wall -Werror -pedantic

TARG_DEBUG=target/debug
TARG_RELEASE=target/release
TARG_TESTS=$(TARG_DEBUG)

LINK_FOLDER=-L$(TARG_DEBUG)
LINK_LIBRARIES=-lchip-gr8

NAME=libchip-gr8

DLL=$(NAME).so
DLL_OUT=$(TARG_DEBUG)/$(DLL)

OBJ_OUT=$(TARG_DEBUG)/$(NAME).o

TESTS_SRC=tests/test.c
TESTS_EXE=test.exe
TESTS_OUT=$(TARG_TESTS)/$(TESTS_EXE)

all: dll #build_tests 

clean:
	rm $(TARG_DEBUG)/$(wildcard *)
	#rm $(OBJ_OUT) $(DLL_OUT) $(TESTS_OUT)

test:
	./target/debug/test.exe

build_tests: $(TESTS_OUT)

dll: $(DLL_OUT)

$(DLL_OUT): $(OBJ_OUT) #$(TESTS_OUT)
	$(CC) -shared -o $(DLL_OUT) $(OBJ_OUT)

$(OBJ_OUT): src/chip-gr8.c includes/chip8.h
	$(CC) -c $(FLAGS) $(INCLUDE) -o $(OBJ_OUT) -fpic src/chip-gr8.c

$(TESTS_OUT): $(TESTS_SRC)
	$(CC) -o $(TESTS_OUT) $(FLAGS) $(LINK_FOLDER) $(LINK_LIBRARIES) $(INCLUDE) -fpic $(TESTS_SRC)
