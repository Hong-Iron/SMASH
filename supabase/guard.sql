-- SMASH 랭킹 정리와 방어 (제안, 아직 실행 안 함). Supabase SQL Editor에서 ①부터 순서대로 실행한다.
-- 다시 실행해도 안전하다.

-- (①② 정리는 restore.sql·restore2.sql로 대신했다. 하루 점수 하나로 거르면 방문이 몰린 날의 정상 기록까지 걸려서 지웠다.)

-- ③ 방어: 같은 IP(날짜와 섞은 해시)가 하루에 보낼 수 있는 점수 합계를 1억 점으로 막는다.
--    정상 플레이어는 하루 100만~200만 점이다. 학교 와이파이처럼 수십 명이 IP 하나를 같이 써도 남는다.
create table if not exists public.smash_ipday (
  k text not null,
  day date not null,
  score bigint not null default 0,
  primary key (k, day)
);
alter table public.smash_ipday enable row level security;
revoke all on public.smash_ipday from anon, authenticated;

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
  v_used bigint;
begin
  select s.buildings into v_bld from smash_school s where s.code = p_code;
  if v_bld is null then return; end if;
  p_kills := least(greatest(coalesce(p_kills, 0), 0), v_bld * 2);
  -- 한 번에 더할 수 있는 점수: 게임은 3분마다, 또는 40만 점이 모이면 40만 점씩 나눠 보낸다.
  -- (부순 건물 수는 첫 묶음에만 실려 오므로, 건물 수로 점수를 제한하면 정상 핵폭탄 점수가 잘린다)
  p_score := least(greatest(coalesce(p_score, 0), 0), 400000::bigint);
  if p_score = 0 and p_kills = 0 and not coalesce(p_new, false) then return; end if;

  begin
    v_hdr := current_setting('request.headers', true)::json;
  exception when others then
    v_hdr := null;
  end;
  -- 게이트웨이가 붙이는 x-forwarded-for의 첫 값을 먼저 본다. IP를 모르면 점수를 받지 않는다(예전에는 검사를 건너뛰었다)
  v_ip := coalesce(nullif(split_part(coalesce(v_hdr ->> 'x-forwarded-for', ''), ',', 1), ''), v_hdr ->> 'cf-connecting-ip', v_hdr ->> 'x-real-ip');
  if v_ip is null then return; end if;
  v_key := md5(v_ip || '|' || v_day::text);

  delete from smash_throttle t where t.at < now() - interval '2 minutes';
  select count(*) into v_cnt from smash_throttle t where t.k = v_key and t.at > now() - interval '1 minute';
  if v_cnt >= 60 then return; end if;              -- 1분에 60번 (학교 와이파이 몫으로 그대로)
  insert into smash_throttle (k) values (v_key);

  insert into smash_ipday as i (k, day, score) values (v_key, v_day, 0)
  on conflict (k, day) do nothing;
  select i.score into v_used from smash_ipday i where i.k = v_key and i.day = v_day for update;
  p_score := least(p_score, greatest(100000000::bigint - v_used, 0));
  update smash_ipday set score = score + p_score where k = v_key and day = v_day;
  if p_score = 0 and p_kills = 0 and not coalesce(p_new, false) then return; end if;

  insert into smash_daily as d (day, code, score, kills, players)
  values (v_day, p_code, p_score, p_kills, case when p_new then 1 else 0 end)
  on conflict (day, code) do update
    set score = d.score + excluded.score,
        kills = d.kills + excluded.kills,
        players = d.players + excluded.players;
end;
$$;
revoke all on function public.smash_add(text, bigint, int, boolean) from public;
grant execute on function public.smash_add(text, bigint, int, boolean) to anon, authenticated;

-- ④ 하루 지난 IP 합계는 지운다(가끔 한 번 실행하거나 pg_cron에 걸어 둔다)
delete from public.smash_ipday where day < (now() at time zone 'Asia/Seoul')::date - 1;
