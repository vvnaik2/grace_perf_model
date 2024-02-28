include ../make.rules

SRCS = $(wildcard *.c)

BINS_ARM = $(SRCS:.c=.ARM)
BINS_X86 = $(SRCS:.c=.X86)

ARM : $(BINS_ARM)

X86 : $(BINS_X86)