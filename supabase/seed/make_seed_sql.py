#!/usr/bin/env python3
"""Emit seed.sql from demo_gloves.json. Run: python3 make_seed_sql.py > seed.sql"""
import json, sys

d = json.load(open(__file__.rsplit('/', 1)[0] + '/demo_gloves.json'))

def q(v):
    if v is None: return 'null'
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, list): return "array[" + ",".join(q(x) for x in v) + "]::text[]"
    return "'" + str(v).replace("'", "''") + "'"

out = ["-- One Glove demo seed. Generated from demo_gloves.json; edit the JSON, not this file.",
       "begin;",
       "delete from reunions; delete from messages; delete from matches; delete from posts; delete from profiles where id::text like '11111111-%';"]

for p in d['profiles']:
    out.append(f"insert into profiles (id, handle, rank, reunions_count) values ({q(p['id'])},{q(p['handle'])},{q(p['rank'])},{p['reunions_count']});")

for p in d['posts']:
    out.append(
        "insert into posts (id, case_number, kind, status, hand, type, colours, material, is_child, photo_path, "
        "location, location_fuzzed, place, city, seen_at, radius_m, note, owner_id, device_id) values ("
        f"{q(p['id'])},{q(p['case_number'])},{q(p['kind'])},{q(p['status'])},{q(p['hand'])},{q(p['type'])},"
        f"{q(p['colours'])},{q(p['material'])},{q(p['is_child'])},{q(p['photo_path'])},"
        f"st_setsrid(st_makepoint({p['lng']},{p['lat']}),4326)::geography,"
        f"st_setsrid(st_makepoint(round({p['lng']}::numeric,3),round({p['lat']}::numeric,3)),4326)::geography,"
        f"{q(p['place'])},{q(p['city'])},{q(p['seen_at'])},{q(p['radius_m'])},{q(p['note'])},{q(p['owner_id'])},"
        f"'demo-device-{p['id'][-2:]}');")

for m in d['matches']:
    out.append(f"insert into matches (id, lost_post_id, found_post_id, score, lost_confirmed, found_confirmed, created_at) values ("
               f"{q(m['id'])},{q(m['lost_post_id'])},{q(m['found_post_id'])},{m['score']},{q(m['lost_confirmed'])},{q(m['found_confirmed'])},{q(m['created_at'])});")

for r in d['reunions']:
    out.append(f"insert into reunions (id, match_id, days_apart, distance_m, shared_count, reunited_at) values ("
               f"{q(r['id'])},{q(r['match_id'])},{r['days_apart']},{r['distance_m']},{r['shared_count']},{q(r['reunited_at'])});")

out.append("commit;")
sys.stdout.write("\n".join(out) + "\n")
