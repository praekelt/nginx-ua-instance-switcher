[program:${name}.fcgi]
command=${buildout:bin-directory}/${control-script} runfcgi host=${host} port=${port} protocol=fcgi daemonize=False
user=${user}
stdout_logfile=${log}
redirect_stderr=true
stopsignal=QUIT
environment=PYTHON_EGG_CACHE='/var/www/.python-eggs'
