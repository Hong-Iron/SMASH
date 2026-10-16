-- SMASH 학교 대항 랭킹: Supabase SQL Editor에 붙여 넣고 한 번 실행한다.
-- 다시 실행해도 안전하다(표는 지우지 않고, 함수만 새로 만든다).
-- 브라우저(공개 키, anon 역할)는 표를 직접 읽거나 쓰지 못하고, 아래 두 함수만 부를 수 있다.

-- 게임이 있는 학교 목록. 목록에 없는 코드로 보낸 점수는 버린다.
create table if not exists public.smash_school (
  code text primary key,
  name text not null,
  buildings int not null check (buildings > 0)
);

-- 날짜(한국 시간)별 학교 합계
create table if not exists public.smash_daily (
  day date not null,
  code text not null references public.smash_school (code) on delete cascade,
  score bigint not null default 0,
  kills bigint not null default 0,
  players int not null default 0,
  primary key (day, code)
);

-- 같은 IP에서 너무 자주 보내는지 세는 임시 표. IP는 날짜와 섞은 해시로만 두고 2분 뒤 지운다.
create unlogged table if not exists public.smash_throttle (
  k text not null,
  at timestamptz not null default now()
);
create index if not exists smash_throttle_k_at on public.smash_throttle (k, at);
create index if not exists smash_throttle_at on public.smash_throttle (at);

alter table public.smash_school enable row level security;
alter table public.smash_daily enable row level security;
alter table public.smash_throttle enable row level security;
revoke all on public.smash_school, public.smash_daily, public.smash_throttle from anon, authenticated;

-- 게임이 30초마다 부르는 함수: 그동안 얻은 점수, 무너뜨린 건물 수, 이번 방문의 첫 전송인지
create or replace function public.smash_add(p_code text, p_score bigint, p_kills int default 0, p_new boolean default false)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_day date := (now() at time zone 'Asia/Seoul')::date;
  v_bld int;
  v_hdr json;
  v_ip text;
  v_key text;
  v_cnt int;
begin
  select s.buildings into v_bld from smash_school s where s.code = p_code;
  if v_bld is null then return; end if;
  -- 한 번에 더할 수 있는 양의 상한: 핵폭탄 한 방이 학교 크기에 따라 16만~27만 점이다
  p_score := least(greatest(coalesce(p_score, 0), 0), greatest(500000, v_bld * 8000)::bigint);
  p_kills := least(greatest(coalesce(p_kills, 0), 0), v_bld * 2);
  if p_score = 0 and p_kills = 0 and not coalesce(p_new, false) then return; end if;

  begin
    v_hdr := current_setting('request.headers', true)::json;
  exception when others then
    v_hdr := null;
  end;
  v_ip := coalesce(v_hdr ->> 'cf-connecting-ip', nullif(split_part(coalesce(v_hdr ->> 'x-forwarded-for', ''), ',', 1), ''), v_hdr ->> 'x-real-ip');
  if v_ip is not null then
    v_key := md5(v_ip || '|' || v_day::text);
    delete from smash_throttle t where t.at < now() - interval '2 minutes';
    select count(*) into v_cnt from smash_throttle t where t.k = v_key and t.at > now() - interval '1 minute';
    -- 학교 와이파이처럼 여러 명이 IP 하나를 함께 쓰는 경우를 생각해 넉넉하게 둔다(한 사람은 1분에 2번)
    if v_cnt >= 60 then return; end if;
    insert into smash_throttle (k) values (v_key);
  end if;

  insert into smash_daily as d (day, code, score, kills, players)
  values (v_day, p_code, p_score, p_kills, case when p_new then 1 else 0 end)
  on conflict (day, code) do update
    set score = d.score + excluded.score,
        kills = d.kills + excluded.kills,
        players = d.players + excluded.players;
end;
$$;

-- 허브와 게임이 읽는 순위표: 학교마다 오늘(한국 시간) 합계와 전체 합계
drop function if exists public.smash_board();
create or replace function public.smash_board()
returns table (code text, name text, today_score bigint, today_kills bigint, today_players bigint, total_score bigint, total_kills bigint, total_players bigint)
language sql
stable
security definer
set search_path = public
as $$
  select s.code, s.name,
    coalesce(sum(d.score) filter (where d.day = (now() at time zone 'Asia/Seoul')::date), 0)::bigint,
    coalesce(sum(d.kills) filter (where d.day = (now() at time zone 'Asia/Seoul')::date), 0)::bigint,
    coalesce(sum(d.players) filter (where d.day = (now() at time zone 'Asia/Seoul')::date), 0)::bigint,
    coalesce(sum(d.score), 0)::bigint,
    coalesce(sum(d.kills), 0)::bigint,
    coalesce(sum(d.players), 0)::bigint
  from smash_school s
  left join smash_daily d on d.code = s.code
  group by s.code, s.name;
$$;

revoke all on function public.smash_add(text, bigint, int, boolean) from public;
revoke all on function public.smash_board() from public;
grant execute on function public.smash_add(text, bigint, int, boolean) to anon, authenticated;
grant execute on function public.smash_board() to anon, authenticated;
