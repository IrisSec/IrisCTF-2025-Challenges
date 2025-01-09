# SineFM - Radio Frequency

While browsing the radio spectrum, I found this interesting radio channel on 434.677 MHz with some intermittent activity. I'm having some trouble making sense of it, but I'm fairly certain that this is being used as some sort of communications channel. Can you find out what's being transmitted?

Note: while not required, it's highly recommended that you do RFoIP before you do this challenge. This challenge is a bit more difficult than RFoIP, and RFoIP will give you a good foundation for understanding this challenge.

`nc sinefm-f94347f3.radio.2025.irisc.tf 6531`

By: skat

Flag: `irisctf{grc_is_great_for_simple_narrowband_modulation}`

(This challenge is gated behind dotdotdot.)

# Notes About Setup

This isn't using kCTF. A single, central server with an organizer backdoor is needed for the live announcements feature of this challenge. kCTF could possibly be used to proxy traffic from the central radio server to the users in a fan-out configuration to alleviate network load on the radio server, but I don't think we anticipate enough people being able to reach this challenge for that to be necessary.

Remember to unzip `server/flag.complex.zip`. Unzipped, it'd be larger than GitHub allows us in a single file.
