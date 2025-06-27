# Calcul de l'Evapotranspiration Potentielle (ETP) et de la Pluie efficace par la méthode du bilan hydrologique de Thornthwaite

## Explication de la méthodologie de calcul

La méthode de Thornthwaite permet de calculer de façon ponctuelle sur une station, le bilan d’eau mensuel ou annuel grâce à des 
valeurs de précipitations mensuelles et des valeurs de températures (Bonnet et al, 1970).

Le schéma conceptuel du bilan de Thornthwaite se base sur le fait que la précipitation sur une zone donnée se répartit en 3 parties que sont l’ETR, le ruissellement (R) et l’infiltration (I), 
selon l’équation :
P = ETR + R + I + ΔS;   ΔS est la variation de stocks d’eau. 

Pour résoudre cette équation, il faut évaluer les différents termes. On admet que pour de longues périodes, les variations de stock ΔS sont nulles (Abdou Babayé, 2012). L’équation devient 
donc : 
P = ETR + R + I   (5) 

La pluie efficace (Peff) est la différence entre P et ETR. Cette pluie efficace est la somme du ruissellement et de l’infiltration. Il est donc possible de calculer cette valeur en connaissant 
l’ETR et la pluie. La pluie étant connue, c’est l’ETR qu’il faut déterminer. Pour cela, la détermination de l’ETP s’avère nécessaire. Avec la méthode de Thornthwaite, il n’est possible 
de déterminer l’ETP que si les températures sont inférieures à 38°C (Bonnet et al, 1970). Il existe alors deux cas de figure : 

### Pour les températures inférieures à 26,5°C  
La formule à utiliser dans ce cas est : 
**ETP = 16.(10/𝑡)^a.K**
  
t : température moyenne mensuelle en °C 

I : indice thermique annuel qui est la somme des indices thermiques mensuels qui se calculent à partir de la formule :

i = ( 𝑡/5)^1,514  

a : fonction complexe de l’indice i ayant pour formule : 

a = **6,75 . 10^−7 . 𝐼^3 − 7,71 . 10^−5 . 𝐼^2 + 1,79 ∗ 10^−2 . 𝐼 + 0,49239**  

K : Coefficient de correction mensuelle qui est donné par une table et qui dépend de la latitude de la zone d’étude.

### Pour les températures supérieures à 26,5°C
  
Pour les températures moyennes se trouvant entre 26,5°C et 38°C, les valeurs d’ETP non corrigées sont données directement par une table (valeurs_etp_temp_sup_26.5).

L'ETP trouvée dans ces deux cas doit être corrigée. Il faut appliquer les coefficients de correction fournis par Thornthwaite, dépendant de la latitude et du mois (k_latitude_nord et k_latitude_sud) 
 
Trois hypothèses seront prises en compte dans la détermination de l’ETR, en référence aux travaux de de Marsily, 2004 et Dassargues, 2007 in Abdou Babayé, 2012 : 
+ l’humidité du sol se présente sous forme d’un stock qui sera noté ici RFU ; 
+ la valeur maximale de la RFU de la zone est connue ; 
+ il ne peut avoir infiltration que si la RFU atteint sa valeur maximale. 

D’une façon plus simple, avec la méthode de Thornthwaite, il ne peut avoir de pluie efficace que si l’ETP et la RFU sont satisfaits. Voilà donc en quoi consiste le principe de 
cette méthode :

+ si on a P > ETP, alors ETP = ETR ; en cas d’excédent des précipitations (P-ETR), il alimente la RFU jusqu’à saturation ; si la RFU est saturée, le surplus des précipitations +est considéré comme la pluie efficace ;

+ si on a P < ETP, alors les précipitations ne peuvent pas satisfaire l’ETP ; l’ETR est donc calculé avec la précipitation et la RFU. Il peut arriver que la réserve du mois précédent soit suffisante pour combler le manque de pluie. Dans ce cas, ETR = ETP. Dans le cas 
où la RFU ne suffit pas pour satisfaire l’ETP, ETR = P.

Le choix de la RFU est la principale contrainte dans ce travail. Cette valeur varie en fonction de la texture et de la nature du sol (Abdou Babayé, 2012). Dans le socle du Bénin, par exemple, la RFU maximale a été fixée à 50 mm, quel que soit le site (Kotchoni, 2019). 
