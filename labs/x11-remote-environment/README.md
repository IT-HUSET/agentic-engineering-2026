# X11 preparation and operations

X11 is individual. The first advanced group has four people: `p01`–`p04`, with VMs `x11-p01`–`x11-p04` in the shared temporary resource group `agentic-engineering-2026`. There is no automatic daily shutdown. The facilitator starts the VMs before the course, keeps them running while jobs need them, and manually deallocates them only after work is saved and no jobs are active. All course resources are removed after the course.

Everything needed to operate or use the environments is in this folder: this runbook, [participant access](access.md), `azure.bicep`, `cloud-init.yaml` and `prepare-course.py`. Participants use plain SSH with one temporary course password. There are no private-key files, access bundles or local secret JSON files to manage. Password hint: **The teacher's favorite country**. Never commit the password or put it in a model prompt.

## Two layers, one development-tool definition

| Layer | Source | Contains |
|---|---|---|
| VM host | Ubuntu 24.04 LTS, x64 Gen2 | Docker, Node 24 and Dev Container CLI |
| Each person's container | Existing `.devcontainer/devcontainer.json` | Dockerfile, Features, environment, volume and `postCreateCommand` |

Reuse the full dev-container configuration. A Dockerfile-only build omits Features and setup. No separate development-tool image, custom Azure image or registry is needed. Mutable image/package references mean a functional rebuild, not byte-identical binaries.

## Before deployment

- Use `IT-Huset MPN Gold`, Sweden Central, and name the cleanup owner. Confirm the selected subscription ID before creating anything.
- Register `Microsoft.Compute` and `Microsoft.Network` if needed.
- Confirm policy allows the VM/public IP with restricted SSH and the package/container registries. Participants need no Azure account, RBAC role, Entra invitation or Azure CLI. If they must manage Azure resources themselves, grant access to a separate per-person group such as `agentic-engineering-2026-p01`, not Contributor on the shared course group.
- Check quota and size availability. The pilot used `Standard_D2s_v6` (2 vCPU, 8 GiB); D2s v5 had zero family quota. Ten regional vCPUs fit four personal VMs plus one rebuild VM at a time. Recheck before the course.
- Use the facilitator's current public IPv4 for preparation, then update SSH access to the venue's source address. Do not open SSH to every address. Use an approved private network instead if policy requires it.
- Agree the cost owner and budget notifications. A budget alert is not a spending cap. Azure pays only for the VMs; model usage comes from each participant's Claude plan (IT-HUSET team seat or own plan, D11).

## 1. Set the temporary course password

For the four **existing** course VMs, run this from the participant repo root after signing into Azure. It prompts once, hashes locally with OpenSSL SHA-512 crypt, then invokes the versioned `password-access.sh` through Azure Run Command:

```bash
uv run labs/x11-remote-environment/prepare-course.py set-password --subscription 'IT-Huset MPN Gold'
```

The default group is `agentic-engineering-2026`, and default VMs are `x11-p01`–`x11-p04`. For one replacement use `--resource-group <rebuild-group> --vms x11-p01-rebuild`. Use `--openssl /path/to/openssl` if your default OpenSSL lacks `passwd -6`; on the facilitator's Mac, `/opt/homebrew/bin/openssl` supports it. The helper stores no password/hash files and never prints the password, salted hash or raw Azure command/output. Errors identify the failed stage without echoing restricted output. It reports `PASSWORD_ACCESS_READY` or an error for each VM.

Only a URL-safe base64 encoding of the salted hash is passed to Azure management; this avoids dollar-sign expansion in the Run Command shell. The script decodes and validates the hash before use. Treat Azure Run Command records as restricted administrative data. The root script applies password-only authentication for `course`, disables root login/password authentication, validates `sshd -t` and effective settings, then reloads SSH. It owns one marked final configuration block and preserves unrelated SSH configuration. No NSG or global authentication rule is loosened. A failed SSH configuration check restores the previous configuration; only `PASSWORD_ACCESS_READY` confirms application.

The selected temporary password is entered interactively. Its only published hint is **The teacher's favorite country**. Do not pre-login anyone's Claude or GitHub account. Participants use their row in [access.md](access.md), enter the course password and sign into their own services inside the container.

**New VMs:** Azure requires a strong bootstrap password during provisioning. Step 2 generates one; after cloud-init completes, run this helper for the new VM to apply the course password. Do not redeploy existing VMs merely to change their authentication.

## 2. Preview and deploy a person

On the facilitator's computer, select and verify the subscription:

