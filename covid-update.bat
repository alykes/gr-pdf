@CALL c:\Users\n3w\anaconda3\condabin\conda.bat activate pdf

e:
cd e:\repos\gr-pdf

del gr-covid.db

python main.py
python reader.py
python plot.py

copy stats.html .\src\index.html /Y
git add .\src\index.html
git commit -m "updating stats"
git push origin main

