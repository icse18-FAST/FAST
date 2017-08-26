import os


if __name__ == "__main__":
    for root, folders, files in os.walk("input/"):
        for file in files:
            if file[0] == ".":
                pass
            elif (file == "fault_matrix_key_tc.pickle" or
                file == "fault_matrix.pickle"):
                pass
            elif ("-bbox.txt" in file or
                  "-function.txt" in file or
                  "-line.txt" in file or
                  "-branch.txt" in file):
                pass
            else:
                print "Deleting {}/{}".format(root, file)
                os.remove("{}/{}".format(root, file))
