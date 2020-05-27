# jitsi-jibri-vimeo-upload
Record Jitsi meetings and upload them to vimeo.


edit your /etc/prosody/conf.avail/[yourhost].cfg.lua.

find app_secret = "xxxxx" and add these 2 lines:

allow_empty_token = false
enable_domain_verification = true


