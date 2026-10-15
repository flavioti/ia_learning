This is an umbrella term. Any neural network with an input layer, an output layer, and **multiple hidden layers** in between is a "deep" neural network.

1980 a 1990
- n-gramas
- Hidden Markov models (HMMs)

```mermaid
graph TD
    %% Style Definitions compatible with Obsidian
    classDef umbrella fill:#2c3e50,stroke:#34495e,stroke-width:2px,color:#fff;
    classDef classic fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff;
    classDef recurrent fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff;
    classDef modern fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    
    %% Main Node / Umbrella Term
    DNN[DNN - Deep Neural Network]
    class DNN umbrella;

    %% Subgraph 1: Feedforward
    subgraph FF [Conventional Feedforward DNN]
        In1[Input] --> H1[Multiple Hidden Layers] --> Out1[Output]
    end
    DNN --> In1
    class In1,H1,Out1 classic;

    %% Subgraph 2: Recurrent Networks
    subgraph RNN_Fam [Recurrent Family - Legacy Sequential]
        In2[Input] --> H2[RNN / LSTM / GRU]
        H2 -->|Memory Loop| H2
        H2 --> Out2[Output]
    end
    DNN --> In2
    class In2,H2,Out2 recurrent;

    %% Subgraph 3: Transformers
    subgraph Trans_Fam [Transformer Family - Modern Sequential]
        In3[Global Input] --> Atn[Self-Attention Mechanism] --> Out3[Parallel Output]
    end
    DNN --> In3
    class In3,Atn,Out3 modern;

    %% Main Connection Lines Styling
    linkStyle 0 stroke:#2c3e50,stroke-width:2px;
    linkStyle 3 stroke:#2c3e50,stroke-width:2px;
    linkStyle 7 stroke:#2c3e50,stroke-width:2px;
    
    %% RNN Loop Line Styling (Red for emphasis)
    linkStyle 5 stroke:#c0392b,stroke-width:3px;
```
