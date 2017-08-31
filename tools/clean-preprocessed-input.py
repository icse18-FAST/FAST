'''
This file is part of an ICSE'18 submission that is currently under review. 
For more information visit: https://github.com/icse18-FAST/FAST.
    
This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
'''

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
