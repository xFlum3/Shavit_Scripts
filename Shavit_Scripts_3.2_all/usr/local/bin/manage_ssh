#!/bin/bash
# Ver: 2.0

display_menu() {
cat << _EOF_

manage_ssh.sh: Helper for managing ssh config

What would you like to do?

    1 - Create a private and public RSA SSH keys
    2 - Copy ${USER} public key to remote server
    3 - Fix .ssh local permission for ${USER}
    4 - Fix 'Agent admitted failure to sign using the key'
    5 - Examine 'AuthorizedKeyFile' in /etc/ssh/sshd_config
    0 - Exit
_EOF_
}

create_ssh() {
    ssh-keygen -t rsa -q -f ~/.ssh/id_rsa -P ""
    touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
    if [ $? -eq 0 ]
    then
        echo "Done!"
    fi
    sleep 1
}

copy_public() {
    clear
    tput cnorm
    echo "Enter remote server IP address: "
    read ip
    echo "Enter user name on remote server: "
    read username
    cat ~/.ssh/id_rsa.pub | ssh ${username}@${ip} 'cat >> ~/.ssh/authorized_keys'
    if [ $? -eq 0 ]
    then
        echo "Done!"
    fi
    sleep 1
}

fix_config() {
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/id_rsa
    touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
    if [ $? -eq 0 ]
    then
        echo "Done!"
    fi
    sleep 1
}

fix_agent_failure() {
    ssh-add
    if [ $? -eq 0 ]
    then
        echo "Done!"
    fi
    sleep 1
}

examine_ssh_config() {
    result=$(grep -E "^AuthorizedKeyFile=.ssh/authorized_keys" /etc/ssh/sshd_config | wc -l)
    if [ $result -eq 1 ]
    then
        echo "Test result: GOOD"
    else
        echo "Test result: BAD"
        echo "No 'AuthorizedKeyFile=.ssh/authorized_keys' in /etc/sshd_config"
        echo "Add\Uncomment line in /etc/sshd_config"
    fi
    sleep 1
}

clear
tput civis # Hide cursor
display_menu

read -n 1 -s choice;
	case $choice in
			1) create_ssh;;
			2) copy_public;;
			3) fix_config;;
            4) fix_agent_failure;;
            5) examine_ssh_config;;
            0) clear;echo $'\n'$"Exiting ... Goodbye!";sleep 2;tput cnorm;exit;;
            *) clear;echo "Not a valid choice: Exiting... Goodbye!";sleep 2;tput cnorm;exit;;
	esac
tput cnorm

