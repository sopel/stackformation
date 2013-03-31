requirements:
  pip.installed:
    - requirements: '/vagrant/requirements.txt'
    - require:
      - file: /vagrant/requirements.txt
      - pkg: git
      - pkg: pip

/vagrant/requirements.txt:
  file.exists:
    - name: '/vagrant/requirements.txt'
