# FAST Approaches to Scalable Similarity-based Test Case Prioritization

This repository is a companion page for the following publication:

> Breno Miranda, Emilio Cruciani, Roberto Verdecchia, and Antonia Bertolino. 2018. FAST Approaches to Scalable Similarity-based Test Case Prioritization. In *Proceedings of ICSE’18: 40th International Conference on Software Engineering, Gothenburg, Sweden, May 27-June 3, 2018 (ICSE’18)*, 11 pages. DOI: [10.1145/3180155.3180210](http://dx.doi.org/10.1145/3180155.3180210)

It contains all the material required for replicating our experiments, including: the implementation of the algorithms, the input data, and supplementary tools. 
Some additional results, not included in the paper for the sake of space, are also provided.


Experiment Results and Data
---------------
The results of our experiments as well as the data we used for our statistical analysis are available [here](results/README.md).

 
Experiment Replication
---------------
In order to replicate the experiment follow these steps:

### Getting started

1. Clone the repository 
   - `git clone https://github.com/icse18-FAST/FAST/`
 
2. Install the additional python packages required:
   - `pip install -r requirements.txt`

### Evaluate the Effectiveness and Efficiency of different test case prioritization (TCP) algorithms

1. Execute the `prioritize.py` script 
   - `python py/prioritize.py <subject> <entity> <algorithm> <repetitions>`
   
      Example: `python py/prioritize.py flex_v3 bbox FAST-pw 50`
      
      The possible values for `<subject>` are: flex_v3, grep_v3, gzip_v1, make_v1, sed_v6, chart_v0, closure_v0, lang_v0, math_v0, and time_v0.
 
      The possible values for `<entity>` are: function, line, and branch, for white-box approaches; and bbox, for black-box TCP.
      
      The possible values for `<algorithm>` are: FAST-pw, FAST-one, FAST-log, FAST-sqrt, FAST-all, GT, GA, GA-S, ART-F, ART-D, STR, and I-TSD. Notice that while the FAST-* algorithms can be applied to both white-box and black-box TCP, GT, GA, GA-S, ART-F, and ART-D, are white-box only; STR and I-TSD are black-box only.

2. View output results stored in folder `output/`

### Evaluate the Scalability of different TCP approaches

1. Run the script  `generate-scalability-input.py` to generate the input testset for the algorithms
   - `python tools/generate-scalability-input.py <test_suite_size> <test_case_size>`

      The argument `<test_suite_size>` accepts any arbitrary integer, while `<test_case_size>` accepts three different sizes for a test case representation: *small*, *medium*, and *large*. *Small* for an average length of 100, *medium* for 1K, and *large* for 10K elements. In all three cases, we allow for a variance of ±25%.

      For example, the command: `python tools/generate-scalability-input.py 1000 small` generates a test suite containing 1000 *small* test cases.

      To display all argument options simply run the script without arguments (i.e. `python tools/generate-scalability-input.py`).

2. Run the script `scalability.py` to measure the time required by the TCP approach to prioritize the target testset
   - `python py/scalability.py <test_suite_size> <test_case_size> <algorithm>`
   
      For example, the command: `python py/scalability.py 1000 small FAST-pw` captures the time required by FAST-pw to prioritize a test suite containing 1000 small test cases. 
   
      To display all argument options simply run `python py/scalability.py`.
   
3. View output results stored in folder `scalability/output/`
 
### Plot the scalability results of our experiment execution

 1. Run the script `plot-scalability-results.py`:
    
    - `python tools/plot-scalability-results.py <test_case_size> <time> <algorithm> ... <algorithm>`

      `<time>` accepts two values, either *prioritization* or *total*, based on the way the prioritization time is measured.
   
      Example: `python tools/plot-scalability-results.py small prioritization FAST-pw FAST-one FAST-log`
 
      To display all argument options simply run `python py/scalability.py`.

### Clean preprocessed input files

 1. Run the script `clean-preprocessed-input.py` to clean preprocessed input files for repeating the experiment in a clean environment.
 
    - `python tools/clean-preprocessed-input.py`


Directory Structure
---------------
This is the root directory of the repository. The directory is structured as follows:

    FAST
     .
     |
     |--- input/         Input of the algorithms, i.e. fault matrix, coverage information, and BB representation of subjects.
     |
     |--- output/        Raw output data of the experiments execution.
     |
     |--- py/            Implementation of the algorithms and scripts to execute the experiments.
     |
     |--- results/       Overview of the experiment results and related data
     |
     |--- scalability/   Input, output, and plots for the scalability experiment.
     |
     |--- tools/         Util scripts, e.g. clean environment, plot results, generate scalability input.
  
