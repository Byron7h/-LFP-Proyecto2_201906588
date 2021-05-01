if __name__ == '__main__':
    # Análisis de cadena y creación de objeto gramatica 

    # Acá vamos a recibir una cadena y de ella vamos a extraer todos los elementos
    # propios de una gramática

    # https://graphviz.readthedocs.io/en/stable/manual.html
    from tkinter import filedialog
    from produccion import Produccion
    from gramatica import Gramatica
    from graphviz import Digraph
    import webbrowser

    Gramaticas_Leidas = []

    def Evaluar_Tabla():

        if len(Gramaticas_Leidas) > 0 :
            print("Ingrese el nombre de la gramática")
            a = str(input())
            encontrada = False
            for i in range(len(Gramaticas_Leidas)):
                if Gramaticas_Leidas[i].getNombre() == a :
                    encontrada = True
                    break
            if encontrada:
                print("Ingrese la cadena que desea evaluar")
                b = str(input())
                tabla_recorrido(b, Gramaticas_Leidas[i])

            else:
                print("No se encontró la gramática")
        
        else:
            print("Aún no se han ingresado gramáticas")

    def Evaluar_Grafo():

        if len(Gramaticas_Leidas) > 0 :
            print("Ingrese el nombre de la gramática")
            a = str(input())
            encontrada = False
            for i in range(len(Gramaticas_Leidas)):
                if Gramaticas_Leidas[i].getNombre() == a :
                    encontrada = True
                    break
            if encontrada:
                print("Ingrese la cadena que desea evaluar")
                b = str(input())
                recorrido(b, Gramaticas_Leidas[i])

            else:
                print("No se encontró la gramática")
        
        else:
            print("Aún no se han ingresado gramáticas")

    def Mostrar_Grafo():
        if len(Gramaticas_Leidas) > 0 :
            print("Ingrese el nombre de la gramática para generar su autómata")
            a = str(input())
            encontrada = False
            for i in range(len(Gramaticas_Leidas)):
                if Gramaticas_Leidas[i].getNombre() == a :
                    encontrada = True
                    break
            if encontrada:
                arbol_de_gramtica(Gramaticas_Leidas[i], Gramaticas_Leidas[i].getNombre())
            else:
                print("No se encontró la gramática")

    def Mostrar_Nombres():
        if len(Gramaticas_Leidas) > 0 :
            print("La gramáticas disponibles son:")
            for i in range(len(Gramaticas_Leidas)):
                print("     " + str(Gramaticas_Leidas[i].getNombre()))

        else:
            print("Aún no se cuenta con gramáticas registradas")

    def Mostrar_info():

        if len(Gramaticas_Leidas) > 0 :
            print("Ingrese el nombre de la gramática para ver su contenido")
            a = str(input())
            encontrada = False
            for i in range(len(Gramaticas_Leidas)):
                if Gramaticas_Leidas[i].getNombre() == a :
                    encontrada = True
                    break
            if encontrada:
                selec = Gramaticas_Leidas[i]
                print("")
                print("• Nombre de la gramática tipo 2: " + str(selec.getNombre()))
                print("• No terminales: " + str(selec.getNo_Terminales()))
                print("• Terminales: " + str(selec.getTerminales()))
                print("• No terminal inicial: " + str(selec.getS_inicial()))
                print("• Producciones:")
                array = selec.getProducciones()
                for k in range(len(array)):
                    produc = array[k]
                    iz = produc.getSimbolo()
                    der = produc.getProducciones()
                    print("   " + str(iz) + " -> " + str(der[0]))
                    if len(der)> 1:
                        for w in range(len(der)-1):
                            print("        | " + str(der[w+1]))
            else:
                print("No se encontró la gramática")

    def tabla_recorrido(cadena, gramatica):

        Doc = open('Tabla_Transiciones.html',mode="w", encoding="utf-8")

        inicio ="""
        <link href="estilo_tabla.css" rel="stylesheet">
        <body>
        <div id="wrapper">
        <h1>Reporte en tabla</h1>
     
        <table id="keywords" cellspacing="0" cellpadding="0">
        <thead>
        <tr>
           <th><span>Iteración</span></th>
           <th><span>Pila</span></th>
           <th><span>Entrada</span></th>
           <th><span>Transición</span></th>
        </tr>
       </thead>
        <tbody>"""
        Doc.write(inicio)

        iteracion = 0
        transicion = ""

        cadena = cadena + str("#")
        alfabeto = gramatica.getTerminales()
        simbolos_pila = gramatica.getTerminales() + gramatica.getNo_Terminales()
        simbolos_pila.append("#")

        posicion = 0
        estado = "So"
        pila = []
        error = False
        razon = ""
        

        while posicion < len(cadena) and error == False:
            entrada = str(cadena[posicion])
            if entrada in simbolos_pila :

                if estado == "So":
                    pila.append("#")
                    estado = "S1"
                    transicion = "λ, λ, #"

                elif estado == "S1":
                    pila.append(str(gramatica.getS_inicial()))
                    estado = "S2"
                    transicion = "λ, λ, " + str(gramatica.getS_inicial())

                elif estado == "S2":

                    top = str(pila[-1]).rstrip().lstrip()
                    if top in gramatica.getNo_Terminales():
                        produc_simbolo = []
                        existe = False
                        producciones = gramatica.getProducciones()
                        for i in range(len(producciones)):

                            simbolo = str(producciones[i].getSimbolo()).rstrip().lstrip()
                            if simbolo == top:
                                produc_simbolo = producciones[i].getProducciones()               
                                existe = True
                                break
                        if existe:
                            opciones = len(produc_simbolo)
                            if opciones == 1:
                                pila.pop()
                                array_produccion = produc_simbolo[0]
                                tamano = len(array_produccion) - 1
                                
                                
                                for i in range(tamano+1):
                                    if array_produccion[tamano] != " ":
                                        pila.append(array_produccion[tamano])
                                    tamano = tamano - 1
                                
                                doc_produ = ""
                                for h in range(len(array_produccion)):                     
                                    doc_produ = doc_produ + str(array_produccion[h])
                                transicion = "λ, " + str(top) + ", "+ doc_produ


                            elif opciones > 1 :
                                elegida = []



                                # •••   Validacion 1
                                for i in range(opciones):
                                    array_produccion = produc_simbolo[i]
                                    if entrada == array_produccion[0]:
                                        elegida.append(array_produccion)

                                # •••   Validacion 2
                                if len(elegida) > 1:
                                    elegida_2 = []

                                    
                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 1:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 1 and str(cadena[posicion+1]) == array_produccion[1]:
                                            elegida_2.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_2




                                # •••   Validacion 3
                                if len(elegida) > 1:
                                    elegida_3 = [] 

                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 2:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 2  and str(cadena[posicion + 2]) == array_produccion[2]:
                                            elegida_3.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_3


                                if len(elegida) == 1:

                                    # Si entra acá quiere decir que solo hay una opció posible
                                    pila.pop()
                                    # Metiendo a la píla
                                    array_produccion = elegida[0]
                                    tamano = len(array_produccion) - 1

                                    for i in range(tamano+1):
                                        if array_produccion[tamano] != " ":
                                            pila.append(array_produccion[tamano])
                                        tamano = tamano - 1



                                    doc_produ = ""
                                    for h in range(len(array_produccion)):                     
                                        doc_produ = doc_produ + str(array_produccion[h])
                                    transicion = "λ, " + str(top) +", " + doc_produ


                                elif len(elegida) != 1:

                                    if len(elegida) > 1:
                                        error = True
                                        razon = "No se incluyeron suficientes validaciones"
                                    if len(elegida) < 1: 

                                        error = True
                                        razon = "Simbolo mal colocado"
                                    # ••• Acá debemos explorar las producciones posibles de las producciones posibles
                                        pass

                        
                        else:
                            error = True
                            razon = "El simbolo no cuenta con producciones asociadas" 


                    elif top in gramatica.getTerminales():
                        if entrada == top:
                            posicion = posicion + 1
                            pila.pop()
                            transicion = str(top) + ", " + str(top) + ", λ" 
                        else:
                            error = True
                            razon = "El simbolo de entrada no coincide con el top de la pila" 
                        
                    elif top == "#":
                        if entrada == top:
                            estado = "S3"
                            transicion = "#, #, λ" 

                        else:
                            error = True
                            razon = "Se acabaron los simbolos en la pila sin llegar al simbolo de aceptación en la entrada" 

                    else:
                        error = True
                        razon = "El simbolo no pertenece al lenguaje reconocido por el autómata"

                elif estado == "S3":
                    posicion = posicion + 1
                    pila.pop()
                    entrada = ""
                    transicion = "Aceptación"    


            else :
                error = True
                razon = "El simbolo de la entrada no pertenece al lenguaje que reconoce el autómata"

            doc_pila = ""
            for q in range(len(pila)):
                doc_pila = doc_pila + str(pila[q])


            if error:

                Doc.write("<tr>\n")
                Doc.write("<td>")
                Doc.write("Error")
                Doc.write("</td>\n")

                Doc.write("<td>")
                Doc.write(str(doc_pila))
                Doc.write("</td>\n")

                Doc.write("<td>")
                Doc.write(str(entrada))
                Doc.write("</td>\n")


                Doc.write("<td>")
                Doc.write(razon)
                Doc.write("</td>\n")
                Doc.write("</tr>\n")

            else:    
                iteracion += 1
                Doc.write("<tr>\n")
                Doc.write("<td>")
                Doc.write(str(iteracion))
                Doc.write("</td>\n")

                Doc.write("<td>")
                Doc.write(str(doc_pila))
                Doc.write("</td>\n")

                Doc.write("<td>")
                Doc.write(str(entrada))
                Doc.write("</td>\n")


                Doc.write("<td>")
                Doc.write(transicion)
                Doc.write("</td>\n")
                Doc.write("</tr>\n")


        final = """
        </tbody>  
        </table>
        </div> 
        </body>
        """
        Doc.write(final)
        Doc.close()

        webbrowser.open_new('Tabla_Transiciones.html')

    def arbol_de_recorrido(gramatica, estado, produccion, id):

        nombre = str(id)
        g = Digraph( nombre , format ='jpg')
        g.attr( rankdir= "LR" , charset= "UTF-8")
        g.attr('node', shape='circle', fontsize = "20.0", fontname = "Arial Black")
        g.attr('edge', shape='normal', fontname = "Arial Black")

        label_So = "λ, λ, " + str(gramatica.getS_inicial())
        label_S_NT= ""
        producciones = gramatica.getProducciones()

        terminales = gramatica.getTerminales()


        if estado != "S2":
            for i in range(len(terminales)):
                nuevo = str(terminales[i]) + ", " + str(terminales[i]) + ", λ \n"
                label_S_NT = label_S_NT + nuevo
            
            for i in range(len(producciones)):
                array = producciones[i].getProducciones()
                simbolo = str(producciones[i].getSimbolo())
                for e in range(len(array)):
                    cadena_aux = ""
                    array = array[e]
                    for j in range(len(array)):
                        cadena_aux = cadena_aux + str(array[j])
                    nuevo = "λ, " + simbolo + ", " + cadena_aux + "\n"
                    label_S_NT = label_S_NT + nuevo

        if estado == "So":
            g.attr('node', shape='circle', color="crimson", fontcolor = "crimson" )
            g.node("n1", "So")
            g.attr('node', shape='circle', color="black", fontcolor = "black" )           
        else:
            g.node("n1", "So")

        if estado == "S1":
            g.attr('node', shape='circle', color="crimson", fontcolor = "crimson")
            g.node("n2", "S1")
            g.attr('node', shape='circle', color="black", fontcolor = "black")            
        else:
            g.node("n2", "S1")

        if estado == "So":
            g.attr('edge', shape='normal', fontcolor="crimson" )
            g.edge("n1", "n2", label = "λ, λ, #", fontsize = "20.0")
            g.attr('edge', shape='normal', fontcolor="black" )          
        else:
            g.edge("n1", "n2", label = "λ, λ, #", fontsize = "20.0")

        if estado == "S2" :
            g.attr('node', shape='circle', color="crimson", fontcolor = "crimson" )
            g.node("n3", "S2", width="1", height="1")
            g.attr('node', shape='circle', color="black", fontcolor = "black" )            
        else:
            g.node("n3", "S2", width="1", height="1")

        if estado == "S1":
            g.attr('edge', shape='normal', fontcolor="crimson" )
            g.edge("n2", "n3", label = label_So, fontsize = "20.0")
            g.attr('edge', shape='normal', fontcolor="black" )          
        else:
            g.edge("n2", "n3", label = label_So, fontsize = "20.0")
        
        if estado == "S2":
            g.attr('edge', shape='normal', fontcolor="crimson" )
            g.edge("n3", "n3", label = produccion , fontsize = "20.0")
            g.attr('edge', shape='normal', fontcolor="black" )          
        else:
            g.edge("n3", "n3", label = label_S_NT, fontsize = "20.0")

        if estado == "S3":
            g.attr('node', shape='doublecircle', color="crimson", fontcolor = "crimson" )
            g.node("n4", "S3")
        else:
            g.attr('node', shape='doublecircle')

        g.edge("n3", "n4", label = "#, #, λ", fontsize = "20.0")
        g.render()
       
    def recorrido(cadena, gramatica):
        Doc = open('Recorrido.html',mode="w", encoding="utf-8")

        inicio ="""
        <meta charset="UTF-8">
        <link rel="stylesheet" href="Estilo_Recorrido.css">
        <div class="cont_principal">"""
        Doc.write(inicio)

        iteracion = 0
        transicion = ""

        cadena = cadena + str("#")
        alfabeto = gramatica.getTerminales()
        simbolos_pila = gramatica.getTerminales() + gramatica.getNo_Terminales()
        simbolos_pila.append("#")

        posicion = 0
        estado = "So"
        pila = []
        error = False
        razon = ""
        

        while posicion < len(cadena) and error == False:
            entrada = str(cadena[posicion])
            if entrada in simbolos_pila :

                if estado == "So":
                    pila.append("#")
                    estado = "S1"
                    transicion = "λ, λ, #"

                elif estado == "S1":
                    pila.append(str(gramatica.getS_inicial()))
                    estado = "S2"
                    transicion = "λ, λ, " + str(gramatica.getS_inicial())

                elif estado == "S2":

                    top = str(pila[-1]).rstrip().lstrip()
                    if top in gramatica.getNo_Terminales():
                        produc_simbolo = []
                        existe = False
                        producciones = gramatica.getProducciones()
                        for i in range(len(producciones)):
                            simbolo = str(producciones[i].getSimbolo()).rstrip().lstrip()
                            if simbolo == top:
                                produc_simbolo = producciones[i].getProducciones()               
                                existe = True
                                break
                        if existe:
                            opciones = len(produc_simbolo)
                            if opciones == 1:
                                pila.pop()
                                array_produccion = produc_simbolo[0]
                                tamano = len(array_produccion) - 1
                                
                                
                                for i in range(tamano+1):
                                    if array_produccion[tamano] != " ":
                                        pila.append(array_produccion[tamano])
                                    tamano = tamano - 1
                                
                                doc_produ = ""
                                for h in range(len(array_produccion)):                     
                                    doc_produ = doc_produ + str(array_produccion[h])
                                transicion = "λ, " + str(top) + ", "+ doc_produ


                            elif opciones > 1 :
                                elegida = []



                                # •••   Validacion 1
                                for i in range(opciones):
                                    array_produccion = produc_simbolo[i]
                                    if entrada == array_produccion[0]:
                                        elegida.append(array_produccion)

                                # •••   Validacion 2
                                if len(elegida) > 1:
                                    elegida_2 = []

                                    
                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 1:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 1 and str(cadena[posicion+1]) == array_produccion[1]:
                                            elegida_2.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_2




                                # •••   Validacion 3
                                if len(elegida) > 1:
                                    elegida_3 = [] 

                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 2:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 2  and str(cadena[posicion + 2]) == array_produccion[2]:
                                            elegida_3.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_3


                                if len(elegida) == 1:

                                    # Si entra acá quiere decir que solo hay una opció posible
                                    pila.pop()
                                    # Metiendo a la píla
                                    array_produccion = elegida[0]
                                    tamano = len(array_produccion) - 1

                                    for i in range(tamano+1):
                                        if array_produccion[tamano] != " ":
                                            pila.append(array_produccion[tamano])
                                        tamano = tamano - 1



                                    doc_produ = ""
                                    for h in range(len(array_produccion)):                     
                                        doc_produ = doc_produ + str(array_produccion[h])
                                    transicion = "λ, " + str(top) +", " + doc_produ


                                elif len(elegida) != 1:

                                    if len(elegida) > 1:
                                        error = True
                                        razon = "No se incluyeron suficientes validaciones"

                                    if len(elegida) < 1: 

                                        error = True
                                        razon = "Simbolo mal colocado"
                                    # ••• Acá debemos explorar las producciones posibles de las producciones posibles
                                        pass

                        
                        else:
                            error = True
                            razon = "El simbolo no cuenta con producciones asociadas" 
                    

                    elif top in gramatica.getTerminales():
                        if entrada == top:
                            posicion = posicion + 1
                            pila.pop()
                            transicion = str(top) + ", " + str(top) + ", λ" 
                        else:
                            error = True
                            razon = "El simbolo de entrada no coincide con el top de la pila" 
                        
                    elif top == "#":
                        if entrada == top:
                            estado = "S3"
                            transicion = "#, #, λ" 

                        else:
                            error = True
                            razon = "Se acabaron los simbolos en la pila sin llegar al simbolo de aceptación en la entrada" 

                    else:
                        error = True
                        razon = "El simbolo no pertenece al lenguaje reconocido por el autómata"

                elif estado == "S3":
                    posicion = posicion + 1
                    pila.pop()
                    entrada = ""
                    transicion = "Aceptación"    



            else :
                error = True
                razon = "El simbolo de la entrada no pertenece al lenguaje que reconoce el autómata"
            doc_pila = ""
            for q in range(len(pila)):
                doc_pila = doc_pila + str(pila[q])


            if error:

                Doc.write("<h2>")
                Doc.write("ERROR")
                Doc.write("</h2>\n")
                Doc.write("<h2>")
                Doc.write(razon)
                Doc.write("</h2>\n")
                Doc.write("<br />\n")
                Doc.write("<br />\n")


            else:
                Doc.write("<br />\n")
                Doc.write("<h2>")
                Doc.write("Entrada: " + str(entrada))
                Doc.write("</h2>\n")
                Doc.write("<h2>")
                Doc.write("Pila: " + doc_pila )
                Doc.write("</h2>\n")

                Doc.write("""<div class="cont_imgs">\n""")
                Doc.write("""<div class="cont_img_1" data-shx-size="6" >\n""")
                
                iteracion = iteracion + 1

                arbol_de_recorrido(gramatica, estado, transicion, iteracion)

                Doc.write("""<img src='""")
                Doc.write(str(iteracion))
                Doc.write(""".gv.jpg' class="imagen_ejemplo" alt="" />\n""")
                Doc.write("</div>\n")
                Doc.write("</div>\n")



        final = """
        </div>
        """
        Doc.write(final)
        Doc.close()

        webbrowser.open_new('Recorrido.html')

    def arbol_de_gramtica(gramatica, nombre):

        name = "AP_" + str(nombre)
        g = Digraph('G', filename= name )
        g.attr( rankdir= "LR" , charset= "UTF-8")
        g.attr('node', shape='circle')
        g.attr('edge', shape='normal')


        label_So = "λ, λ, " + str(gramatica.getS_inicial())
        label_S_NT= ""
        producciones = gramatica.getProducciones()

        terminales = gramatica.getTerminales()

        for i in range(len(terminales)):
            nuevo = str(terminales[i]) + ", " + str(terminales[i]) + ", λ \n"
            label_S_NT = label_S_NT + nuevo
            
        for i in range(len(producciones)):
            array = producciones[i].getProducciones()
            simbolo = str(producciones[i].getSimbolo())
            for e in range(len(array)):
                cadena_aux = ""
                array = array[e]
                for j in range(len(array)):
                    cadena_aux = cadena_aux + str(array[j])
                nuevo = "λ, " + simbolo + ", " + cadena_aux + "\n"
                label_S_NT = label_S_NT + nuevo

        g.node("n1", "So")
        g.node("n2", "S1")
        g.edge("n1", "n2", label = "λ, λ, #", fontsize = "16.0") 
        g.node("n3", "S2", width="1", height="1")
        g.edge("n2", "n3", label = label_So, fontsize = "16.0")
        g.edge("n3", "n3", label = label_S_NT, fontsize = "16.0")
        g.attr('node', shape='doublecircle')
        g.node("n4", "S3")
        g.edge("n3", "n4", label = "#, #, λ", fontsize = "16.0")
        g.view()
        
    def resolver_autómata(cadena, gramatica):
        cadena = cadena + str("#")



        # Vamos siguiendo los pasos que nos da el libro

        #  1. Designamos alfabeto y simbolos de pila}
        #      • Terminales a,b,z 
        #      • No teminales S, A, B, C
        #  Alfabeto = terminales de la gramática
        #  simbolos de pila = terminales y no terminales junto con el símbolo de aceptación

        alfabeto = gramatica.getTerminales()
        simbolos_pila = gramatica.getTerminales() + gramatica.getNo_Terminales()
        simbolos_pila.append("#")

        #  Acá vamos a manejar la cadena entrante como en un dfa, llendo de 
        #  posición a posición 
        posicion = 0
        #  Creamos nuestra variable para ir moviendonos entre estados
        estado = "So"
        # Instanciamos nuestra pila
        pila = []


        #  2. Designamos los 4 estados estándar de un autómata de píla
        #     Desde acá podemos empezar a hacer nuestro ciclo, al parecer
        #     es esto de autómatas se usa bastante el while, por no necesariamente
        #     avanzar en la entrada a un ritmo uniforme, si no que dependemos bastanmte
        #     de las condiciones que se den, lo que venga en la entrada y lo que esté en la pila

        error = False
        razon = ""
        

        while posicion < len(cadena) and error == False:
            #Acá vamos a ir extrayendo los valores del actual y del siguiente
            # del actual para poder elegir entre las dierentes opciones de sustitución
            # de un no terminal 
            entrada = str(cadena[posicion])

            # Verificando que la entrada sea válida
            if entrada in simbolos_pila :
            


            #  3. Metemos el estado de aceptación a la pila
            #     acá metemos # a la pila y cambiamos de estado

                if estado == "So":
                    pila.append("#")
                    estado = "S1"
            #  4. Ya en el estado S1 nos pasamos al estado S2 y metemos
            #     el símbolo inicial de la gramática a la pila
                elif estado == "S1":
                    pila.append(str(gramatica.getS_inicial()))
                    estado = "S2"

                elif estado == "S2":
                # Acá empieza lo interesante, como hacer que acepte gramáticas de forma dinámica
                    #Primero debemos saber si lo que está en el top de la pila es un Terminal o un no Terminal

                    top = str(pila[-1]).rstrip().lstrip()
                    if top in gramatica.getNo_Terminales():
                        # Recordemos, si es un terminal primero debemos ver si existe más de una producción
                        # Para el símbolo que estamos analizando, nosotros ya tenemos todas las gramáticas agru
                        # padas por simbolo terminal en el array produuciones

                        produc_simbolo = []
                        existe = False
                        producciones = gramatica.getProducciones()
                        for i in range(len(producciones)):

                            simbolo = str(producciones[i].getSimbolo()).rstrip().lstrip()

                            if simbolo == top:
                                produc_simbolo = producciones[i].getProducciones()               
                                existe = True
                                break
                        if existe:

                            #Llegando a este punto sabemos que:
                            # • El símbolo en la pila es un no terminal
                            # • El símbolo de la pila tiene producciones asociadas y ya
                            #   las tenemos en la varible produc_simbolo

                            # Si es no terminal hay 2 opciones

                            # Ahora nos falta elegir que producción de las disponibles usar
                            # Si solo existe una, pues ponemos esa

                            opciones = len(produc_simbolo)

                            if opciones == 1:
                                 #Acá no nos interesa la entrada, solo debemos sacar el simbolo
                                # que queremos sustituir deñ top de la pila y colocar la sustitución 
                                # en la pila, de atrás para delante
                                pila.pop()

                                # Metiendoa la píla
                                array_produccion = produc_simbolo[0]
                                tamano = len(array_produccion) - 1

                                for i in range(tamano+1):
                                    if array_produccion[tamano] != " ":
                                        pila.append(array_produccion[tamano])
                                    tamano = tamano - 1


                            elif opciones > 1 :

                                # Introduccimos el concepto de elegida, que será el camino que escogemos
                            
                                elegida = []

                                # ••• Analizamos la primera posicón de las posibles producciones
                                #       y las comparamos con la entrada para encontrar coincidencias
                                #       las cuales llevaremos a elegida
                            


                                # •••   Validacion 1
                                for i in range(opciones):
                                    array_produccion = produc_simbolo[i]
                                    if entrada == array_produccion[0]:
                                        elegida.append(array_produccion)

                                # •••   Validacion 2
                                if len(elegida) > 1:
                                    elegida_2 = []

                                    
                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 1:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 1 and str(cadena[posicion+1]) == array_produccion[1]:
                                            elegida_2.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_2




                                # •••   Validacion 3
                                if len(elegida) > 1:
                                    elegida_3 = [] 

                                    for i in range(len(elegida)):
                                        array_produccion = elegida
                                        if len(array_produccion[i]) == 2:
                                            elegida_2.append(array_produccion[i])

                                    for i in range(len(elegida)):
                                        array_produccion = elegida[i]
                                        if len(array_produccion) > 2  and str(cadena[posicion + 2]) == array_produccion[2]:
                                            elegida_3.append(array_produccion)
                                    elegida = []
                                    elegida = elegida_3


                                if len(elegida) == 1:

                                    # Si entra acá quiere decir que solo hay una opció posible
                                    pila.pop()
                                    # Metiendo a la píla
                                    array_produccion = elegida[0]
                                    tamano = len(array_produccion) - 1

                                    for i in range(tamano+1):
                                        if array_produccion[tamano] != " ":
                                            pila.append(array_produccion[tamano])
                                        tamano = tamano - 1

                                elif len(elegida) != 1:

                                    if len(elegida) > 1:
                                        error = True
                                        razon = "No se incluyeron suficientes validaciones"

                                    if len(elegida) < 1: 

                                        error = True
                                        razon = "Simbolo mal colocado"
                                    # ••• Acá debemos explorar las producciones posibles de las producciones posibles
                                        pass                        
                        else:
                            error = True
                            razon = "El simbolo no cuenta con producciones asociadas" 
                        

                    elif top in gramatica.getTerminales():
                        if entrada == top:
                            posicion = posicion + 1
                            pila.pop()
                        else:
                            error = True
                            razon = "El simbolo de entrada no coincide con el top de la pila" 
                        
                    elif top == "#":
                        if entrada == top:
                            estado = "S3"
                            pila.pop()

                        else:
                            error = True
                            razon = "Se acabaron lo0s simbolos en la pila sin llegar al simbolo de aceptación en la entrada" 
                    else:
                        error = True
                        razon = "El simbolo no pertenece al lenguaje reconocido por el autómata"

                elif estado == "S3":

                    posicion = posicion + 1   


            else :
                error = True
                razon = "El simbolo de la entrada no pertenece al lenguaje que reconoce el autómata"

    def Leer_archivo(nombre_archivo):

        archivo = open(nombre_archivo, mode="r", encoding="utf-8")
        posicion = 0 
        producciones = []
        for line in archivo.readlines():
            valor = str(line)
            valor = valor.rstrip().lstrip() # Le quitamos los espacios al final y al inicio
                                        # al valor porque sin esto no nos reconoce el *
            if valor != "*":
                if posicion == 0:
                    nombre = valor

                elif posicion == 1:
                    listas = valor.split(";")

                    #Extrayendo datos
                    cadena = listas[0]
                    no_terminales = []
                    for i in range(len(cadena)):
                        if cadena[i] != ",":
                            no_terminales.append(cadena[i])
                    
                    cadena = listas[1]
                    terminales = []
                    for i in range(len(cadena)):
                        if cadena[i] != ",":
                            terminales.append(cadena[i])

                    s_inicial = listas[2]

            
                else:
                    produccion = valor.split("->")
                    derecho = str(produccion[0]).rstrip().lstrip()
                    izq = str(produccion[1]).rstrip().lstrip()
                    izquierdo = []

                    for q in range(len(izq)):
                        if izq[q] != " " :
                            izquierdo.append(izq[q])
        
                    if len(producciones) == 0:
                        nuevo = Produccion(derecho, [izquierdo])
                        producciones.append(nuevo)
                    else:
                        es_nuevo = True
                        for i in range(len(producciones)):
                            if derecho == producciones[i].getSimbolo():
                                producciones[i].producciones.append(izquierdo)
                                es_nuevo = False
                                break
                        if es_nuevo:        
                            nuevo = Produccion(derecho, [izquierdo])
                            producciones.append(nuevo)
                posicion +=1
            else:

                for j in range(len(producciones)):
                    p = producciones[j]
                    g = p.getProducciones()



                nuevo = Gramatica(nombre, no_terminales, terminales, s_inicial, producciones)
                Gramaticas_Leidas.append(nuevo)
                posicion = 0
                producciones = []
        archivo.close()
        #arbol_de_gramtica(Gramaticas_Leidas[0])
        #resolver_autómata("zzbbbzbbbz", Gramaticas_Leidas[0])
        #tabla_recorrido("zzbbbzbbbz", Gramaticas_Leidas[0])
        #recorrido("zzbbbUbbbz", Gramaticas_Leidas[0])
        #arbol_de_recorrido(Gramaticas_Leidas[0],)
    
    def Seleccionar_archivo():
        nombre_archivo =  filedialog.askopenfilename(title = "Select file")
        Leer_archivo(nombre_archivo)

    def presentacion():
        print("")
        print("::::::::::::::   Proyecto 2 - LFP  ::::::::::::::")
        print("")
        print("LENGUAJES FORMALES Y DE PROGRAMACION Sección A+")
        print("Nombre: Byron Estuardo Solís González")
        print("Carné : 201906588")
        print("")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                 ¡Bienvenido!                    ")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::")
        print("")

    def Menu_principal():
        print("")
        print("Menú Principal:")
        print("     1. Cargar archivo")
        print("     2. Mostrar información general de la gramática")
        print("     3. Generar autómata de pila equivalente")
        print("     4. Reporte de recorrido")
        print("     5. Reporte en tabla")
        print("     6. Salir")
        print("Ingrese una opción:")
        print("")
        a = int(input())
        if a == 1:
            try:
                print("Seleccione un archivo")
                Seleccionar_archivo()
            except:
                print("No se pudo leer el archivo")
            Menu_principal()     

        elif a == 2:
            Mostrar_Nombres()
            Mostrar_info()
            Menu_principal()
        elif a == 3:
            Mostrar_Nombres()
            Mostrar_Grafo()
            Menu_principal()
        elif a == 4:
            Evaluar_Grafo()
            Menu_principal()
        elif a == 5:
            Evaluar_Tabla()
            Menu_principal()
        elif a == 6:
            print("¡ Gracias por usar la aplicación !")
            pass

    presentacion()
    Menu_principal()

