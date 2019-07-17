# Concept-finder
Course project for Mining Massive Datasets course at UCU.

## Preliminary steps (Ubuntu 18.04, 16.04)

### Install software

* Java 8 (at the time of writing, newer versions are not supported by Hadoop and Spark)
* Hadoop 3.1.2 (check that installation contains libhdfs files in lib/native sub-folder)
* Spark 2.4.3 (choose Pre-built with user-provided Apache Hadoop)
* Python 3 (tested with 3.6.8)

Java 8: `sudo apt install openjdk-8-jdk`

Hadoop: https://hadoop.apache.org/releases.html

Spark: https://spark.apache.org/downloads.html

Python: https://www.python.org/downloads/

### Configure software

* Java: `sudo update-alternatives --config java` (set priority, if you have multiple installations)
* Hadoop: http://cloudyrathor.com/hadoop-installation-configuration/
* ~/.bashrc: append contents of `append_to_bashrc.txt` (contains environmental variables for Java, Hadoop and Spark) 

Also, as stated here: http://spark.apache.org/docs/latest/hadoop-provided.html and extended here: http://apache-spark-user-list.1001560.n3.nabble.com/Running-Spark-on-user-provided-Hadoop-installation-td24076.html, append to the conf/spark-env.sh (located in Spark installation folder):
```bash
SPARK_DIST_CLASSPATH=$(hadoop classpath)
export SPARK_DIST_CLASSPATH="$SPARK_DIST_CLASSPATH:/usr/local/hadoop/share/hadoop/tools/lib/*" 
```

### Install python libraries

// TODO: revise requirements.txt

```
pip install -r requirements.txt
```

### Download data 

Project uses data from Semantic Scholar Open Research Corpus: https://api.semanticscholar.org/corpus/

Download by running from project folder (creates data/ subfolder and stores there):
```
sh get_data.sh
```
Or by following instructions on the website. In later case, make sure to remove sample file **sample-S2-records.gz** in order to avoid data duplication.

### Download pre-trained fastText model

// TODO: add download script (?)

## References

Waleed Ammar et al. 2018. Construction of the Literature Graph in Semantic Scholar. NAACL. https://www.semanticscholar.org/paper/09e3cf5704bcb16e6657f6ceed70e93373a54618

```
{"@inproceedings{ammar:18,"}
          {"title={Construction of the Literature Graph in Semantic Scholar},"}
          {"author={Waleed Ammar and Dirk Groeneveld and Chandra Bhagavatula and Iz Beltagy and Miles Crawford and Doug Downey"}
          {" and Jason Dunkelberger and Ahmed Elgohary and Sergey Feldman and Vu Ha and Rodney Kinney"}
          {" and Sebastian Kohlmeier and Kyle Lo and Tyler Murray and Hsu-Han Ooi and Matthew Peters and Joanna Power"}
          {" and Sam Skjonsberg and Lucy Lu Wang and Chris Wilhelm and Zheng Yuan and Madeleine van Zuylen and Oren Etzioni},"}
          {"booktitle={NAACL},"}
          {"year={2018},"}
          {"url={https://www.semanticscholar.org/paper/09e3cf5704bcb16e6657f6ceed70e93373a54618}"}
```

T. Mikolov, E. Grave, P. Bojanowski, C. Puhrsch, A. Joulin. Advances in Pre-Training Distributed Word Representations. https://arxiv.org/abs/1712.09405
```
@inproceedings{mikolov2018advances,
  title={Advances in Pre-Training Distributed Word Representations},
  author={Mikolov, Tomas and Grave, Edouard and Bojanowski, Piotr and Puhrsch, Christian and Joulin, Armand},
  booktitle={Proceedings of the International Conference on Language Resources and Evaluation (LREC 2018)},
  year={2018}
}
```
