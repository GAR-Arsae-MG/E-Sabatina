# Package
version       = "0.1.0"
author        = "Túlio Horta"
description   = "An AI tool made in order to allow government officials to identify contradictions \
                 within any two legal regulatory documents regarding the same subject."
license       = "Apache-2.0"
srcDir        = "src/nim"
installExt    = @["nim"]
bin           = @["builds/application"]

# Dependencies
requires "nim >= 2.0.8", "nimpy", "toktok"
