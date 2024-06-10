import os
import inspect


def extract_docstrings():
    res = []

    for root, dirs, files in os.walk('./plugins'):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()
                    docstring = inspect.cleandoc(source_code.split('"""')[1] if '"""' in source_code else "")
                    if docstring:
                        res.append(docstring)

    return res
