-- Migration: Add ai_discovered column to texts table if not exists
ALTER TABLE texts ADD COLUMN IF NOT EXISTS ai_discovered BOOLEAN DEFAULT FALSE;
