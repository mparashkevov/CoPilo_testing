-- Begin document --
1. Login commands (by landscape / region)
Use the correct API endpoint, org and space for each region.
bash

# Log into EU10 landscape using SSO, set org 'saceu10' and space 'sac'
cf login -a https://api.<org>.eu10.hana.ondemand.com -o saceu10 -s sac --sso
# Comment: Opens SSO flow and targets the EU10 API endpoint.

# Log into US10 landscape using SSO
cf login -a https://api.<org>.us10.hana.ondemand.com -o sacus10 -s sac --sso
# Comment: Use for US10 region.

# Log into BR10 landscape using SSO
cf login -a https://api.<org>.br10.hana.ondemand.com -o sacbr10 -s sac --sso
# Comment: Use for Brazil region.

# Log into JP10 landscape using SSO
cf login -a https://api.<org>.jp10.hana.ondemand.com -o sacjp10 -s sac --sso
# Comment: Use for Japan region.

# Log into AP10 / AP11 landscapes using SSO
cf login -a https://api.<org>.ap10.hana.ondemand.com -o sacap10 -s sac --sso
cf login -a https://api.<org>.ap11.hana.ondemand.com -o sacap11 -s sac --sso
# Comment: Use appropriate AP region commands.

# Log into EU20 / EU11 landscapes
cf login -a https://api.<org>.eu20.hana.ondemand.com -o saceu20 -s sac --sso
cf login -a https://api.<org>.eu11.hana.ondemand.com -o saceu11 -s sac --sso
# Comment: EU region variations.

# Specialized login (example for sapml-sti)
cf login -a https://api.<org>.eu1.hana.ondemand.com -o <org>_sapml-sti -s production-sti
# Comment: Target special org/space.

# Login to CA10 (example without --sso)
cf login -a https://api.<org>.ca10.hana.ondemand.com -o saceu10 -s sac
# Comment: Interactive login if SSO not used.

# China region (cn40) with SSO
cf login -a https://api.<org>.cn40.platform.sapcloud.cn -o <org> -s production --sso
# Comment: China cloud endpoint uses different domain.

# Internal endpoint (example)
cf login -a https://api.<org>.int.sap.hana.ondemand.com
# Comment: Internal API endpoint; may require internal network access.
2. Inspecting apps / services
Get summary of an app: instances, state, memory, routes, and instance details.
bash

# Show app summary and instances
cf app <service_name>
# Comment: Displays app summary, instance counts and state.

# Show recent logs (non-continuous)
cf logs <service_name> --recent
# Comment: Fetches recent logs after restart or for troubleshooting.

# Tail logs in real time
cf logs <service_name>
# Comment: Live log streaming; press Ctrl+C to stop.
Reference for services:
Internal service directory (example): https://github.wdf.sap.corp/orca/boc_service_directory/tree/master/services
3. Restarting instances / targeted restarts (one-by-one)
Use targeted instance restarts to avoid full downtime.
bash

# Restart a specific instance index (index starts at 0)
cf restart-app-instance <APP> <INDEX>
# Example: restart instance 0 of 'daservice'
cf restart-app-instance daservice 0
# Comment: Restarts only instance 0; useful for rolling maintenance.

# Example: restart instance 0 of 'dwaas-core'
cf restart-app-instance dwaas-core 0
# Comment: Targeted restart for dwaas-core instance 0.

# Example: restart contentmanager instance 0
cf restart-app-instance contentmanager 0
# Comment: CN region example.

# After each restart, confirm health before proceeding:
cf app <APP>
# Comment: Wait until instance shows RUNNING/healthy before restarting next.
4. Full app restart and rolling strategy
bash

# Restart the whole app (all instances)
cf restart <APP>
# Comment: Full restart; may cause short downtime.

# Restart the app using Cloud Foundry's rolling strategy to minimize downtime
cf restart <APP> --strategy rolling
# Example:
cf restart APP-NAME --strategy rolling
# Comment: Replaces instances gradually according to CF's rolling implementation.
5. Health checks and restage (v3 health check example for approuter)
bash

# Set v3 HTTP health-check for 'approuter' with a custom endpoint and increased timeout
cf v3-set-health-check approuter http --endpoint /health --invocation-timeout 180
# Comment: Configures HTTP /health path; increases invocation timeout to 180s.

# Restage the app to rebuild droplet and apply new health-check or env changes
cf restage approuter
# Comment: Restage triggers a rebuild and restart with updated config.
6. Rename, route unmap/map, delete (blue/green cleanup)
bash

# Rename the old app to a temporary name
cf rename nlq-indexer-venerable nlq-indexer-venerable-tobedeleted
# Comment: Renames old app to free original name/hostname.

