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

If you have multiple installations of Java, set priority with: `sudo update-alternatives --config java`

For Hadoop configuration check: http://cloudyrathor.com/hadoop-installation-configuration/

For .bashrc file, add contents of `append_to_bashrc.txt`. It contains environmental variables for Java, Hadoop and Spark. 

Also, as stated here: http://spark.apache.org/docs/latest/hadoop-provided.html and extended here: http://apache-spark-user-list.1001560.n3.nabble.com/Running-Spark-on-user-provided-Hadoop-installation-td24076.html, append to the conf/spark-env.sh (located in Spark installation folder):
```bash
SPARK_DIST_CLASSPATH=$(hadoop classpath)
export SPARK_DIST_CLASSPATH="$SPARK_DIST_CLASSPATH:/usr/local/hadoop/share/hadoop/tools/lib/*" 
```
