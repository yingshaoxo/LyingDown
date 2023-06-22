python3 -m nuitka --include-data-dir="./lyingdown"="./" --plugin-enable=multiprocessing --follow-imports --standalone --onefile --remove-output --output-filename="program.run" lyingdown/main.py
