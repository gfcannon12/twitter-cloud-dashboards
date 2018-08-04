create table tweet_counts (id int generated always as identity, time varchar(8), end_time bigint, player varchar(50), tweets int, primary key(id));

select * from tweet_counts;

select count(*) from tweet_counts;

insert into tweet_counts (time, end_time, player, tweets) values ('5:10 PM', 201807221702, 'Jim Woods', 200);

delete from tweet_counts;

drop table tweet_counts;