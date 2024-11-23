# Project Plan

## Title
<!-- Give your project a short title. -->
US crime and Unemployment Correlation

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How does unemployment correlate with educational attainment levels across different age groups in the U.S.?

## Description

Unemployment and educational attainment are pivotal factors in shaping economic and social dynamics in the U.S. 
This analysis explores the relationship between unemployment rates and educational attainment levels across various age groups, 
aiming to uncover how education influences job security and economic stability at different life stages. By examining these correlations, 
the study seeks to highlight patterns that reveal how education impacts employment stability across life stages, potentially offering insights to shape policies 
that promote both economic security and equitable educational access.


## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: 2023 to 2020 Offenders data
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads
* Data 2022: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2022/cps-detailed-tables/table-1-1.xlsx
* Data 2021: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2021/cps-detailed-tables/table-1-1.xlsx
* Data 2020: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2020/cps-detailed-tables/table-1-1.xlsx
* Data 2019: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2019/cps-detailed-tables/table-1-1.xlsx
* Data 2018: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2018/cps-detailed-tables/table-1-1.xlsx
* Data 2017: https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/2017/cps-detailed-tables/table-1-1.xlsx
* Data Type: xlsx

Educational Attainment of the Population 18 Years and Over, by Age, Sex, Race, and Hispanic Origin, provided by the U.S. Census Bureau, contains **annual** detailed statistics 
on educational attainment in the United States for 2022. It includes breakdowns by age, gender, race, and ethnicity, offering comprehensive insights 
into the distribution of education levels across the population.

### Datasource2: 2023 to 202 Employment status data
* Metadata URL: https://nces.ed.gov/
* Data: https://nces.ed.gov/programs/digest/d23/tables/xls/tabn501.80.xlsx
* Data Type: xlsx

The Unemployment rates of persons 16 to 64 years old, by age group and highest level of educational attainment: Selected years, 1975 through 2023 dataset, 
published by the National Center for Education Statistics (NCES), provides detailed information on unemployment rates by educational attainment level for 
various demographic groups in the United States. 

### Data License: 
* Datasource1 permission source: https://www.census.gov/about/policies/citation.html
* Datasource1 permission description: Data users who create their own estimates using data from disseminated tables and other data should cite the Census Bureau 
as the source of the original data only. Conclusions drawn from any analysis of these data are the sole responsibility of the performing party.  
  
  
  
* Datasource2 permission source: https://nces.ed.gov/help/?
* Datasource2 permission description: Permission to Replicate Information
Unless stated otherwise, all information on the U.S. Department of Education's NCES website at http://nces.ed.gov is in the public domain and may be reproduced,
published, linked to, or otherwise used without NCES' permission. This statement does not pertain to information at websites other than http://nces.ed.gov, 
whether funded by or linked to from NCES.

The following citation should be used when referencing all NCES products: U.S. Department of Education. Institute of Education Sciences, National Center for Education Statistics.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Find suitable datasets with suitable features regarding the question
2. How to pull datasets from the links and not locally? learn to mimic browser download
3. Creat data pipeline and select the needed features(data cleaning) and combine them into a table 
4. Work on the data to check for anomalies and visualize them to find the correlation
5. Write the final report to answer the question based on the visualizations and works done on the data