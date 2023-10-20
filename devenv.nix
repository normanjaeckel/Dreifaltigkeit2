{ pkgs, ... }:

{
  packages = [
    pkgs.go-task
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
  };

  enterShell = ''
    pip install --upgrade --requirement requirements.txt
    pip freeze
  '';

  env.PGUSER = "dreifaltigkeit";

  services.postgres = {
    enable = true;
    initialDatabases = [
      { name = "dreifaltigkeit_parish"; }
      { name = "dreifaltigkeit_kindergarden"; }
    ];
    initdbArgs = [ "--username=dreifaltigkeit" "--locale=C" "--encoding=UTF8" ];
  };

  languages.elm.enable = true;

  # https://devenv.sh/basics/
  # env.GREET = "devenv";

  # https://devenv.sh/packages/
  # packages = [ pkgs.git pkgs.nixfmt ];

  # https://devenv.sh/scripts/
  # scripts.hello.exec = "echo hello from $GREET";

  # https://devenv.sh/languages/
  # languages.nix.enable = true;
  # languages.python = {
  #   enable = true;
  #   venv.enable = true;
  # };

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
