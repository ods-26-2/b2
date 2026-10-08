import os
import json
import paho.mqtt.client as mqtt
from time_service import TimeService

# Configurações obtidas do ambiente ou valores padrão
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "broker.hivemq.com")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))

TOPIC_REQUEST = "ods/system/time/requests"
TOPIC_RESPONSE = "ods/system/time/responses"

# Instancia o serviço de tempo
time_service = TimeService()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[+] Conectado com sucesso ao Barramento Pub/Sub!")
        client.subscribe(TOPIC_REQUEST)
        print(f"[+] Inscrito no tópico de requisições: {TOPIC_REQUEST}")
    else:
        print(f"[-] Falha na conexão com o broker. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)
        
        # Filtra apenas se for uma query solicitando o tempo global
        if data.get("message_type") == "query" and data.get("payload", {}).get("action") == "get_global_time":
            correlation_id = data["payload"].get("correlation_id")
            requester = data.get("producer", "desconhecido")
            
            print(f"\n[!] Pedido de tempo recebido de: {requester} (ID: {correlation_id})")

            # Gera a resposta usando a classe TimeService
            response = time_service.create_reply_payload(correlation_id)

            # Publica a resposta no barramento
            client.publish(TOPIC_RESPONSE, json.dumps(response))
            print(f"[->] Resposta enviada para o tópico: {TOPIC_RESPONSE}")

    except Exception as e:
        print(f"[-] Erro ao processar mensagem: {e}")

if __name__ == "__main__":
    print("Iniciando o Global Time Service...")
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    
    # Mantém o container executando e escutando por eventos
    client.loop_forever()