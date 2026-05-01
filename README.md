# 🧠 Sensor de Fadiga com Alerta Psicoacústico
Este projeto é uma aplicação Python desenvolvida para monitorar o estado de alerta de motoristas ou estudantes. Utilizando visão computacional, o sistema detecta sinais de sonolência e variações de postura, acionando um alerta sonoro estratégico para despertar o usuário.

## Funcionalidades
- Detecção de Cochilos: Monitora o fechamento prolongado dos olhos ou a inclinação excessiva da cabeça (conhecido como "pescar").

- Monitoramento de Presença: Identifica se o rosto do usuário saiu da área de cobertura do sensor, emitindo um aviso de segurança.

- Alerta Sonoro Estratégico: Utiliza um som de despertador padrão.

- Diferencial: O uso do despertador evita sustos desnecessários (que poderiam causar reações bruscas) e utiliza o condicionamento cerebral que associa esse som específico ao ato de acordar.

## 🛠️ Tecnologias Utilizadas
- Python 3.11

- OpenCV / Numpy / MediaPipe / PlayGame

- Docker & Docker Compose (Conteinerização)

## Por que Docker?
O projeto foi totalmente conteinerizado para garantir que a aplicação rode exatamente da mesma forma em qualquer máquina, sem a necessidade de instalar manualmente dependências complexas de visão computacional ou drivers de áudio no sistema anfitrião.

## Como Rodar o Projeto
### Pré-requisitos
Ter o Docker e o Docker Compose instalados.

Uma webcam conectada ao computador.

## Passo a Passo :

### Clone o Repositório:
``` Bash
git clone https://github.com/BrenoMontenegro/fatigue-sensor.git
cd no repositório
```
### Construa e inicie o contêiner:

``` Bash
docker-compose up --build
```
### Acesse a aplicação:
- O Docker iniciará o script detector.py automaticamente. 
- Ao desejar sair, basta digitar a tecla 'Esc' do teclado ou 'q'.

---

Nota para Linux: Para que o contêiner acesse a webcam e o áudio, pode ser necessário rodar o comando xhost +local:docker antes de iniciar o serviço.
