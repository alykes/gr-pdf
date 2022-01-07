@CALL e:\miniconda3\condabin\conda.bat activate pdf

e:
cd e:\repos\gr-pdf

del gr-covid.db

e:\miniconda3\python.exe main.py
e:\miniconda3\python.exe reader.py
e:\miniconda3\python.exe plot.py

copy stats.html .\src\index.html /Y
git add .\src\index.html
git commit -m "updating stats"
git push origin main

