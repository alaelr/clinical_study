anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
API URL: http://127.0.0.1:54321

# PostgreSQL vs. Supabase Setup

| Feature          | PostgreSQL          | Supabase            |
|------------------|--------------------|---------------------|
| **Port**         | 5432               | 54322               |
| **Default User** | postgres           | postgres            |
| **Password**     | Your local password | postgres            |
| **Auth Method**  | Peer/MD5           | Password            |
| **RLS**          | Disabled by default | Enabled by default  |
| **API Access**   | None               | REST/graphQL APIs   |

# Key Notes:
1. Supabase requires RLS (Row Level Security) configuration
2. Supabase runs on port 54322 to avoid conflicts
3. Always use `postgres` user for local Supabase