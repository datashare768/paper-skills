

## Page 1

 
Contents lists available at ScienceDirect
Neurocomputing
journal homepage: www.elsevier.com/locate/neucom
 
STADNN: Spatio-temporal adaptive decomposition neural network for 
traffic prediction
Yong Wang a , Ruidong Li b , Xiaoyu Li c,∗ , Yongshun Gong d , Xiushan Nie e , Yilong Yin d
a Faculty of Electronic and Information Engineering, Xi’an Jiaotong University, Xi’an, China 
b Shandong Yunhai Guochuang Cloud Computing Equipment Industry Innovation Co., Ltd. Jinan, China 
c Department of Data Science and Artificial Intelligence, The Hong Kong Polytechnic University, Hong Kong, China 
d School of Software, Shandong University, Jinan, China 
e School of Computer Science, Shandong Jianzhu University, Jinan, China
A R T I C L E  I N F O
Communicated by F.G. Guimaraes
Keywords:
Spatio-temporal learning 
Adaptive learning 
Traffic prediction 
Sequence decomposition
A B S T R A C T
Accurate traffic forecasting is critical for intelligent transportation systems, yet it remains challenging due 
to the complex and dynamic correlations of spatial and temporal patterns. Traffic sequences embed multiple 
latent patterns, notably long-term trends and short-term periodicities, that evolve under different rules and in­ 
teract across space and time. In this paper, we propose the Spatio-Temporal Adaptive Decomposition Neural 
Network (STADNN), a framework that adaptively disentangles traffic sequences into trend and periodic sub­ 
components to enable more effective modeling. For temporal modeling, the trend component is processed using 
a time-aware attention mechanism to capture long-range dependencies and evolving patterns, while the peri­ 
odic component is handled by a Temporal Convolutional Network (TCN) to extract repeating, short-term traffic 
properties. Spatial dependencies for both streams are then modeled using a shared spatial attention module 
that identifies dynamic node-wise dependencies. Extensive experiments on multiple public datasets show that 
STADNN achieves consistent performance improvements over leading baselines. Further model analysis verifies 
that adaptive decomposition enables more effective capture of underlying traffic dynamics.
1 . Introduction
Traffic prediction is a fundamental task in modern intelligent trans­ 
portation systems, directly supporting applications such as route plan­ 
ning and congestion management [23,26,48]. As cities grow and mo­ 
bility demands intensify, the ability to forecast traffic conditions with 
high accuracy becomes increasingly vital. Traffic data, typically col­ 
lected from sensors or GPS devices, forms spatio-temporal sequences 
that reflect the collective movement of vehicles across road networks. 
By analyzing the historical traffic sequences, prediction models aim to 
learn the underlying patterns of traffic conditions and forecast the future 
traffic states at specific locations and times.
Recent years have seen significant progress in traffic prediction, 
largely due to deep learning architectures that effectively capture com­ 
plex spatio-temporal dependencies. Several advances [13,31,43,51,53] 
have proven that data-driven methods outperform traditional statisti­ 
cal time series models in modeling traffic sequences. Spatial Temporal 
Graph Neural Networks [1,21,36] model road networks as graphs and 
explicitly capture spatial dependencies through graph-based learning. 
Attention-based methods [18,29,32,54,57] dynamically weight relevant 
neighbors or time steps to enhance adaptability and long-range depen­ 
dency modeling. These methods model spatio-temporal dynamics from 
different perspectives. A key consensus is that traffic sequences exhibit 
inherently complex patterns. For example, the time series at a node often 
contains multiple embedded signals, including periodicity and trend as 
shown in Fig. 1. Periodicity refers to recurring patterns, such as morning 
and evening rush hours while trend reflects structural changes such as 
gradual traffic growth. These patterns reflect different aspects of traffic 
state evolution and decomposing them can enhance the prediction.
The decomposition of historical series is a standard technique in time 
series analysis [2,9]. Researchers have proposed several decomposition-
based strategies to capture distinct patterns in historical sequences. 
Autoformer [45] embeds decomposition as a basic component to sep­ 
arate trend and seasonal patterns in time series. STWave [12] decom­ 
poses traffic sequences in the frequency domain to capture multi-scale 
∗ Corresponding author.
 
Email addresses: wangyong@stu.xjtu.edu.cn (Y. Wang), lird@inspur.com (R. Li), xiao-y.li@connect.polyu.hk (X. Li), ysgong@sdu.edu.cn (Y. Gong), 
niexsh@sdufe.edu.cn (X. Nie), ylyin@sdu.edu.cn (Y. Yin).
https://doi.org/10.1016/j.neucom.2025.132486 
Received 2 November 2025; Received in revised form 10 December 2025; Accepted 18 December 2025
Neurocomputing 669 (2026) 132486 
Available online 19 December 2025 
0925-2312/© 2025 Elsevier B.V. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 


## Page 2

Y. Wang, R. Li, X. Li et al.
Fig. 1. Traffic sensors exhibit spatially heterogeneous patterns and each se­ 
quence inherently contains both trend and periodic dynamics.
features. However, both methods ignore dynamic interactions between 
traffic nodes when applying decomposition to individual sensors. While 
KARMA [49] proposes an adaptive time-channel decomposition, it does 
not incorporate spatio-temporal aware features during the decompo­ 
sition process. STDN [6] attempts to address this by decomposing 
sequences based on learned spatio-temporal relationships, yet it ap­ 
plies identical model structures to all decomposed components, poten­ 
tially overlooking their distinct spatio-temporal semantics. We identify 
three potential limitations in existing decomposition-based approaches: 
1. They often neglect spatio-temporal aware contextual information 
that governs how patterns evolve across space and time; 2. Many rely 
on fixed or predefined decomposition schemes without the adaptabil­ 
ity to dynamic traffic states; 3. They typically apply homogeneous 
feature extractors to all decomposed components, ignoring their dis­ 
tinct semantic natures. In summary, the core research problem is: 
How to achieve adaptive decomposition with spatio-temporal and 
semantic awareness.
To achieve this, we propose the Spatio-Temporal Adaptive 
Decomposition Neural Network (STADNN) to address the above chal­ 
lenges. STADNN adaptively decomposes traffic sequences into trend and 
periodic components, guided by spatio-temporal aware embeddings that 
capture location and time specific semantics. Given their distinct spatio-
temporal semantics, trend and periodic components are then processed 
separately. Specifically, the trend component, characterized by slow 
structural evolution and long-term patterns, is processed by the attention 
mechanism to capture global temporal dependencies. The periodic com­ 
ponent, driven by short-term fluctuations and local dynamics, is handled 
by gated TCN. Both streams are fused and refined through the spatial 
attention module to model dynamic node interactions. Experiments con­ 
ducted on four public datasets demonstrate that STADNN consistently 
outperforms state-of-the-art methods across multiple prediction hori­ 
zons. The ablation studies designed for adaptive decomposition confirm 
its critical role in improving model performance. The contributions of 
our study are summarized as follows:
• We propose the STADNN model, a spatio-temporal adaptive decom­
position neural network for traffic forecasting. This work addresses 
a key limitation in existing methods by enabling spatio-temporal 
aware decomposition of heterogeneous traffic dynamics.
• We design an adaptive decomposition framework guided by spatio-
temporal aware embeddings, which not only disentangles the traffic 
sequences into trend and periodic components, but also enables 
component specific modeling.
• We validate STADNN through extensive experiments on four real-
world datasets, demonstrating superiority over multiple baselines 
and proving via ablation that adaptive decomposition and pattern 
specific modeling are effective for traffic prediction.
2 . Related work 
2.1 . Traffic forecasting
Traffic prediction is a fundamental task in intelligent transporta­ 
tion systems and has received increasing research attention in recent 
years. Existing methods can be categorized into traditional statistical 
approaches and deep learning models. Traditional statistical models like 
ARIMA [37] and VAR [39] are simple but limited by linear assumptions. 
Deep learning methods such as LSTM [15] and GRU [8] have demon­ 
strated strong nonlinear modeling capabilities for time series, but lack 
the ability to capture spatial dependencies. Some recent works [16,17] 
integrate hybrid feature extraction into spatio-temporal modeling for 
traffic forecasting. Recent research, such as STGCN [50] and STSGCN 
[38], constructs the graph based on the road network and captures 
the traffic patterns with spatio-temporal graph convolutional networks, 
which effectively improve the forecasting performance. To capture the 
dynamic evolution of traffic graphs, methods such as AGCRN [4] and 
GWNet [46] construct adaptive adjacency matrices based on learnable 
node embeddings. For modeling multilevel spatio-temporal dependen­ 
cies, DyHSL [56] introduces hypergraphs, which encode higher-order 
node dependencies beyond pairwise relations. These graph-based frame­ 
works typically incorporate additional temporal modules to complement 
the spatial modeling. However, GCN-based approaches often face chal­ 
lenges of high computational cost and oversmoothing [30]. In response, 
STMLP [44] and STID [35] adopt MLP structures to model spatial-
temporal dependencies without explicit graph construction. An alterna­ 
tive strategy reduces complexity by sparsifying the graph topology [11] 
or selecting a subset of pivotal nodes for propagation [22]. Together, 
these innovations in spatio-temporal graph modeling have substantially 
advanced the field of graph-based traffic forecasting.
Besides the STGNNs, the attention mechanism has been widely 
adopted to capture spatio-temporal patterns in traffic forecasting due 
to its strong capacity to model long-range dependencies. ASTGCN [14] 
designs spatial and temporal attention modules to model dynamic node 
interactions across space and time. GMAN [57] introduces a graph multi-
attention architecture that jointly encodes spatial topology and tem­ 
poral. PDFormer [18] further incorporates the concept of propagation 
delay for traffic forecasting through a delay-aware dynamic transformer. 
Compared to GNN-based approaches, attention-based methods offer 
greater flexibility without the need for predefined graph structures. For 
instance, STAEFormer [29] achieves competitive prediction accuracy us­ 
ing a pure Transformer architecture. DSM-STWave [28] employs spatio-
temporal attention mechanisms that account for both online and offline 
deployment scenarios. Despite their effectiveness, attention-based mod­ 
els face well-recognized challenges, particularly sparse connectivity 
patterns and quadratic computational complexity [45,58]. Nevertheless, 
these methods remain a powerful and increasingly effective solution for 
accurate traffic prediction.
2.2 . Time series decomposition
Time series decomposition [2,9] is commonly used to disentangle 
composite signals into more predictable sub-patterns. Traditionally, de­ 
composition functions as a preprocessing step applied before forecasting 
[3,40]. Autoformer [45] redefines it as an intrinsic architectural block 
embedded within the model and effectively improves forecasting accu­ 
racy. KARMA [49] proposes a multilevel decomposition framework to 
decompose the time series into the time domain and frequency domain. 
In the context of spatio-temporal forecasting, particularly in grid-based 
urban flow prediction, underlying traffic patterns—such as regional 
trends and periodic commuters are often modeled separately to bet­ 
ter capture their distinct dynamics [25,52,55]. For graph-based models, 
Neurocomputing 669 (2026) 132486 
2 


