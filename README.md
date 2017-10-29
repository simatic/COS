<div id="table-of-contents">
<h2>Table des matières</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Introduction</a></li>
<li><a href="#sec-2">2. Installation de <i>COS</i></a>
<ul>
<li><a href="#sec-2-1">2.1. Généralités</a></li>
<li><a href="#sec-2-2">2.2. Linux</a></li>
<li><a href="#sec-2-3">2.3. MacOS</a></li>
<li><a href="#sec-2-4">2.4. Windows</a>
<ul>
<li><a href="#sec-2-4-1">2.4.1. 1er cas</a></li>
<li><a href="#sec-2-4-2">2.4.2. 2e cas</a></li>
<li><a href="#sec-2-4-3">2.4.3. 3e cas</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#sec-3">3. Configuration initiale de COS</a>
<ul>
<li><a href="#sec-3-1">3.1. Configuration du système d'exploitation et du tableur que vous utilisez</a>
<ul>
<li><a href="#sec-3-1-1">3.1.1. Le coin du geek (à ne lire que si vous souhaitez en savoir plus)</a></li>
</ul>
</li>
<li><a href="#sec-3-2">3.2. Configuration de votre nom dans les documents de synthèse générés par COS</a></li>
</ul>
</li>
<li><a href="#sec-4">4. Phase 1 (pré-soutenance)</a>
<ul>
<li><a href="#sec-4-1">4.1. Configuration de COS</a>
<ul>
<li><a href="#sec-4-1-1">4.1.1. Bonus accordé aux étudiants</a></li>
<li><a href="#sec-4-1-2">4.1.2. Types des critères d'évaluation</a></li>
<li><a href="#sec-4-1-3">4.1.3. Critères d'évaluation</a></li>
<li><a href="#sec-4-1-4">4.1.4. Titres des soutenances</a></li>
<li><a href="#sec-4-1-5">4.1.5. Liste des étudiants</a></li>
</ul>
</li>
<li><a href="#sec-4-2">4.2. Exécution de la phase 1 de COS</a>
<ul>
<li><a href="#sec-4-2-1">4.2.1. Linux/MacOS</a></li>
<li><a href="#sec-4-2-2">4.2.2. Windows</a></li>
</ul>
</li>
<li><a href="#sec-4-3">4.3. Préparation de la soutenance</a>
<ul>
<li><a href="#sec-4-3-1">4.3.1. Mise à disposition sur Internet des fiches d'évaluation nominatives</a></li>
<li><a href="#sec-4-3-2">4.3.2. Impression des fiches d'évaluation génériques</a></li>
<li><a href="#sec-4-3-3">4.3.3. Enrichissement du fichier canevas de notes</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#sec-5">5. Phase de soutenance</a></li>
<li><a href="#sec-6">6. Phase 2 (post-soutenance) :</a>
<ul>
<li><a href="#sec-6-1">6.1. Configuration de COS</a></li>
<li><a href="#sec-6-2">6.2. Exécution de la phase 2 de COS</a></li>
<li><a href="#sec-6-3">6.3. Exploitation des fichiers générés par COS (en phase 2)</a></li>
</ul>
</li>
<li><a href="#sec-7">7. Changement des noms ou des valeurs utilisés par défaut</a>
<ul>
<li><a href="#sec-7-1">7.1. Changement des noms de fichier</a>
<ul>
<li><a href="#sec-7-1-1">7.1.1. Ajout automatique de la date dans le nom des fichiers générés</a></li>
<li><a href="#sec-7-1-2">7.1.2. Répertoire racine</a></li>
<li><a href="#sec-7-1-3">7.1.3. Renommage de configuration.txt</a></li>
<li><a href="#sec-7-1-4">7.1.4. Renommage des fichiers autres que configuration.txt</a></li>
</ul>
</li>
<li><a href="#sec-7-2">7.2. Changement des valeurs par défaut</a></li>
</ul>
</li>
<li><a href="#sec-8">8. Conclusion</a></li>
</ul>
</div>
</div>



    # Introduction<a id="sec-1" name="sec-1"></a>

Lorsqu'un enseignant fait passer une soutenance à certains étudiants
d'une classe, souvent, il demande aux autres étudiants de la classe
d'assister à cette soutenance pour que les étudiants qui ne
soutiennent pas :
1.  profitent de la soutenance pour apprendre de nouvelles choses,
2.  profitent des remarques qu'il fera aux étudiants en train de
    soutenir,
