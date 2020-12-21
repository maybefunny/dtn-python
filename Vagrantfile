# vi: set ft=ruby :

n = 3

Vagrant.configure("2") do |config|
  n.times do |i|
    config.vm.define "app-#{i+1}" do |app|
      app.vm.box = 'ubuntu/trusty64'
      app.vm.hostname = "app-#{i+1}"
      app.vm.network :private_network, ip: "192.168.10.#{10+i+1}"
    end
  end
end
