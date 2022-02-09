import time
#Détermine si le noeud est terminal
def TerminalTest(s,dernierCoup):
    grillePleine=True
    for list in s:
        if 0 in list :grillePleine=False
    if grillePleine==True : return True
    elif AGagne(s,dernierCoup)==1 or AGagne(s,dernierCoup)==2 :return True
    return False
#crée une copie de la grille à  utiliser par l'IA
def ReinitialiserGrille2(grille):
    grille2=[]
    for ligne in grille:
        ligne2=[]
        for element in ligne:
            ligne2.append(element)
        grille2.append(ligne2)
    return grille2
#Définit la nouvelle grille de jeu après avoir appliqué une action a
def Result(grille,a,isMax):
    grille2=ReinitialiserGrille2(grille)
    i=a[0]
    j=a[1]
    if isMax==True:grille2[i][j]=1
    else : grille2[i][j]=2
    return grille2
#Définit la liste des actions possibles
def Actions(grille):
    list=[]
    for j in range(len(grille[0])):
        for i in range(len(grille),0,-1):
            if grille[i-1][j]==0:
                list.append((i-1,j))
                break
    return list

#Première heuristique utilisant uen évaluation des cases de la grille
#Chaque valeur correspond au nombre de possibilités de victoire associé à  la case
def heuristique1(grille,joueur):
    tableauEvaluation=[ 
    [  3,  4,  5,  7,  7,  7,  7,  7,  7,  5,  4,  3],
    [  4,  6,  8, 10, 10, 10, 10, 10, 10,  8,  6,  4],
    [  5,  8, 11, 13, 13, 13, 13, 13, 13, 11,  8,  5],
    [  5,  8, 11, 13, 13, 13, 13, 13, 13, 11,  8,  5],
    [  4,  6,  8, 10, 10, 10, 10, 10, 10,  8,  6,  4],
    [  3,  4,  5,  7,  7,  8,  8,  7,  7,  5,  4,  3]]
    joueurAdv = 1 if joueur == 2 else 2
    evaluation = 0
    for ligne in range(len(grille)):
        for colonne in range(len(grille[0])) :
            if(grille[ligne][colonne]==joueurAdv):evaluation -= tableauEvaluation[ligne][colonne]
            elif(grille[ligne][colonne]==joueur):evaluation += tableauEvaluation[ligne][colonne]
    return evaluation
 
def heuristique2(joueur,grille,dernierCoup,dernierCoup2):
    
    evaluation = 0
    for derCoup in [dernierCoup,dernierCoup2]:
        i=derCoup[0]
        j=derCoup[1]
        ligneTest=""
        for element in grille[i]:
            ligneTest=ligneTest+str(element)
        colonneTest=""
        for ligne in grille:
            colonneTest=colonneTest+str(ligne[j])
        diagDescTest=str(grille[i][j])
        diagMontTest=str(grille[i][j])
        for k in range(1,len(grille),1):
            if i+k in range(len(grille)) and j+k in range(len(grille[0])):
                diagDescTest=diagDescTest+str(grille[i+k][j+k])
            if(i-k) in range(len(grille)) and (j-k)in range(len(grille[0])):
                diagDescTest=str(grille[i-k][j-k])+diagDescTest
            if(i-k) in range(len(grille)) and (j+k)in range(len(grille[0])):
                diagMontTest=diagMontTest+str(grille[i-k][j+k])
            if(i+k) in range(len(grille)) and (j-k)in range(len(grille[0])):
                diagMontTest=str(grille[i+k][j-k])+diagMontTest
        
        for element in [ligneTest,colonneTest,diagDescTest,diagMontTest]:
            evaluation+=(element.count("0011")+element.count("1100")+element.count("1001")+element.count("1010")+element.count("0101"))
            evaluation+=3*(element.count("0111")+element.count("1110")+element.count("1101")+element.count("1011"))
            evaluation-=(element.count("0022")+element.count("2200")+element.count("2002")+element.count("2020")+element.count("0202"))
            evaluation-=3*(element.count("0222")+element.count("2220")+element.count("2202")+element.count("2022"))
          
    
    return evaluation if joueur==1 else -evaluation
    
   


   
#Regarde la grille autour de la dernière position jouée pour déterminer s'il y a victoire
def AGagne(grille,lastPlay=None):
    if lastPlay==None:
        return 0
    i=lastPlay[0]
    j=lastPlay[1]
    ligneTest=""
    for element in grille[i]:
        ligneTest=ligneTest+str(element)
    colonneTest=""
    for ligne in grille:
        colonneTest=colonneTest+str(ligne[j])
    diagDescTest=str(grille[i][j])
    diagMontTest=str(grille[i][j])
    for k in range(1,len(grille),1):
        if i+k in range(len(grille)) and j+k in range(len(grille[0])):
            diagDescTest=diagDescTest+str(grille[i+k][j+k])
        if(i-k) in range(len(grille)) and (j-k)in range(len(grille[0])):
            diagDescTest=str(grille[i-k][j-k])+diagDescTest
        if(i-k) in range(len(grille)) and (j+k)in range(len(grille[0])):
            diagMontTest=diagMontTest+str(grille[i-k][j+k])
        if(i+k) in range(len(grille)) and (j-k)in range(len(grille[0])):
            diagMontTest=str(grille[i+k][j-k])+diagMontTest
    
    for element in [ligneTest,colonneTest,diagDescTest,diagMontTest]:
        if "1111" in element : return 1 
        if "2222" in element : return 2 
    return 0