## Page 3

Y. Wang, R. Li, X. Li et al.
D 2 STGNN [36] decouples the diffusion and inherent traffic information 
through the estimation gate and a residual decomposition mechanism. 
DSTG [42] decomposes the time dependencies into latent trend and sea­ 
sonal terms by incorporating inductive biases of time-series structures. 
Other approaches [6,12] explore decomposition through the lens of 
spatio-temporal feature semantics. While recent decomposition meth­ 
ods have advanced spatio-temporal modeling, most remain limited by 
spatial-temporal contextual constraints and a lack of semantic-aware 
adaptability. To bridge this gap, we propose a spatio-temporal adap­ 
tive decomposition neural network, designed to enable spatial-temporal 
aware, semantics-guided decomposition for more accurate traffic fore­ 
casting.
3 . Preliminaries
In this section, we define the key components and objectives of our 
study. We consider traffic forecasting as a spatio-temporal sequence pre­ 
diction problem over 𝑁 spatially distributed monitoring points, typically 
corresponding to locations equipped with traffic sensors. Each location 
𝑣  (
) generates a time series of -dimensional traffic obser­
𝑛𝑛 = 1, … , 
 
𝑁
𝐶
 
vations (e.g., traffic volume, speed, or occupancy), forming a sequence 
𝑥 
 
 = {
𝑇
𝑥 
 ∈ R 𝐶 } 
. At any time step 
𝑛,𝑡
𝑡=1 
𝑡, the traffic state of all nodes is 
𝑛
⊤
×
represented by a feature matrix 𝑋 𝑡 = [𝑥1
 
 
𝑁𝐶. Given 
,𝑡…
 
 ,
, 𝑥
] 
∈R
 
 𝑁,𝑡
 
 
a historical window of length 𝑇 , the input is organized as a tensor 
𝑋 = [𝑋 
, … , 𝑋 ] ∈ R 𝑇×𝑁×𝐶
−
 
 +1 
 
. The goal is to predict the target traf­
𝑡𝑇
𝑡
fic state over the next 𝜏 steps. This forecasting process can be formally 
expressed as:
̂ 𝑌 = 𝑓 𝜃 (𝑋) ∈ R 𝜏×𝑁 , 
(1)
where 𝑓 𝜃  denotes a learnable forecasting function that captures spatio-
temporal dependencies.
4 . Methodology
This section presents the proposed spatio-temporal adaptive de­ 
composition neural network, a unified architecture designed to model 
dynamic spatio-temporal patterns through adaptive decomposition. Our 
framework consists of the following four core components. The spatio-
temporal embedding module is designed to encode space and time con­ 
text into high level spatio-temporal representations. The spatio-temporal 
adaptive decomposition module aims to disentangle the trend and pe­ 
riodic components through the underlying traffic patterns. Temporal 
encoder and spatial encoder are used to capture long-range sequential 
dependencies within each decomposed stream and model spatial inter­ 
actions, respectively. The overall framework of our STADNN is shown 
in Fig. 2.
4.1 . Spatio-temporal embedding
Effective modeling of traffic dynamics requires not only the raw 
sensor measurements but also an explicit encoding of the underlying 
spatio-temporal context. Specifically, the spatial context denotes the 
spatial identity of each location and the temporal context refers to the 
representation of timestamps. These two properties can be summarized 
as spatiotemporal indistinguishability, which has been proven effective 
in spatio-temporal modeling [34,35]. These spatio-temporal contexts 
enable the model to recognize region-specific roles and time condi­ 
tioned patterns, which are essential for sequence decomposition and 
discriminative spatio-temporal feature learning.
×
Formally, given the raw input 𝑋 ∈ R 𝑇
𝑁×𝐶 , we first project 𝑋 into 
a latent space via a linear transformation: 𝐻 =
 
 𝑋𝑊in
 
∈ R 𝑇×𝑁×𝑑, where 
𝑊 
∈ R 𝐶×𝑑 
in
 is a learnable weight matrix and 𝑑 is the embedding di­ 
mension. To enrich 𝐻 with spatial context, we introduce a set of node 
s
×
specific spatial embeddings 𝐸
 
 
∈ R 𝑁𝑑1
 
 , where each row 𝑒s 
𝑖
  serves as 
a learnable feature embedding for node 𝑣 
 . This enables the model to 
𝑖
capture the inherent spatio-temporal properties of each sensor.
Simultaneously, we encode temporal context using two time embed­ 
dings: time-of-day embedding 𝑒
 
 tod ∈ R 𝑁 𝑑×𝑑1
  and day-of-week embedding 
𝑒 dow ∈ R 𝑁 𝑤 ×𝑑1
 , where 𝑁  is the number of time slots in a day and 
𝑑
𝑁 
 = 7 represents the days in a week. Following the previous study 
𝑤
[35], these temporal embeddings are broadcast and added to all spatial 
locations and the spatial embedding is shared across all time stamps. 
The final spatio-temporal enriched input is obtained by concatenating 
all components along the feature dimension:
̂𝐻 𝑖,𝑡 = 𝐻 𝑖,𝑡‖ 𝑒 𝑠
𝑖‖ 𝑒 𝑡𝑜𝑑
𝑡
‖ 𝑒 𝑑𝑜𝑤
𝑡
∈ R 𝐷 ,
where the hidden dimension 𝐷 equals 𝑑 + 3𝑑 1 . This representation ̂𝐻 𝑖,𝑡
now jointly encodes the original traffic semantics, the static spatial iden­ 
tity of each node, and the information of time stamps, which provides 
a context-aware foundation for subsequent adaptive decomposition and 
spatio-temporal encoding.
4.2 . Spatio-temporal adaptive decomposition
Sequence decomposition is a standard strategy in time series and 
spatio-temporal modeling to disentangle underlying patterns [45,49]. 
However, conventional decomposition methods underutilize available 
Fig. 2. Overall framework of STADNN.
Neurocomputing 669 (2026) 132486 
3 


## Page 4

