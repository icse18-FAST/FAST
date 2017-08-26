# FAST
"FAST Approaches to Scalable Similarity-based Test Case Prioritization" online material.

In this repository we provide the entirety of the material required to replicate the experiment, including: the implementation of the algorithms, the input data, and supplementary tools required to launch the experiment. In addition, the raw output experimental reaults are also provided.

The subjects
---------------
The subjects of the experimentation were taken from well known repositories for software testing ([SIR][sir] and [Defects4j][defects4j]) and consisted of C and Java software artifacts respectively: 

|   Subject            | Language         | SLOC           | Test cases | Faults | Fault type | 
|----------------------|------------------|----------------|------------|--------|------------|
| Flex                 | C                | 10296          |  670       | 9      | seeded     |
|  Grep                | C                | 10124          |  809       | 8      | seeded     |
| Gzip                 | C                | 4594           |  214       | 7      | seeded     |
| Sed                  | C                | 13413          |  370       | 6      | seeded     |
| Make                 | C                | 14330          |  875       | 19     | seeded     |
|  Closure compiler    | Java             | 90697          |  221       | 101    | real       |
| Apache commons-lang  | Java             | 21787          |  113       | 39     | real       |
| Apache commons-math  | Java             | 84323          |  385       | 7      | real       |
| Jfree Chart          | Java             | 96382          |  356       | 26     | real       |
|Joda-Time             | Java             | 27801          |  123       | 27     | real       |

The FAST family algorithms
---------------
We propose 5 different algorithms, varying according to the approach adopted to select test cases and the number of test cases taken in input:

 - FAST-pw: based on Jaccard Distance
 - FAST-1: selects progressively one test case
 - FAST-log: selects test cases based on logarithmic function
 - FAST-sqrt: selects test cases based on square root function
 - FAST-all: selects the entirety of the test cases
 
Experiment replication
---------------
In order to replicate the experiment follow these steps:

### Getting started

1. Clone the replication repository 
   - `git clone https://github.com/icse18-FAST/FAST/`
 
2. Make sure that all requirements are met:
   - `pip install -r requirements.txt`

### Run algorithms on specific subject

3. Execute the `prioritize.py` script 
   - `python py/prioritize.py <dataset> <entity> <algorithm> <repetitions>`
   
      Example: `python py/prioritize.py flex_v3 BB FAST-pw 50`
     
     To display all argument options simply run the script without arguments (i.e. `python py/prioritize.py`). NOTE:
      STR, I-TSD are BB prioritization only.
      ART-D, ART-F, GT, GA, GA-S are WB prioritization only.

4. View output results stored in folder `output/`

### Run algorithms to evaluate scalability 

3. Run the script  `generate-scalability-input.py` to generate the input for the algorithms
   - `python py/generate-scalability-input.py <tssize> <tcsize>`

   Example: `python py/generate-scalability-input.py 1000 small`

   To display all argument options simply run the script without arguments (i.e. `python py/generate-scalability-input.py`).

4. Run the script  `scalability.py` to run the algorithms
   - `python py/scalability.py <tssize> <tcsize> <algorithm>`
   
   Example: `python py/scalability.py 1000 small FAST-pw`
   
   To display all argument options simply run the script without arguments (i.e. `python py/scalability.py`).

5. Run the script  `scalability.py` to run the algorithms
   - `python py/scalability.py <tssize> <tcsize> <algorithm>`
   
   Example: `python py/scalability.py 1000 small FAST-pw`
   
   To display all argument options simply run the script without arguments (i.e. `python py/scalability.py`).
   
6. View output results stored in folder `output/`
 
### Plot scalability results of our experiment execution

 3. Run the script  `plot-scalability-results.py` to generate the input for the algorithms.
    
    - `python tools/plot-scalability-results.py <tcsize> <time> <algorithm> ... <algorithm>`

   Example: `python tools/plot-scalability-results.py small prioritization FAST-pw FAST-one FAST-log`
 
   To display all argument options simply run the script without arguments (i.e. `python py/scalability.py`).


Results
---------------
In the directory [results](https://github.com/icse18-FAST/FAST/tree/master/results) the main results of the experiment are reported.
More in detail:

- [SampleResults](https://github.com/icse18-FAST/FAST/blob/master/results/SampleResult.md) reports some random plots that of course have to be changed
- [KittenComparison](https://github.com/icse18-FAST/FAST/blob/master/results/kitten_comparison.md) we have a comparison of kitten

Directory Structure
---------------
This is the root directory of the repository. The directory is structured as follows:

    FAST
     |
     |--- input:         Input of the algorithms, consisting of fault matrices and coverage information of the subjects.
     |
     |--- output:        Raw output data of the experiment execution.
     |
     |--- prioritized:   Prioritized test suite generated from the algorithm execution.  
     |
     |--- py:            Implementation of the algorithms and scripts to execute the experiment      
     |
     |--- results:       Overview of the experiment results and related data
     |
     |--- tools:         Util script required to run the experiment
  

[defects4j]: https://github.com/rjust/defects4j/
[sir]: http://sir.unl.edu/portal/index.php
