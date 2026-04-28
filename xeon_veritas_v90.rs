use std::thread;
use std::time::Duration;

fn main() {
    println!("--- PROTOCOLO DE RE-TENTATIVA XEON v90.0 ---");

    let mut tentativas = 0;
    let max_tentativas = 3;
    let mut sucesso = false;

    while tentativas < max_tentativas {
        tentativas += 1;
        println!("[TENTATIVA {}] Conectando ao Nó de Rede...", tentativas);

        // Simulando uma falha (em um cenário real, aqui viria o código de rede)
        if tentativas == 3 {
            sucesso = true; // Simula sucesso na última tentativa
        }

        if sucesso {
            println!("SUCESSO: CONEXÃO ESTABELECIDA NO CICLO {}.", tentativas);
            break;
        } else {
            println!("FALHA: RUIDO DETECTADO. Aguardando 1s para nova tentativa...");
            thread::sleep(Duration::from_secs(1));
        }
    }

    if !sucesso {
        println!("ALERTA: LIMITE DE RE-TENTATIVAS ALCANÇADO. ACIONAR MODO OFFLINE.");
    }
}