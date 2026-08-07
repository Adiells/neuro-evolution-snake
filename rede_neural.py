import numpy as np
import matplotlib.pyplot as plt

class RedeNeural:
    def __init__(self, n_entrada=11, n_oculta=10, n_saida=3):
        self.n_entrada = n_entrada
        self.n_oculta = n_oculta
        self.n_saida = n_saida
        
        # Inicialização dos pesos aleatórios entre -1 e 1 com NumPy
        self.pesos_entrada_oculta = np.random.uniform(-1, 1, (self.n_entrada, self.n_oculta))
        self.pesos_oculta_saida = np.random.uniform(-1, 1, (self.n_oculta, self.n_saida))
        
    def relu(self, valores):
        """Função de ativação ReLU."""
        return np.maximum(0, valores)
        
    def prever(self, sensores):
        """Executa o forward pass e retorna a ação predita (0, 1 ou 2) como int."""
        entrada_sensores = np.array(sensores)
        saida_oculta = self.relu(np.dot(entrada_sensores, self.pesos_entrada_oculta))
        saida = np.dot(saida_oculta, self.pesos_oculta_saida)
        return int(np.argmax(saida))
        
    def obter_pesos(self):
        """Achata e concatena ambas as matrizes de pesos em um único vetor 1D NumPy."""
        return np.concatenate([self.pesos_entrada_oculta.flatten(), self.pesos_oculta_saida.flatten()])
        
    def definir_pesos(self, novos_pesos):
        """Recebe um vetor 1D de pesos e reconstrói as matrizes de pesos."""
        limite = self.n_entrada * self.n_oculta
        self.pesos_entrada_oculta = novos_pesos[:limite].reshape(self.n_entrada, self.n_oculta)
        self.pesos_oculta_saida = novos_pesos[limite:].reshape(self.n_oculta, self.n_saida)
        
    def visualizar_pesos(self, caminho_salvar="pesos_heatmap.png"):
        """Gera e salva o heatmap de ambas as matrizes de pesos (entrada->oculta e oculta->saída)."""
        figura, (eixo1, eixo2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [11, 3]})
        
        # Heatmap pesos entrada -> oculta
        imagem1 = eixo1.imshow(self.pesos_entrada_oculta, cmap="coolwarm", aspect="auto")
        figura.colorbar(imagem1, ax=eixo1, label="Força da conexão")
        eixo1.set_title("Pesos: Entrada -> Camada Oculta")
        eixo1.set_xlabel("Neurônio Oculto")
        eixo1.set_ylabel("Sensor de Entrada")
        
        # Heatmap pesos oculta -> saída
        imagem2 = eixo2.imshow(self.pesos_oculta_saida, cmap="coolwarm", aspect="auto")
        figura.colorbar(imagem2, ax=eixo2, label="Força da conexão")
        eixo2.set_title("Pesos: Camada Oculta -> Saída")
        eixo2.set_xlabel("Ação de Saída")
        eixo2.set_ylabel("Neurônio Oculto")
        
        plt.tight_layout()
        plt.savefig(caminho_salvar)
        plt.close()

if __name__ == "__main__":
    # Instanciando a rede neural
    rede = RedeNeural()
    print("1. Rede neural instanciada com sucesso.")
    print(f"   Formato pesos_entrada_oculta: {rede.pesos_entrada_oculta.shape}")
    print(f"   Formato pesos_oculta_saida: {rede.pesos_oculta_saida.shape}")
    
    # Executando uma previsão de teste com 11 sensores
    sensores_teste = np.random.uniform(-1, 1, 11)
    acao = rede.prever(sensores_teste)
    print(f"2. Previsão de teste efetuada. Ação escolhida: {acao} (Tipo: {type(acao)})")
    
    # Obtendo os pesos como vetor 1D
    vetor_pesos = rede.obter_pesos()
    print(f"3. Pesos obtidos. Tamanho do vetor: {len(vetor_pesos)} (Esperado: 140)")
    
    # Definindo novos pesos
    pesos_aleatorios = np.random.uniform(-1, 1, 140)
    rede.definir_pesos(pesos_aleatorios)
    print("4. Novos pesos definidos com sucesso via definir_pesos().")
    
    # Verificando se os pesos foram aplicados corretamente
    pesos_verificados = rede.obter_pesos()
    assert np.allclose(pesos_aleatorios, pesos_verificados), "Erro ao definir pesos."
    print("   assert: Os pesos foram atribuídos e recuperados corretamente.")
    
    # Salvando a visualização dos pesos
    caminho_imagem = "pesos_heatmap.png"
    rede.visualizar_pesos(caminho_imagem)
    print(f"5. Heatmap dos pesos salvo com sucesso em: {caminho_imagem}")
