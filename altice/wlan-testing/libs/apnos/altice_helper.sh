#!/usr/bin/expect

set timeout -1

# Default values
set ssh_password "DustBunnyRoundup9#"
set sudo_password "lanforge"
set target_user "admin"
set target_ip "192.168.1.1"

# Flag to track if user commands are provided
set send_commands ""
set output ""
# Function to process command-line arguments
proc process_arguments {args} {
    global ssh_password sudo_password target_user target_ip send_commands

    set index 0
    foreach arg $args {
        if {[string match "-ssh_password*" $arg]} {
            set ssh_password [string range $arg 14 end]
        } elseif {[string match "-sudo_password*" $arg]} {
            set sudo_password [string range $arg 15 end]
        } elseif {[string match "-target_user*" $arg]} {
            set target_user [string range $arg 13 end]
        } elseif {[string match "-target_ip*" $arg]} {
            set target_ip [string range $arg 11 end]
        } elseif {[string match "-send_command*" $arg]} {
            set send_commands [string range $arg 15 end]
        }
        incr index
    }
}

# Function to spawn SSH command and enter interactive mode
proc spawn_ssh {} {
    global ssh_password sudo_password target_user target_ip send_commands

    spawn ssh -t lanforge@192.168.200.43 "sudo -S /home/lanforge/vrf_exec.bash eth1 ssh $target_user@$target_ip" && exit
    expect {
        "*$target_user*" {
            send "$ssh_password\r"
            exp_continue
        }
        "*lanforge*" {
            send "$sudo_password\r"
            exp_continue
        }
        "*GEN*" {
            send "cli\r"
            exp_continue
        }
        "*cli*" {
              if {$send_commands ne ""} {
                  send "$send_commands\r"
                  expect -timeout -1 "*cli*"
#                  expect -timeout -1 eof
                  send "quit\r"
                  expect -timeout -1 "*GEN*"
                  send "exit\r"
                  expect -timeout -1 "43 closed*"
              } else {
                  send "quit\r"
                  expect -timeout -1 "*GEN*"
                  send "exit\r"
                  expect -timeout -1 "*43 closed*"
              }

        }  
    }
}


# Process command-line arguments
process_arguments $argv

# Run the spawn_ssh function
spawn_ssh
#pid=$(pgrep -f "ssh -t lanforge@192.168.200.43")
#kill "$pid"

#if ($send_commands ne "") {
#    send "quit\r"
#    expect -timeout -1 "*GEN*"
#    send "exit\r"
#    expect -timeout -1 "43 closed*"
#}
