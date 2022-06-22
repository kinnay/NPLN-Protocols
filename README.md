# NPLN-Protocols
This repo contains protobuf files for Nintendo's [NPLN services](https://github.com/kinnay/NintendoClients/wiki/NPLN-Servers) and IPS patches that disable TLS certificate verification.

`generate_patch.py` generates an IPS patch automatically, given the filename of the main NSO.

The protobuf files for NPLN version 0.20.x and 0.21.x were decompiled automatically from reflection data that is stored in the Monster Hunter Rise game.

Unfortunately, Nintendo enabled the [LITE_RUNTIME](https://developers.google.com/protocol-buffers/docs/proto#options) optimization in later versions, which means that the reflection data is no longer available. The protobuf files in the `latest` folder were decompiled manually using various sources.
