select * from parts
limit 10;

alter table parts
add unique (code);

update parts
set description = 'NA'
where description IS NULL OR description = ' ';

alter table parts
alter description SET NOT NULL;

select * from parts
limit 10;

/*insert into parts (id, code, manufacturer_id)
values (54, 'V1-009', 9);*/

alter table reorder_options
add check (price_usd IS NOT NULL AND quantity IS NOT NULL);

alter table reorder_options
add check (price_usd > 0 AND quantity > 0);

alter table reorder_options 
add check (price_usd/quantity > 0.02 and price_usd/quantity < 25);

alter table parts
add PRIMARY KEY (id);

alter table reorder_options
add FOREIGN KEY (part_id) REFERENCES parts(id);

alter table locations
add UNIQUE (part_id, location);

delete from locations
where part_id = 54;
alter table locations
add FOREIGN KEY (part_id) REFERENCES parts(id);

alter table parts
add FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id);

insert into manufacturers (id, name)
VALUES (11, 'Pip-NCC Industrial');

update parts
set manufacturer_id = 11
where manufacturer_id IN (1, 2);

delete from manufacturers where id = 1 and id = 2;
select * from manufacturers;

