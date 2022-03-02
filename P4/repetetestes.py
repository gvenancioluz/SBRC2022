#!/usr/bin/env python
import sys
import struct
import os
import time
import random

def main():
    #argumento 2 = numero repeticoes
    for i in range(int(sys.argv[2])):
        varPodSrc=0
        varPodDst=0
        varHostSrc=0
        varHostDst=0
        while varPodSrc==varPodDst:
            varPodSrc=random.randint(1,4)
            varPodDst=random.randint(1,4)
            #if (sys.argv[1]==1) and ((varPodDst+1==varPodSrc) or (varPodDst==4 and varPodSrc==1)):
            #    varPodSrc=varPodDst 
        varHostSrc=random.randint(1,4)
        varHostDst=random.randint(1,4)
        #forca determinado teste
        #varHostSrc=3
        #varPodSrc=4
        #varHostDst=4
        #varPodDst=2
        
        file = open("teste.txt", 'w')
        file.write(str(sys.argv[1])+str(sys.argv[3])+"-"+str(varHostSrc)+"-"+str(varPodSrc)+"-"+str(varHostDst)+"-"+str(varPodDst)+"\n")
        file.close()
       
        file = open("/home/p4/FRRFTK4/P4/script_mininet."+str(sys.argv[3]),'w')
        file.write("sh sleep 10 \n")
        
        if sys.argv[1] == "ufscar2":
            file.write("sh /home/p4/FRRFTK4/pod-topo/nomeia_sw.sh \n")
        
        file.write("sh /home/p4/FRRFTK4/Control/gatilhodown-randomico \n")
        file.write("xterm h"+str(varHostSrc)+"c"+str(varPodSrc)+" h"+str(varHostDst)+"c"+str(varPodDst)+" \n")
        file.write("sh sleep 90 \n")
        file.close()

        file = open("/home/p4/FRRFTK4/Control/gatilhodown-randomico",'w')
        file.write("cd /home/p4/FRRFTK4/Control/ \n")
        
        #se for codigo p4 limpo precisa rodar controller
        if sys.argv[1] == "limpo":
            file.write("./controller.py & \n")

        #um erro no core para acesso ao pod destino
        if sys.argv[3] == "1":
            if varHostSrc<=2:
                #switch S1CORE
                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")              
            else:
                #switch S3CORE
                file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                
        
        #dois erro no core para acesso ao pod destino (rota principal e backup)
        if sys.argv[3] == "2":
            if varHostSrc<=2:
                #switch S1CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S1CORE porta backup
                
                if varPodDst<4:
                    file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst+1)+"down250.txt \n")
                    file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst+1)+" < gatilhoporta3down250.txt \n")
                else:
                    file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(1)+"down250.txt \n")
                    file.write("simple_switch_CLI  --thrift-port "+str(9100)+" < gatilhoporta3down250.txt \n")
            else:
                #switch S3CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S3CORE porta backup
                if varPodDst<4:
                    file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst+1)+"down250.txt \n")
                    file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst+1)+" < gatilhoporta3down250.txt \n")
                else:
                    file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(1)+"down250.txt \n")
                    file.write("simple_switch_CLI  --thrift-port "+str(9105)+" < gatilhoporta3down250.txt \n")
    
        #dois erros na agregacao destino... erro sequencial
        if sys.argv[3] == "3":
            if varHostSrc<=2:
                #switch S1CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S2CORE porta backup
                file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta4down250.txt \n")
            else:
                #switch S3CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S4CORE porta backup
                file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta4down250.txt \n")


        #dois erros na agregacao prinicpal destino + um erro na agregacao backup destino
        if sys.argv[3] == "4":
            if varHostSrc<=2:
                #switch S1CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S2CORE porta princial
                file.write("simple_switch_CLI  --thrift-port 9099 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta4down250.txt \n")
                #switch S3CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
            else:
                #switch S3CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9104 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta3down250.txt \n")
                #switch S4CORE porta backup
                file.write("simple_switch_CLI  --thrift-port 9109 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9104+varPodDst)+" < gatilhoporta4down250.txt \n")
                #switch S1CORE porta principal
                file.write("simple_switch_CLI  --thrift-port 9094 < gatilhoporta"+str(varPodDst)+"down250.txt \n")
                file.write("simple_switch_CLI  --thrift-port "+str(9099+varPodDst)+" < gatilhoporta3down250.txt \n")

        file.close()
        #vai chamar o bash m que executa o mininet
        #argumento 1 = nome do teste
        #argumento 3 = erro
        os.system("/home/p4/FRRFTK4/m "+str(sys.argv[1])+" "+str(sys.argv[3]))
        time.sleep(random.randint(10,25))
if __name__ == '__main__':
    main()
