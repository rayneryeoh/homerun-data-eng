# Configuration

Copy `local.example.json` to `local.json` on each laptop and fill in the local paths. The local file is ignored by Git.

The example is a configuration template, not a runnable pipeline configuration. Set the network dataset path, travel mode and school source on the licensed laptop. Record the actual coordinate reference system, input versions and network settings in each export manifest.

Service-area thresholds are 5, 10 and 15 minutes. The proposed counts are cumulative: the 10-minute count includes schools counted within 5 minutes. Confirm this convention against the existing ArcPy workflow before generating production outputs.

Resolve relative paths from the repository root, independently of the current working directory.