Y. Wang, R. Li, X. Li et al.
spatio-temporal contextual information, limiting their ability to adapt 
decomposition to the dynamic roles of locations or time stamps. Our 
spatio-temporal embedding resolves this by encoding node specific and 
time aware context. Yet, a second limitation persists in that most de­ 
composition schemes rely on predefined rules and lack the flexibility 
to adjust to evolving traffic conditions. To address this, we propose 
an adaptive decomposition mechanism that adaptively decomposes the 
inputs into trend and periodic components based on latent embeddings.
Leveraging the learned representation ̂ 𝐻, we first apply dropout reg­
ularization to enhance generalization. We then compute adaptive gating 
weights Γ using using a fully connected layer:
Γ = 𝜎(FC(Dropout( ̂𝐻)) ) , 
(2)
where 𝜎(⋅) denotes the sigmoid function, and FC is a fully connected layer 
with the hidden size unchanged. The output Γ serves as a soft signal that 
is learned to retain persistent patterns (e.g., morning congestion).
The trend and periodic components are derived via gating and 
residual subtraction:
̂ 𝐻 𝑡 = Γ ⊙̂𝐻, 
(3)
̂ 𝐻 𝑝 = ̂ 𝐻 −̂ 𝐻 𝑡 .
(4)
Finally, both components are independently projected onto their 
respective output spaces:
𝐻 𝑡= Proj 𝑡( ̂ 𝐻 𝑡 ), 
(5)
𝐻 𝑝= Proj 𝑠( ̂ 𝐻 𝑝 ).
(6)
The adaptive decomposition module enhances representation qual­ 
ity by disentangling trend and periodic components in a spatio-temporal 
aware manner. Ablation results in the experiments section demon­ 
strate clear performance gains, confirming its critical role in the overall 
framework.
4.3 . Temporal encoder
Accurate modeling of temporal dynamics is fundamental to traffic 
forecasting. However, existing decomposition-based approaches often 
treat the extracted components with similar temporal encoders, over­ 
looking their inherently different temporal semantic properties. To 
address this, we design specialized temporal encoders tailored to the na­ 
ture of each signal. For the trend component 𝐻 𝑡 , we employ a temporal 
transformer [41] to capture its sparse and long-range temporal depen­ 
dencies. For the periodic component 𝐻 𝑝 , we adopt a gated temporal 
convolutional network [46] to model the locally structured fluctuations. 
The detailed formulations of these two encoders are presented below.
Given the trend spatio-temporal embedding 𝐻 𝑡 ∈ R 𝑇×𝑁×𝐷 , we first 
project ̂𝐻 𝑡 into query, key, and value representations: 
𝑄 𝑡 = 𝐻 𝑡 𝑊 𝑡
𝑄, 
𝐾 𝑡 = 𝐻 𝑡 𝑊 𝑡 
𝐾, 
𝑉 𝑡 = 𝐻 𝑡 𝑊 𝑡
𝑉, 
(7)
×
where 𝑊 𝑡, 𝑊𝑡, 𝑊𝑡
∈ R 𝐷𝐷𝑘
  are learnable projection matrices, and 
𝑄
𝐾
𝑉
𝐷 𝑘= 
 
𝐷∕ℎ denotes the per-head dimension for ℎ attention heads. The 
temporal attention score for each node is computed as:
𝐴 𝑡 = Softmax 
(
𝑄 𝑡 𝐾 𝑡 ⊤
√
𝐷 𝑘
) 
∈ R 𝑁×𝑇×𝑇 , 
(8)
where 𝐴 𝑡 
 enables adaptive weighting over the full temporal horizon 
𝑖,∶,∶
at node 𝑖. The attended output for each head is:
𝑍 𝑡 = 𝐴 𝑡𝑉 𝑡 , 
(9)
and we aggregate and project it back to the original dimension 𝑍 𝑡 ∈ 
R 𝑇×𝑁×𝐷 . Finally, we apply residual connection followed by layer nor­ 
malization, adhering to the standard transformer architecture.
With the periodic spatio-temporal embedding 𝐻 𝑝 , we apply a gated 
temporal convolutional network to capture local temporal patterns. 
Specifically, we adopt the dilated causal convolution as the temporal 
convolutional network. First, the model computes a dilated causal con­ 
volution along the temporal axis. For each node 𝑛, the dilated causal 1D 
convolution at time step 𝑡 is computed as:
𝑍 𝑝
𝑡,𝑛= 
𝐾−1
∑
𝑘=0
𝐻 𝑝
𝑡−𝑑⋅𝑘, 𝑛𝑊 𝑝
𝑘+ 𝑏 𝑝, 
(10)
𝑝
where 𝑍 
∈ R 𝐷  denotes the feature representation of node  
𝑡,𝑛
𝑛at time 
step 𝑡; 𝑊𝑝 ∈
 
 
 R 𝐾×𝐷×𝐷 is the learnable kernel, with 𝐾 being the kernel 
size and 𝑏 𝑝∈ R 𝐷  is the bias. We denote the calculation in Eq. (10) as 
TCN(⋅). Therefore, the temporal embedding can be captured through a 
gating mechanism:
𝑍 𝑝 = tanh ( TCN 𝑎 (𝐻 𝑝 ) ) ⊙ 𝜎 ( TCN 𝑏 (𝐻 𝑝 ) ) , 
(11)
where 𝜎(⋅) and tanh(⋅) are the activation functions; ⊙ represents element-
wise multiplication and 𝑍 𝑝  is the final output representation for the 
periodic component.
4.4 . Spatial encoder
Traffic networks possess complex and non-local spatial dependen­ 
cies. Explicit spatial modeling is therefore essential for accurate forecast­ 
ing. After processing the input through 𝐿 layers of temporal encoders, we 
obtain two temporally refined feature tensors: 𝑍 𝑝  capturing periodic dy­ 
namics, and 𝑍𝑡 
  encoding long-term trends. To model spatial interactions 
within each of these representations, we introduce a spatial encoder that 
is implemented as a spatial transformer module operating along the spa­ 
tial dimension. It computes node-to-node attention at each time step 
instead of attending over time steps compared to the temporal trans­
former. The spatially enhanced features, denoted 𝑍̃
 𝑝  and 𝑍̃ 
 𝑡 , are then 
fused via element-wise summation to form a unified spatio-temporal rep­ 
resentation: 𝐻 
𝑝 
𝑡 
st
𝑍
 
 
 = ̃
+ 𝑍̃
 . This fused tensor is subsequently projected 
through a learnable linear layer to produce the final prediction 𝑌̂ 
 . The 
model is trained by minimizing the Mean Squared Error (MSE) between 
the predicted traffic states 𝑌̂  and the ground-truth observations. The loss 
function is defined as:
 MSE =
1
𝜏𝑁 ‖ ̂𝑌− 𝑌 ‖2
𝐹, 
(12)
where 𝜏 denotes the number of predicted time steps, and 𝑁 is the number 
of nodes.
In summary, our approach decomposes traffic dynamics into se­ 
mantically distinct temporal patterns, trend and periodicity, and tailors 
dedicated temporal encoders to capture their unique characteristics. 
By further incorporating a spatial transformer, our framework achieves 
effective spatio-temporal modeling and demonstrates strong empirical 
performance.
5 . Experiments 
5.1 . Datasets
We use four widely-used traffic datasets PEMS03, PEMS04, PEMS07 
and PEMS08 [38] to evaluate the performance of the proposed model. 
Table 1 summarizes the core attributes of these datasets. These four 
datasets contain the traffic flow records collected from road traffic 
detectors of the California Department of Transportation (CalTrans) 
Performance Measurement System 1  (PeMS) [7]. PEMS04 contains the 
traffic data in the San Francisco Bay Area, with a time span from January 
to February 2018. PEMS08 refers to the traffic data in San Bernardino 
from July to August 2016. Redundant detectors were removed from both 
1 https://pems.dot.ca.gov
Neurocomputing 669 (2026) 132486 
4 


## Page 5

Y. Wang, R. Li, X. Li et al.
Table 1 
Statistics of Datasets.
Dataset
PEMS03
PEMS04
PEMS07
PEMS08
Nodes 
358 
307 
883 
170 
Edges 
546 
338 
865 
276 
Time steps 
26,208 
16,992 
28,224 
17,856 
Time interval
5 min
5 min
5 min
5 min
raw datasets, following [14], to ensure the distance between any adja­ 
cent detectors is longer than 3.5 miles. The missing values in PEMS04 
and PEMS08 are filled using linear interpolation. These datasets are split 
into training, validation, and test sets in a ratio of 6:2:2.
5.2 . Baselines
To evaluate the performance of STADNN, we conduct extensive com­ 
parisons against 12 advanced baseline models in traffic flow forecasting. 
Below, we provide a concise description of each baseline:
• GWNet [IJCAI 2019] [46]: It introduces an adaptive dependency 
matrix to capture spatial relationships and adopts stacked dilated 
convolutions to model temporal sequences.
• AGCRN [NeurIPS 2020] [4]: It proposes two adaptive modules 
to learn node-specific parameters and infer spatial dependencies 
between series.
• MTGNN [KDD 2020] [47]: It combines mix-hop graph propaga­
tion and dilated inception layers to capture spatial and temporal 
correlations.
• StemGNN [NeurIPS 2020] [5]: It models inter-series correlations 
and temporal patterns in the spectral domain by integrating Graph 
Fourier Transform and Discrete Fourier Transform.
• GTS [ICLR 2021] [33]: It learns an underlying graph structure 
and its associated GNN by parameterizing a probabilistic graph 
distribution and infers pairwise dependencies from sequences.
• DGCRN [TKDD 2023] [24]: It generates time-varying graph struc­
tures using hyper-networks, then combines them with a static graph 
to model spatial dependencies.
• MegaCRN [AAAI 2023] [19]: It incorporates a Meta-Graph Learner 
into a graph convolutional recurrent network to model spatial de­ 
pendencies.
• DFDGCN [ICASSP 2024] [27]: It captures spatial dependencies in 
the frequency domain via the Fourier transform to reduce sensitivity 
to time-shift and noisy observations in traffic data.
• STPGNN [AAAI 2024] [22]: It introduces a pivotal node identifi­
cation module to detect highly connected nodes and designs a dedi­ 
cated graph convolution to model spatio-temporal dependencies.
 
