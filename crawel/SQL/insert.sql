insert into fund.fund(person,company,money,project_id,project_type,department,approval_year,subject,subject_classification,subject_code,execution_time) 
(select person,company,money,project_id,project_type,department,approval_year,subject,subject_classification,subject_code,execution_time from fund.fund1);
