# Social Network Analysis
## Usage
You can create conda env from file for convenience: ``` conda env create -f conda_env.yml ```. 

## Structure
- `data/`: data files should be there as names provided from zip. Full data files are in .gitignore, only samples in git for quick testing stuff. May add more samples
- `src/`
    - `notebook/`: notebook stuff, presenting etc
    - `pyhton/`: add modules there

## ToDo:
- do Todos (R DONE)
- implement modularity maximization (R DONE)
- Strache bug fix + deep dive (V DONE)
- Community von einem Artikel -> Nodes davon nehmen -> Lookup auf Following Graph -> Similarity berechnen (O DONE)
- Metriken finden um zwei Communities zu vergleichen (O, G DONE)
- Plot similarity between timestamps and "final state" = last timestep (scale 0-1) (V DONE)
  - needs Similarity measure = #interactions (similar to line plot in semantic.ipynb) 
- Line Chart: plot relative interactions for each community over time (#interactions / #members), similar to lineplot in semantic.ipynb (G DONE kinda)
- Cyclic behavior -> do above plot each day and plot them on top of each other (R DONE)
  - add vertical lines for biggest articles (R DONE)
- Präsi (G)
- Report
  - theoretical background
    - community detection (mod maxim) (R)
    - anderer der langsamer war: Girvan-Newman (O)