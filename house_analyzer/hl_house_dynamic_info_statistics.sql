# ----------------------------------------------------------------------------------------------------------------------- #
# total_on_sale | total_off_sale | total_sold
# 截至统计月的月末，所有在售、下架、已售房源数量

# 统计 total_on_sale = a + b + c
# a = 截至统计月月底在售的所有房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 1 and list_date < '2019-01-01';
# b = 统计月底至统计之日，从在售变成下架的房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and list_date < '2019-01-01' and update_time >= '2019-01-01';
# c = 统计月月底至统计之日，从在售变成成交的房源数量
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and list_date < '2019-01-01' and deal_date >= '2019-01-01';

# 统计 total_off_sale = a + b
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time < '2019-01-01';
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time is null and create_time < '2019-01-01';

# total_sold
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and deal_date < '2019-01-01';

# ----------------------------------------------------------------------------------------------------------------------- #
# new_on_sale
# 统计这个月刚上架的房源数量，包括这个月上架后当月下架或当月成交的房源
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and list_date between '2019-01-01' and  '2019-02-01';

# new_off_sale
# 统计这个月刚下架的房源数量，包括这个月上架后当月下架的房源
# 由于update_time会不断变更（下架后有可能又会上架），所以不同时间统计同一个月的数据，也会发生变化
# 如五月下架了某房子，六月统计五月的下架房源时，该房子被统计在内。后来房子又重新上架了，上架后再去统计五月的下架房源时，该房子就没被统计进去了
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time between '2019-01-01' and '2019-02-01';
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 2 and update_time is null and create_time between '2019-01-01' and '2019-02-01';

# new_sold
# 统计这个月刚成交的房源数量，包括这个月上架后当月成交的房源
select count(1) from hl_house_basic_info where city = 'nj' and community = '江岸水城' and status = 4 and deal_date between '2019-01-01' and  '2019-02-01';

# ----------------------------------------------------------------------------------------------------------------------- #
# total_on_sale_unit_price | total_on_sale_unit_price_per_size
select a.house_id, b.record_date, b.total_price, a.house_size, b.unit_price from hl_house_basic_info as a
inner join hl_house_dynamic_info as b
on a.house_id = b.house_id
where a.city = 'nj' and a.community = '江岸水城'
and ((a.status = 1 and a.list_date < '2019-05-01')
or (a.status = 2 and a.list_date < '2019-05-01' and a.update_time >= '2019-05-01')
or (a.status = 4 and a.list_date < '2019-05-01' and a.deal_date >= '2019-05-01'))
and b.record_date < '2019-05-01';

# ----------------------------------------------------------------------------------------------------------------------- #
# new_sold_unit_price | new_sold_unit_price_per_size | new_sold_time_span
select count(1), avg(deal_unit_price), sum(deal_total_price), sum(house_size), avg(deal_time_span) from hl_house_basic_info
where city = 'nj' and community = '江岸水城' and status = 4 and deal_date between '2019-01-01' and '2019-02-01';