Table 2 
Overall prediction performance of different methods on the PEMS03 and PEMS04 datasets. The best result in each column is highlighted in bold and the second 
best is underlined.
Datasets
PEMS03
PEMS04
Models
15 min
30 min
60 min
15 min
30 min
60 min
MAE
RMSE
MAPE
MAE
RMSE
MAPE
MAE
RMSE
MAPE
MAE
RMSE
MAPE
MAE
RMSE
MAPE
MAE
RMSE
MAPE
GWNet
14.32
24.83
13.91
15.36
27.23
15.40
17.30
29.84
16.38
18.39
29.71
13.08
19.14
31.21
13.37
20.71
32.80
14.26
AGCRN
14.82
25.33
14.70
15.68
27.63
17.12
17.93
30.47
16.83
18.63
29.98
13.01
19.57
31.62
13.30
20.74
33.34
13.91
MTGNN
14.47
26.05
13.94
15.89
27.57
14.93
17.48
30.26
16.56
18.76
29.86
12.92
19.24
31.20
13.25
20.67
33.44
13.95
StemGNN
14.99
25.13
14.12
16.20
27.36
15.91
17.68
30.62
17.86
19.36
30.54
13.30
21.07
32.97
14.57
24.32
37.27
16.90
GTS
14.75
25.12
14.21
16.36
27.82
15.32
18.29
30.82
17.79
19.53
30.66
13.38
21.91
33.91
15.68
28.42
42.05
24.88
DGCRN
14.43
25.09
13.84
15.62
27.28
14.98
17.31
30.06
16.52
18.57
29.92
12.93
18.99
30.81
13.35
20.39
33.15
14.61
MegaCRN
14.59
25.20
14.06
15.97
27.54
15.30
17.53
30.45
17.50
18.34
29.90
13.09
19.06
31.17
13.42
20.36
32.89
14.03
DFDGCN
14.30
24.93
13.92
15.84
27.17
15.19
17.34
29.94
16.44
18.45
29.97
13.11
19.03
30.91
13.43
19.91
32.87
13.85
STPGNN
14.87
25.14
14.20
16.29
27.32
15.01
18.03
30.34
17.09
19.09
30.45
12.82
21.08
33.25
14.31
25.24
38.76
18.04
HimNet
14.52
24.77
14.93
15.52
27.22
16.13
17.39
31.18
18.12
18.41
29.50
12.47
19.21
30.97
13.45
20.33
32.81
13.74
M3Net
14.41
24.90
14.68
15.71
27.27
15.95
17.43
30.12
17.73
18.46
29.80
12.61
19.17
31.27
13.56
20.09
32.98
14.58
STDN
14.47
25.23
14.37
15.87
27.39
15.31
17.46
30.14
17.16
18.26
34.60
19.40
18.95
35.82
19.23
20.24
39.22
21.48
STADNN
14.14
24.66
13.50
15.40
26.94
14.62
17.06
29.73
16.22
17.85
29.18
12.39
18.61
30.61
12.94
19.57
32.21
13.40
• HimNet [SIGKDD 2024] [10]: It proposes a heterogeneity-informed 
meta-parameter learning scheme that captures spatiotemporal het­ 
erogeneity and dynamically generates spatiotemporal-specific pa­ 
rameters from meta-parameter pools.
• M3Net [CIKM 2025] [20]: It proposes a cost-effective, graph-free 
MLP-based model for traffic prediction that avoids reliance on full 
network topology or complex architectures.
• STDN [AAAI 2025] [6]: It employs a trend-seasonality decomposi­
tion module to separate different temporal components. 
5.3 . Metrics
In the experimental evaluation, we adopt three widely used met­ 
rics to assess the prediction performance: Root Mean Square Error 
(RMSE), Mean Absolute Error (MAE), and Mean Absolute Percentage 
Error (MAPE). Their formal definitions are as follows:
MAE = 
1
𝑁 × 𝜏
𝑁
∑ 
𝑖=1
𝜏∑
𝑗=1
|||𝑦𝑖𝑗− ̂𝑦 𝑖𝑗||| ,
(13)
√
√
√
√
RMSE = √
1
𝑁 × 𝜏 
𝑁
∑ 
𝑖=1
𝜏∑
𝑗=1
(𝑦𝑖𝑗− ̂𝑦 𝑖𝑗
) 2, 
(14)
MAPE = 100 %
𝑁 × 𝜏 
𝑁
∑ 
𝑖=1
𝜏∑
𝑗=1
|||||
𝑦 𝑖𝑗− ̂𝑦 𝑖𝑗
𝑦 𝑖𝑗
|||||
, 
(15)
where 𝑦 𝑖𝑗  and ̂𝑦 𝑖𝑗 denote the ground-truth and predicted traffic values, 
respectively, at node 𝑖 and future time step 𝑗.
5.4 . Implementation details
All models, including the proposed method and baselines, are im­ 
plemented in PyTorch and evaluated on NVIDIA RTX 3090 GPUs. The 
model consists of 2 stacked layers for temporal and spatial encoders, 
with the input embeddings of dimension 16 and all learnable spatial and 
temporal embeddings are set to 32 dimensions. The attention mecha­ 
nism employs 4 heads. Following standard practice in traffic forecasting, 
the model takes the past 12 time steps as input to predict the next 
12 steps, and evaluation metrics are reported at three prediction hori­ 
zons: 15 min, 30 min, and 60 min. Training is conducted for up to 100 
epochs using the Adam optimizer, with early stopping applied to prevent 
overfitting based on validation performance.
5.5 . Main results
The main results of our proposed model against other baselines are 
shown in Tables 2 and 3. Several key observations can be drawn from 
Neurocomputing 669 (2026) 132486 
5 


## Page 6

