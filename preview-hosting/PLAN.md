# Isolated iPhone preview deployment

Status: NOT DEPLOYED. GitHub API access is blocked by the execution environment's
network proxy (HTTP CONNECT 403 for api.github.com). Existing Git authentication
works for Git operations; no new GitHub token has been requested.

## Deployment target

Create a separate repository owned by rhy4cn7rwp-prog named
`my-garden-grows-preview`, if that name is available. Never change Pages settings,
workflows, main, DNS, or the custom domain of `my-garden-grows`.

Copy only `development/` from the tested development/1.0 commit to the root of
the new preview repository. The layout already uses relative asset paths, so it
works beneath a GitHub Pages project path. Do not copy the original root index.
Enable Pages on the new repository only. Expected address, conditional on
successful creation and publication:
`https://rhy4cn7rwp-prog.github.io/my-garden-grows-preview/`.
Do not describe that address as live before verifying it responds with the game.

## Steps for the agent after access is restored

1. Read existing game repository and Pages metadata without editing it. Check
   whether the candidate preview repository already exists; preserve any work.
2. Check GitHub API permissions and repository/public-hosting eligibility.
3. Stage and validate a static copy locally. Create/configure only the new
   preview repository, push the reviewed files there, and enable its Pages site.
4. Check Pages build/deployment status and the actual HTTPS page and assets.
5. Run touch-only purchase → planting → watering/growth → harvesting → customer
   conversation → total calculation → payment/change → reload/save tests on
   the deployed HTTPS origin at an iPhone-sized viewport.
6. Confirm the original main SHA and Pages settings have not changed.
7. Supply the direct verified HTTPS address to the user. Explain Safari's normal
   browsing mode is needed for reliable storage; progress stays in that browser
   and origin. Do not promise survival after cleared website data.

## Current evidence and limits

The browser smoke test uses touch taps, a 390 × 844 viewport, device scale 3,
and a mobile Chromium context. This checks touch hit targets and saved progress,
but is not Safari validation. WebKit is not installed here, and no real iPhone
is attached. Real Safari confirmation remains outstanding. Hosted saves belong
to the preview origin; existing downloaded-file saves do not transfer.

## Network/settings prerequisite

Allow HTTPS access to `api.github.com` in the Codex environment's Internet
allowlist, retaining existing entries and GitHub presets. The preview's final
`rhy4cn7rwp-prog.github.io` hostname must also be reachable for deployment checks.
This is an environment networking change, not a change to the live game's
GitHub Pages source. Never ask the user to paste credentials into chat.
