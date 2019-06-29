# Concept-finder
Course project for Mining Massive Datasets course at UCU.

### Run docker with pyspark and jupyter notebook
```
docker run -it -p 8888:8888 -v `pwd`:/home/jovyan/work jupyter/pyspark-notebook
```
 
### Install prerequisite packages
```
pip install -r requirements.txt
```

### Upload data
Make sure to check Semantic Scholars Open Research Corpus license.
```
sh get_gata.sh
```

### Change format
```
python convert_to_orc.py
```
