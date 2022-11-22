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


Columns are reordered as such:

* first (MIC and) SIR, ordered according to antibiotics classes
* then any other metadata (including antibiotics for which there were no conversion data available
in the scheme chosen, e.g colistin in CLSI)

A log file is also generated, containing the list of antibiotic MICs converted, the breakpoints
used, according to the scheme supplied (CLSI in this example), and any other metadata added.

Logfile:

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



