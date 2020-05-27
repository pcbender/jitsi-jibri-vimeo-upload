# jitsi-jibri-vimeo-upload
Record Jitsi meetings and upload them to vimeo.


edit your /etc/prosody/conf.avail/[yourhost].cfg.lua.

find app_secret = "xxxxx" and add these 2 lines:

allow_empty_token = false
enable_domain_verification = true

make a backup of /usr/share/jitsi-meet/prosody-plugins/token/util.lib.lua

download [util.lib.lua](https://raw.githubusercontent.com/pcbender/jitsi-jibri-vimeo-upload/master/util.lib.lua)
and replace the existing version

restart everything

Generate tokens that look like this:

For wild card rooms (any room)

Header:
{
	"typ":"JWT",
	"alg":"HS256"
}
Payload:
{
	"context":
	{
		"user":
		{
			"avatar":"a080d4168333c9d21a98be2d05a4a27f",
			"name":"someuser",
			"email":"someuser@gmail.com","id":"1"
		},
		"group":"beerfarts"
	},
	"aud":"jitsi",
	"iss":"somehost.com",
	"sub":"somehost.com",
	"room":"*",
	"exp":1622042066
}

This works:
https://somehost.com/beerfarts/curious?jwt=yourtoken

So does this:
https://somehost.com/beerfarts/bobo?jwt=yourtoken


For room specific token:

Header:

{
	"typ":"JWT",
	"alg":"HS256"
}

Payload:

{
	"context":
	{
		"user":
		{
			"avatar":"a080d4168333c9d21a98be2d05a4a27f",
			"name":"someuser",
			"email":"someuser@gmail.com",
			"id":"1"
		},
		"group":"beerfarts"
	},
	"aud":"jitsi",
	"iss":"somehost.com",
	"sub":"somehost.com",
	"room":"curious",
	"exp":1622046389
}


This works:
https://somehost.com/beerfarts/curious?jwt=yourNewtoken

This does not:
https://somehost.com/beerfarts/bobo?jwt=yourNewtoken

