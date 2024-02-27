import pyprojroot

root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

import sys
sys.path.append(str(root))

from src.Index import InverseIndex

Index = InverseIndex(directory_path=root/'webpages/WEBPAGES_RAW')
Index.build_index()

if __name__ == '__main__':
    # Add your code here to run when the script is executed directly
    pass
