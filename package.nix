# python packages context
{ lib, pythonPackages }:
pythonPackages.buildPythonPackage {
  name = "mavlink2cue";
  pyproject = true;

  # Minimise rebuilds due to changes to files that don't impact the build
  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./pyproject.toml
      ./src
      ./tests
    ];
  };

  dependencies = with pythonPackages; [
    pymavlink
    click
    attrs
  ];
  dev-dependencies = with pythonPackages; [
    pytest
  ];
  build-system = with pythonPackages; [ hatchling ];

  nativeCheckInputs = with pythonPackages; [ pytestCheckHook ];
  pytestFlagsArray = [ "tests" ];
}