# Unmap the route from the old app to free hostname
cf unmap-route nlq-indexer-venerable-tobedeleted cfapps.ap11.hana.ondemand.com --hostname nlq-indexer-sac-sacap11
# Comment: Removes the mapping, freeing the hostname.

# Map the route to the new app
cf map-route nlq-indexer cfapps.ap11.hana.ondemand.com --hostname nlq-indexer-sac-sacap11
# Comment: Binds the hostname to the new app.

# Delete the old/venerable app after verifying new app receives traffic
cf delete nlq-indexer-venerable-tobedeleted
# Comment: Deletes the old application; confirm before running.
7. Generic restarts and other examples
bash

# Generic whole-app restart
cf restart <service_name>
# Comment: Restarts entire app.

# Targeted restart using restart-app-instance
cf restart-app-instance <service_name> 0
# Comment: Restarts a specific instance.

# Rename an app (example)
cf rename old-app-name new-app-name
# Comment: Useful during version swaps.

# Show routes for the targeted org/space
cf routes
# Comment: Lists all routes; useful to verify mapping.
8. Operational checklist and tips
After any restart:
cf app <APP> to check instances and state.
cf logs <APP> --recent to inspect startup logs.
For rolling maintenance:
Restart one instance, wait until it's RUNNING and healthy, then continue.
For route changes:
Verify DNS and TLS after remapping routes.
For SSO:
SSO sessions may expire; re-run login when required.
For destructive actions:
Add confirmations or dry-run checks in scripts.
Appendix: Manual rolling-restart procedure
Login to target region:
cf login -a <API_ENDPOINT> -o <org> -s <space> --sso
Check app and instance count:
cf app <APP>
For i in 0..N-1 (where N is instance count), do:
cf restart-app-instance <APP> <i>
Wait until the instance is RUNNING: poll cf app <APP>
Confirm logs: cf logs <APP> --recent
When all instances are healthy, finish.
9. Other useful CF CLI commands (grouped by logic)
General / info
bash

# Show CF CLI version
cf --version
# Comment: Verify binary/version.

# Show current targeted API, org and space
cf target
# Comment: Confirms current target.

# List orgs you can access
cf orgs
# Comment: See accessible organizations.

# List spaces in the current org
cf spaces
# Comment: Discover spaces within targeted org.

# Show available commands and help (or for a specific command)
cf help
cf help <command>
# Comment: Use to check syntax and options.
Apps lifecycle (push, start, stop, restart, restage, scale)
bash

# Push a new app or update using local dir or manifest
cf push <APP> -p PATH_TO_APP -b BUILDPACK -m 512M -i 2
# Comment: Pushes app; prefer manifest.yml for consistent config.

# Start an app
cf start <APP>
# Comment: Starts app instances.

# Stop an app
cf stop <APP>
# Comment: Stops all instances.

# Restage an app (rebuild droplet)
cf restage <APP>
# Comment: Rebuilds droplet with current buildpack/env.

# Scale app: change instance count, memory, and disk
cf scale <APP> -i 3 -m 1G -k 2G
# Comment: Sets instances/memory/disk quotas.
App configuration and environment
bash

# Set an environment variable for the app
cf set-env <APP> KEY VALUE
# Comment: Persists env var; may require restage.

# Unset an environment variable
cf unset-env <APP> KEY
# Comment: Removes env var.

# Show environment variables and VCAP_* info
cf env <APP>
# Comment: View env and bound services.
Routes, domains, and networking
bash

# List routes in targeted org/space
cf routes
# Comment: Audit route mappings.

# Create a route (org and domain must exist)
cf create-route <ORG> <DOMAIN> --hostname <HOSTNAME>
# Comment: Creates a route to be mapped to an app.

# Map a route to an app
cf map-route <APP> <DOMAIN> --hostname <HOSTNAME>
# Comment: Bind hostname+domain to app.

# Unmap a route from an app
cf unmap-route <APP> <DOMAIN> --hostname <HOSTNAME>
# Comment: Remove mapping.

# Delete a route (with confirmation skip)
cf delete-route <DOMAIN> --hostname <HOSTNAME> -f
# Comment: Use -f to skip confirmation in scripts (careful).
Service marketplace & service instances
bash

# Show marketplace services and plans
cf marketplace
# Comment: Lists service offerings/plans.

# Create a service instance
cf create-service <SERVICE> <PLAN> <SERVICE_INSTANCE_NAME>
# Comment: Provisions service broker instance.

# List service instances in the space
cf services
# Comment: Lists provisioned service instances.

# Show details for a service instance
cf service <SERVICE_INSTANCE_NAME>
# Comment: Shows status and dashboard URL.

