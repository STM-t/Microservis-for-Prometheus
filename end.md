## Шаги развертывания

### 1. Настройка ВМ с помощью Vagrant

1. Устновка virt-manager:
  
   ```
   sudo dnf install virt-manager qemu-kvm libvirt-daemon-system libvirt-clients
   ```
   
2. Установка Vagrant:

   Если возникают проблемы с установкой Vagrant (плагинов или боксов) используйте VPN, например AdGuardVPN с бесплатной версией - https://adguardaccount.net
  
   ```
   sudo dnf install vagrant
   ```
   
3. Установка libvirt плагина для Vagrant:
  
   ```
   vagrant plugin install vagrant-libvirt
   ```
   
4. Установка AlmaLinux 9 box:
  
   ```
   vagrant box add generic/alma9
   ```
   
5. Запуск ВМ:
  
   ```
   cd vagrant
   vagrant up --provider=libvirt
   ```
   
### 2. Использование Ansible

1. Установка Ansible:
  
   ```
   sudo dnf install ansible
   ```
   
2. Генерация SSH ключа:
  
   ```
   ssh-keygen
   ```
   
3. Copy SSH key to the VM (password is "password"):
  
   ```
   ssh-copy-id stm@<VM_IP>
   ```

Пароль по умолчанию:_password_, он может быть изменен в Vagranfile
   
4. Запуск Ansible playbook:
  
   ```
   cd ansible
   ansible-playbook playbook.yml -K
   ```

После запуска ввести пароль _password_. Он указывается в Vagranfile
   

### 3. Проверка метрик

1. Подключение к ВМ:
  
   ```
   ssh stm@<VM_IP>
   ```
   
2. Метрики с микросервиса:
  
   ```
   curl http://localhost:8080
   ```
