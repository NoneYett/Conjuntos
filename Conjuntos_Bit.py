def cria_relacoes(r,b,elem,arq): #r: relacao atual, b: lista de referencia, elem: numero de elemento, arq: referencia do arquivo.
    aux = 0
    n = elem*elem-1
    #utlizando a lista eh alterado colocando valores de False e True dependendo de qual bit ta ligado(True) ou desligado(False).
    for i in range(elem):
        for j in range(elem):
            b[i][j] = r & (1<<(n-aux)) == 1<<(n-aux) #esse eh o unico momento que a lista eh alterado.
            aux += 1                                 #todo resto do codigo apenas verifica o valor booleano na lista.
    
    #dependendo de qual bit ligado no r, a relacao sera criada.
    resp = '{'                      #Ex: no r = 6 (0110 em binario) com 2 elem, b = [[False,True],[True,False]]
    for i in range(elem):           #b[0][1] = True, resp += (0+1,1+1) = (1,2)
        for j in range(elem):
            if(b[i][j]):
                resp += "("+ str(i+1) + "," + str(j+1) +")"
    resp += '}'

    aux_txt = resp
    arq.write(aux_txt+ " " + classifica(b, elem) + "\n") #Eh chamado a funcao para classificar e dps eh escrito no arquivo a relacao e a classe.

#Funcao para a classificacao
def classifica(b, elem):#Como toda a relacao dos bits ligados estao na lista b, foi usado apenas ela para verificar as classificacoes.
    if(elem == 0):
        return 'STI' # para o caso unico e especifico do numero de elementos ser 0.
    classe = ""                    
    
    #lista aux ajuda na logica da classificacao.
    aux = [True for x in range(4)] #[reflexiva,simetrica,transitiva,irreflexiva]
     
    for i in range(elem):#primeiro for percorre os elementos como numa relacao (x,y).
                         #no caso o i representara o X na relacao usando a lista b para verificar os valores.
        #reflexiva
        if(not b[i][i]):
            aux[0] = False

        for j in range(elem): #o j seria o Y, dai todo o resto utiliza os conceitos logicos de cada classificacao.

            #simetrica
            if(b[i][j] and not b[j][i]):
                aux[1] = False

            #transitiva
            for k in range(elem):
                if(b[i][j] and b[j][k] and not b[i][k]):
                    aux[2] = False

            #Irreflexiva
            if(i == j and b[i][j]):
                aux[3] = False

    #utiliza os valores booleanos da lista aux para concatenar as classificacoes de acordo com o relacao.
    if(aux[0]):
        classe += 'R'
    if(aux[1]):
        classe += 'S'
    if(aux[2]):
        classe += 'T'
    if("R" in classe and "S" in classe and "T" in classe):
        classe += 'E'
    if(aux[3]):
        classe += 'I'

    classe += classificaFuncao(b,elem) #chama a funcao para classificacao das funcoes.

    return classe

def classificaFuncao(b,elem): #responsavel pela classificacao de funcoes.
    #variaveis que auxiliam nas classificacoes de funcao.
    aux_Fi = []
    aux_Fs = False
    Fi = True
    Fs = True
    classe = ''
    #o for aqui usa a mesma logica do for anterior nas classificacoes.
    for i in range(elem):
        
        #Funcao
        aux_F = b[i].count(True) #se em b[i] tiver mais de um valor True significa que existe mais de um elemento na relacao ligado a i.
        if(aux_F == 0 or aux_F > 1):#lembrando que i pode ser pensado como X, entao mais de um valor True significa o mesmo 
                                    #X associado a mais de um Y diferente.       
            return ''    #caso nao seja funcao, ja sera retornado a string vazia sem analisar bijetora, sobrejetora ou injetora.

        for j in range(elem):
            
            #Injetora
            if(b[j][i] and len(aux_Fi) < 1):
                aux_Fi.append(b[j][i])
            elif(b[j][i]):
                Fi = False
            
            #Sobrejetora
            if(b[j][i]):
                aux_Fs = True
                continue
        #daqui para baixo esta fora do segundo for e dentro do primeiro
        #por causa da logica usada para classificar em sobre e injetora esse codigo abaixo dentro do 1 for e necessario
        if(not aux_Fs):
            Fs = False
        aux_Fs = False
                
        aux_Fi = []
    
    #atribui as classes de funcao da relacao
    classe += 'F'
    if(Fi and Fs):
        classe += 'FbFsFi'
    else:
        if(Fs):
            classe += 'Fs'
        if(Fi):
            classe += 'Fi'

    return classe

def arquiva_conjunto(elem): #elem = quantidade de elementos
    b = [[0 for i in range(elem)] for j in range(elem)] #cria a lista que sera usada de referencia o codigo inteiro
    arq = open("Conjunto_de_{}_Elementos.txt".format(elem),'w') 
    for r in range(1<<(elem*elem)):
        cria_relacoes(r,b,elem,arq) #cada r diferente representa uma relacao diferente, no range do numero de elementos ao quadrado
    arq.close()

arquiva_conjunto(3) #Funcao chamada para cria e classificar relacao de 5 elementos
                    #so eh necessario chamar a funcao passando a quantidade de elementos