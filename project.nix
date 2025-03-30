{
  name = "mavlink2cue";
  languages.python = {
    enable = true;
    callPackageFunction = import ./package.nix;
  };
}
