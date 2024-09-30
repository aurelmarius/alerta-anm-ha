# Atentionare meteorologica ANM Home Assistant

1. Despre

Integrarea foloseste API ANM de pe site-ul https://www.meteoromania.ro/ pentru a prelua atentionarile meteorologice si le stocheaza in senzorul sensor.avertizari_meteo_anm. Datele sunt stocate ca si atribut al senzorului.

Exemplu:

	- judet: GL
	culoare: '1'
	fenomene_vizate: intensificări ale vântului;
	data_expirarii: 2024-10-02T10:00
	data_aparitiei: 2024-09-30T10:00
	intervalul: 01 octombrie, ora 10 – 02 octombrie, ora 10;

Atributul culoare: 1 - cod Galben, 2 - cod Portocaliu, 3 - cod Rosu


2. Instalare
   - Descarcati acest repository in format zip.
   - Copiati folderul alerta_anm in folderul /config/custom_components din Home Assistant
   - Reporniti Home Assistant
   - Adaugati integrarea din Settings > Devices & Services > Integrations > Add Integration
   - Setati durata in minute pentru preluarea datelor de pe site-ul ANM (Implicit 10 minute)
  
3. Pentru a crea un senzor cu informatii pentru regiunea dorita, puteti folosi exemplu_senzor.yaml inlocuind indicativul judetului.

Exemplu:

	{% set judet = 'B' %} - Bucuresti
 	{% set judet = 'GL' %} - Galati
  	{% set judet = 'IS' %} - Iasi
   	etc...

 Este necesar sa inlocuiti indicativul in toate atributele senzorului.

 4. Automatizare:

```
alias: Avertizare ANM
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.avertizare_meteo_bucuresti
    to: alerta
    for:
      hours: 0
      minutes: 0
      seconds: 5
condition: []
action:
  - action: notify.mobile_app_xxxxxx
    metadata: {}
    data:
      title: Avertizare Meteo
      message: >-
        {{ state_attr('sensor.avertizare_meteo_bucuresti', 'mesaj') }}.
        Fenomene: {{ state_attr('sensor.avertizare_meteo_bucuresti',
        'fenomene_vizate') }}
mode: single
```

![Preview](https://raw.githubusercontent.com/aurelmarius/alerta-anm-ha/refs/heads/main/.github/img/IMG_PREV.png)

