-- Jobs table for Intelligence Service
-- Run this in Supabase SQL Editor

create table if not exists jobs (
  id uuid primary key default gen_random_uuid(),
  job_type text not null,
  status text not null default 'pending',
  input jsonb not null,
  output jsonb,
  error text,
  callback_url text,
  created_at timestamp with time zone default now(),
  started_at timestamp with time zone,
  completed_at timestamp with time zone
);

-- Index for worker polling (find pending jobs efficiently)
create index if not exists idx_jobs_status_created
  on jobs (status, created_at)
  where status = 'pending';

-- Index for job lookups by ID (already covered by primary key, but explicit for clarity)
create index if not exists idx_jobs_id on jobs (id);

-- Optional: Add check constraint for valid status values
alter table jobs
  add constraint jobs_status_check
  check (status in ('pending', 'processing', 'completed', 'failed'));

-- Optional: Add check constraint for valid job types
alter table jobs
  add constraint jobs_job_type_check
  check (job_type in ('company_research', 'competitor_analysis', 'industry_research'));

-- Enable Row Level Security (recommended for Supabase)
alter table jobs enable row level security;

-- Policy: Allow all operations for authenticated service role
-- (Your backend uses the service key, so this allows full access)
create policy "Service role has full access" on jobs
  for all
  using (true)
  with check (true);
