# -*- coding: utf-8 -*-
import sys
import io

# Force UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import and run the main function
# Note: sys.argv is already set, distribute_rules.main() will use it
from distribute_rules import main

if __name__ == "__main__":
    main()