# Delete a service instance
cf delete-service <SERVICE_INSTANCE_NAME> -f
# Comment: Deletes instance; -f skips confirmation.

# Bind/unbind a service instance to/from an app
cf bind-service <APP> <SERVICE_INSTANCE_NAME>
cf unbind-service <APP> <SERVICE_INSTANCE_NAME>
# Comment: Creates or removes credentials in VCAP_SERVICES; restage may be required.

# Create a service key (non-app clients)
cf create-service-key <SERVICE_INSTANCE_NAME> <KEY_NAME>
# Comment: Generates credentials accessible with cf service-key.

# List service keys
cf service-keys <SERVICE_INSTANCE_NAME>
# Comment: Shows service keys for that instance.

# Retrieve a specific service key
cf service-key <SERVICE_INSTANCE_NAME> <KEY_NAME>
# Comment: Prints JSON credentials for the key.
App logs and files
bash

# Tail logs in real time
cf logs <APP>
# Comment: Live logs; press Ctrl+C to stop.

# Show recent logs only
cf logs <APP> --recent
# Comment: Useful to inspect startup messages.

# Retrieve files from app container filesystem
cf files <APP> <INSTANCE_INDEX> PATH
# Example:
cf files <APP> 0 /tmp/app.log
# Comment: Retrieve a file from the app instance.
SSH & remote access
bash

# Enable SSH for the app (org/space and app-level must allow it)
cf enable-ssh <APP>
# Comment: Enable container SSH for debugging.

# Disable SSH for the app
cf disable-ssh <APP>
# Comment: Disable SSH access.

# SSH into an app container (requires enable-ssh)
cf ssh <APP>
# Comment: Opens remote shell into app container if supported.
Tasks (one-off jobs)
bash

# Run a one-off task in the app (async)
cf run-task <APP> "<COMMAND>" --name <TASK_NAME> -k 512M
# Comment: Runs a one-off command in the app's environment.

# List tasks for an app
cf tasks <APP>
# Comment: Show status of tasks.

# Get task status
cf task <APP> <TASK_ID>
# Comment: Shows task details and exit code.
Application manifests & blue/green deployment helpers
bash

# Push using a manifest (recommended)
cf push -f manifest.yml
# Comment: Use manifest to maintain consistent config.

# Rename an app (helpful for blue/green)
cf rename <OLD_APP_NAME> <NEW_APP_NAME>
# Comment: Useful in route swap patterns.

# Blue/green route switch (map new, unmap old)
cf map-route <NEW_APP> <DOMAIN> --hostname <HOSTNAME>
cf unmap-route <OLD_APP> <DOMAIN> --hostname <HOSTNAME>
# Comment: Redirect traffic with minimal downtime.
Buildpacks, stacks, and droplets
bash

# List available buildpacks
cf buildpacks
# Comment: Shows platform buildpacks.

# Set a specific buildpack on push
cf push <APP> -b https://github.com/.../buildpack.git
# Comment: Override default buildpack.

# List app droplets (v3 endpoints or plugins may be required)
# Use cf v3 commands or cf curl /v3/apps for advanced droplet info.
Organization & space management (admin/developer)
bash

# Create an org (admin only)
cf create-org <ORG>
# Comment: Requires admin privileges.

# Create a space in the targeted org
cf create-space <SPACE>
# Comment: Create new space.

# Assign a user role in org/space
cf set-org-role <USER> <ORG> OrgManager
cf set-space-role <USER> <ORG> <SPACE> SpaceDeveloper
# Comment: Manage user roles (admin privileges required).
Diagnostics & troubleshooting
bash

# Show app health & instance states
cf app <APP>
# Comment: Primary command to get current state and crash counts.

# List recent events (if supported)
cf events
# Comment: Shows platform-level events in targeted org/space.

# Query v3 API for detailed info (advanced)
# Example: cf curl /v3/apps/<app-guid>
# Comment: Use cf curl for advanced diagnostics via CF API.
Safety flags & automation helpers
bash

# Skip confirmation prompts in scripts (use with care)
cf delete <APP> -f
# Comment: Non-interactive; verify before use.

# Prepare app without starting (useful in pipelines)
cf push <APP> -f manifest.yml --no-start
# Comment: Useful for deploy pipelines that separate push and start steps.
Final notes
Replace placeholders with real values before running commands.
Add monitoring/alerts to observe app health during maintenance.
For automation, implement robust checks: verify target, check app state, log outputs, and add retries/timeouts.
If you want, I can:
Replace the remaining placeholders (<org>, <APP>, etc.) with concrete values you provide and deliver the filled .md file; or
Produce a version that also removes angle brackets from other placeholders (e.g., org, APP) if you prefer. Which would you like?