-- One Glove: core schema. Matches the product brief's tech plan.
create extension if not exists postgis;
create extension if not exists vector;

create table profiles (
  id uuid primary key,                       -- auth.users.id in production
  handle text unique not null,
  rank text not null default 'Recruit',      -- Recruit, Constable, Inspector, Commissioner
  reunions_count int not null default 0,
  created_at timestamptz not null default now()
);

create table posts (
  id uuid primary key default gen_random_uuid(),
  case_number text unique not null,          -- OG-YYYY-NNNNN (lost) or WR-YYYY-NNNNN (found)
  kind text not null check (kind in ('lost','found')),
  status text not null default 'open' check (status in ('open','matched','reunited','archived')),
  hand text check (hand in ('L','R')),       -- null = unknown
  type text not null check (type in ('glove','mitten')),
  colours text[] not null default '{}',
  material text,
  is_child boolean not null default false,
  photo_path text not null,
  embedding vector(768),                     -- on-device feature print; null until the app uploads one
  location geography(point,4326) not null,   -- exact, participants only
  location_fuzzed geography(point,4326) not null, -- ~200 m, shown on the public Wall
  place text,
  city text,
  seen_at timestamptz not null,
  radius_m int,                              -- lost posts only
  note text,
  owner_id uuid references profiles(id),
  device_id text not null,
  created_at timestamptz not null default now()
);
create index posts_location_idx on posts using gist (location);
create index posts_open_idx on posts (kind, status, hand, seen_at);

create table matches (
  id uuid primary key default gen_random_uuid(),
  lost_post_id uuid not null references posts(id),
  found_post_id uuid not null references posts(id),
  score numeric(4,3) not null,
  lost_confirmed boolean not null default false,
  found_confirmed boolean not null default false,
  rejected_by uuid references profiles(id),
  created_at timestamptz not null default now(),
  unique (lost_post_id, found_post_id)
);

create table messages (
  id uuid primary key default gen_random_uuid(),
  match_id uuid not null references matches(id),
  sender_id uuid not null references profiles(id),
  body text not null,
  created_at timestamptz not null default now()
);

create table reunions (
  id uuid primary key default gen_random_uuid(),
  match_id uuid unique not null references matches(id),
  days_apart int not null,
  distance_m int not null,
  card_path text,
  shared_count int not null default 0,
  reunited_at timestamptz not null default now()
);

-- ponytail: RLS deliberately left for the next migration, once Sign in with Apple is wired.