Y. Wang, R. Li, X. Li et al.
Table 3 
Overall prediction performance of different methods on the PEMS07 and PEMS08 datasets. The best result in each column is highlighted in bold and the second best 
is underlined.
Datasets
PEMS07
PEMS08
Models
15 min
30 min
60 min
15 min
30 min
60 min
MAE 
RMSE 
MAPE 
MAE 
RMSE 
MAPE 
MAE 
RMSE 
MAPE 
MAE 
RMSE 
MAPE 
MAE 
RMSE 
MAPE 
MAE 
RMSE 
MAPE
GWNet
19.37 
31.27 
9.04
21.83 
34.53 
10.36 
24.46 
38.27 
11.84 
13.70 
21.92 
9.14
14.54 
24.15 
9.54
16.01 
26.12 
10.39
AGCRN
19.59 
31.85 
9.25
21.91 
34.84 
9.79
24.98
38.36
12.04
14.83
23.16
10.06
15.92
26.54
10.74
17.55
28.16
11.47
MTGNN
19.57 
31.28 
8.67
22.02 
34.77 
10.09 
24.72 
38.47 
11.79 
14.08 
21.96 
9.51
14.75 
24.34 
9.84
16.25 
25.99 
10.68
StemGNN 
19.83 
31.94 
8.72
21.82 
35.16 
10.26 
25.38 
40.08 
11.90 
14.56 
22.90 
9.24
15.90
25.17
10.09
18.41
28.93
11.74
GTS
21.06 
32.89 
9.17
23.68 
36.53 
10.79 
28.44 
42.83 
12.81 
15.03 
23.47 
9.60
16.78
26.38
10.84
20.21
31.28
14.05
DGCRN
19.67 
31.58 
9.10
21.97 
34.64 
10.29 
25.01 
38.42 
12.12 
13.36 
22.35 
8.95
14.34 
24.10 
9.49
16.02 
25.96 
10.45
MegaCRN 
19.43 
31.16 
8.86
21.77 
34.65 
10.44 
24.82 
37.99 
12.08 
13.85 
22.17 
9.44
14.93 
23.96 
10.09 
16.63 
26.32 
11.22
DFDGCN
19.90 
31.07 
8.95
21.56 
34.94 
9.70 
24.26 
38.47 
11.96 
13.49 
21.96 
8.97
14.28 
24.27 
9.45 
15.47 
26.03 
10.32
STPGNN
19.68 
32.02 
8.84
21.86 
35.51 
10.36 
25.89 
41.19 
11.95 
14.42 
22.98 
9.25
15.98 
25.59 
10.26 
18.97 
29.84 
12.27
HimNet
19.54 
31.14 
8.52
21.42 
34.56 
10.72 
24.13 
38.39 
11.91 
13.31 
22.00 
9.19
14.08 
23.83 
9.75
15.50 
26.13 
10.56
M3Net
19.72 
31.68 
8.96
21.97 
34.78 
10.53 
24.34 
38.61 
11.85 
13.67 
22.53 
9.50
14.19 
24.34 
9.50
15.73 
26.57 
10.62
STDN
19.81 
38.86 
9.42
22.15
41.30
10.02
24.34
43.86
12.71
13.77
22.36
10.29
14.54
24.18
10.81
15.71
26.34
11.77
STADNN 
19.18 
30.89 
8.46 
21.23 
34.00 
9.80 
23.81 
37.95 
11.46 
12.87 
21.65 
8.57 
13.66 
23.54 
9.01 
14.94 
25.77 
9.85
these two tables, which highlight the overall prediction performance 
in terms of MAE, RMSE, and MAPE at different time horizons. Firstly, 
STADNN consistently outperforms other baselines across most evalu­ 
ation metrics and prediction horizons on four datasets. For instance, 
on the PEMS08 dataset, STADNN achieves the lowest MAE of 12.87, 
RMSE of 21.65, and MAPE of 8.57 at the 15-minute horizon, surpassing 
other models by a margin. This trend is maintained at the 30-minute 
and 60-minute horizons, where STADNN continues to exhibit the best 
performance. The experimental results on other datasets lead to similar 
conclusions from the table.
Secondly, spatio-temporal forecasting models such as GWNet and 
AGCRN leverage adaptive graph learning or recurrent architectures 
to capture time-varying spatial dependencies. This dynamic modeling 
capability enables them to better represent complex and evolving traf­ 
fic patterns. These models adapt to the changing conditions of traffic 
networks more effectively than those relying solely on static graphs. 
The attention mechanism in STADNN can also capture the dynamic 
nature of traffic data. A recent advancement, the STPGNN model, 
which integrates pivotal pattern modeling, has shown promising results. 
HimNet achieves improved performance over previous methods, thanks 
to its explicit modeling of spatiotemporal heterogeneity. M3Net deliv­ 
ers competitive results without using any predefined graph structure. 
Nonetheless, these approaches do not explicitly address spatio-temporal 
pattern decomposition. STDN attempts to decompose spatio-temporal 
patterns but does so without tailoring its modeling specifically to the de­ 
composed features. Our STADNN incorporates spatio-temporal adaptive 
decomposition, demonstrating an average performance improvement of 
more than 5 % across various metrics.
In summary, STADNN’s method of spatio-temporal decomposition 
followed by specialized modeling offers superior performance. This out­ 
come highlights the forecasting effectiveness and generalizability across 
different datasets of our method.
5.6 . Ablation study
We conducted a comprehensive analysis from two perspectives to 
evaluate the contributions of individual components within our model. 
The results are shown in Fig. 3 and Tables 4 and 5. Firstly, we evalu­ 
ated the impact of individual modules on overall model performance by 
constructing five variants of our model. Secondly, we delved into the 
effectiveness of our proposed spatio-temporal adaptive decomposition 
method.
To assess the contribution of each module, we designed the following 
model variants: w/o DINW: removes the learnable day of week embed­ 
ding; w/o TIND: removes the learnable time of day embedding; w/o 
SPA: removes the learnable spatial embedding; w/o SENC: eliminates 
the spatial encoder responsible for spatial modeling; w/o TENC: re­ 
moves the temporal encoder, including those for spatio-temporal trend 
Fig. 3. Ablation study across four datasets.
Neurocomputing 669 (2026) 132486 
6 


## Page 7

Y. Wang, R. Li, X. Li et al.
Table 4 
Spatio-temporal decomposition analysis on the PEMS03 and PEMS04 datasets. The best result in each column is highlighted in bold.
Model variants
PEMS03
PEMS04
15 min
30 min
60 min
15 min
30 min
60 min
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
STADNN-ND
15.21
25.57
16.40
28.20
17.73
30.55
19.21
30.25
19.81
31.54
20.33
33.15
STADNN-MA
14.71
25.12
15.69
27.42
17.50
30.15
18.56
29.64
18.97
31.22
20.08
32.47
STADNN-DA
14.42
24.92
15.74
27.25
17.42
30.00
18.21
29.47
19.02
30.85
19.98
32.62
STADNN-DT
14.86
25.25
15.63
27.30
17.25
29.85
18.77
29.76
18.89
30.91
19.79
32.35
STADNN
14.14
24.66
15.40
26.94
17.06
29.73
17.85
29.18
18.61
30.61
19.57
32.21
Table 5 
Spatio-temporal decomposition analysis on the PEMS07 and PEMS08 datasets. The best result in each column is highlighted in bold.
Model variants
PEMS07
PEMS08
15 min
30 min
60 min
15 min
30 min
60 min
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
STADNN-ND
21.18
33.48
23.57
35.94
26.38
40.49
14.21
23.47
15.16
24.89
16.55
27.51
STADNN-MA
20.45
32.59
22.04
35.26
24.88
39.39
13.72
22.83
14.18
24.42
15.61
26.74
STADNN-DA
19.93
31.87
21.91
35.12
24.36
38.52
13.37
22.13
14.05
24.31
15.28
26.16
STADNN-DT
19.81
31.70
21.76
34.61
24.60
38.60
13.29
22.21
14.00
23.97
15.44
26.20
STADNN
19.18
30.89
21.23
34.00
23.81
37.95
12.87
21.65
13.66
23.54
14.94
25.77
and periodicity modeling. The results, as shown in Fig. 3, indicate 
that all these modifications led to performance degradation compared 
to the full model. Notably, the removal of the spatial encoder or the 
temporal encoder highlights the critical role of spatio-temporal joint 
modeling in traffic prediction. Additionally, the exclusion of learnable 
embeddings across different dimensions also resulted in decreased per­ 
formance, which suggests that incorporating learnable parameters for 
time intervals and spatial nodes can enhance model capability.
To further validate the design of our spatio-temporal adaptive 
decomposition, we conducted a targeted ablation study across four 
datasets. The results are shown in Tables 4 and 5. We constructed four 
variants to isolate the impact of decomposition strategy and modeling 
structure: STADNN-WD: removes decomposition entirely and raw in­ 
puts are fed directly into the temporal encoder; STADNN-MA: replaces 
adaptive decomposition with classical moving average for decomposi­ 
tion; STADNN-DA: applies decomposition but routes both components 
through attention-based encoders; STADNN-DT: similarly decomposes 
inputs but processes both components with TCN-based encoders. Results 
show that the full STADNN consistently achieves the lowest error. The 
performance drop in STADNN-WD and STADNN-MA confirms that de­ 
composition is essential—not merely as a preprocessing step, but as an 
adaptive, learnable mechanism that captures meaningful patterns more 
effectively than fixed heuristics like moving average. The degradation 
in STADNN-DA and STADNN-DT reveals a second critical insight: trend 
and periodic components exhibit distinct temporal dynamics and thus 
require specialized modeling pathways.
In summary, the ablation confirms that the model design of STADNN 
and adaptive decomposition is effective in capturing spatio-temporal 
correlations. Both elements are indispensable to the model’s predictive 
power.
5.7 . Parameter sensitivity study
To investigate the impact of parameter sensitivity on model per­ 
formance, we conducted an exploration of two critical parameters— 
embedding dimension and the number of layers. These parameters were 
selected as they fundamentally govern the model’s expressiveness and 
complexity: the embedding dimension dictates the granularity of la­ 
tent feature representation, while the number of layers determines the 
ability to capture high-order non-linear interactions. The experimental 
results across four datasets are illustrated in Fig. 4. As shown in Fig. 4, 
it is evident that an embedding dimension of 16 yields the lowest er­ 
ror rates for both metrics on most datasets. As the dimension increases 
from 8 to 16, there is a noticeable performance improvement, indi­ 
cating that a higher-dimensional space initially enhances the model’s 
capacity to capture intricate feature representations. However, further 
increasing the dimension beyond 16 leads to a gradual increase in errors, 
particularly pronounced at 64 dimensions. This suggests that while a 
moderate increase in embedding size can be beneficial, excessively high 
dimensions introduce unnecessary complexity, potentially leading to 
overfitting. Turning to the sensitivity of the number of layers, the model 
achieves the best performance at two layers. In summary, our parame­ 
ter experiments reveal that an embedding dimension of 16 and a 2-layer 
architecture offer the best trade-off between model capacity and gener­ 
alization. These settings ensure that the model can effectively learn from 
the data without becoming overly complex. Practically, this offers a key 
insight for decomposition-based approaches in short-term traffic predic­ 
tion: deep stacking is not strictly necessary. Our results demonstrate that 
a shallow parallel structure (e.g., 2 layers) combined with a compact 
embedding space is sufficient to model temporal dynamics effectively, 
avoiding the overfitting risks associated with over-parameterized deep 
networks.
5.8 . Convergence analysis
To better understand the training dynamics and generalization be­ 
havior of our model, we analyze its validation loss convergence across 
multiple datasets. We visualize the validation loss curves of STADNN 
alongside several representative baselines on four datasets. As shown 
in Fig. 5, STADNN converges within a comparable or slightly fewer 
number of epochs than most baselines, with a relatively stable decline 
in validation loss. This indicates that the model not only learns effi­ 
ciently from the training data but also maintains stable generalization 
throughout training. The steady decline in validation loss further sug­ 
gests that STADNN is well-regularized and effectively captures essential 
spatio-temporal dependencies without overfitting.
5.9 . Efficiency analysis
To evaluate the computational cost of our approach, we report 
model size, training time per epoch, and inference latency on four 
traffic datasets in comparison with representative baselines. As shown 
in Table 6, STADNN adopts a parallel decomposition structure to 
Neurocomputing 669 (2026) 132486 
7 


