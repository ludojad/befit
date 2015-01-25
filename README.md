# befit
Aby odpalić scheduler potrzebujemy 3 rzeczy:

Ad 1. Odpowiednio skonfigurowanego linux'a najlepiej jakieś ubuntu w chmurze: http://aws.amazon.com/ec2/
po zalogowaniu na naszej maszynie konfigurujemy:


  sudo apt-get update
  
  sudo apt-get install firefox

  sudo apt-get install python-pip
  
  sudo apt-get install xvfb
  
  sudo apt-get install xserver-xephyr
  
  sudo apt-get install tightvncserver
  

  sudo pip install pyvirtualdisplay
  
  sudo pip install selenium

  sudo apt-get install git


Clonujemy repo: 
  git clone https://github.com/ludojad/befit.git


Wchodzimy do katalogu
  cd befit


Ad 2. Wyedytować plik befitscheduler.properties, który zawiera sekcję

[app]
Kluczem jest nazwa dnia tygodnia po angielsku z dużej litery, wartością indexy tabeli w kalendarzu {tr} oraz {td}, domyslnie są tam wpisane zajęcia na popołudniowe bodypump. Jak chcemy dokładnie wiedzieć użyjmy zbadaj element w przeglądarce i sprawdźmy xpath danych zajęć. Powinien wyglądać np tak:

(Fitball we Wtorek)
  //*[@id="scheduler"]/div[1]/table/tbody/tr[2]/td[3]/div/p[2]

Niestety nie można dodać dwóch zajęć na ten sam dzień, jak chcesz zrób brancha ;)

[auth]

Tu podajemy dane logowania do befit (uważaj aby nie spushować swojego hasła do repo :P)

Ad 3. Uruchomić skrypt:

  python befitScheduler.py&

Wszystkie zdarzenia będą w pliku befitScheduler.log

Pozdro!
