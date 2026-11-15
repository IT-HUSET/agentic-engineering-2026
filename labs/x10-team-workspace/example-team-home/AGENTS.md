# Team Betala – workspace

Home for what no single repo owns. Sessions that touch more than one repo start here.

## Rules for all repos

- No direct pushes to `main`. Every change goes through a PR with at least one reviewer.
- Run tests with the command in `catalog/<repo>.md`, never a guessed one.
- Personal ID numbers (personnummer) and customer data must not appear in logs, fixtures or prompts.
- One repo, one worktree per feature: `git -C <path> worktree add ../<repo>-<feature>`.

## Where things live

- `catalog/` – one file per repo: owner, stack, test command, dependencies. Read the catalog file before you open the repo.
- `decisions/` – ADRs that apply to more than one repo.
- `sessions/` – approved session notes. Search here (`grep -ril <term> sessions/`) when a task resembles something the team has done before. Do not read them up front.

## Other repos

| Name | Path | Remote | What it is |
|---|---|---|---|
| orders-api | `~/work/orders-api` | `git@github.com:betala/orders-api.git` | Order handling, Kotlin and Postgres. Owns order status. |
| web-shop | `~/work/web-shop` | `git@github.com:betala/web-shop.git` | The web shop, TypeScript. Calls orders-api. |
| infra | `~/work/infra` | `git@github.com:betala/infra.git` | Terraform for all environments. |

If a path is missing: clone from the remote to that path.