#Retourne une évalutation de la grille à  un état donné
def Utility(grille,dernierCoup,dernierCoup2,profondeur):
    
    joueur=grille[dernierCoup[0]][dernierCoup[1]]
    joueurAdv=1 if joueur==2 else 2
    if AGagne(grille,dernierCoup)==1 : return 1000-profondeur
    if AGagne(grille,dernierCoup)==2 : return -1000+profondeur
    return heuristique1(grille,joueurAdv)+heuristique2(joueurAdv,grille,dernierCoup,dernierCoup2) if profondeur%2==0 else heuristique1(grille,joueur)+heuristique2(joueur,grille,dernierCoup,dernierCoup2)
    
#évaluation d'un noeud min
def MinValue(grille,profondeur,alpha,beta,profondeurMax,dernierCoup,dernierCoup2):
    if TerminalTest(grille,dernierCoup)==True or profondeur==profondeurMax : 
        return Utility(grille,dernierCoup,dernierCoup2,profondeur)
    else:
        v=100000#valeur du coup
        profondeur+=1
        listActions=Actions(grille)
        for cpt in range(len(listActions)):#a est une action/ un coup de la forme (x, y)
            a=listActions[cpt]
            a2=listActions[cpt-1] if cpt>0 else dernierCoup
            v2,ak=MaxValue(Result(grille,a,False),profondeur,alpha,beta,profondeurMax,a,a2)
            v=min(v,v2)
            if v<=alpha : return v
            beta=min(beta,v)
        return v
    
#évaluation d'un noeud max
def MaxValue(grille,profondeur,alpha,beta,profondeurMax,dernierCoup,dernierCoup2=None):
    if TerminalTest(grille,dernierCoup)==True or profondeur==profondeurMax : 
        return Utility(grille,dernierCoup,dernierCoup2,profondeur),(-1,-1)
    else:
        v=-100000#valeur du coup
        listv=[]
        listv.append(v)
        listActions=Actions(grille)
        profondeur+=1
        for cpt in range(len(listActions)):#a est une action/ un coup de la forme (x, y)
            a=listActions[cpt]
            a2=listActions[cpt-1] if cpt>0 else dernierCoup
            listv.append(MinValue(Result(grille,a,True),profondeur,alpha,beta,profondeurMax,a,a2))
            v=max(listv)
            ab=listActions[listv.index(v)-1]#ab est l'action choisie à  retourner par le min 
            if v>=beta :return v,ab
            alpha=max(alpha,v)
        return v,ab
    
#Alpha-beta searching algorithm:
def AlphaBetaSearching(grille,profondeur,profondeurMax,dernierCoup):
    v,ak=MaxValue(grille,profondeur,-100000,100000,profondeurMax,dernierCoup)
    return ak
#Corps principal de l'IA
def iA(compteur,grille,joueur,dernierCoupAdv,dernierCoupIA=None):
    joueurAdv = 2 if joueur == 1 else 1 
    listeCoupsPossibles=Actions(grille)
    if compteur>=3:
        coupVictoire = coupEvident(joueur,dernierCoupIA,grille,listeCoupsPossibles)
        if (coupVictoire != None): return coupVictoire
        coupDefense= coupEvident(joueurAdv,dernierCoupAdv,grille,listeCoupsPossibles)
        if (coupDefense != None): return coupDefense
    
    if compteur==0 : return AlphaBetaSearching(ReinitialiserGrille2(grille),0,4,dernierCoupAdv)
    elif compteur+2<21 : return AlphaBetaSearching(ReinitialiserGrille2(grille),0,5,dernierCoupAdv)
    elif compteur==20 : return -1
    else : return AlphaBetaSearching(ReinitialiserGrille2(grille),0,4,dernierCoupAdv)
