# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Load default configuration.
_config = YAML.load(File.open(File.join(File.dirname(__FILE__),
                    'vagrantconfig.yaml'), File::RDONLY).read)

# Load local configuration (excluded from git).
begin
  _config.merge!(YAML.load(File.open(File.join(File.dirname(__FILE__),
                    'vagrantconfig_local.yaml'), File::RDONLY).read))
rescue Errno::ENOENT # No vagrantconfig_local.yaml found - not a problem.

end

# Store the _config into a global for later use.
CONF = _config

# Define the virtual machines.
Vagrant.configure("2") do |config|
  # The inital package update can take a long time,
  # increase vagrant's patience for long builds.
  # config.ssh.max_tries = 100
  # config.ssh.timeout   = 2400

  CONF['machines'].each do |machine_name, machine|
    config.vm.define machine_name do |this_machine|
      # Establish the vagrant box to use.
      if machine['box'] == 'default_box'
        this_machine.vm.box = CONF['default_box']
      else
        this_machine.vm.box = machine['box']
      end

      # Establish the vagrant box url for fetching the box.
      if machine['box'] == 'default_box_url'
        this_machine.vm.box_url = CONF['default_box_url']
      else
        this_machine.vm.box_url = machine['box_url']
      end

      # Give the VM a name in VirtualBox.
      this_machine.vm.provider 'virtualbox' do |vbox|
        vbox.name = "local.#{machine_name}.vm"
        this_machine.vm.hostname = machine_name

        # Include machine-specific ramsize.
        if machine.include?('ramsize')
          vbox.customize ["modifyvm", :id, "--memory", machine['ramsize'] ]
        end
      end

      # Vagrant network settings to be used.
      if machine.include?('network') && machine['network'].include?('type')
        case machine['network']['type']
        when 'private_network'
          if machine['network'].include?('ip')
            if machine['network']['ip'] == 'listed'
                this_machine.vm.network :private_network, ip: CONF['iplist'][machine_name]
            else
                this_machine.vm.network :private_network, ip: machine['network']['ip']
            end
          end
        when 'forwarded_port'
          if machine['network'].include?('guest') && machine['network'].include?('host')
            this_machine.vm.network :forwarded_port, guest: machine['network']['guest'], host: machine['network']['host']
          end
        when 'public_network'
          this_machine.vm.network :public_network
        else
        end
      end

      # Set up the synced folder within the VM.
      if machine.include?('synced_folder_local') && machine.include?('synced_folder_vm')
        if CONF['nfs'] == false || RUBY_PLATFORM =~ /mswin(32|64)/
          this_machine.vm.synced_folder machine['synced_folder_local'], machine['synced_folder_vm']
        else
          this_machine.vm.synced_folder machine['synced_folder_local'], machine['synced_folder_vm'], type: "nfs", mount_options: ["nolock"],nfs_udp: false
        end
      end

      # Include any provisioning options.
      if machine.include?('provision')
        case machine['provision']['provider']
        when 'puppet'
          this_machine.vm.provision :puppet do |puppet|
            if machine['provision'].include?('manifests_path')
              puppet.manifests_path = machine['provision']['manifests_path']
            end
            if machine['provision'].include?('module_path')
              puppet.module_path = machine['provision']['module_path']
            end
            if machine['provision'].include?('manifest_file')
              puppet.manifest_file = machine['provision']['manifest_file']
            end
            if machine['provision'].include?('facter')
              vars = Array.new
              machine['provision']['facter'].each do |var_name, var|
                vars << [var_name, var]
              end
              puppet.facter = vars
            end
          end
        when 'chef'
          #TODO add chef handling
        when 'shell'
          #TODO add shell script handling
        else
        end
      end

      # Turn on GUI if not headless.
      if CONF['gui'] == true
        this_machine.vm.boot_mode = :gui
      end
    end
  end
end

