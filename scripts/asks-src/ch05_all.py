import runpy, glob, os
A = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch05_[a-z].py"))):
    A += runpy.run_path(f)["A"]