#Regarde si 3 pions sont alignés, utilisé pour les coups évidents de l'IA
def checkPionsAlignes(grille,lastPlay=None):
    if lastPlay==None:
        return 0
    i=lastPlay[0]
    j=lastPlay[1]
    ligneTest=""
    for element in grille[i]:
        ligneTest=ligneTest+str(element)
    colonneTest=""
    for ligne in grille:
        colonneTest=colonneTest+str(ligne[j])
    diagDescTest=str(grille[i][j])
    diagMontTest=str(grille[i][j])
    for k in range(1,len(grille),1):
        if i+k in range(len(grille)) and j+k in range(len(grille[0])):
            diagDescTest=diagDescTest+str(grille[i+k][j+k])
        if(i-k) in range(len(grille)) and (j-k)in range(len(grille[0])):
            diagDescTest=str(grille[i-k][j-k])+diagDescTest
        if(i-k) in range(len(grille)) and (j+k)in range(len(grille[0])):
            diagMontTest=diagMontTest+str(grille[i-k][j+k])
        if(i+k) in range(len(grille)) and (j-k)in range(len(grille[0])):
            diagMontTest=str(grille[i+k][j-k])+diagMontTest
    cpt=0
    valeur=["ligne","colonne","diagDesc","diagMont"]
    for element in [ligneTest,colonneTest,diagDescTest,diagMontTest]:
        if "111" in element : return 1, valeur[cpt],element
        cpt+=1
    cpt=0
    for element in [ligneTest,colonneTest,diagDescTest,diagMontTest]:
        if "222" in element : return 2, valeur[cpt],element
        cpt+=1
    return None,None,None
#cherche les coups évidents de défense ou de victoire
def coupEvident(joueur,coup,grille,listeCoupsPossibles):
    a,result,element=checkPionsAlignes(grille,coup)
    
    if result=="colonne" and (coup[0]-1,coup[1]) in listeCoupsPossibles:
        return (coup[0]-1,coup[1])
    elif result=="ligne":
        for i  in range(len(element)-2):
            if element[i]==str(joueur) and element[i+1]==str(joueur) and element[i+2]==str(joueur):
                try:
                    if(coup[0],i-1) in listeCoupsPossibles:
                        return (coup[0],i-1)
                except:
                    print("Erreur d'index")
                try :
                    if (coup[0],i+3) in listeCoupsPossibles:
                        return (coup[0],i+3)
                except:
                    break
        return None 
#Initialiser une grille vide  
def Grille():
    grille=[]
    for i in range(6):
        ligne=[]
        for j in range(12):
            ligne.append(0)
        grille.append(ligne)
    return grille
#Affichage du puissance 4
def AfficherPuissance4(grille):
    
    grille2=[]
    for ligne in grille:
        ligne2=[]
        for element in ligne:
            if element==0: ligne2.append(" . ")
            elif element==1:ligne2.append(" X ")
            else:ligne2.append(" O ")
        grille2.append(ligne2)
    for i,l in enumerate(grille2):
        for j,c in enumerate(grille2[i]):
            k=grille2[i][j]
            print(k,end='')
        print()
    print(" 1  2  3  4  5  6  7  8  9 10 11 12")
    return grille2
#Fonction principale du jeu
compteur=-1
def JeuPuissance4(joueur,grille,dernierCoupAdv,dernierCoupIA=None):
    global compteur
    compteur+=1
    if compteur<21 and joueur==1:
        print("compteur :",compteur)
        print('Tour IA')
        temps = time.time()
        a=iA(compteur,grille,1,dernierCoupAdv,dernierCoupIA)
        print(time.time()-temps)
        print(a[1]+1)
        grille=Result(grille,a,True)
        AfficherPuissance4(grille)
        #if AGagne(grille,a)==1 : print('IA a gagnÃ© !' )
        #if AGagne(grille,a)==2 : print('Joueur a gagnÃ©')
        #if AGagne(grille,a)==0 : print('Match nul' )
    
        #Tour Joueur:
        print('Tour Joueur :')
        j=int(input('Saisissez numÃ©ro de colonne entre 1 et 12'))
        j=j-1
        k=-1
        for i in range(len(grille)-1,-1,-1):
            if grille[i][j]==0:
                k=i
                break
        grille=Result(grille,(k,j),False)
        AfficherPuissance4(grille)
        JeuPuissance4(1,grille,(k,j),a)
    elif compteur<21:
        #Tour Joueur:
        if compteur==0:
            AfficherPuissance4(grille)
        print('Tour Joueur :')
        j=int(input('Saisissez numÃ©ro de colonne entre 1 et 12'))
        j=j-1
        k=-1
        for i in range(len(grille)-1,-1,-1):
            if grille[i][j]==0:
                k=i
                break
        grille=Result(grille,(k,j),False)
        AfficherPuissance4(grille)
        print('Tour IA')
        temps = time.time()
        a=iA(compteur,grille,1,dernierCoupAdv,dernierCoupIA)
        print(time.time()-temps)
        print(a[1]+1)
        grille=Result(grille,a,True)
        AfficherPuissance4(grille)
        JeuPuissance4(2,grille,(k,j),a)

grille2=[ 
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

a=input("commence ? O/N")
joueur=1 if a=='O' else 2
JeuPuissance4(joueur,grille2,(5,7))

