# ----------------------------------------------------------------------------------------------------------------------- #
# total_on_sale | total_off_sale | total_sold
# 截至上个月月末，所有在售、下架、已售房源数量

# 统计 total_on_sale = a + b + c
# a = 截至四月底在售的所有房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 1 and list_date < '2019-01-01';
# b = 四月底至统计之日，从在售变成下架的房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and list_date < '2019-01-01' and update_time >= '2019-01-01';
# c = 四月底至统计之日，从在售变成成交的房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and list_date < '2019-01-01' and deal_date >= '2019-01-01';

# 统计 total_off_sale = a + b
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time < '2019-01-01';
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time is null and create_time < '2019-01-01';

# total_sold
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and deal_date < '2019-01-01';

# ----------------------------------------------------------------------------------------------------------------------- #
# new_on_sale
# 上个月刚上架的房源数量，包括上个月上架后当月下架或当月成交的房源
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and list_date between '2019-01-01' and  '2019-02-01';

# new_off_sale
# 上个月刚下架的房源数量，包括上个月上架后当月下架的房源
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time between '2019-01-01' and '2019-02-01';
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time is null and create_time between '2019-01-01' and '2019-02-01';

# new_sold
# 上个月刚成交的房源数量，包括上个月上架后当月成交的房源
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and deal_date between '2019-01-01' and  '2019-02-01';

# ----------------------------------------------------------------------------------------------------------------------- #
# total_on_sale_unit_price
select a.house_id, b.record_date, b.total_price, a.house_size, b.unit_price from hl_house_basic_info as a
inner join hl_house_dynamic_info as b
on a.house_id = b.house_id
where a.city = 'nj' and a.community = '江岸水城'
and ((a.status = 1 and a.list_date < '2019-05-01')
or (a.status = 2 and a.list_date < '2019-05-01' and a.update_time >= '2019-05-01')
or (status = 4 and list_date < '2019-05-01' and deal_date >= '2019-05-01'))
and b.record_date < '2019-05-01';





# total_on_sale_unit_price_per_size
select a.house_id, record_date, total_price, house_size from hl_house_basic_info as a inner join hl_house_dynamic_info as b on a.house_id = b.house_id 
 where a.city = 'sx' and a.community = '润泽大院' and a.status = 1;

# new_sold_unit_price | new_sold_unit_price_per_size | new_sold_time_span
select count(1), avg(deal_unit_price), sum(deal_total_price), sum(house_size), avg(deal_time_span) from hl_house_basic_info
where city = 'sx' and community = '润泽大院' and deal_date between '2019-04-01' and '2019-05-01' and status = 4;





# ----------------------------------------------------------------------------------------------------------------------- #
#
select house_id, deal_date as record_date, deal_total_price as total_price, deal_unit_price as unit_price from hl_house_basic_info where status = 4 and deal_date is not null;