## Page 8

Y. Wang, R. Li, X. Li et al.
Fig. 4. Prediction performance of different parameter settings across four datasets. Each column represents the results on one dataset.
Fig. 5. Validation loss of STADNN and key models across four datasets.
Table 6 
Model efficiency comparison of STADNN and several key models across four datasets. Reported metrics: number of parameters (M), training 
time per epoch (s/epoch), and inference time per sample (ms/sample).
Model
PEMS03
PEMS04
PEMS07
PEMS08
Params
Train
Infer
Params
Train
Infer
Params
Train
Infer
Params
Train
Infer
MegaCRN
0.395
92.00
2.589
0.393
64.33
3.171
0.416
213.59
5.656
0.387
12.78
0.863
DFDGCN
0.835
92.50
1.579
0.763
66.56
1.697
1.575
215.16
4.053
0.570
84.35
1.601
STPGNN
0.380
75.33
2.032
0.377
52.33
2.291
0.414
131.01
2.742
0.368
4.79
0.290
HimNet
1.253
209.94
5.064
1.254
149.21
5.021
1.262
815.81
33.912
2.070
161.14
3.035
M3Net
0.428
23.69
0.771
0.425
15.73
0.790
0.450
34.69
0.940
0.420
15.48
0.710
STDN
6.358
123.43
2.811
6.227
70.20
2.352
4.489
272.99
5.348
5.876
55.94
1.854
STADNN
0.599
52.29
1.101
0.598
29.44
0.898
0.616
193.65
3.865
0.591
15.18
0.502
capture multi-scale temporal patterns, resulting in a moderate model 
scale—larger than the compact M3Net but smaller than several other 
methods, including the decomposition-based STDN. In terms of ef­ 
ficiency, STADNN demonstrates competitive training and inference 
speeds across all datasets, benefiting from its shallow two-layer archi­ 
tecture and streamlined embedding design. While HimNet achieves high 
predictive accuracy, its model scale and training cost are relatively 
high. Similarly, STDN utilizes over 4.4 million parameters and shows 
moderate convergence speed across datasets. M3Net attains the highest 
efficiency among the compared models, owing to its graph-free design 
that entirely bypasses explicit spatial message passing. In summary, 
STADNN achieves a favorable trade-off between model complexity and 
predictive performance. By combining a shallow architecture with a 
lightweight parallel decomposition scheme, it avoids the high parame­ 
ter counts and prolonged training times of deeper or over-parameterized 
models. This balance between efficiency and accuracy makes STADNN 
more suitable for real-world deployment than other heavier models. Its 
lower training and inference costs, combined with competitive forecast­ 
ing performance, suggest greater practical potential in effective traffic 
forecasting tasks.
5.10 . Few-shot traffic prediction
This section evaluates the model’s performance under few-shot traf­ 
fic forecasting scenarios, which commonly arise in the early stages of 
smart city deployment. In such settings, historical spatio-temporal data 
are often limited due to newly installed sensors, immature data collec­ 
tion infrastructure, or sparse sensor coverage. To emulate this practical 
constraint, we train STADNN and recent baselines using only 30 % of the 
data as the training set. As shown in Tables 7 and 8, STADNN achieves 
competitive performance despite the reduced training data, maintaining 
both prediction accuracy and stability better than most baselines. This 
Neurocomputing 669 (2026) 132486 
8 


## Page 9

Y. Wang, R. Li, X. Li et al.
Table 7 
Few-shot traffic prediction on the PEMS03 and PEMS04 datasets. The best result in each column is highlighted in bold.
Model variants
PEMS03
PEMS04
15 min
30 min
60 min
15 min
30 min
60 min
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MegaCRN
15.22
27.35
16.97
30.41
19.02
34.19
20.16
30.87
20.44
32.50
21.58
34.87
STPGNN
15.15
27.50
16.73
30.24
19.02
34.05
21.97
32.17
22.23
34.01
26.87
40.25
HimNet
15.06
27.05
16.81
30.30
18.64
33.92
19.39
30.91
19.62
32.31
21.32
35.34
M3Net
14.88
27.61
16.86
30.42
19.27
34.19
19.52
31.10
19.66
32.25
21.31
35.25
STDN
15.25
27.88
16.83
25.17
18.58
33.83
19.34
35.89
19.75
37.91
21.84
41.32
STADNN
14.84
27.00
16.37
29.94
18.52
33.79
18.65
30.34
19.17
31.22
20.37
33.49
Table 8 
Few-shot traffic prediction on the PEMS07 and PEMS08 datasets. The best result in each column is highlighted in bold.
Model variants
PEMS07
PEMS08
15 min
30 min
60 min
15 min
30 min
60 min
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MAE
RMSE
MegaCRN
21.75
33.61
23.64
36.54
26.58
40.76
14.15
23.10
15.23
25.32
17.25
27.91
STPGNN
22.71
35.06
25.32
39.04
30.48
45.99
14.91
23.49
16.75
26.53
20.44
31.77
HimNet
21.47
33.91
23.21
36.88
24.76
40.31
13.81
22.94
14.63
24.92
19.26
27.58
M3Net
21.41
33.45
22.86
36.18
25.02
40.11
13.54
22.88
14.47
24.86
16.18
27.76
STDN
23.55
42.34
24.37
43.73
26.79
45.72
14.07
22.98
14.83
25.17
16.58
27.63
STADNN
21.01
33.40
22.41
36.20
24.46
39.65
13.39
22.51
14.28
24.52
15.81
27.16
Table 9 
Average prediction performance of STADNN and several key models across three large-scale 
traffic datasets. The best result in each column is highlighted in bold.
Model
SD
GBA
GLA
MAE
RMSE
MAPE
MAE
RMSE
MAPE
MAE
RMSE
MAPE
GWNet
18.38
31.14
12.15
20.96
34.11
17.07
20.78
34.63
13.05
STPGNN
22.33
36.13
14.67
20.95
34.23
17.21
20.74
34.58
12.93
M3Net
18.07
31.19
11.93
21.70
35.45
17.91
20.73
34.45
13.10
STDN
19.33
77.61
16.55
22.67
69.10
21.68
29.14
190.04
43.63
STADNN
18.21
30.81
11.89
20.80
34.25
17.13
20.71
34.43
12.99
demonstrates its robustness in data-scarce regimes and underscores its 
potential for real-world applications where extensive historical records 
are unavailable.
5.11 . Large-scale traffic forecasting
To evaluate the model’s scalability and performance in complex, 
large-scale traffic systems, we conduct experiments on a large-scale traf­ 
fic benchmark LargeST [31], including three datasets—SD (716 nodes), 
GBA (2352 nodes), and GLA (3834 nodes)—representing increasingly 
challenging spatio-temporal graph structures. Given the computational 
constraints, we select several state-of-the-art models that can be trained 
on a single GPU. We report the average prediction metrics across these 
datasets in Table 9. STADNN demonstrates competitive results across 
all settings. On the largest dataset GLA, it achieves the lowest MAE 
and RMSE among all compared methods. On SD and GBA, while it 
does not always obtain the best score, the performance gap is marginal. 
STDN, which also relies on the decomposition strategy, shows a de­ 
cline in performance as the network scale increases. This degradation 
suggests that its decomposition mechanism, while effective on smaller 
graphs, may struggle to maintain spatio-temporal coherence when ap­ 
plied to highly complex traffic systems. For prediction efficiency, our 
model achieves an average single-sample inference time of 37.8 ms 
on the largest GLA dataset on a commodity GPU. This latency is well 
within the widely adopted 30-second data update interval of real-
world traffic monitoring systems, satisfying the real-time requirement 
for operational deployment. Overall, the results suggest that STADNN 
can maintain stable performance across traffic networks of varying 
scales.
6 . Conclusion
In this paper, we propose a decomposition-based spatio-temporal 
modeling framework STADNN for traffic forecasting. STADNN 
adaptively separates traffic dynamics into trend and periodic compo­ 
nents, and designs dedicated temporal encoders to capture their distinct 
patterns. A spatial transformer is further introduced to model global 
node interactions. Extensive experiments on real-world benchmarks 
demonstrate that our method achieves state-of-the-art performance, 
outperforming existing approaches across multiple prediction horizons. 
Moreover, it maintains a reasonable balance between model complexity 
and performance. For future work, the decomposition framework could 
be adapted to broader spatio-temporal forecasting tasks by incorpo­ 
rating domain-specific structural priors. The current architecture also 
provides a foundation for exploring cross-city generalization in traffic 
prediction.
CRediT authorship contribution statement
Yong Wang: Writing – review & editing, Writing – original 
draft, Validation, Resources, Methodology, Investigation, Formal anal­ 
ysis, Conceptualization. Ruidong Li: Writing – review & editing, 
Visualization, Validation, Resources, Conceptualization. Xiaoyu Li: 
Writing – review & editing, Writing – original draft, Supervision, 
Methodology, Investigation, Conceptualization. Yongshun Gong: 
Writing – review & editing, Supervision, Project administration, 
Methodology, Funding acquisition, Formal analysis. Xiushan Nie: 
Writing – review & editing, Visualization, Supervision, Resources, 
Neurocomputing 669 (2026) 132486 
9 


