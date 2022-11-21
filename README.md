# NPLN-Protocols
This repo contains protobuf files for Nintendo's [NPLN services](https://github.com/kinnay/NintendoClients/wiki/NPLN-Servers).

The protobuf files for NPLN version 0.20.x and 0.21.x were decompiled automatically from reflection data that is stored in the Monster Hunter Rise game.

Because Nintendo enabled the [LITE_RUNTIME](https://developers.google.com/protocol-buffers/docs/proto#options) optimization in later versions, this reflection data is no longer available. The protobuf files in the `latest` folder were decompiled manually using various sources.

`generate_patch.py` generates an IPS patch that disables TLS certificate verification, given the filename of the main NSO. This is useful if you want to capture traffic or write your own NPLN servers.