3.  fassent des remarques à leurs collègues qui soutiennent. Ainsi, ces
    derniers auront un volument plus important de remarques/conseils et
    pourront encore plus s'améliorer.

Hélas, très souvent, dans la pratique, les étudiants qui ne soutiennent
pas n'écoutent pas la soutenance, car ils font autre chose.

*COS* (Collecte d'Opinions lors de Soutenances) est un outil destiné
à favoriser l'attention des étudiants lors des soutenances de leur
collègues. Ainsi, les objectifs évoqués précédemment ont plus de
chances d'être atteints.

*COS* a été testé sous Linux, MacOS et Windows. Il est compatible avec
LibreOffice/OpenOffice Calc et Excel.

*COS* s'inscrit dans la procédure suivante qui sera détaillée dans la
suite de ce document:
-   Phase 0 (configuration initiale) : l'enseignant configure *COS* en
    indiquant :
    -   sur quel système d'exploitation il travaille (Linux, MacOS, Windows),
    -   quel tableur il envisage d'utiliser (*Excel* ou *LibreOffice
        Calc*). NB: *COS* n'impose pas d'utiliser un tableur, mais
        l'utilisation d'un tableur facilite grandement la saisie de
        certaines informations ;
    -   sous quel nom il veut apparaître dans les documents de synthèse qui
        seront fournis aux étudiants,
-   Phase 1 (pré-soutenance) :
    -   l'enseignant spécifie les données concernant une soutenance :
        -   Le bonus qui sera accordé à la note de soutenance des étudiants
            qui ont fait la même évaluation de certains critères que le
            l'enseignant ;
        -   Type des critères d'évaluation (par exemple, "Fond", "Forme", etc.),
        -   Liste des critères d'évaluation (par exemple, "Résultats et
            recul", "Dynamisme", etc.),
        -   Liste des titres des soutenances,
        -   Liste des étudiants qui assisteront aux soutenances,
    -   l'enseignant exécute *COS* pour générer :
        -   un fichier avec des fiches d'évaluation nominatives qui seront
            remplies par les étudiants,
        -   un fichier avec des fiches d'évaluation génériques,
        -   un canevas fichier qui lui servira à entrer ses notes et
            commentaires pour les différentes soutenances.
    -   l'enseignant prépare la soutenance :
        -   il recopie le fichier des fiches d'évaluation nominatives dans
            un éditeur de texte collaboratif (par exemple, [framapad](https://framapad.org/)) ;
        -   il imprime autant de fiches d'évaluation génériques qu'il y aura
            d'étudiants sans accès à l'éditeur de texte collaboratif pendant
            les soutenances ;
        -   il enrichit le canevas de fichier pour que la saisie de notes
            et de commentaires lui soit plus facile.
-   Phase Soutenance. Pendant la soutenance :
    -   l'enseignant explique comment seront exploitées les informations
        fournies par les étudiants. En particulier, il évoque le bonus
        dont profiteront les étudiants qui "joueront le jeu" de remplir
        ces informations ;
    -   les étudiants utilisent l'éditeur de texte collaboratif ou bien
        remplisse une fiche d'évaluation générique ;
    -   l'enseignant saisit des notes et des commentaires.
-   Phase 2 (post-soutenance) :
    -   l'enseignant récupère le contenu du fichier qui a été rempli avec
        l'éditeur de texte collaboratif ;
    -   l'enseignant retranscrit les notes prises manuellement sur les
        fiches d'information génériques dans ce fichier.
    -   l'enseignant finit de saisir ses notes et commentaires ;
    -   l'enseignant exécute *COS* pour générer :
        -   Une synthèse des comentaires faits par les étudiants durant la
            soutenance,
        -   Un fichier donnant le détail des notes de chaqsue étudiant (note
            de soutenance attribuée par l'enseignant, bonus pour bonne
            évaluation de soutenance de collègues, note finale).

Dans la suite de ce document, nous commençons par présenter
l'installation de *COS*, avant de détailler chacune des phases
mentionnées dans cette introduction. La dernière section explique
comment changer les noms de fichier et les valeurs utilisés par
défaut.

# Installation de *COS*<a id="sec-2" name="sec-2"></a>

## Généralités<a id="sec-2-1" name="sec-2-1"></a>

-   Téléchargez l'archive ZIP `COS-master.zip` de *COS* sur [github](https://github.com/simatic/COS)
      (L'accès à l'archive se fait en cliquant sur le bouton vert `Clone
      or download` en haut à droite, puis en cliquant sur `Download ZIP`).
-   Dézipper cette archive sur votre ordinateur à l'endroit qui vous
    arrange.
-   *COS* est un programme écrit en *Python 3*. Les sous-sections
    suivantes détaillent l'installation de *Python 3* selon votre
    système d'exploitation.

## Linux<a id="sec-2-2" name="sec-2-2"></a>

Vous n'avez rien de spécial à faire (*Python 3* est installé par
défaut sur Linux).

## MacOS<a id="sec-2-3" name="sec-2-3"></a>

Ouvrez un terminal de commande.

Tapez la commande `python3`

Si vous avez une fenêtre dont le contenu ressemble au contenu suivant
(notez les `>>>` en dernière ligne) :

    $ python3
    Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
    [GCC 5.4.0 20160609] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

alors *Python 3* est déjà installé : vous n'avez rien à faire (hormis
fermer votre terminal).

