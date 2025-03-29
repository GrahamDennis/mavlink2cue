{
  description = "mavlink2cue";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.11";
    rising-tide.url = "github:GrahamDennis/rising-tide";
  };

  outputs =
    {
      flake-utils,
      nixpkgs,
      rising-tide,
      self,
      ...
    }:
    let
      perSystemOutputs = flake-utils.lib.eachDefaultSystem (
        system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlays.default ];
          };
          project = rising-tide.lib.mkProject { inherit pkgs; } (import ./project.nix);
        in
        {
          inherit project;
          inherit (project) packages devShells hydraJobs;
        }
      );
      systemIndependentOutputs = rising-tide.lib.project.mkSystemIndependentOutputs {
        rootProjectBySystem = perSystemOutputs.project;
      };
    in
    perSystemOutputs // ({ inherit (systemIndependentOutputs) overlays pythonOverlays; });
}
