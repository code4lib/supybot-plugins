
## Zoia Deployment Details

The zoia IRC bot has changed hands a few times, but for many years has been under the supervision of @lbjay. The current deployment utilizes a supybot docker container and dropbox and is "hosted" on docker cloud (via an digitalocean droplet).

### Docker Images

* [lbjay/zoia-supybot](https://hub.docker.com/r/lbjay/zoia-supybot/) - this is based on another supybot image and just layers on the installation of dependencies + pip for installing the plugins' `requirements.txt` file.
* [janeczku/dropbox](https://hub.docker.com/r/janeczku/dropbox/) - provides a dropbox volume which is mounted into the supybot container to persist zoia's config and database files.

### Docker Cloud

The current zoia instance is running via [Docker Cloud](https://cloud.docker.com) and depends on only the two services (containers) mentioned above. 

### Re-deployment & plugin refreshing

Should zoia freeze up or fall over there is a Docker Cloud webhook for redeploying the supybot container. Ping @lbjay or @Wooble if you'd like to be a someone with awesome zoia webhook restart powers.

There is also a github webhook that will trigger a `git pull` within the running service on any pushes to the plugin repo.

