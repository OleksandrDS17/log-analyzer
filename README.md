# log-analyzer
Python tool for parsing and analyzing log files, detecting errors and warnings using regex

# Log Analysis Tool (Python)

A lightweight Python-based utility for processing and analyzing log files.  
The tool helps to identify common error patterns, warnings and operational anomalies.

## Goals of the project
- reduce manual effort during troubleshooting  
- quickly detect critical events  
- structure unorganized log information  
- support administrators in daily operations  

## Features
- parsing of large log files  
- filtering by keywords, severity or patterns  
- identification of recurring errors  
- summary statistics generation  
- extraction of relevant entries  

## Technologies
- Python  
- Regular Expressions (re)  
- file system operations  
- structured data processing  

## Example use cases
- detecting failed login attempts  
- searching for network/service interruptions  
- extracting warnings from application logs  
- preparing data for incident analysis  

## Example execution
```bash
python log_analyzer.py /var/log/syslog
