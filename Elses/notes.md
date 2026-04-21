command to convert ipynb to py file -- 'jupyter nbconvert --to script main.ipynb'

### Other methods to convert pdf to text --
Using marker-pdf --> converts pdf to markdown
> pip install marker-pdf 
> marker file.pdf

### Ways to import required packages
1. using freeze -> gives all packages installed in the environment
> pip freeze > requirements.txt
2. using pipreqs -> gives only packages used in the project
> pipreqs . --encoding utf-8 --ignore venv
3. using pigar (best) -> gives only packages used in the project and ignores the ones installed in the environment
> pigar generate



