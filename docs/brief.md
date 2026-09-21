# One Glove — Product Brief

As of 2026-09-22. Living version: https://claude.ai/code/artifact/3ec49344-f5e8-41d5-aeb2-cba9d25475d8

## The pitch

One Glove is a missing-persons bureau for gloves: post a lost glove or a found glove, get matched with its other half nearby, and share the reunion. Gloves are the one lost item people already photograph and joke about (the @single_glove Instagram account, NPR's "Single Glove, Slightly Used, Looking for a Mate", Brooklyn's Lonely Gloves Club, Tom Hanks's lost-glove photo habit), but nobody has built the matching layer. Existing lost-and-found apps are utilitarian and generic.

Why now: iOS share sheets, on-device image embeddings and App Clips make "photograph it, post it, share the poster" a 20-second loop. Launch is worldwide, timed to northern-hemisphere winter; Whistler and the Sea-to-Sky corridor are the first on-the-ground proving town.

Success in season one: 10,000 posts, 500 confirmed reunions, one reunion story picked up by a local outlet. Free app; version one is about attention, not revenue.

## Brand and tone

Original direction: a deadpan bureaucracy that takes gloves with total seriousness (every lost glove is a Case with a case number, every found glove a Witness Report, a match is a Reunion, unclaimed after 30 days is Archived, presumed single). Warmth only at the reunion moment.

Now under review: a warmer "one love" feeling. Five directions are up for a vote (Sunrise Session, Two Hands, Knit Together, Good Vibrations, Warm Bureau); see `brand-directions.html` and the live ballot in the README. This section gets rewritten once a direction wins.

## Core loop

Post, match, reunite, share, in under a minute of user effort. The found side is the engine: finders have zero stake, so a found-glove report is one photo and one tap, no account. A lost post includes a photo of the survivor (the glove you still have): we match glove to glove, not glove to memory. Handoff is low-trust by default: finders leave the glove somewhere public and record where.

## Viral hooks

| Hook | What the user gets | Why it spreads |
|---|---|---|
| Missing Poster | Auto-generated poster from any case, 9:16 story + printable PDF | Their own glove, funny with zero matches |
| Reunion Card | "REUNITED after 11 days, 3.4 km apart", both handles | Tags a second person, credits the finder |
| Glove of the Week | One editorial pick, pinned and posted | Gives official accounts a reason to exist |
| The Wall | Public map/feed of unclaimed gloves by "days single" | Locals browse it like a blotter |
| Detective ranks | Constable at 1 reunion, Inspector at 5, Commissioner at 25 | Repeat finders |
| Season Report | "Whistler lost 1,412 gloves. 61% were left hands." | Annual press hook |
| QR posters | App Clip report flow from a poster, no install | Meets the finder at the glove |

KPI: shares per post, target 0.3 in month one.

## Screens (MVP)

The Wall (home), Report (found), Open a Case (lost), Case File, Matches, Chat + Handoff, Reunion. Sign in with Apple only when chatting or confirming a match.

## Matching

Ranked shortlist, humans confirm. Hand (L/R) is a hard filter; then geo (default 5 km radius), time (60-day window), attributes (glove/mitten, colours, material, child), and on-device image embedding compared by cosine distance (also against the mirrored survivor image).

`score = 0.45·sim + 0.20·geo + 0.15·time + 0.20·attr; hand mismatch ⇒ 0`

Both sides confirm → Handoff. "Not mine" is never resurfaced. Confirmed reunions become labelled pairs for tuning.

## Tech

SwiftUI, Swift 6, iOS 17+. Vision (hand pose, subject lift) and Core ML feature print on device. Supabase: Postgres + PostGIS + pgvector, Storage, Auth (Sign in with Apple), Edge Functions, Realtime. APNs via Edge Function. Share assets rendered with SwiftUI ImageRenderer. App Clip for the report flow. Tables: profiles, posts, matches, messages, reunions (`supabase/migrations/0001_init.sql`).

## Roadmap

| Phase | Ends | Ships |
|---|---|---|
| 1 Case file | 16 Oct 2026 | Schema, Wall, Report, Open a Case, poster export. TestFlight to 20 friends. |
| 2 Matching | 13 Nov 2026 | Embeddings, match function, Matches, push, chat, reunion card. |
| 3 Launch | 27 Nov 2026 | Worldwide App Store release, QR posters in Whistler Village, Wall seeded with 20 demo cases, Glove of the Week. |

Out of scope v1: Android, web, rewards, partnerships, monetisation.

## Open questions

- Second proving town after Whistler?
- Which entity owns it: Watchkeeper, Ctrl Alt Delete, or new?
- Budget for printed posters and a launch-weekend stunt?
- Mittens in classifier scope? (recommended: yes)
