#!/bin/sh
# This script runs a command specified in the Docker container "project-manager"

# A variable "command" is defined that is set equal to all command-line arguments
# (denoted by the asterisk "*")
# or, if no arguments are provided, it is set to "sh".
command="${*:-sh}";

# The command is executed in the Docker container "project-manager"
# The "-it" option is used to connect to the container in interactive mode, and the "-w" option
# is used to set the working directory in the container.
if test "$command" = "sh"; then
  echo "\n Attaching shell, to leave, type "exit" \n";
fi

docker exec -it project-manager ${command};

echo "\n Closing Project Manager API!";
