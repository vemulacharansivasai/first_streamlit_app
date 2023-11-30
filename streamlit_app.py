select current_region();
select current_account();

create database UTIL_DB;

use role accountadmin;
create or replace api integration dora_api_integration api_provider = aws_api_gateway api_aws_role_arn = 'arn:aws:iam::321463406630:role/snowflakeLearnerAssumedRole' enabled = true api_allowed_prefixes = ('https://awy6hshxy4.execute-api.us-west-2.amazonaws.com/dev/edu_dora');

SHOW INTEGRATIONS;


use role accountadmin;

create or replace external function util_db.public.grader(        
 step varchar     
 , passed boolean     
 , actual integer     
 , expected integer    
 , description varchar) 
 returns variant 
 api_integration = dora_api_integration 
 context_headers = (current_timestamp,current_account, current_statement) 
 as 'https://awy6hshxy4.execute-api.us-west-2.amazonaws.com/dev/edu_dora/grader'  
;

select grader(step, (actual = expected), actual, expected, description) as graded_results from 
  ( SELECT 
  'DORA_IS_WORKING' as step
 ,(select 223) as actual
 , 223 as expected
 ,'Dora is working!' as description
);

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
  SELECT 'DABW01' as step
 ,( select count(*) 
   from PC_RIVERY_DB.INFORMATION_SCHEMA.SCHEMATA 
   where schema_name ='PUBLIC') as actual
 , 1 as expected
 ,'Rivery is set up' as description
);

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
 SELECT 'DABW02' as step
 ,( select count(*) 
   from PC_RIVERY_DB.INFORMATION_SCHEMA.TABLES 
   where ((table_name ilike '%FORM%') 
   and (table_name ilike '%RESULT%'))) as actual
 , 1 as expected
 ,'Rivery form results table is set up' as description
);

select * from pc_rivery_db.public.fruityvice;

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
SELECT 'DABW03' as step
 ,( select sum(round(nutritions_sugar)) 
   from PC_RIVERY_DB.PUBLIC.FRUITYVICE) as actual
 , 35 as expected
 ,'Fruityvice table is perfectly loaded' as description
);


set mystery_bag='This bag is empty!!?';

select $mystery_bag;

set var1=2;
set var2=5;
set var3=7;

select $var1+$var2+$var3;


create function sum_mystery_bag_vars(var1 number, var2 number,var3 number)
 returns number as 'var1+var2+var3';


 select sum_mystery_bag_vars(12,36,204);


 set eeny=4;
 set meeny=67.2;
 set miney_mo=-39;

 select sum_mystery_bag_vars($eeny,$meeny,$miney_mo);


 set this = -10.5;
set that = 2;
set the_other =  1000;


select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
  SELECT 'DABW04' as step
 ,( select util_db.public.sum_mystery_bag_vars($this,$that,$the_other)) as actual
 , 991.5 as expected
 ,'Mystery Bag Function Output' as description
);


create or replace function  neutralize_whining ( hi text ) 
returns text as 'select initcap(hi)';


set neutralize_whining = 'bUt mOm i wAsHeD tHe dIsHes yEsTeRdAy'; select initcap($neutralize_whining);

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
 SELECT 'DABW05' as step
 ,( select hash(neutralize_whining('bUt mOm i wAsHeD tHe dIsHes yEsTeRdAy'))) as actual
 , -4759027801154767056 as expected
 ,'WHINGE UDF Works' as description
);

show stages in account;

list @my_internal_named_stage;

select $1 from @my_internal_named_stage/my_file.txt.gz;

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
  SELECT 'DABW06' as step
 ,( select count(distinct METADATA$FILENAME) 
   from @util_db.public.my_internal_named_stage) as actual
 , 3 as expected
 ,'I PUT 3 files!' as description
);


use role pc_rivery_role;
use warehouse pc_rivery_wh;

create or replace TABLE PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST (
	FRUIT_NAME VARCHAR(25)
);

insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
values ('banana')
, ('cherry')
, ('strawberry')
, ('pineapple')
, ('apple')
, ('mango')
, ('coconut')
, ('plum')
, ('avocado')
, ('starfruit');

insert into fruit_load_list values('test');

select * from fruit_load_list;


delete from fruit_load_list
where fruit_name like 'test'
or fruit_name like 'from streamlit';

select GRADER(step, (actual = expected), actual, expected, description) as graded_results from (
   SELECT 'DABW07' as step 
   ,( select count(*) 
     from pc_rivery_db.public.fruit_load_list 
     where fruit_name in ('jackfruit','papaya', 'kiwi', 'test', 'from streamlit', 'guava')) as actual 
   , 4 as expected 
   ,'Followed challenge lab directions' as description
);












import streamlit
import pandas
import requests

streamlit.title(' My Moms New Healthy Diner')

streamlit.header(' Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry oatmeal')
streamlit.text(' 🥗Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))


streamlit.dataframe(my_fruit_list)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit to get information.")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()



import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_rows)






my_cur.execute("insert into fruit_load_list values('from streamlit')")
