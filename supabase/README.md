# One Glove — Supabase

migrations/0001_init.sql   core schema (profiles, posts, matches, messages, reunions); needs postgis + vector
seed/demo_gloves.json      20 demo posts, 6 profiles, 4 matches, 2 reunions — edit this
seed/make_seed_sql.py      python3 make_seed_sql.py > seed.sql
seed/seed.sql              generated; loads with `supabase db reset` or psql -f

Verified: migration + seed load cleanly on Postgres 16 with PostGIS 3 and pgvector.
Embeddings are null in the seed; the app fills them when demo photos are uploaded to Storage under demo/.