Sinon, téléchargez *Python 3* sur le [site officiel](https://www.python.org/downloads/mac-osx/). Puis, installez-le.

## Windows<a id="sec-2-4" name="sec-2-4"></a>

-   Appuyez sur la touche `Windows`, puis sur la touche `R` (sans
    appuyer sur la touche `Majuscule` : une fenêtre `Exécuter` apparaît.
-   Dans cette fenêtre, dans le champ `Ouvrir:`, tapez `cmd`. Puis,
    cliquez sur `OK` : uène fenêtre `C:\WINDOWS\system32\cmd.exe`
    apparaît.
-   Dans cette fenêtre, tapez `python`, puis appuyez sur la touche
    `Entrée`. 3 cas sont possibles :

### 1er cas<a id="sec-2-4-1" name="sec-2-4-1"></a>

Vous obtenez l'affichage :

    Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 17:26:49) [MSC v.1900 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Vu qu'il y a écrit `Python 3.` au début de la première ligne, cela
signifie que *Python 3* est déjà installé sur votre machine : vous
n'avez rien à faire (hormis fermer cette fenêtre).

### 2e cas<a id="sec-2-4-2" name="sec-2-4-2"></a>

Vous obtenez l'affichage :

    'python' n’est pas reconnu en tant que commande interne
    ou externe, un programme exécutable ou un fichier de commandes.

Cela signifie que *Python 3* n'est pas installé sur votre machine :
-   Téléchargez *Python 3* sur le [site officiel](https://www.python.org/downloads/)
-   Lancez l'installation sur votre ordinateur : une fenêtre `Python 3
      (32-bit) Setup` apparaît.
-   Dans cette fenêtre, cochez : `Install laucher for all users
      (recommended)` et `Add Python 3.6 to PATH`. Puis, cliquez sur
    "Install Now".
-   Windows vous demande si vous autorisez cette application à apporter
    des modifications à votre ordinateur. Répondez que "Oui".
-   Au bout d'un moment, une fenêtre affiche un message "Setup was
    successful". Cliquez sur "Close"

### 3e cas<a id="sec-2-4-3" name="sec-2-4-3"></a>

Vous obtenez l'affichage :

    Python 2.7.3 (default, Apr 10 2012, 23:24:47) [MSC v.1500 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Vu qu'il y a écrit `Python 2.` au début de la première ligne, cela
signifie que c'est *Python 2* qui est installé sur votre machine et
non *Python 3*. Il faut installer *Python 3*, mais sans déranger
l'installation de *Python 2*. Pour ce faire :

-   Téléchargez *Python 3* sur le [site officiel](https://www.python.org/downloads/)
-   Lancez l'installation sur votre ordinateur : une fenêtre `Python 3
      (32-bit) Setup` apparaît.
-   Dans cette fenêtre, cochez : `Install laucher for all users
      (recommended)`. Vérifiez que `Add Python 3.6 to PATH` est
    **décoché**. Puis, cliquez sur "Install Now".
-   Windows vous demande si vous autorisez cette application à apporter
    des modifications à votre ordinateur. Répondez que "Oui".
-   Au bout d'un moment, une fenêtre affiche un message "Setup was
    successful". Cliquez sur "Close"

*Python 3* est désormais installé sur votre machine. Mais, vous devez
préciser à *COS* qu'il doit utiliser ce *Python 3* et non le *Python
2* auquel il accéderait spontanément :
-   Avec un explorateur de fichier, allez dans le répertoire où vous
    avez dézippé *COS*.
-   Clic gauche sur le fichier `cos.bat`, puis clic droit pour choisir
    de l'éditer avec votre éditeur de texte (par exemple, *Notepad++*).
-   Ajoutez la ligne `set PATH=C:\Program Files (x86)\Python36-32\` 
    après la ligne `echo off` et enregistrez votre fichier. Il doit 
    donc désormais ressembler à ceci :

    echo off
    set PATH=C:\Program Files (x86)\Python36-32\
    set PYTHONPATH=collectopiniondefenses
    python collectopiniondefenses/main.py -%1 configuration.txt
    pause

# Configuration initiale de COS<a id="sec-3" name="sec-3"></a>

## Configuration du système d'exploitation et du tableur que vous utilisez<a id="sec-3-1" name="sec-3-1"></a>

Avec un explorateur de fichier, allez dans le répertoire `modeles` de
*COS*. Ce répertoire contient 4 fichiers archives. Double-cliquez sur
l'archive correspondant à votre combinaison Système d'exploitation
(Linux et MacOS OU BIEN Windows) / Tableur (LibreOffice Calc et
OpenOffice Calc OU BIEN Excel), comme indiqué dans le tableau
ci-dessous.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="left" />

<col  class="left" />

<col  class="left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="left">&#xa0;</th>
<th scope="col" class="left">LibreOffice Calc</th>
<th scope="col" class="left">Excel</th>
</tr>
</thead>

<tbody>
<tr>
<td class="left">Linux/MacOS</td>
<td class="left">`linux_MacOS_LibreOffice_Calc.zip`</td>
<td class="left">`linux_MacOS_Excel.zip`</td>
</tr>
</tbody>

<tbody>
<tr>
<td class="left">Windows</td>
<td class="left">`windows_LibreOffice_Calc.zip`</td>
<td class="left">`windows_Excel.zip`</td>
</tr>
</tbody>
</table>

Extrayez les fichiers de cette archive de sorte que :
-   `configuration.txt` soit extrait dans le répertoire principal de
    *COS*;
-   `Phase_1_entree/listeCriteres.csv` soit extrait dans le répertoire
    `Phase_1_entree` de *COS*;
-   etc.

### Le coin du geek (à ne lire que si vous souhaitez en savoir plus)<a id="sec-3-1-1" name="sec-3-1-1"></a>

Le fichier `configuration.txt` extrait de l'archive dépend du système
d'exploitation de la manière suivante :
-   en Linux-MacOS, le champ `encoding` vaut `utf-8` ;
-   en Windows, ce champ vaut `windows-1252`.

Tous les fichiers extraits de l'archive dépendent du système
d'exploitation de la manière suivante :
-   en Linux-MacOS, ils sont encodés en `utf-8` avec des retours à la
    ligne simples ;
-   en Windows, ils sont encodés en `ASCII` (`windows-1252`) avec des
    retours à la ligne typiques de Windows (*linefeed* suivi de
    *Carriage return*).

Le fichier `configuration.txt` extrait de l'archive dépend du tableur
de la manière suivante :
-   pour LibreOffice/OpenOffice Calc, le champ `csvSeparator` vaut ","
    (virgule, sans les guillements) ;
-   pour Excel, ce champ vaut ";" (point-virgule, sans les guillements).

Tous les fichiers d'extension **.csv** extraits de l'archive dépendent
du système d'exploitation de la manière suivante :
-   pour LibreOffice/OpenOffice Calc, le séparateur utilisé est une ","
    (virgule, sans les guillements) ;
-   pour Excel, c'est ";" (point-virgule, sans les guillements).

Remarque : si vous travaillez avec un tableur configuré pour
interpréter les nombres décimaux à l'américaine (pi s'écrit "3.14" et
non "3,14"), il vous faut changer, dans `configuration.txt`, le champ
`decimalSeparator` en "." (point, sans les guillemets) à la place de
"," (virgule, sans les guillemets).

## Configuration de votre nom dans les documents de synthèse générés par COS<a id="sec-3-2" name="sec-3-2"></a>

-   Éditez le fichier `configuration.txt` en double-cliquant dessus
    avec un explorateur de fichiers.
-   Modifiez le champ `teacherName` pour y indiquer le nom sous lequel
    vous souhaitez apparaître dans les documents générés par *COS*. Par
    exemple, `teacherName = Jeanne Dupont` si vous souhaitez que
    l'encadrante s'appelle *Jeanne Dupont*.
-   Sauvegardez le fichier.

# Phase 1 (pré-soutenance)<a id="sec-4" name="sec-4"></a>

## Configuration de COS<a id="sec-4-1" name="sec-4-1"></a>

### Bonus accordé aux étudiants<a id="sec-4-1-1" name="sec-4-1-1"></a>

Lors de la phase 2, quand *COS* comparera les évaluations des
étudiants et les évaluations de l'enseignant, il attribuera à chaque
étudiant un bonus par évaluation d'étudiant correspondant à
l'évaluation enseignant. Même si ce bonus ne servira qu'en phase 2,
nous vous proposons de réfléchir à la valeur de ce bonus, **dès la
phase 1**, pour pouvoir l'indiquer aux étudiants lors de la phase de
soutenance.

Pour changer la valeur de ce bonus :
-   Éditez le fichier `configuration.txt` en double-cliquant dessus
    avec un explorateur de fichiers.
-   Modifiez le champ `bonusCriteriaOK` pour y indiquer la valeur de ce
    bonus. Par exemple, mettez `bonusCriteriaOK = 0.1` pour indiquer un
    bonus de *0.1*. NB : écrivez ce nombre décimal en notation
    américaine (donc, "." (point) pour séparer la partie entière de la
    partie décimale).
-   Sauvegardez le fichier.

### Types des critères d'évaluation<a id="sec-4-1-2" name="sec-4-1-2"></a>

*COS* impose de catégoriser les différents critères d'évaluation. (par
exemple, "Fond", "Forme", etc.).

Pour changer la liste des types de critères d'évaluation :
-   Éditez le fichier `Phase_1_entree/listeTypesCriteres.txt` en
    double-cliquant dessus avec un explorateur de fichiers.
-   Modifiez la liste des types de critère. L'exemple définit les types
    `Fond` et `Forme`, la ligne `# Nom de chaque type de critère` étant
    un commentaire.

    # Nom de chaque type de critère
    Fond
    Forme

-   Sauvegardez le fichier.

### Critères d'évaluation<a id="sec-4-1-3" name="sec-4-1-3"></a>

*COS* vous permet de personnaliser les critères d'évaluation de vos
soutenances.

Pour changer la liste des critères d'évaluation :
1.  Éditez le fichier `Phase_1_entree/listeCriteres.txt` en
    double-cliquant dessus avec un explorateur de fichiers. Cela ouvre
    votre tableur.
    -   NB (lié à LibreOffice/OpenOffice Calc) : Dans le cas de
        *LibreOffice Calc*, une fenêtre `Import de texte` s'affiche dans
        un premier temps. Veillez à ce que, dans la zone `Options de
             séparateur`, 1) `Séparé par` soit sélectionné, 2) seul `Virgule`
        soit coché.
2.  Modifiez la liste des critères. L'exemple définit 10 critères (5 de
    `Fond` et 5 de `Forme`).
