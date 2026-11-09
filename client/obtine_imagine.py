from pydicom.data import get_testdata_file
import shutil

imagine_ascunsa = get_testdata_file("CT_small.dcm")
shutil.copy(imagine_ascunsa, "test.dcm")
print("Fișierul test.dcm a fost extras cu succes!")