import cv2
import mediapipe as mp
import numpy as np
import pygame

LIMITE_EAR = 0.2
FRAMES_ALERTA = 15
FRAMES_SEM_ROSTO = 20

OLHO_DIR = [33, 160, 158, 133, 153, 144]
OLHO_ESQ = [362, 385, 387, 263, 373, 380]

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

pygame.mixer.init()
pygame.mixer.music.load("samsung-alert-sound.mp3")

def tocar_alerta():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)  

def parar_alerta():
    pygame.mixer.music.stop()

def capturar_frame(cap):
    return cap.read()

def processar_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(rgb)

def extrair_pontos(face_landmarks, indices, w, h):
    pontos = []
    for i in indices:
        lm = face_landmarks.landmark[i]
        x = int(lm.x * w)
        y = int(lm.y * h)
        pontos.append((x, y))
    return pontos

def calcular_ear(pontos):
    p1, p2, p3, p4, p5, p6 = pontos

    vertical1 = np.linalg.norm(np.array(p2) - np.array(p6))
    vertical2 = np.linalg.norm(np.array(p3) - np.array(p5))
    horizontal = np.linalg.norm(np.array(p1) - np.array(p4))

    return (vertical1 + vertical2) / (2.0 * horizontal)

def detectar_fadiga(ear, contador):
    if ear < LIMITE_EAR:
        contador += 1
    else:
        contador = 0

    alerta = contador >= FRAMES_ALERTA
    return contador, alerta

def desenhar(frame, pontos_dir, pontos_esq, ear, alerta):
    for p in pontos_dir + pontos_esq:
        cv2.circle(frame, p, 2, (0, 255, 0), -1)

    cv2.putText(frame, f"EAR: {ear:.2f}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if alerta:
        cv2.putText(frame, "ALERTA: SONOLENCIA!", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def main():
    cap = cv2.VideoCapture(0)

    contador = 0
    estado_alerta = "nenhum"
    alerta_ativo = False

    while True:
        ret, frame = capturar_frame(cap)
        if not ret:
            break

        resultado = processar_frame(frame)

        novo_estado = "nenhum"

        if resultado.multi_face_landmarks:
            frames_sem_rosto = 0

            for face_landmarks in resultado.multi_face_landmarks:
                h, w, _ = frame.shape

                pontos_dir = extrair_pontos(face_landmarks, OLHO_DIR, w, h)
                pontos_esq = extrair_pontos(face_landmarks, OLHO_ESQ, w, h)

                ear_dir = calcular_ear(pontos_dir)
                ear_esq = calcular_ear(pontos_esq)
                ear_medio = (ear_dir + ear_esq) / 2.0

                contador, alerta = detectar_fadiga(ear_medio, contador)

                if alerta:
                    novo_estado = "fadiga"

                desenhar(frame, pontos_dir, pontos_esq, ear_medio, alerta)

        else:
            frames_sem_rosto += 1

            if frames_sem_rosto > FRAMES_SEM_ROSTO:
                novo_estado = "sem_rosto"

                cv2.putText(frame, "OLHE PARA A CAMERA!", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        if novo_estado != estado_alerta:
            parar_alerta()

            if novo_estado == "fadiga":
                tocar_alerta()

            elif novo_estado == "sem_rosto":
                tocar_alerta()

            estado_alerta = novo_estado

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) == 27:
            break

        if cv2.getWindowProperty("Webcam", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()