# RFoIP - Radio Frequency

"I found this radio station on the Internet."

"Like they continuously stream songs on YouTube or something?"

"No, it's like... a radio station, and they play... Well, it's hard to explain."

`nc rfoip-620ac7b1.radio.2025.irisc.tf 6531`

By: skat

Flag: `irisctf{welcome_to_iris_radio_enjoy_surfing_the_waves}`

(This challenge is gated behind dotdotdot.)

# Notes About Setup

This isn't using kCTF. A single, central server with an organizer backdoor is needed for the live announcements feature of this challenge. kCTF could possibly be used to proxy traffic from the central radio server to the users in a fan-out configuration to alleviate network load on the radio server, but I don't think we anticipate enough people being able to reach this challenge for that to be necessary.
