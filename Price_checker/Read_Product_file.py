from time import sleep,time
import os


def read_file_by_line(filename):
    with open(filename, "r") as f:
        
        for line in f:
            return line



if __name__ == "__main__":
    read_file_by_line("Carts-laptop.txt")
