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
    *
from
    kind a
inner join words b
    on a.
;