```bash
az login
az account set --subscription 'IT-Huset MPN Gold'
az account show --query '{name:name,id:id,tenant:tenantId}' --output table
x11_group='agentic-engineering-2026'
x11_location='swedencentral'
x11_size='Standard_D2s_v6'
x11_source_ip='<current-facilitator-public-ipv4>'
az vm list-skus --location "$x11_location" --resource-type virtualMachines --size "$x11_size" --all --output table
az vm list-usage --location "$x11_location" --output table
x11_image_version='24.04.202610250'
az vm image show --location "$x11_location" --urn "Canonical:ubuntu-24_04-lts:server:${x11_image_version}" --query name --output tsv
az group create --name "$x11_group" --location "$x11_location" --tags course=agentic-engineering-2026 lifecycle=temporary
```

Record the resolved image version and repo commit in the public preparation record below, so rebuilds use the same inputs. Select one person, then repeat for `p02`, `p03` and `p04`:

```bash
x11_participant='p01'
x11_vm="x11-${x11_participant}"
x11_bootstrap_password=$(openssl rand -base64 24)
az deployment group what-if --resource-group "$x11_group" --template-file labs/x11-remote-environment/azure.bicep --parameters vmName="$x11_vm" vmSize="$x11_size" sshSourceIpv4="$x11_source_ip" adminPassword="$x11_bootstrap_password" imageVersion="$x11_image_version"
```

Review the preview. This separate command creates chargeable resources:

```bash
az deployment group create --name "$x11_vm" --resource-group "$x11_group" --template-file labs/x11-remote-environment/azure.bicep --parameters vmName="$x11_vm" vmSize="$x11_size" sshSourceIpv4="$x11_source_ip" adminPassword="$x11_bootstrap_password" imageVersion="$x11_image_version"
```

Use this template only for a **new** VM. `adminPassword` is a secure Bicep parameter containing the strong generated bootstrap password, never the memorable course password. Clear the local variable after deployment:

```bash
unset x11_bootstrap_password
```

There is no VM managed identity, Azure login or personal model token in the deployment. Read its IP:

```bash
az deployment group show --name "$x11_vm" --resource-group "$x11_group" --query properties.outputs.publicIpAddress.value --output tsv
```

