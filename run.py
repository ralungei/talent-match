import os
import sys
from pathlib import Path

src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

os.system("streamlit run src/talent_match/main.py --server.runOnSave=true")