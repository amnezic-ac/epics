Epics est un logiciel permettant de créer et modifier des calendriers numériques, aussi appelés _ICalendars_, à travers une interface graphique mais aussi une intégration complète dans une stack Python. Ce projet est un projet personnel qui a pour but d'apporter plus de flexibilité et de personnalisation (pour la partie interface utilisateur) que [py-icalendar](https://icalendar.org/) mais aussi de m'apprendre à lire de la documentation RFC. Les calendriers numériques sont stockés dans des fichiers ICS dont la syntaxe est déterminée par la [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545).

Un Ical permet de créer et partager des _composantes_ de 4 types:
- alarme
- évènement
- temps libre/occupé: permet d'indiquer si l'on peut rajouter une composante sur une plage horaire spécifique
- journal: désigne comme une note ou un commentaire que l'on fait sur une journée
- tâche
Pour plus d'explications sur les différentes composantes, veuillez vous reporter au fichier ICS\_format\_explained.md.

Ce programme possède un fichier de configuration qui permet de déterminer un certain nombre de règles et de possibilités pour d'une part respecter la RFC, indispensable à son utilisation globale et sur des logiciels utilisants des Icals, d'autres part pour simplifier la création de ces calendriers numériques pour l'utilisateur final. Ce paragraphe s'adresse aux développeurs, les choix proposés pouvant être modifiés directement depuis l'interface utilisateur. Le fichier "default_configuration.json" contient l'ensemble des règles qui s'appliquent aux différents éléments du logiciel, c'est à dire:
- les règles de conformance à la RFC 5545: ce sont majoritairement les éléments qui ne peuvent prendre qu'un nombre fini de valeurs (indication de participation à un évènement, la classification d'un évènement); ces listes peuvent être modifiées mais les nouveaux éléments apportés pourraient ne pas être correctement interprétés par les logiciels tiers utilisés
- les règles graphiques: couleurs, agencement, détails graphiques
- règles de comportement: désigne les éléments qui doivent un certain comportement dont ce dernier ne peut être déterminé à l'avance (par exemple: un évènement peut durer toute la journée (comme un anniversaire) rendant l'heure inutile mais peut être vitale (comme une réunion))


Les choses qui restent à faire:
- [ ] pour FBTYPE: il faudra gérer le duo UTC/Period
- [ ] comprendre pq `Resources.__str__()` ne fonctionne pas
- [ ] dans un notebook, les notes doivent avoir le titre du summary