Record that IP in the public [connection table](access.md#connection-table). After bootstrap, apply the course password with step 1. Do not write passwords into this table.

## 3. Prebuild and verify before handoff

Azure deployment success does not prove cloud-init succeeded. From the facilitator's computer, use Azure management, without exporting SSH keys:

```bash
az vm run-command invoke --resource-group "$x11_group" --name "$x11_vm" --command-id RunShellScript --scripts 'set -e; cloud-init status --wait; usermod -aG docker course; ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub; cat /etc/ssh/ssh_host_ed25519_key.pub'
```

Check the script result, and publish the trusted ED25519 host fingerprint/public host key in `access.md` for that VM. Run Command executes as an elevated user; participants do not receive this management permission. If bootstrap fails, inspect the cloud-final journal and cloud-init output through management. Do not put credentials in those logs.

Then run the following **on each VM as `course`**, through a course-password SSH session or the Azure management channel using `su - course -c '<commands>'`. Use a permitted repo URL, without a token, and a recorded **published** commit. The current private local export was transferred as a git bundle by the facilitator; its tag is not available from upstream:

```bash
git clone https://github.com/<owner>/<repo>.git course-repo
cd course-repo
git switch -c x11-course <recorded-course-commit>
devcontainer up --workspace-folder "$PWD"
devcontainer exec --workspace-folder "$PWD" bash -lc 'cd todo-app && uv run pytest'
docker ps
```

Use the container ID from `up`/`docker ps` to enable restart when the VM starts again:

```bash
docker update --restart unless-stopped <container-id>
docker inspect <container-id> --format '{{.HostConfig.RestartPolicy.Name}} {{.HostConfig.Privileged}} {{json .Mounts}}'
```

Expect `unless-stopped`, `false`, the workspace and declared Claude volume. No host SSH/cloud credentials or Docker socket may be mounted. Run the lab's boundary probes before handoff. Do not log into a personal agent or GitHub account during prebuild. The current app has 63 tests; `check.py` cannot be fully GREEN until the recipient signs in.

If the repo directory already exists, inspect its commit and container instead of cloning over it. Finish the public table and preparation record below. Give each person their ID and the link to [access.md](access.md). They paste one plain SSH command, enter the shared course password, then perform their own Claude/GitHub sign-ins.

## 4. Operate during the course

All commands run on the facilitator's computer. There is no automatic daily stop. Start the VMs before the course and leave them running while participants need active jobs. Before manually deallocating a VM, confirm that its participant saved their work and no job is running. A VM restart can restart the container under `unless-stopped`, but it cannot restore an interrupted tmux/agent process.

Start the four VMs before participants arrive:

```bash
az vm start --resource-group agentic-engineering-2026 --name x11-p01
az vm start --resource-group agentic-engineering-2026 --name x11-p02
az vm start --resource-group agentic-engineering-2026 --name x11-p03
az vm start --resource-group agentic-engineering-2026 --name x11-p04
```

Inspect their actual states:

```bash
az vm list --resource-group agentic-engineering-2026 --show-details --query '[].{name:name,power:powerState,ip:publicIps}' --output table
```

Only after each participant has saved their work and confirmed that no jobs are active, manually deallocate the relevant VMs to stop compute billing:

```bash
az vm deallocate --resource-group agentic-engineering-2026 --name x11-p01
az vm deallocate --resource-group agentic-engineering-2026 --name x11-p02
az vm deallocate --resource-group agentic-engineering-2026 --name x11-p03
az vm deallocate --resource-group agentic-engineering-2026 --name x11-p04
```

Disks/public IPs can still cost money while deallocated. Shutting down Linux alone is not equivalent to deallocation.

### Change the allowed SSH source to the venue

Keep an existing connection open, obtain the actual venue public IPv4 and update each NSG. This affects incoming SSH, not outbound model traffic:

```bash
x11_venue_ip='<venue-public-ipv4>'
az network nsg rule update --resource-group agentic-engineering-2026 --nsg-name x11-p01-nsg --name SSH-from-course-network --source-address-prefixes "${x11_venue_ip}/32"
az network nsg rule update --resource-group agentic-engineering-2026 --nsg-name x11-p02-nsg --name SSH-from-course-network --source-address-prefixes "${x11_venue_ip}/32"
az network nsg rule update --resource-group agentic-engineering-2026 --nsg-name x11-p03-nsg --name SSH-from-course-network --source-address-prefixes "${x11_venue_ip}/32"
az network nsg rule update --resource-group agentic-engineering-2026 --nsg-name x11-p04-nsg --name SSH-from-course-network --source-address-prefixes "${x11_venue_ip}/32"
```

Test SSH from the venue before closing the old connection. Do not replace `/32` with unrestricted access. If another network must be supported, get the policy decision first. Re-deploying Bicep can replace a manually updated rule, so use the current allowed source in future deployments.

## 5. Rebuild proof and final cleanup

The rebuild is a **per-participant sequence**, because the regional quota holds four participant VMs plus one rebuild VM. For each participant in turn: deploy `x11-pNN-rebuild` with the same repo commit and exact Ubuntu image version, a distinct `vmName` and a new strong bootstrap password. After bootstrap, apply the shared course password with step 1. The participant transfers the source and repeats the checks using plain SSH/SCP password prompts. When their proof is saved, delete the rebuild before the next participant's starts. Keep the first machine throughout. Do not copy disks, Docker volumes or credential caches.

Put each rebuild in its own temporary group, so one deletion removes all of it:

```bash
x11_participant='p01'
x11_vm="x11-${x11_participant}-rebuild"
x11_rebuild_group="agentic-engineering-2026-${x11_participant}-rebuild"
az group create --name "$x11_rebuild_group" --location "$x11_location" --tags course=agentic-engineering-2026 lifecycle=temporary
x11_bootstrap_password=$(openssl rand -base64 24)
az deployment group what-if --resource-group "$x11_rebuild_group" --template-file labs/x11-remote-environment/azure.bicep --parameters vmName="$x11_vm" vmSize="$x11_size" sshSourceIpv4="$x11_source_ip" adminPassword="$x11_bootstrap_password" imageVersion="$x11_image_version"
```

After reviewing the preview, run the same command as `az deployment group create --name "$x11_vm" …`, then `unset x11_bootstrap_password`. Wait for `cloud-init status --wait` and verify the replacement's host fingerprint through Azure management, as in step 3. Apply the course password with `prepare-course.py set-password --subscription 'IT-Huset MPN Gold' --resource-group "$x11_rebuild_group" --vms "$x11_vm"` before the first SSH connection.

The current prepared export is private and **not published upstream**, so transfer its git history without copying the container or credentials. On the original VM host:

```bash
cd /home/course/course-repo
git bundle create /home/course/x11-source.bundle x11-course-20261116
git bundle verify /home/course/x11-source.bundle
```

The participant, on their own computer, uses the two public IPs and enters the course password at each SCP prompt. Replace both IP placeholders:

```bash
scp -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@<original-public-ip>:/home/course/x11-source.bundle ./x11-source.bundle
scp -o StrictHostKeyChecking=accept-new -o ForwardAgent=no ./x11-source.bundle course@<replacement-public-ip>:/home/course/x11-source.bundle
```

On the replacement VM host as `course`, with no existing `course-repo` directory:

```bash
git clone /home/course/x11-source.bundle /home/course/course-repo
cd /home/course/course-repo
git switch -c x11-course x11-course-20261116
git remote remove origin
devcontainer up --workspace-folder "$PWD"
```

Then the participant repeats the tests, mount/boundary probes and fresh sign-ins. The bundle holds only the recorded source tree and history, not uncommitted work or containers. Push or save the participant's changes before deleting anything. After the proof is saved, remove the bundle from both VM homes and the participant's computer, then delete the rebuild group as a separate interactive action and confirm it is gone:

```bash
az group delete --name "$x11_rebuild_group"
az group exists --name "$x11_rebuild_group"
```

For a published case commit, the normal permitted clone route in step 3 applies instead of the bundle.

After the course, verify **every participant** saved their code and proof outside the VMs. Inventory the shared group through ARM directly: `az resource list` returned an empty result despite existing resources in this tenant. Check the selected subscription, then delete the group as a separate interactive action:

```bash
x11_subscription_id=$(az account show --query id --output tsv)
az rest --method get --url "https://management.azure.com/subscriptions/${x11_subscription_id}/resourceGroups/agentic-engineering-2026/resources?api-version=2021-04-01" --query 'value[].{name:name,type:type}' --output table
```

```bash
az group delete --name agentic-engineering-2026
```

Read the name and confirm at the CLI prompt; do not use `--yes`. This removes its VMs, disks, IPs, NICs, VNets, and NSGs. Confirm `az group exists --name agentic-engineering-2026` returns `false`. Separately inventory and remove any optional per-person groups and any leftover rebuild groups. Once no longer needed, end use of the temporary course password; keep participants' saved work and public proof.

## Public preparation record

- Host baseline: Ubuntu 24.04 x64, `Standard_D2s_v6`, Sweden Central.
- Runtime policy: no automatic daily stop; manual deallocation after saved work and no active jobs.
- Resolved Ubuntu image version: `24.04.202610250` (`Canonical:ubuntu-24_04-lts:server`).
- Course source: `https://github.com/IT-HUSET/agentic-engineering-2026` (private). App/devcontainer baseline: `f0f3b76d12b9276668700784e05db3ebbaf94400`. The prepared local export includes X11 and is tagged `x11-course-20261116`; run `git rev-parse x11-course-20261116` on the VM for its exact commit. This export is not a published upstream commit and the prepared clone has no `origin`.
- Current four-VM tests: all 63 app tests pass on each machine. Personal sign-ins, full `check.py` GREEN and a model-driven task are participant checks after handoff.
- Pilot infrastructure checks passed: separate rebuild VM, container boundary probes, unapproved SSH-source rejection, HTTP 200 through the tunnel and deterministic tmux completion after SSH disconnect. Hetzner has not been provision-tested.

## Hetzner alternative

Use an organisation-owned project and Ubuntu 24.04 **x86** VMs, one per person. Restrict SSH by Cloud Firewall and supply `cloud-init.yaml` as user data. Create a non-root sudo `course` account per VM, then run `password-access.sh` as root with the URL-safe base64 encoding (without padding) of the locally generated SHA-512 crypt hash, matching the Azure helper's argument format and apply the same full dev-container/prebuild/reconnect/rebuild checks. The Azure Bicep file does not apply. Keep these VMs running while jobs need them; stop or delete them manually only after work is saved and no jobs are active. Powering off a rented server is not a promise that billing stops. Delete servers and retained disks/IPs after saving work.

## Sources

- [Azure Linux/Bicep](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-bicep), [cloud-init](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/using-cloud-init), [Run Command](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/run-command), [VM billing states](https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing).
- [Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/), [restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/), [NodeSource](https://github.com/nodesource/distributions), [Dev Container CLI](https://github.com/devcontainers/cli).
- [Hetzner server creation](https://docs.hetzner.com/cloud/servers/getting-started/creating-a-server/), [Cloud Firewalls](https://docs.hetzner.com/cloud/firewalls/overview/).
