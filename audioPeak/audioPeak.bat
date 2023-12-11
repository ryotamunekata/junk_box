@echo off
CALL conda activate py310
python audioPeak.py
CALL conda deactivate