## Page 10

Y. Wang, R. Li, X. Li et al.
Investigation, Formal analysis. Yilong Yin: Writing – review & editing, 
Validation, Supervision, Project administration, Investigation.
Declaration of competing interest
The authors declare the following financial interests/personal rela­ 
tionships that may be considered as potential competing interests:
Yongshun Gong reports that financial support was provided by 
Shandong University. If there are other authors, they declare that they 
have no known competing financial interests or personal relationships 
that could have appeared to influence the work reported in this paper.
Acknowledgements
This work was supported by the Key Technology Breakthrough and 
Industrialization Demonstration Project of Qingdao (Grant No. 24-1–2-
qljh-23-gx), the National Natural Science Foundation of China (Grant 
No. 62476154), and the Major Basic Research Project of Shandong 
Provincial Natural Science Foundation (Grant No. ZR2024ZD03).
Data availability
Data will be made available on request. 
References
[1] Y. An, Z. Li, X. Li, W. Liu, X. Yang, H. Sun, M. Chen, Y. Zheng, Y. Gong, Spatio-
temporal multivariate probabilistic modeling for traffic prediction, IEEE Trans. 
Knowl. Data Eng. (2025) 2986–3000.
[2] O.D. Anderson, M.G. Kendall, Time-series. 2nd edn., Stat. (1976) 308.
[3] R. Asadi, A.C. Regan, A spatio-temporal decomposition based deep neural network 
for time series forecasting, Appl. Soft Comput. (2020) 105963.
[4] L. Bai, L. Yao, C. Li, X. Wang, C. Wang, Adaptive graph convolutional recurrent 
network for traffic forecasting, in: NeurIPS, 2020, pp. 17804–17815.
[5] D. Cao, Y. Wang, J. Duan, C. Zhang, X. Zhu, C. Huang, Y. Tong, B. Xu, J. Bai, J. 
Tong, et al., Spectral temporal graph neural network for multivariate time-series 
forecasting, in: NeurIPS, 2020, pp. 17766–17778.
[6] L. Cao, B. Wang, G. Jiang, Y. Yu, J. Dong, Spatiotemporal-aware trend-
seasonality decomposition network for traffic flow forecasting, in: AAAI, 2025, 
pp. 11463–11471.
[7] C. Chen, K. Petty, A. Skabardonis, P. Varaiya, Z. Jia, Freeway performance 
measurement system: mining loop detector data, Transp. Res. Rec. (2001) 96–102.
[8] J. Chung, C. Gulcehre, K. Cho, Y. Bengio, Empirical evaluation of gated recurrent 
neural networks on sequence modeling, arXiv preprint arXiv:1412.3555, 2014. 
[9] R.B. Cleveland, W.S. Cleveland, J.E. McRae, I. Terpenning, et al., Stl: a seasonal-
trend decomposition, J. Off. Stat. (1990) 3–73.
[10] Z. Dong, R. Jiang, H. Gao, H. Liu, J. Deng, Q. Wen, X. Song, Heterogeneity-informed 
meta-parameter learning for spatiotemporal time series forecasting, in: KDD, 2024, 
pp. 631–641.
[11] W. Duan, X. He, Z. Zhou, L. Thiele, H. Rao, Localised adaptive spatial-temporal 
graph neural network, in: KDD, 2023, pp. 448–458.
[12] Y. Fang, Y. Qin, H. Luo, F. Zhao, B. Xu, L. Zeng, C. Wang, When spatio-temporal 
meet wavelets: disentangled traffic forecasting via efficient spectral graph attention 
networks, in: ICDE, 2023, pp. 517–529.
[13] Y. Gong, P. Yu, X. Zhang, X. Zhang, X. Nie, H. Sun, Exploiting dynamic spatio-
temporal correlations for origin-destination demand prediction, Expert Syst. Appl. 
(2025) 130095.
[14] S. Guo, Y. Lin, N. Feng, C. Song, H. Wan, Attention based spatial-temporal graph 
convolutional networks for traffic flow forecasting, in: AAAI, 2019, pp. 922–929.
[15] S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Comput. (1997) 
1735–1780.
[16] A. Ji, D. Li, Z. Dai, M. Cui, L. Yu, Z. Duan, A hybrid graph memory network ap­ 
proach with multi-level feature representation for traffic flow forecast, Expert Syst. 
Appl. (2025) 130316.
[17] A. Ji, Z. Liu, L. Su, Z. Dai, A hybrid framework for spatio-temporal traffic flow 
prediction with multi-scale feature extraction, Inf. Sci. (2025) 122259.
[18] J. Jiang, C. Han, W.X. Zhao, J. Wang, Pdformer: propagation delay-aware dynamic 
long-range transformer for traffic flow prediction, in: AAAI, 2023, pp. 4365–4373.
[19] R. Jiang, Z. Wang, J. Yong, P. Jeph, Q. Chen, Y. Kobayashi, X. Song, T. Suzumura, 
S. Fukushima, Megacrn: Meta-graph convolutional recurrent network for spatio-
temporal modeling, arXiv preprint arXiv:2212.05989, 2022. 
[20] G. Jin, S. Lai, X. Hao, J. Zhang, M. Zhang, M3-Net: a cost-effective graph-free mlp-
based model for traffic prediction, in: CIKM, 2025, pp. 4847–4851.
[21] G. Jin, Y. Liang, Y. Fang, Z. Shao, J. Huang, J. Zhang, Y. Zheng, Spatio-temporal 
graph neural networks for predictive learning in urban computing: a survey, IEEE 
Trans. Knowl. Data Eng. (2023) 5388–5408.
[22] W. Kong, Z. Guo, Y. Liu, Spatio-temporal pivotal graph neural networks for traffic 
flow forecasting, in: AAAI, 2024, pp. 8627–8635.
[23] S. Lan, Y. Ma, W. Huang, W. Wang, H. Yang, P. Li, Dstagnn: dynamic spatial-
temporal aware graph neural network for traffic flow forecasting, in: ICML, 2022, 
pp. 11906–11917.
[24] F. Li, J. Feng, H. Yan, G. Jin, F. Yang, F. Sun, D. Jin, Y. Li, Dynamic graph con­ 
volutional recurrent network for traffic prediction: benchmark and solution, ACM 
Trans. Knowl. Discov. Data (2023) 1–21.
[25] X. Li, Y. Gong, W. Liu, Y. Yin, Y. Zheng, L. Nie, Dual-track spatio-temporal learn­ 
ing for urban flow prediction with adaptive normalization, Artif. Intell. (2024) 
104065.
[26] X. Li, Y. Zhang, G. Long, Y. Hu, W. Lu, M. Chen, C. Zhang, Y. Gong, Adaptive traffic 
forecasting on daily basis: a spatio-temporal context learning approach, IEEE Trans. 
Knowl. Data Eng. (2025) 1–14.
[27] Y. Li, Z. Shao, Y. Xu, Q. Qiu, Z. Cao, F. Wang, Dynamic frequency domain graph 
convolutional network for traffic forecasting, in: ICASSP, 2024, pp. 5245–5249.
[28] Y. Liang, S. Liu, Y. Bai, Y. Gong, T. Zhu, Dsm-stwave: enhancing traffic flow 
prediction for both offline and online scenarios, Neurocomputing (2025) 131836.
[29] H. Liu, Z. Dong, R. Jiang, J. Deng, J. Deng, Q. Chen, X. Song, Spatio-temporal 
adaptive embedding makes vanilla transformer SOTA for traffic forecasting, in: 
CIKM, 2023, pp. 4125–4129.
[30] X. Liu, Y. Liang, C. Huang, H. Hu, Y. Cao, B. Hooi, R. Zimmermann, Do 
we really need graph neural networks for traffic forecasting? arXiv preprint 
arXiv:2301.12603, 2023. 
[31] X. Liu, Y. Xia, Y. Liang, J. Hu, Y. Wang, L. Bai, C. Huang, Z. Liu, B. Hooi, R. 
Zimmermann, Largest: a benchmark dataset for large-scale traffic forecasting, in: 
NeurIPS, 2023, pp. 75354–75371.
[32] J. Qi, H. Fan, Routeformer: transformer utilizing routing mechanism for traffic flow 
forecasting, Neurocomputing 633 (2025) 129753.
[33] C. Shang, J. Chen, Discrete graph structure learning for forecasting multiple time 
series, in: ICLR, 2021.
[34] Z. Shao, F. Wang, Y. Xu, W. Wei, C. Yu, Z. Zhang, D. Yao, T. Sun, G. Jin, X. Cao, 
et al., Exploring progress in multivariate time series forecasting: comprehensive 
benchmarking and heterogeneity analysis, IEEE Trans. Knowl. Data Eng. (2024) 
291–305.
[35] Z. Shao, Z. Zhang, F. Wang, W. Wei, Y. Xu, Spatial-temporal identity: a simple 
yet effective baseline for multivariate time series forecasting, in: CIKM, 2022, pp. 
4454–4458.
[36] Z. Shao, Z. Zhang, W. Wei, F. Wang, Y. Xu, X. Cao, C.S. Jensen, Decoupled dy­ 
namic spatial-temporal graph neural network for traffic forecasting, PVLDB (2022) 
2733–2746.
[37] S. Siami-Namini, N. Tavakoli, A.S. Namin, A comparison of arima and LSTM in 
forecasting time series, in: ICMLA, 2018, pp. 1394–1401.
[38] C. Song, Y. Lin, S. Guo, H. Wan, Spatial-temporal synchronous graph convolu­ 
tional networks: a new framework for spatial-temporal network data forecasting, 
in: AAAI, 2020, pp. 914–921.
[39] J.H. Stock, M.W. Watson, Vector autoregressions, J. Econ. Perspect. (2001) 
101–115.
[40] S.J. Taylor, B. Letham, Forecasting at scale, Am. Stat. (2018) 37–45.
[41] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A.N. Gomez, Ł. Kaiser, 
I. Polosukhin, Attention is all you need, in: NeurIPS, 2017.
[42] B. Wang, P. Wang, Y. Zhang, X. Wang, Z. Zhou, L. Bai, Y. Wang, Towards dy­ 
namic spatial-temporal graph learning: a decoupled perspective, in: AAAI, 2024, 
pp. 9089–9097.
[43] J. Wang, J. Jiang, W. Jiang, C. Li, W.X. Zhao, Libcity: an open library for traffic 
prediction, in: SIGSPATIAL, 2021, pp. 145–148.
[44] Z. Wang, Y. Nie, P. Sun, N.H. Nguyen, J. Mulvey, H.V. Poor, St-mlp: A cascaded 
spatio-temporal linear framework with channel-independence strategy for traffic 
forecasting, arXiv preprint arXiv:2308.07496, 2023. 
[45] H. Wu, J. Xu, J. Wang, M. Long, Autoformer: decomposition transformers 
with auto-correlation for long-term series forecasting, in: NeurIPS, 2021, pp. 
22419–22430.
[46] Z. Wu, S. Pan, G. Long, J. Jiang, C. Zhang, Graph wavenet for deep spatial-temporal 
graph modeling, in: IJCAI, 2019, pp. 1907–1973.
[47] Z. Wu, S. Pan, G. Long, J. Jiang, X. Chang, C. Zhang, Connecting the dots: mul­ 
tivariate time series forecasting with graph neural networks, in: KDD, 2020, pp. 
753–763.
[48] P. Xie, T. Li, J. Liu, S. Du, X. Yang, J. Zhang, Urban flow prediction from 
spatiotemporal data using machine learning: a survey, Inf. Fusion (2020) 1–12.
[49] H. Ye, G. Duan, H. Zeng, Y. Zhu, L. Meng, X. Zheng, Y. Zhu, Karma: a multilevel 
decomposition hybrid mamba framework for multivariate long-term time series 
forecasting, in: WAI-CSA, 2025, pp. 266–276.
[50] B. Yu, H. Yin, Z. Zhu, Spatio-temporal graph convolutional networks: a deep 
learning framework for traffic forecasting, in: IJCAI, 2018, pp. 3634–3640.
[51] P. Yu, X. Zhang, Y. Gong, J. Zhang, H. Sun, J. Zhang, X. Zhang, Y. Yin, Enhancing 
origin–destination flow prediction via bi-directional spatio-temporal inference and 
interconnected feature evolution, Expert Syst. Appl. 264 (2025) 125679.
[52] J. Zhang, Y. Zheng, D. Qi, Deep spatio-temporal residual networks for citywide 
crowd flows prediction, in: AAAI, 2017, pp. 1655–1661.
[53] X. Zhang, Y. Gong, X. Zhang, X. Wu, C. Zhang, X. Dong, Mask-and contrast-
enhanced spatio-temporal learning for urban flow prediction, in: CIKM, 2023, pp. 
3298–3307.
[54] Y. Zhang, J. Yan, Crossformer: transformer utilizing cross-dimension dependency 
for multivariate time series forecasting, in: ICLR, 2023.
[55] L. Zhao, M. Gao, Z. Wang, St-gsp: spatial-temporal global semantic representation 
learning for urban flow prediction, in: WSDM, 2022, pp. 1443–1451.
[56] Y. Zhao, X. Luo, W. Ju, C. Chen, X.-S. Hua, M. Zhang, Dynamic hypergraph 
structure learning for traffic flow forecasting, in: ICDE, 2023, pp. 2303–2316.
[57] C. Zheng, X. Fan, C. Wang, J. Qi, Gman: a graph multi-attention network for traffic 
prediction, in: AAAI, 2020, pp. 1234–1241.
Neurocomputing 669 (2026) 132486 
10 


