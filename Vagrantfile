Vagrant.configure("2") do |config|
  (1..3).each do |i|
    config.vm.define "sftp_#{i}" do |sftp|
      sftp.vm.box = "ubuntu/bionic64"
      sftp.vm.hostname = "sftp-#{i}"
      sftp.vm.network "private_network", ip: "10.0.0.20#{i}"

      sftp.vm.provider "virtualbox" do |vb|
        vb.name = "sftp-#{i}"
        vb.memory = "1024"
        vb.cpus = 2
      end
      sftp.vm.provision "file", source: "scripts", destination: "/tmp/scripts/"
      sftp.vm.provision "shell", path: "provision/provision.sh"
  
    end
  end
end
