CC := gcc
CFLAGS := -wall -g
BIN_DIR := build
EXEC := $(BIN_DIR)/library
SCR := main.c

$(EXEC): $(BIN_DIR) $(SCR)
	$(CC) $(CFLAGS) -o $(EXEC) $(SCR)
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)
	
clean:
	rm -rf $(BIN_DIR)

all: $(EXEC)