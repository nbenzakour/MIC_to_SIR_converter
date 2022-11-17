README.md

Description
-----------

Convert MIC data to SIR (Sensitive, Intermediate, Resistant), given MIC conventions. 
This allows easier large scale comparisons of several samples for which several antiobitics 
are tested that have different breakpoint values.


Usage
-----

To run this tool, you need to provide the following minimum information: 
	* the file containing the screening data, in .csv format (see the example in the test folder)
	* the output directory
    
You can also specify:
    * the MIC breakpoint convention scheme, either CLSI or EUCAST (default = CLSI_entero_2018)
    * the position of the column you wish to use as identifier, e.g strain name (default = 3) 
	* the species of interest: Enterobacteriacae (default) or Saureus (default = Entero)
	* the output to include a full description with MIC + SIR conversion (default = True)


Running the test example
------------------------

```python bz_MIC_to_SIR_converter.py -i test/MIC_test_data.csv -o test_output```

STANDARD OUTPUT is as follows:

::

	Created output directory...
	Log info stored in: test_output/logfile.txt
	Loading scheme: CLSI
	Loading screening data: test/MIC_test_data.csv
	   poc id ampicillin ampicillin  ... chloramphenicol nitrofurantoin nitrofurantoin
	0  SYD001        >16          R  ...               S             64              I
	1  SYD002        >16          R  ...               S           <=32              S
	2  SYD003        >16          R  ...               S           <=32              S
	3  SYD004        >16          R  ...               S           <=32              S
	4  SYD005        >16          R  ...               S           <=32              S
	5  SYD006         >1          S  ...               S           <=32              S
	6  SYD007        >16          R  ...               S           <=32              S
	7  SYD008        >16          R  ...               R           >128              R
	8  SYD009        >16          R  ...               S           <=32              S
	9  SYD010        >16          R  ...               S           <=32              S

	[10 rows x 47 columns]
	Writing results to test_output/MIC-conversion-results_20221117-151809.csv
	
A log file is also generated, containing the list of antibiotic MICs converted and the breakpoints
used, according to the scheme supplied (CLSI in this example).

::

	Loading scheme: CLSI
	Loading screening data: test/MIC_test_data.csv
	-------
	ampicillin	 cut-offs are S <= 8.0 and R >= 32.0
	-------
	piperacillin	 not tested
	-------
	mecilinam	 not tested
	-------
	amoxicillin-clavulanate	 cut-offs are S <= [8.0, 4.0] and R >= [32.0, 16.0]
	-------
	ampicillin-sulbactam	 not tested
	-------
	ceftolozane-tazobactam	 not tested
	-------
	ceftdazidim-avibactam	 not tested
	-------
	piperacillin-tazobactam	 cut-offs are S <= [16.0, 2.0] and R >= [128.0, 4.0]
	-------
	ticarcillin-clavulanate	 cut-offs are S <= [16.0, 2.0] and R >= [128.0, 4.0]

	[truncated]



