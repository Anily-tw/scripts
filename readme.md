# Anily scripts

This is main part of Anily infrastructure.

# Setting up
1. Clone scripts
```bash
$ git clone https://github.com/Anily-tw/scripts.git servers
$ cd ~/servers
```
2. Edit enviroment variables for preffered
```bash
$ nano ~/servers/set_enviroment.sh
```
3. Create python-venv for python scripts
```bash
$ sudo apt-get install python3-full
$ python3 -m venv script-venv
```
4. Install needed packages
```bash
$ source ~/script-venv/bin/activate
$ pip install requests mysql-connector-python nextcord watchdog
```
* `nextcord` and `watchdog` are needed if you are planning on using [FifoToDiscordBridge](https://github.com/Anime-pdf/FifoToDiscordBridge-tw)
5. Make Bash/Zsh use Anily enviroment by default
```bash
$ echo "source ~/servers/set_enviroment.sh" >> ~/.bashrc
$ echo "echo \"Loaded Anily enviroment\"" >> ~/.bashrc
$ echo "source ~/servers/script-venv/bin/activate" >> ~/.bashrc
$ echo "echo \"Loaded Python venv enviroment\"" >> ~/.bashrc
```

# Database
If you already have SQL dump, just import it and specify credentials in `set_enviroment.sh` and `ddrace/mysql.cfg`

If you **don't** have SQL dump, create new scheme, specify it in `set_enviroment.sh` and `ddrace/mysql.cfg`, and set last argument of `add_sqlserver` to `1`
Like this:
```
add_sqlserver r teeworlds record teeworlds "superPass" "localhost" "3306" 1
add_sqlserver w teeworlds record teeworlds "superPass" "localhost" "3306" 1
                ^ scheme name                                             ^ 1 to setup database
```
* Don't forget to set it back to `0` after first start

# Crontab
`crontab` file contains my crontab routine for restarting servers and uploading maps to repository.
To make map updating work, you need to change remote in `ddrace/maps` and configure git to store your credentials.

# Permissions
I use [web interface](https://github.com/Anily-tw/web) for uploading and updating maps. It's working on `apache2`, so `www-data` user does not have permissions to needed directories.
I create group `ddrace`:
```bash
$ sudo addgroup ddrace
```
Add there `$USER` and `www-data`:
```bash
$ sudo usermod -aG ddrace $USER
$ sudo usermod -aG ddrace www-data
```
Set `servers`'s owner to `$USER:ddrace`: 
```bash
$ sudo chown -R --changes "$USER:ddrace" -- servers
```
Give group permissions:
```bash
$ sudo chmod -R --changes "a-x,ug=rwX,o=rX" -- servers
```

# Servers
To run the servers themselves you need server executable placed at `ddrace` root, or clone ddnet next to `ddrace` directory and specify path in `set_enviroment.sh`, then use `ddrace/update.sh`.