3.  Sauvegardez le fichier (au format **CSV**).

### Titres des soutenances<a id="sec-4-1-4" name="sec-4-1-4"></a>

*COS* impose de lui fournir la liste des titres des soutenances qui
vont avoir lieu. Nous vous recommandons de les lui fournir dans
l'ordre de passage envisagé (cela facilite le remplissage des fiches
par les étudiants et l'enseignant).

Pour changer la liste des types de critères d'évaluation :
-   Éditez le fichier `Phase_1_entree/listeSoutenances.txt` en
    double-cliquant dessus avec un explorateur de fichiers.
-   Modifiez la liste des soutenances. L'exemple définit 3 soutenances
    `Eugénie Grandet`, `La Touche étoile` et `... Et mon tout est un
      homme`, la ligne `# Nom de chaque soutenance` étant un commentaire.

    # Nom de chaque soutenance
    Eugénie Grandet
    La Touche étoile
    ... Et mon tout est un homme

-   Sauvegardez le fichier.

### Liste des étudiants<a id="sec-4-1-5" name="sec-4-1-5"></a>

*COS* impose de lui fournir la liste des étudiants qui vont soutenir
et, sur quelle soutenance, ils vont soutenir. Notez que :
-   Plusieurs étudiants peuvent soutenir ensemble (cf., dans l'exemple,
    `M. AYRAUD Pierre (dit Thomas Narcejac)` et `M. BOILEAU Pierre
      Louis` qui font la même soutenance de titre `... Et mon tout est un
      homme`)