## Page 11

Y. Wang, R. Li, X. Li et al.
[58] H. Zhou, S. Zhang, J. Peng, S. Zhang, J. Li, H. Xiong, W. Zhang, Informer: beyond 
efficient transformer for long sequence time-series forecasting, in: AAAI, 2021, pp. 
11106–11115.
Author biography
Yong Wang is currently a Ph.D. candidate at the School of 
Computer Science and Technology, Xi’an Jiaotong University. 
He received his B.S. degree from Qingdao University of 
Science and Technology and his M.S. degree from Shandong 
University. His research interests include machine learning, 
computer vision, and data mining.
Ruidong Li is a Senior Engineer at Shandong Yunhai 
Guochuang Cloud Computing Equipment Industry Innovation 
Co., Ltd. He received his M.S. degree from Shandong 
University and has been selected as a recipient of the Taishan 
Industrial Leading Talent Program of Shandong Province. His 
research focuses on deep learning and data mining.
Xiaoyu Li is currently a Ph.D. student at The Hong Kong 
Polytechnic University. He received his B.S. and M.S. degrees 
in Software Engineering from Shandong University, China. 
His research interests include spatio-temporal data mining 
and machine learning. He has published multiple papers in 
top-tier venues, including AIJ and IEEE TKDE.
Yongshun Gong received the Ph.D. degree from the 
University of Technology Sydney. He is a professor with 
the School of Software, Shandong University, China. His 
Principal research interest covers data science and ma­ 
chine learning, in particular, the following areas: spatio-
temporal data mining and traffic prediction. He has published 
above 80 papers in top journals and refereed conference 
proceedings, including the IEEE Transactions on Pattern 
Analysis and Machine Intelligence, Artificial Intelligence, 
IEEE Transactions on Knowledge and Data Engineering, IEEE 
Transactions on Neural Networks and Learning Systems, IEEE
 
 Transactions on Cybernetics, NeurIPS, KDD, CVPR, CIKM, 
 
 AAAI.
Xiushan Nie received the Ph.D. degree from Shandong 
University, China, in 2011. He is currently a full profes­ 
sor with the School of Computer Science and Technology, 
Shandong Jianzhu University, China. He was a research fel­ 
low under the supervision of Prof. Wenjun (Kevin) Zeng with 
the University of Missouri-Columbia, Columbia, Missouri 
(2013–2014). His research interests include multimedia re­ 
trieval and indexing, multimedia security, and computer 
vision.
Yilong Yin received the Ph.D. degree from Jilin University, 
Changchun, China, in 2000. He is the director of the Machine 
Learning and Applications Group and a Distinguished 
Professor with Shandong University, Jinan, China. From 2000 
to 2002, he was a Postdoctoral Fellow with the Department 
of Electronic Science and Engineering, Nanjing University, 
Nanjing, China. His research interests include machine learn­ 
ing, data mining, computational medicine, and biometrics. 
He has published more than 100 papers in top journals and 
refereed conference proceedings including TKDE, TIP, TMM, 
ICML, IJCAI, etc.
Neurocomputing 669 (2026) 132486 
11 
