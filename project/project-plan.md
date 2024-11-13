# Project Plan

## Title
<!-- Give your project a short title. -->
US crime and Unemployment Correlation

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How does unemployment correlate with various types of crime across age groups in the U.S. in recent years?

## Description

Crime rates in the U.S. are a frequent topic of debate, and so are the issues on employment dynamics. 
This analysis wants to find the relationship between unemployment and crime across different age groups, 
shedding light on whether economic pressures and joblessness may drive individuals toward criminal activities. 
By examining this intersection, the study aims to reveal patterns that could help us understand how economic stability affects crime rates, 
potentially offering insights to guide more effective social and economic policies in the U.S.


## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: 2023 Offenders data
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
* Data URL: 
* Data Type: xlsx

The FBI's Crime Data Explorer (CDE) aims to provide transparency, create easier access, and expand awareness of criminal, 
and noncriminal, law enforcement data sharing; improve accountability for law enforcement; and provide a foundation to help 
shape public policy in support of a safer nation. These data are the **annual** offenders sex by offense category.

### Datasource2: 2022 Offenders data
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
* Data URL: 
* Data Type: xlsx

### Datasource3: 2021 Offenders data
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
* Data URL: 
* Data Type: xlsx

### Datasource4: 2020 Offenders data
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
* Data URL: 
* Data Type: xlsx

### Datasource5: 2023 Employment status data
* Metadata URL: https://www.bls.gov/cps/tables.htm
* Data URL: https://www.bls.gov/cps/cpsaat03.xlsx
* Data Type: xlsx

The Current Population Survey (CPS) provides a wealth of information on the nation’s labor force including data on the employed, 
unemployed, and those not in the labor force. These data are the **annual** employment status of the civilian noninstitutional population 
by age, sex, and race.  

### Datasource6: 2022 Employment status data
* Metadata URL: https://www.bls.gov/cps/tables.htm
* Data URL: https://www.bls.gov/cps/aa2022/cpsaat03.xlsx
* Data Type: xlsx  

### Datasource7: 2021 Employment status data
* Metadata URL: https://www.bls.gov/cps/tables.htm
* Data URL: https://www.bls.gov/cps/aa2021/cpsaat03.xlsx
* Data Type: xlsx  

### Datasource8: 2020 Employment status data
* Metadata URL: https://www.bls.gov/cps/tables.htm
* Data URL: https://www.bls.gov/cps/aa2020/cpsaat03.xlsx
* Data Type: xlsx  

### Data License: 
All these webpages has the 'An official website of the United States government' mark and The United States government has established several 
laws and policies to promote the accessibility and use of its datasets. Key among these is the Open, Public, Electronic, and 
Necessary (OPEN) Government Data Act, enacted on January 14, 2019, as part of the Foundations for Evidence-Based Policymaking Act. 
This legislation mandates that federal agencies publish their information online as open data, utilizing standardized, machine-readable formats.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Find suitable datasets with suitable features regarding the question
2. Creat data pipeline and select the needed features(data cleaning) and combine them into a table  
3. Work on the data to check for anomalies and visualize them to find the correlation
4. Write the final report to answer the question based on the visualizations and works done on the data