-   Une soutenance de `Phase_1_entree/listeSoutenances.txt` peut ne pas
    se voir mentionnée à cette étape.

Pour changer la liste des étudiants :
1.  Éditez le fichier `Phase_1_entree/listeEtudiants.txt` en
    double-cliquant dessus avec un explorateur de fichiers. Cela ouvre
    votre tableur.
    -   NB (lié à LibreOffice/OpenOffice Calc) : Dans le cas de
        *LibreOffice Calc*, une fenêtre `Import de texte` s'affiche dans
        un premier temps. Veillez à ce que, dans la zone `Options de
             séparateur`, 1) `Séparé par` soit sélectionné, 2) seul `Virgule`
        soit coché.
2.  Modifiez la liste des étudiants. L'exemple définit 4 étudiants.
3.  Sauvegardez le fichier (au format **CSV**).

## Exécution de la phase 1 de COS<a id="sec-4-2" name="sec-4-2"></a>

Le lancement de la phase 1 de *COS* dépend de votre système
d'exploitation.

### Linux/MacOS<a id="sec-4-2-1" name="sec-4-2-1"></a>

Dans le répertoire de *COS*, exécutez le programme
`cos_phase_1.sh`. En cas d'erreur, un message vous explique le
problème détecté : à vous de le corriger. Si tout se passe bien, *COS*
affiche le message :

    cos version 1.0.0
    
    OK, exécution de la phase 1 terminée : les fichiers...

