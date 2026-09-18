Ce petit projet vise à créer un programme permettant de créer et modifier facilement des évènements à travers le format ICS. Il se veut le plus complet possible. Les explications en ligne sur ce format sont illisibles donc certaines explications seront données ici. La documentation complète se trouve en ligne dans la [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545.txt) d'où seront tirés les sections données dans ce document.
Un fichier ICS représente un icalendar composé de composantes qui ont chacune leurs propriétés spécifiques, que l'on peut compléter par des paramètres de propriétés.

Un ical possède des propriétés de base qui ne sont pas associées à une composante mais au calendrier global (3.7):
- CALSCALE: permet de définir le type de calendrier (grégorien par défaut) (pas réussi à trouver les autres valeurs)
- METHOD (pas compris)
- PROID (OBLIGATOIRE): identifiant du calendrier
- VERSION (OBLIGATOIRE): version des normes ical

### Composantes

Une composante est un bloc contenu dans un calendrier, il est toujours nommé en majuscules et précédé d'un "V". Il en existe 5 différents:
- alarm: représente une alarme qui peut se déclencher sur le calendrier
- event: représente un évènement (composante majoritaire d'un calendrier)
- freebusy: représente les périodes durant lesquelles un utilisateur est libre ou non
- journal: représente un bloc contenant des informations sur une période de temps spécidique
- timezone: représente toutes les informations concernant le fuseau horaire du calendrier ou d'une composante
- todo: représente une tâche à réaliser

Une composante est générée comme suit
```
BEGIN:V<composante>
<properties>
END:V<composante>
```

### Propriétés
Les tableaux ci-dessous représente les propriétés possibles pour chaque composante (? indique que l'élément est présent au plus une fois et + au moins une fois)

Propriétés de description des composantes
|           |ATTACHEMENT|CATEGORIES|CLASS|COMMENT|DESCRIPTION|GEO|LOCATION|PERCENT-COMPLETE|PRIORITY|RESOURCES|STATUS|SUMMARY|
|:-         |:-:        |:-:       |:-:  |:-:    |:-:        |:-:|:-:     |:-:             |:-:     |:-:      |:-:   |:-:    |
|alarm      |[0-9]+     |Non       |Non  |Non    |?          |Non|Non     |Non             |Non     |Non      |Non   |Oui    |
|event      |Non        |Oui       |Oui  |[0-9]+ |?          |?  |?       |Non             |?       |?        |?     |Oui    |
|freebusy   |[0-9]+     |Non       |Non  |[0-9]+ |?          |Non|Non     |Non             |Non     |Non      |Non   |Non    |
|journal    |[0-9]+     |Oui       |Oui  |[0-9]+ |[0-9]+     |Non|Non     |Non             |Non     |Non      |?     |Non    |
|timezone   |Non        |Non       |Non  |Non    |?          |Non|Non     |Non             |Non     |Non      |Non   |Oui    |
|todo       |[0-9]+     |Oui       |Oui  |[0-9]+ |?          |?  |?       |?               |?       |?        |?     |Oui    |

Propriétés de datetime des composantes
|           |COMPLETED |DTEND|DUE|DTSTART|DURATION|FREEBUSY|TRANSP|
|:-         |:-:       |:-:  |:-:|:-:    |:-:     |:-:     |:-:   |
|alarm      |Non       |Non  |Non|Non    |Oui     |Non     |Non   |
|event      |Non       |Oui  |Non|?      |Oui     |Non     |?     |
|freebusy   |Non       |Oui  |Non|?      |Non     |Oui     |Non   |
|journal    |Non       |Non  |Non|Non    |Non     |Non     |Non   |
|timezone   |Non       |Non  |Non|Non    |Non     |Non     |Non   |
|todo       |Oui       |Non  |?  |?      |Oui     |Non     |Non   |


Propriétés de fuseau horaire des composantes
|           |TZID   |TZNAME|TZOFFSETFROM |TZOFFSETTO|TZURL  |
|:-         |:-:    |:-:   |:-:          |:-:       |:-:    |
|alarm      |Non    |      |Non          |          |Non    |
|event      |Non    |      |Non          |          |Non    |
|freebusy   |Non    |      |Non          |          |Non    |
|journal    |Non    |      |Non          |          |Non    |
|timezone   |Oui    |      |Oui          |          |Oui    |
|todo       |Non    |      |Non          |          |Non    |

Propriétés de relation des composantes:
|           |ATTENDEE|CONTACT|ORGANIZER|RECURRENCE-ID|RELATED-TO|URL|UID|
|:-         |:-:     |:-:    |:-:      |:-:          |:-:       |:-:|:-:|
|alarm      |Oui     |Non    |Non      |Non          |Non       |Non|Non|
|event      |Oui     |Oui    |Oui      |Oui          |Oui       |?  |Oui|
|freebusy   |Oui     |Oui    |Oui      |Non          |Non       |?  |Oui|
|journal    |Oui     |Oui    |Oui      |Oui          |Oui       |?  |Oui|
|timezone   |Oui     |Non    |Non      |Non          |Non       |Non|Non|
|todo       |Oui     |Oui    |Oui      |Oui          |Oui       |?  |Oui|

Propriétés des composantes récurrentes:
|           |EXDATE |RDATE|RRULE|
|:-         |:-:    |:-:  |:-:  |
|alarm      |Non    |Non  |Non  |
|event      |Oui    |Oui  |Oui  |
|freebusy   |Non    |Non  |Non  |
|journal    |Oui    |Oui  |Oui  |
|timezone   |Non    |Oui\*|Oui\*|
|todo       |Oui    |Oui  |Oui  |

Propriétés de l'alarme
|     |ACTION|REPEAT|TRIGGER|
|:-   |:-:   |:-:   |:-:    |
|alarm|1     |Oui   |Oui    |


Description des différentes propriétés:
- propriétés de description:
    * ATTACH: permet d'associer un document à une composante (peut être présent plus d'une fois sauf pour un audio)
    * CATEGORIES: les catégories sont séparées par des ","
    * CLASS: plus ou moins comme categories, avec comme valeur PUBLIC (par défaut), PRIVATE, CONFIDENTIAL ou ce qu'on veut, une valeur unique
    * COMMENT: ajout de texte optionnel
    * DESCRIPTION: description détaillé de la composante (peut être présente plus d'une fois pour un journal)
    * GEO: position géographique de la composante sous la forme "GEO:\<float lat>;\<float long>
    * LOCATION: lieu de la composante, doit suivre une des RFC suivantes: [4516](https://datatracker.ietf.org/doc/html/rfc4516), [2392](https://www.rfc-editor.org/info/rfc2392/), [2426](https://www.rfc-editor.org/info/rfc2426/)
    * PERCENT-COMPLETE: nombre entier entre 0 et 100 qui indique le niveau d'avancée d'une tâche
    * PRIORITY: nombre entier entre 0 et 9 indiquant l'importance de la composante (0 indique une priorité indéfinie, 1 la priorité maximale et 9 la priorité minimale); il est aussi possible d'avoir les valeurs HIGH (1-4), MEDIUM (5) ou LOW (6 à 9)
    * RESOURCES: éléments qui pourraient être utile pour la composante (comme des outils physiques ou numériques par exemple)
        - ROOM
        - UNKNOWN
        - other: on peut mettre ce que l'on veut en réalité
    * STATUS: indique un status général ou une confirmation d'une composante
        - pour un event: TENTATIVE, CONFIRMED ou CANCELED
        - pour un todo: NEEDS-ACTION, COMPLETED, IN-PROCESS ou CANCELLED
        - pour un journal: DRAFT, FINAL ou CANCELLED
    * SUMMARY: résumé de la description
- propriétés temporelles:
    * COMPLETED: indique la datetime à laquelle la tâche a été achevé, la valeur doit être une datetime au format UTC
    * DTEND: indique la fin temporelle (au format UTC) d'une composante, doit être obligatoirement complétée d'un DTSTART dont le type de la valeur est identique et la valeur postérieure à cette dernière
    * DUE: indique la deadline d'une tâche
    * DTSTART: indique la date à laquelle la composante commence, valeur au format UTC
    * DURATION
    * FREEBUSY: à voir plus tard (3.8.2.6)
    * TRANSP: indique si l'évènement doit bloquer ou non son créneau sur le calendrier, avec comme valeur OPAQUE (valeur par défaut) pour oui ou TRANSPARENT pour non  
- propriétés de timezone:
    * TZID:  identifiant de la timezone selon la TWDB
    * TZNAME: nom du fuseau horaire utilisé
    * TZOFFSETTO: indique le décalage horaire par rapport à UTC+0 sous la forme "TZOFFSETTO:(+|-)?hhmm"
    * TZURL: indique l'url correspondant au fuseau horaire utilisé
- propriétés de relations:
    * ATTENDEE: liste des personnes présentes pour cette composante 
    * CONTACT: contact privilégiée pour la composante
    * ORGANIZER: personne qui a créé cette composante
    * RECURRENCE-ID (3.8.4.4): pas compris
    * RELATED-TO: permet d'indiquer un lien avec une autre composante du calendrier
    * URL: permet d'ajouter un lien à la composante
    * UID: identifiant unique d'une composante
- propriétés des composantes récurrentes:
    * EXDATE: permet d'ajouter des exceptions de date(time) aux éléments récurrents
    * RDATE: à comprendre (3.8.5.2)
    * RRULE (3.8.5.3): permet d'ajouter une règle de récurrence pour une composante récurrente (ex: tous les jours, premier jour une semaine sur deux...)
- propriétés d'alarme:
    * ACTION: indique une action à réaliser lorsque l'alarme sonne (simple texte brut, ne sera pas exécuté)
    * REPEAT: indique le nombre de fois que l'alarme doit se répéter (à compléter par DURATION si utilisé)
    * TRIGGER: indique quand l'alarme doit sonner (datetime ou période relative à une autre composante)


### Types de valeurs
Chaque propriété prend une valeur, voire plusieurs pour certaines. Ces valeurs peuvent être des types suivants (les noms en majuscules sont ceux qui doivent être explicités):
- BINARY: représentation binaire d'une valeur --> `VALUE=BINARY:<BINARY VALUE>`, l'encodage doit systématiquement être explicité sous la forme `ENCODING=<encoding>`
- booléen: TRUE ou FALSE
- CAL-ADDRESS: lien d'un calendrier numérique
- date: indique l'annnée, le mois, le mois et le jour (format saxon MM-DD) ou les 3 à la fois (YYYYMMDD)
- dur-X (3.3.6): représentation d'une durée (allant de la semaine à la seconde), avec X:
    * time: heure + minute + seconde
    * week
    * day
    * hour
    * minute
    * second
- nombre flottant: la virgule doit être un point
- nombre entier
- PERIOD (3.3.9): période de temps sous la forme "\<start\>/\<end\>" ou "\<start>/\<duration>"
- RECUR: règle de récurrence d'un évènement (trop long pour être développé ici (3.3.10))
- texte: du texte basique
- TIME: indique une heure précise de la journée sous la forme ([00-23]? [00-59]? [00-60]? [time-utc (Z)]?)
- uri: lien numérique
- utf offset: indique un décalage avec le fuseau horaire UTC sous la forme (+|-)?[0-9]{4}

### Paramètres de propriétés
Chaque propriété peut être complétée par des paramètres afin d'ajouter des informations aux différentes composantes. Les tableaux ci-dessous représentent les paramètres possibles pour chaque propriété. Pour des raisons de lisibilité, seules les colonnes et lignes qui contiennent au moins une case différente de Non seront conservées

|           |ATTACHEMENT|CATEGORIES|COMMENT|DESCRIPTION|LOCATION|RESOURCES|SUMMARY|
|:-         |:-:        |:-:       |:-:    |:-:        |:-:     |:-:      |:-:    |
|ALTREP     |Non        |Non       |?      |?          |?       |?        |?      |
|FMTTYPE    |?          |Non       |Non    |Non        |Non     |Non      |Non    |
|LANGUAGE   |Non        |?         |?      |?          |?       |?        |?      |

|           |DTEND|DUE|DTSTART|FREEBUSY|
|:-         |:-:  |:-:|:-:    |:-:     |
|FBTYPE     |Non  |Non|Non    |?       |
|TZID       |?    |?  |?      |Non     |
|VALUE      |Non  |?  |?      |Non     |

|           |TZID   |TZNAME|TZOFFSETFROM |TZOFFSETTO|TZURL  |
|:-         |:-:    |:-:   |:-:          |:-:       |:-:    |
|LANGUAGE   |Non    |?     |Non          |Non       |Non    |

|           |ATTENDEE|CONTACT|ORGANIZER|RECURRENCE-ID|RELATED-TO|
|:-         |:-:     |:-:    |:-:      |:-:          |:-:       |
|ALTREP     |Non     |?      |Non      |Non          |Non       |
|CN         |?       |Non    |?        |Non          |Non       |
|CUTYPE     |?       |Non    |Non      |Non          |Non       |
|DELFROM    |?       |Non    |Non      |Non          |Non       |
|DELTO      |?       |Non    |Non      |Non          |Non       |
|DIR        |?       |Non    |?        |Non          |Non       |
|LANGUAGE   |?       |?      |?        |Non          |Non       |
|RANGE      |Non     |Non    |Non      |?            |Non       |
|RELTYPE    |Non     |Non    |Non      |Non          |?         |
|ROLE       |?       |Non    |Non      |Non          |Non       |
|RSVP       |?       |Non    |Non      |Non          |Non       |
|SENTBY     |?       |Non    |?        |Non          |Non       |
|TZID       |Non     |Non    |Non      |?            |Non       |

|           |EX-DATE|RDATE|
|:-         |:-:    |:-:  |
|TZID       |?      |?    |


Description des différents paramètres de propriétés:
* ALTREP: spécifie une représentation du texte alternative (pas très bien compris (3.2.1))    
* CN: permet de donner un nom + usuel à une valeur de propriété                               
* CUTYPE (3.2.3): permet d'identifier le type d'utilisateur de la propriété                   
    - INDIVIDUAL (valeur par défaut)                                                          
    - GROUP                                                                               
* DELFROM: indique les personnes ayant délégué leur participation à une autre personne (normalement spécifiées par DELTO)
* DELTO: indique les personnes auxquelles on a délégué la participation d'une réunion (spécifiées par DELFROM)
* DIR (3.2.6): indique le chemin d'un dossier utile pour l'évènement
* ENCODING: précise l'encodage de la valeur de propriété (si nécessaire)
* FMTTYPE: indique le type du format de la valeur de propriété
* FBTYPE: indique les périodes libres ou occupées (les créneaux occupés sont précisés dans ce cas à la suite du BUSY\*)
    - FREE
    - BUSY
    - BUSY-UNAVAILABLE
    - BUSY-TENTATIVE
    - other: on peut mettre ce que l'on veut
* LANGUAGE: la valeur de ce paramètre de ce propriété est définie par la norme [RFC 5646](https://datatracker.ietf.org/doc/html/rfc5646)
* MEMBER: LISTE indiquant les différents participants
* PARTSTAT: indique le status de participation de l'utilisateur du calendrier, se décline en PARTSTAT, PARTSTAT-EVENT, PARSTAT-TODO et PARSTAT-JOUR
    - ACCEPTED
    - DECLINED
    - NEEDS-ACTION (valeur par défaut)
    - TENTATIVE (sauf pour PARSTAT-JOUR)
    - DELEGATED (sauf pour PARSTAT-JOUR)
    - COMPLETED (pour PARSTAT-TODO seulement)
    - IN-PROCESS (pour PARSTAT-TODO seulement)
    - customisé
* RANGE: à comprendre (3.2.13)
* TRIGREL: permet d'ajouter une alarme un certain temps avant ou après le début d'un évènement sous la forme "TRIGGER;RELATED=(START/END):XXX" (pas compris ce qu'on devait mettre au XXX (3.2.14))
    - START
    - END
* RELTYPE: indique la relation entre l'utilisateur du calendrier et celui d'un autre calendrier
* ROLE: indique le rôle de l'utilisateur du calendrier
    - CHAIR: partipants principaux
    - REQ-PARTICIPANT: participants récurrents (valeur par défaut)
    - OPT-PARTICIPANT: participants optionnels
    - NON-PARTCIPANT: participants absents
    - customisé
* RSVP: indique le status de présence
    - FALSE (valeur par défaut)
    - TRUE
* SENTBY: indique la personne qui a envoyé ce calendrier
* TZID (3.2.19): indique le fuseau horaire (à revoir)

Notes à garder en tête:
- Une ligne ne doit jamais faire plus de 75 caractères. Si une ligne dépasse cette limite, elle doit être coupée en deux avec un léger décalage de la deuxième ligne vers la droite par rapport à la première.
- L'ordre des éléments dans une liste n'influe pas sur son traitement. (revoir pargraphe 3.1.1)
- altrep ne peut pas être utilisé seul, il faut toujours sa représentation initiale
- pour FBTYPE: il faudra gérer le duo UTC/Period