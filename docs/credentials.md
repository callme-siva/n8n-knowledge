# Credentials: set up once, use everywhere

| Credential | Used in | Free? |
|---|---|---|
| [Google Gemini](#google-gemini) | L11–L18, L22 | ✅ free tier |
| [Gmail](#gmail) | almost all | ✅ |
| [Google Sheets / Drive](#google-sheets--drive) | L06, L07, L09, L12, L19–L22 | ✅ |
| [Jira Software Cloud](#jira) | L08, L10, L15 | ✅ free for up to 10 users |
| [SerpAPI](#serpapi) | L03 | ✅ 100 searches/month |
| [GitHub](#github) | L16 | ✅ |

> 🔒 **Never commit credentials.** n8n stores them encrypted in its own database; exported workflows only reference them by name. `tools/validate.py` fails if a workflow still contains a `credentials` block.

## Google Gemini
1. Go to https://aistudio.google.com/app/apikey → **Create API key**.
2. In n8n: *Credentials → Add → Google Gemini(PaLM) Api*. Paste the key and leave Host as the default.
3. Models used: `gemini-2.5-flash` (chat) and `gemini-embedding-001` (RAG in L13).
4. Free-tier limits are per minute. If you see `429`, wait, or switch to `gemini-2.5-flash-lite`.

**Other models:** every workflow uses a separate *Chat Model* sub-node. To switch, delete the Gemini node, attach *OpenAI / Anthropic / Mistral / Ollama Chat Model*, and nothing else changes. (Ollama runs fully offline and free.)

## Gmail
**n8n Cloud:** *Add credential → Gmail OAuth2 → Sign in with Google.* Done.

**Self-hosted:** you need your own Google OAuth client (one-time, about 10 minutes):
1. https://console.cloud.google.com → create a project.
2. *APIs & Services → Library* → enable **Gmail API**, **Google Sheets API**, **Google Drive API**.
3. *OAuth consent screen* → External → add yourself as a **test user**.
4. *Credentials → Create → OAuth client ID → Web application*. Authorised redirect URI = the one shown in the n8n credential dialog (`…/rest/oauth2-credential/callback`).
5. Paste the Client ID and Secret into n8n → *Sign in with Google*.

## Google Sheets / Drive
Use the same OAuth client as Gmail and create *Google Sheets OAuth2* and *Google Drive OAuth2* credentials.
In workflows, replace `PASTE_YOUR_GOOGLE_SHEET_URL` with your sheet URL, and create the tab and header row listed in the lesson README.

## Jira
1. https://id.atlassian.com/manage-profile/security/api-tokens → **Create API token**.
2. n8n: *Jira SW Cloud API*. Email = your Atlassian email, domain = `https://your-site.atlassian.net`.
3. In Jira nodes, replace `REPLACE_PROJECT_ID` / `REPLACE_…_ISSUE_TYPE_ID` by switching the field to **From list** and picking.

## SerpAPI
Sign up at https://serpapi.com → copy the key → n8n *SerpApi* credential.

## GitHub
https://github.com/settings/tokens → *classic token* with `repo` + `read:project` → n8n *GitHub API* credential.
