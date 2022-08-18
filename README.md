# Segue o enunciado do Trabalho Final (TF)

Enunciado do TF:

Construir um protocolo confiável de transporte sobre o protocolo não confiável UDP.

Para este trabalho você terá uma comunicação ponto a ponto (cliente e servidor) utilizando um UDP modificado para troca de pacotes. São requisitos deste protocolo ter as seguintes funcionalidades:

1) Entrega ordenada para aplicação baseado na ordem dos pacotes (# de sequência).
2) Confirmação acumulativa (ACK acumulativo) do destinatário para o remetente.
3) Utilização de um Buffer de pacotes de tamanho T, onde pacotes ocupam M Bytes.
4) O tamanho de cada pacote é de, no máximo, 1024 Bytes. (M)
5) Deve haver uma janela deslizante com tamanho N no buffer do remetente e do servidor. Onde N é igual a pelo menos 10 pacotes de tamanho M.
6) Números de sequência devem ser utilizados. Eles podem ser inteiros em um total de N*2, ou serem incrementados conforme o fluxo de bytes, como no TCP.
7) Adicione no protocolo um controle de fluxo, onde o remetente deve saber qual o tamanho da janela N do destinatário, a fim de não afogá-lo.
8) Por fim, crie um equação de controle de congestionamento, a fim de que, se a rede estiver apresentando perda (muitos pacotes com ACK pendentes e timeout), ele deve ser utilizado para reduzir o fluxo de envio de pacotes.
9) Avalie seu protocolo sobre um remetente que envia um arquivo de, pelo menos, 10MB, qualquer, para 1 destinatário. Para avaliar o controle de congestionamento, insira perdas arbitrárias de pacotes no destinatário (você pode fazer isso sorteando a cada chegada de um novo pacotes se ele será contabilizado e processado ou descartado).

Escreva um relatório como documentação da lógica do protocolo, e mostre gráficos da utilização do protocolo em relação à vazão da rede para o envio do arquivo de 10MB sem e com perdas.

# Roteiro de execução

Dividimos o projeto em dois arquivo principais: o [udp_sender.py](udp_sender.py) e o [udp_receiver.py](udp_receiver.py) onde no primeiro temos os métodos para o divisão e envio devido dos pacotes e no segundo os métodos para recebimento, confirmação e escrita do arquivo recebido. Dentro do diretório com os *scripts* existe o diretório **input** em que estão armazenados os arquivos teste de entrada do *software*. O arquivo com 10MB é o nomeado **default_input.txt**. Para a execução do arquivo **udp_sender.py** é necessário executar o seguinte comando **python3 udp_sender.py --input caminho/para/input** onde no argumento **input** deve ser indicado o caminho do arquivo de entrada. Para a execução do *script* **udp_receiver.py** deve utilizar o seguinte padrão de comando **python3 udp_receiver.py --window_size tamanho_do_pacote**. 