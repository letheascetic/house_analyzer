# total_on_sale | total_off_sale | total_sold
select status, count(1) from hl_house_basic_info where city = 'sx' and community = '润泽大院' group by status;

# new_on_sale 
select * from hl_house_basic_info where city = 'sx' and community = '润泽大院' 
and list_date between '2019-04-01' and  '2019-05-01' and status = 1;

# new_off_sale
select * from hl_house_basic_info where city = 'sx' and community = '润泽大院'
and update_time between '2019-04-01' and  '2019-05-01' and status = 2;

# new_sold
select * from hl_house_basic_info where city = 'sx' and community = '润泽大院'
and deal_date between '2019-04-01' and  '2019-05-01' and status = 4;

# total_on_sale_unit_price
select a.house_id, record_date, unit_price from hl_house_basic_info as a inner join hl_house_dynamic_info as b on a.house_id = b.house_id 
 where a.city = 'sx' and a.community = '润泽大院' and a.status = 1;

# total_on_sale_unit_price_per_size
select a.house_id, record_date, total_price, house_size from hl_house_basic_info as a inner join hl_house_dynamic_info as b on a.house_id = b.house_id 
 where a.city = 'sx' and a.community = '润泽大院' and a.status = 1;

# new_sold_unit_price | new_sold_unit_price_per_size | new_sold_time_span
select count(1), avg(deal_unit_price), sum(deal_total_price), sum(house_size), avg(deal_time_span) from hl_house_basic_info
where city = 'sx' and community = '润泽大院' and deal_date between '2019-04-01' and '2019-05-01' and status = 4;

# 