### Windows<a id="sec-4-2-2" name="sec-4-2-2"></a>

Avec un explorateur de fichiers, allez dans le répertoire de
*COS*. Puis, double-cliquez sur le programme `cos_phase_1.bat` : une
fenêtre s'ouvre et affiche un message d'erreur ou bien un message de
bonne exécution (cf. exemple Linux/MacOS ci-dessus). Dans les 2 cas,
appuyez sur une touche pour fermer la fenêtre.

## Préparation de la soutenance<a id="sec-4-3" name="sec-4-3"></a>

### Mise à disposition sur Internet des fiches d'évaluation nominatives<a id="sec-4-3-1" name="sec-4-3-1"></a>

-   Dans un éditeur de texte collaboratif (par exemple, [framapad](https://framapad.org/)), créez
    un *pad* public ou privé (à vous de décider, l'essentiel étant que
    les étudiants puissent y accéder).
-   Dans le répertoire `Phase_1_sortie`, double-cliquez sur le fichier
    `listeFichesEtudiants.txt`
-   Recopiez son contenu dans le *pad* créé.

### Impression des fiches d'évaluation génériques<a id="sec-4-3-2" name="sec-4-3-2"></a>

-   Si vous savez que des étudiants n'auront pas accès à un ordinateur
    (ou une tablette, si vous estimez qu'une tablette peut permettre de
    modifier le *pad*) pendant la soutenance, comptez le nombre
    d'étudiants dans ce cas.
-   Dans le répertoire `Phase_1_sortie`, imprimez le fichier
    `ficheGeneriqueEtudiant.txt` en autant d'exemplaires que nécessaire.

### Enrichissement du fichier canevas de notes<a id="sec-4-3-3" name="sec-4-3-3"></a>

-   Dans le répertoire `Phase_1_sortie`, double-cliquez sur le fichier
    `Phase_1_sortie/canevasNotesEncadrant.csv` : votre tableur s'ouvre.
-   Enrichissez ce fichier, par exemple :
    -   en changeant la largeur des colonnes
    -   en changeant la colonne 1 de la ligne `Ligne inutilisée (par
            exemple...`
    -   en mettant dans les autres colonnes de cette ligne, une formule de
        calcul de somme des éléments de cette colonne
    -   etc.
-   Sauvegardez le tableau obtenu dans le répertoire `Phase_2_entree` au
    format standard de votre tableur (`.odt` pour LibreOffice/OpenOffice
    et `.xlsx` pour Excel).

# Phase de soutenance<a id="sec-5" name="sec-5"></a>

1.  Indiquez aux étudiants comment ils peuvent fournir les
    informations. En particulier, fournissez l'adresse du *pad*, voire
    un crayon pour les étudiants qui rempliront un exemplaire papier.
2.  Expliquez les "règles du jeu", i.e. les informations que les
    étudiants doivent fournir et comment ces informations seront
    exploitées :
    -   L'étudiant doit remplir la fiche correspondant à son nom.
    -   Pour chaque soutenance (hormis la sienne, évidemment), l'étudiant doit :
        -   Mettre un "+" au début de la ligne d'un critère dont il pense
            que l'enseignant estimera que le critère ne nécessite aucune
            amélioration (voire qu'il est impeccable).
        -   Mettre un commentaire au niveau du champ
            `Commentaire/Justification du +`.
        -   S'il estime que l'enseignant considérera qu'il n'y aucun
            critère impeccable pour cette soutenance, l'étudiant doit
            mettre un "+" devant un critère dont il pense que l'enseignant
            estimera que le critère ne nécessite qu'une (ou des)
            amélioration(s) mineure(s).
        -   Même principe avec un "-" correspondant à un critère
            nécessitant une (ou des) amélioration(s) majeure(s).
    -   Au moment du dépouillement par l'enseignant :
        -   Un "+" n'est pris en compte que si le champ
            `Commentaire/Justification du +` est rempli (intelligemment).
        -   Idem pour un "-"
        -   Si, pour une même soutenance, l'étudiant écrit plusieurs "+" ou
            plusieurs "-", aucun "+" ne sera considéré pour cette
            soutenance.
        -   Idem pour les "-"
        -   Si, pour une soutenance, l'étudiant remplit le champ
            `Commentaire/Justification du +` sans donner de "+" à un
            critère, son commentaire est ignoré.
        -   Idem pour `Commentaire/Justification du -`
        -   Chaque "+" qui correspondant à un critère jugé impeccable par
            l'enseignant rapport un bonus de *nombre de point bonus que
            vous avez décidé précédemment* à la note finale.
        -   Idem pour chaque "-"
        -   Expliquez le principe de bonus si, pour une soutenance,
            l'enseignant ne met aucun "+".
        -   Expliquez que c'est pareil dans le cas où il ne met aucun "-".
3.  Faites passer les soutenances.
4.  Remplissez votre fichier de notes/commentaires

# Phase 2 (post-soutenance) :<a id="sec-6" name="sec-6"></a>

## Configuration de COS<a id="sec-6-1" name="sec-6-1"></a>

-   Complétez le *pad* avec les réponses récupérées au format papier.
-   Recopiez le contenu de votre *pad* dans le fichier
    `reponsesEtudiants.txt` du répertoire `Phase_2_entree`
-   Sauvegardez dans le répertoire `Phase_2_entree` votre fichier de
    notes/commentaires au format **CSV** et sous le nom
    `notesEncadrant.csv`
-   NB : si vous le souhaitez, vous pouvez changer le bonus accordé aux
    étudiants. En effet, c'est seulement maintenant que sa valeur va
    vraiment être exploitée.

## Exécution de la phase 2 de COS<a id="sec-6-2" name="sec-6-2"></a>

De même que pour la phase 1, la phase 2 de *COS* dépend de votre
système d'exploitation :
-   Linux/MacOS : exécutez `cos_phase_2.sh` au lieu de `cos_phase_1.sh`
      précédemment.
-   Windows : exécutez `cos_phase_2.bat` au lieu de `cos_phase_1.bat`
      précédemment.

En cas d'exécution correcte, vous aurez l'affichage suivant :

    cos version 1.0.0
    
    OK, exécution de la phase 2 terminée : les fichiers...

## Exploitation des fichiers générés par COS (en phase 2)<a id="sec-6-3" name="sec-6-3"></a>

Les deux fichiers générés par *COS* sont disponibles dans le
répertoire `Phase_2_sortie` :
-   `syntheseCommentaires.txt` contient la synthèse des commentaires
    faits par les étudiants et vous durant la soutenance. À vous de
    décider comment l'exploiter.
-   `notesEtudiants.csv` contient le calcul des différentes notes.
    -   La note de soutenance
        -   Elle est calculée en faisant la somme des notes que vous avez
            attribuée à chaque critère, pour cette soutenance.
        -   Si vous préférez mettre d'autres valeurs que 0, 1 ou 2, allez
            dans le fichier `configuration.txt` pour changer les champs
            (NB : actuellement, ces champs doivent être des entiers) :
            -   `pointsCriteriaOK = 2` (valeur actuelle : 2)
            -   `pointsCriteriaAverage = 1` (valeur actuelle : 1)
            -   `pointsCriteriaKO = 0` (valeur actuelle : 0)
    -   La note de bonus (qui, rappelons-le, dépend du champ
        `bonusCriteriaOK` dans le fichier `configuration.txt`)
    -   La note finale du module (qui est la somme de ces deux notes).
    -   À vous de décider comment exploiter `notesEtudiants.csv`.

# Changement des noms ou des valeurs utilisés par défaut<a id="sec-7" name="sec-7"></a>

## Changement des noms de fichier<a id="sec-7-1" name="sec-7-1"></a>

### Ajout automatique de la date dans le nom des fichiers générés<a id="sec-7-1-1" name="sec-7-1-1"></a>

À chaque fois que vous exécutez *COS*, les fichiers qu'il génère
écrase les anciens fichiers présents dans `Phase_1_sortie` et
`Phase_1_sortie`. Vous pouvez demander à *COS* de générer un fichier à
chaque fois différent. Pour ce faire, dans `configuration.txt`, mettre
`insertDateInFilename = 0`. Les fichiers générés incluent désormais la
date et l'heure d'éxécution de *COS*. Par exemple, au lieu de générer
le fichier `listeFichesEtudiants.txt`, *COS* génère le fichier
`listeFichesEtudiants_2017-10-29_07:15:21.txt`.

### Répertoire racine<a id="sec-7-1-2" name="sec-7-1-2"></a>

Dans `configuration.txt`, le champ `rootDirectory` permet de spécifier
à partir de quel répertoire *COS* doit chercher les fichiers qu'il lit
ou écrit. Par exemple, `rootDirectory = Soutenances/Eco/Nov2016` dit à
*COS* de chercher ses fichiers à partir du répertoire `Nov2016` qui
est dans le répertoire `Eco` qui est lui-même dans le répertoire
`Soutenances`. `rootDirectory =` (notez qu'il n'y a rien derrière le
signe "=") dit à *COS* de chercher ses fichiers à partir du répertoire
courant.

### Renommage de configuration.txt<a id="sec-7-1-3" name="sec-7-1-3"></a>

Si vous souhaitez que le fichier `configuration.txt` s'appelle
autrement, renommez-le et modifiez le nom dans `cos.sh` (si vous êtes
sous Linux/MacOS) et `cos.bat` (si vous êtes sous Windows).

### Renommage des fichiers autres que configuration.txt<a id="sec-7-1-4" name="sec-7-1-4"></a>

Le nom des autres fichiers et leur localisation peuvent être changés
en modifiant le champ correspondant à ce fichier dans le fichier
`configuration.txt`.

Imaginons, par exemple, que vous n'êtes pas satisfait du fait que le
fichier des retours des étudiants s'appelle `reponsesEtudiants.txt` et
est stocké dans `Phase_2_entree`. Il faut alors changer la valeur du
champ `filledNominativeSheetsFilename`. Par exemple, supposons que
vous voulez que le fichier s'appelle désormais
`retoursDesEtudiants.txt` et soit stocké au même niveau que le fichier
`configuration.txt`, il faut modifier `configuration.txt` en
écrivant :

`filledNominativeSheetsFilename = retoursDesEtudiants.txt`

## Changement des valeurs par défaut<a id="sec-7-2" name="sec-7-2"></a>

Nous avons déjà évoqué comment (et pourquoi) changer dans
`configuration.txt`:
-   `bonusCriteriaOK`
-   `pointsCriteriaOK`
-   `pointsCriteriaAverage`
-   `pointsCriteriaKO`

`configuration.txt` contient également la configuration des lignes
générées dans `listeFichesEtudiants.txt` lors de la phase 1 :
-   `studentBound` (Délimiteur entre les etudiants dans le fichier avec
    toutes les fiches nominatives)
-   `defenseBound` (Délimiteur entre les soutenances dans les fichiers
    avec les fiches (nominatives ou génériques))
-   `positiveCommentBound` (Délimiteur des commentaires positifs dans
    les fichiers avec les fiches (nominatives ou generiques))
-   `negativeCommentBound` (Délimiteur des commentaires négatifs dans
    les fichiers avec les fiches (nominatives ou generiques))

# Conclusion<a id="sec-8" name="sec-8"></a>

Avec *COS*, nous vous souhaitons des soutenances encore plus
intéressantes qu'avant ! N'hésitez pas à nous faire des retours sur
 [github](https://github.com/simatic/COS) ou à [Michel.Simatic@telecom-sudparis.eu](Michel.Simatic@telecom-sudparis.eu).