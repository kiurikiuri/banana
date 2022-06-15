select
a.id as deck_id,
a.deck as deck,
b.word_id as word_id,
b.last_date as last_date,
b.check_list as check_list,
b.c_num as c_num,
b.ic_num as ic_num
from
wordwork.decks as a
right join wordwork.dwsts as b
on a.id = b.deck_id
inner join wdindk as c
on word_id = c.word_id;



select
*
from
decks as a
right join dwsts as b
on a.id = b.deck_id
inner join wdindk as c
on b.word_id = c.word_id
inner join words as d
on b.word_id = d.id
inner join StudyForget as e
on e.wdindk_id = c.id
where a.user_id = 1
order by e.id;



select
    a.id as deck_id,
    a.user_id as user_id,
    a.deck_kind_id as deck_kind_id,
    a.shared_flg as shared_flg,
    a.appear_flg as appear_flg,
    b.word_id as word_id,
    b.last_date as last_date,
    b.check_list as check_list,
    b.c_num as c_num,
    b.ic_num as ic_num,
    b.ans_num as ans_num,
    c.word as word,
    c.discription,
    d.*
from decks as a 
right join dwsts as b
    on a.id = b.deck_id
inner join words as c
    on b.word_id = c.id
inner join wdindk as d
    on b.word_id = d.word_id
;


select
    a.id as study_id,
    b.user_id as user_id,
    a.study_kind_id as study_kind_id,
    a.deck_id as deck_id,
    b.deck as deck,
    c.study_kind as study_kind,
    d.last_date as last_date,
    e.word as word,
    e.discription as discription,
    f.ans_num as ans_num,
    f.next_date as next_date
from
    study a
inner join decks b
    on a.deck_id = b.id
left join studyKind c
    on a.study_kind_id = c.id
right join dwsts as d
    on a.deck_id = d.deck_id
inner join words as e
    on e.id = d.word_id
inner join StudyForget as f
    on f.deck_id = a.deck_id
where
    b.user_id = 1
and
    a.deck_id = 8
and
    f.next_date > "2022/06/12";
;
 

select
    a.id as study_id, 
    a.study_kind_id as study_kind_id, 
    a.deck_id as deck_id,  
    b.user_id as user_id, 
    b.deck as deck,
    c.study_kind as study_kind,
    d.id as dwsts_id, 
    d.last_date as last_date,  
    d.c_num as c_num,  
    d.ic_num as ic_num,  
    d.check_list as check_list,
    e.word as word,  
    e.discription as discription,
    g.id as study_forget_id,      
    g.ans_num as ans_num,  
    g.next_date as next_date  
from 
    study as a 
inner join 
    decks as b 
        on a.deck_id = b.id
inner join
    studyKind as c
        on a.study_kind_id = c.id
inner join 
    dwsts as d 
        on a.deck_id = d.deck_id
        and b.user_id = d.user_id
inner join 
    words as e 
        on d.word_id = e.id
        and b.user_id = e.user_id
inner join 
    wdindk as f 
        on e.id = f.word_id
        and b.user_id = f.user_id
        and d.deck_id = f.deck_id
inner join 
    studyforget as g 
        on f.id = g.wdindk_id
        and g.deck_id = b.id
where 
    b.user_id = 1
order by b.id
;











select
*
from
    study a
inner join
    studyKind b
        on a.study_kind_id = b.id
;
select
*
from
    study a
inner join
    decks b
        on a.deck_id = b.id
;
select
*
from
    dwsts a
inner join
    wdindk b
        on a.deck_id = b.deck_id
        and a.word_id = b.word_id
inner join
    words c
        on a.word_id = c.id
inner join
    decks d
        on a.deck_id = d.id
        and b.deck_id = d.id

;
        









select 
    --a.id as study_id,  
    --b.user_id as user_id,  
   -- a.study_kind_id as study_kind_id,  
   -- a.deck_id as deck_id,  
   -- d.id as dwsts_id,  
    g.id as study_forget_id,  
   -- b.deck as deck,  
   -- c.study_kind as study_kind,  
   -- d.last_date as last_date,  
--     e.word as word,  
--     e.discription as discription,  
    --d.c_num as c_num,  
   -- d.ic_num as ic_num,  
   -- d.check_list as check_list,  
    g.ans_num as ans_num,  
    g.next_date as next_date  
from 
    study as a 
inner join 
    decks as b 
        on a.deck_id = b.id 
left join 
    studyKind as c 
        on a.study_kind_id = c.id 
inner join 
    dwsts as d 
        on a.deck_id = d.deck_id 
inner join 
    words as e 
        on d.word_id = e.id 
inner join 
    wdindk as f 
        on e.id = f.word_id 
inner join 
    studyforget as g 
        on f.id = g.wdindk_id 
;


