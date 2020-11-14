import cv2
import serial
import time

def serial_enviar(letra):
    #time.sleep(1)
    textoSaida = letra
    ser.write(textoSaida.encode()) 
    #time.sleep(1)

def Area_central(folga, b0, b1, b2 ,b3):
    QX = int(b2)
    QY = int(b3)
    M1 = (340 - folga) - (QX/2) #680x470
    M2 = (340 + folga) + (QX/2)
    M3 = (235 - folga) - (QY/2)
    M4 = (235 + folga) + (QY/2)
    p1Q = (int(M1), int(M3))  
    p2Q = (int(M2), int(M4))  
    cv2.rectangle(frame, p1Q, p2Q, (0,255,0), 2, 2)
    return M1,M2,M3,M4

#pip3 install opencv-contrib-python
#Apertar ESC para abrir a janela de seleção
tracker = cv2.TrackerKCF_create() #TrackerKCF_create() > Padrão
                                   #TrackerCSRT_create() >Segue bem, mas não salva o padrão e sim entende o movimento
                                   #TrackerTLD_create()
x = 0
video = cv2.VideoCapture(0) #chamar abertura da webcam
ser = serial.Serial('COM8', 9600)
time.sleep(1)
while 1:
    while True: #enquanto o video continua rodando
        k,frame = video.read() #uma parte do video será selecionada
        cv2.imshow("Tracking",frame) #captura frame a ser levado em consideração
        k = cv2.waitKey(30) & 0xff #tecla precisa ser acionada para retornar a camera em Live
        if k == 27: #se não esperará 27s
            break
    bbox = cv2.selectROI(frame, False) #caixa a parte aberta para seleção do frame relevante

    ok = tracker.init(frame, bbox) #começa a seguir a caixa delimitada

    cv2.destroyWindow("ROI selector") #Janela de tracking não fecha sozinha nem clincando por isso essa função

    

    while True:
        ok, frame = video.read() #começa a ler o video novamente
        ok, bbox = tracker.update(frame) #atualiza as imagens da Webcam para manter o tracking com a caixa delimitada


        if ok:
            p1 = (int(bbox[0]), int(bbox[1])) # até a linha 25 trata-se do desenho do retangulo recebendo as variaveis demilimitadoras dentro da variavel BBOX
            p2 = (int(bbox[0] + bbox[2]),
                int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,0,255), 2, 2) #Somente as cores das linhas do retangulo desenhado
            print(p1 , p2) #Coordenadas do retangulo
            
        folga_principal = 12
        M1 = Area_central(folga_principal, bbox[0],bbox[1],bbox[2],bbox[3])[0]
        M2 = Area_central(folga_principal, bbox[0],bbox[1],bbox[2],bbox[3])[1]
        M3 = Area_central(folga_principal, bbox[0],bbox[1],bbox[2],bbox[3])[2]
        M4 = Area_central(folga_principal, bbox[0],bbox[1],bbox[2],bbox[3])[3]


        folga_v1 = 20  #dentro dessa região, a velocidade em que o servo se moverá é menor e possui um delay
        Qv1_1 = (int(M1 - folga_v1),int(M3 - folga_v1) )
        Qv1_2 = (int(M2 + folga_v1),int(M4 + folga_v1) )
        cv2.rectangle(frame, Qv1_1, Qv1_2, (255,0,255), 2, 2)

        folga_v2 = 70 #dentro dessa região, a velocidade em que o servo se moverá é menor e NÂO possui um delay
        Qv2_1 = (int(M1 - folga_v2),int(M3 - folga_v2) )
        Qv2_2 = (int(M2 + folga_v2),int(M4 + folga_v2) )
        cv2.rectangle(frame, Qv2_1, Qv2_2, (234,215,125), 2, 2)
        #fora da região de V2, o servo se moverá 5° por vez

        if(int(bbox[0]) <M1 and int(bbox[0]) > M1 - folga_v1 ):
            serial_enviar('a')
            time.sleep(0.1)
        elif(int(bbox[0]) < M1 - folga_v1 and int(bbox[0]) > M1 - folga_v2):
            serial_enviar('a')
        elif(int(bbox[0]) < M1 - folga_v2):
            serial_enviar('aa')

        if(int(bbox[0] + bbox[2]) > M2 and int(bbox[0] + bbox[2]) < M2 + folga_v1):
            serial_enviar('c')
            time.sleep(0.1)
        elif(int(bbox[0] + bbox[2]) > M2 + folga_v1 and int(bbox[0] + bbox[2]) < M2 + folga_v2):
            serial_enviar('c')
        elif(int(bbox[0] + bbox[2]) > M2 + folga_v2 ):
            serial_enviar('cc')


        if(int(bbox[1]) < M3 and int(bbox[1]) > M3 - folga_v1 ):
            serial_enviar('d')
            time.sleep(0.1)
        elif(int(bbox[1]) < M3 - folga_v1 and int(bbox[1]) > M3 - folga_v2):
            serial_enviar('d')
        elif(int(bbox[1]) < M3 - folga_v2):
            serial_enviar('dd')

        if(int(bbox[1] + bbox[3]) > M4 and int(bbox[1] + bbox[3]) < M4 + folga_v1):
            serial_enviar('e')
            time.sleep(0.1)
        elif(int(bbox[1] + bbox[3]) > M4 + folga_v1 and int(bbox[1] + bbox[3]) < M4 + folga_v2):
            serial_enviar('e')
        elif(int(bbox[1] + bbox[3]) > M4 + folga_v2):
            serial_enviar('ee')
        
            #
        cv2.imshow("Tracking", frame) #para o rastremanto apos aperta a tecla para sair
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
    #cv2.Tracker.clear(frame, bbox1)

