# File: setup_web_servers.pp

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data/web_static/releases/test':
  ensure  => directory,
  mode    => '0755',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  mode    => '0755',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => 'Hello, this is a test',
  mode    => '0644',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  force   => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

# Update Nginx configuration
file_line { 'nginx_alias':
  path    => '/etc/nginx/sites-available/default',
  line    => "location /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n",
  match   => 'server_name _;',
  ensure  => present,
  require => Package['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File_line['nginx_alias'],
}

