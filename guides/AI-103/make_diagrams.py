"""Generate the ORIGINAL inline-SVG diagram library for the public AI-103 guide.

Clean-room: these are original schematic diagrams in our own visual style, expressing
well-documented, factual Azure AI Foundry concepts (project topology, model selection,
RAG, agents, deployment options, content safety, evaluation, security, vision, speech,
search/retrieval, document extraction). No Microsoft images/slides are used or reproduced.
Each diagram is saved to assets/diagrams/<id>.svg with a responsive viewBox.
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "diagrams")
os.makedirs(OUT, exist_ok=True)

# palette
NAVY="#0b3d63"; BLUE="#0f6cbd"; BLUEL="#3a9bdc"; PALE="#eaf3fb"; INK="#1b2733"
MUTE="#5b6b7a"; OK="#107c41"; WARN="#b45309"; DANGER="#b3261e"; PURP="#5c2d91"
LINE="#c9d6e2"; WHITE="#ffffff"; PALE2="#dcebf8"
FONT="font-family='Segoe UI,Arial,sans-serif'"

def esc(s): return html.escape(str(s), quote=True)

def svg(w, h, body, title=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f"<svg viewBox='0 0 {w} {h}' xmlns='http://www.w3.org/2000/svg' "
            f"role='img' aria-label='{esc(title)}' {FONT}>{t}"
            f"<rect x='0' y='0' width='{w}' height='{h}' fill='{WHITE}'/>{body}</svg>")

def box(x,y,w,h,fill=BLUE,txt_="",sub="",tc=WHITE,r=10,fs=17,sfs=12.5,stroke="none",tcsub=None):
    o=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='1.5'/>"
    if txt_ and sub:
        o+=f"<text x='{x+w/2}' y='{y+h/2-4}' text-anchor='middle' fill='{tc}' font-size='{fs}' font-weight='600'>{esc(txt_)}</text>"
        o+=f"<text x='{x+w/2}' y='{y+h/2+15}' text-anchor='middle' fill='{tcsub or tc}' font-size='{sfs}'>{esc(sub)}</text>"
    elif txt_:
        o+=f"<text x='{x+w/2}' y='{y+h/2+6}' text-anchor='middle' fill='{tc}' font-size='{fs}' font-weight='600'>{esc(txt_)}</text>"
    return o

def txt(x,y,s,fill=INK,fs=13,w="400",anchor="start",italic=False):
    st=" font-style='italic'" if italic else ""
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}' font-size='{fs}' font-weight='{w}'{st}>{esc(s)}</text>"

def defs_arrow():
    return (f"<defs><marker id='ah' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>"
            f"<path d='M0,0 L8,3 L0,6 Z' fill='{MUTE}'/></marker>"
            f"<marker id='ahb' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>"
            f"<path d='M0,0 L8,3 L0,6 Z' fill='{BLUE}'/></marker>"
            f"<marker id='ahg' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>"
            f"<path d='M0,0 L8,3 L0,6 Z' fill='{OK}'/></marker></defs>")

def arrow(x1,y1,x2,y2,color=MUTE,dash=False,w=2):
    d=" stroke-dasharray='6 5'" if dash else ""
    mk="ah"
    if color==BLUE: mk="ahb"
    elif color==OK: mk="ahg"
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='{w}'{d} marker-end='url(#{mk})'/>"

def chip(x,y,w,h,s,fill=PALE,tc=NAVY,fs=12.5,r=6,stroke=LINE):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='1'/>"
            + txt(x+w/2,y+h/2+4,s,fill=tc,fs=fs,w="600",anchor="middle"))

D={}

# 1) Foundry project topology
def d_foundry():
    b=defs_arrow()
    b+=txt(400,32,"Azure AI Foundry topology",NAVY,20,"700","middle")
    b+=box(40,60,720,54,NAVY,"","",r=12)
    b+=txt(400,84,"Foundry resource (account)",WHITE,15,"700","middle")
    b+=txt(400,103,"Region \u00b7 identity \u00b7 networking \u00b7 shared quota",PALE,11.5,"400","middle")
    # projects
    px=[60,300,540]
    for i,x in enumerate(px):
        b+=arrow(400,114,x+100,140,BLUE)
        b+=box(x,142,200,48,BLUE,f"Project {i+1}","",r=10,fs=14)
    # under a project: deployments + connections + agents
    items=[("Model deployments",OK),("Connections",BLUEL),("Agents & threads",PURP)]
    y=210
    for j,(name,col) in enumerate(items):
        x=60+j*240
        b+=arrow(160,190,x+100,y,MUTE)
        b+=box(x,y,200,44,col,name,"",r=9,fs=13)
    b+=txt(400,286,"One account groups projects; each project owns its deployments, connections, and agents",MUTE,12,"400","middle")
    return svg(800,304,b,"Azure AI Foundry account, projects, deployments")
D["foundry-topology"]=d_foundry

# 2) Model selection decision
def d_modelselect():
    b=defs_arrow()
    b+=txt(400,30,"Choosing a model for the task",NAVY,19,"700","middle")
    rows=[("Complex reasoning / broad knowledge","Large language model (LLM)",BLUE),
          ("Low latency / low cost / on-device","Small language model (SLM)",OK),
          ("Images + text (or audio) together","Multimodal model",PURP),
          ("Search relevance / RAG grounding","Embedding model",BLUEL),
          ("Prebuilt skill (vision, speech, docs)","Foundry Tool / AI service",NAVY)]
    y=58
    for need,pick,col in rows:
        b+=box(40,y,360,40,PALE,"","",r=8,stroke=LINE)
        b+=txt(56,y+25,need,INK,12.8,"600")
        b+=arrow(400,y+20,452,y+20,MUTE)
        b+=box(456,y,304,40,col,pick,"",r=8,fs=13)
        y+=50
    return svg(800,y+8,b,"Model selection by task")
D["model-selection"]=d_modelselect

# 3) Deployment options
def d_deploy():
    b=""
    b+=txt(400,30,"Model deployment options",NAVY,19,"700","middle")
    cols=[("Standard",BLUEL,["Pay per token","Shared capacity","Quick start"]),
          ("Global / DataZone",BLUE,["Pay per token","Broad capacity","Best availability"]),
          ("Provisioned (PTU)",NAVY,["Reserved throughput","Predictable latency","High volume"]),
          ("Managed compute",PURP,["Dedicated VMs","Open / custom models","You size the SKU"])]
    x=30; colw=190
    for name,col,cells in cols:
        b+=box(x,56,colw-14,38,col,name,"",r=9,fs=14)
        for i,c in enumerate(cells):
            yy=100+i*40
            b+=box(x,yy,colw-14,34,PALE if i%2==0 else WHITE,"",r=6,stroke=LINE)
            b+=txt(x+(colw-14)/2,yy+21,c,INK,11.6,"500","middle")
        x+=colw
    b+=txt(400,244,"Pick per token for variable load; provisioned for steady high volume; managed compute for custom models",MUTE,11.5,"400","middle")
    return svg(800,262,b,"Deployment options comparison")
D["deployment-options"]=d_deploy

# 4) RAG pipeline
def d_rag():
    b=defs_arrow()
    b+=txt(400,30,"Retrieval-augmented generation (RAG)",NAVY,19,"700","middle")
    steps=[("User query","",BLUEL),("Retrieve","from index",BLUE),("Augment","prompt + context",NAVY),("Generate","grounded answer",OK)]
    x=30
    for i,(t,s,col) in enumerate(steps):
        b+=box(x,66,168,60,col,t,s,r=10,fs=14,sfs=11)
        if i<3: b+=arrow(x+168,96,x+192,96,MUTE)
        x+=192
    # knowledge store feeding retrieve
    b+=box(150,168,220,50,"#062338","Search index (vectors + text)",r=10,fs=12.5)
    b+=arrow(260,168,260,128,BLUE)
    b+=txt(400,246,"Ground the model on your data: retrieve relevant chunks, add them to the prompt, then generate",MUTE,12,"400","middle")
    return svg(800,264,b,"RAG retrieve augment generate flow")
D["rag-pipeline"]=d_rag

# 5) Agent anatomy
def d_agent():
    b=defs_arrow()
    b+=txt(400,30,"Anatomy of a Foundry agent",NAVY,19,"700","middle")
    b+=box(300,58,200,58,NAVY,"Agent","",r=12,fs=17)
    parts=[("Model","deployment",BLUE,60,150),
           ("Instructions","role & goals",OK,300,150),
           ("Tools","functions, search, APIs",PURP,540,150),
           ("Threads","conversation memory",BLUEL,300,232)]
    for t,s,col,x,y in parts:
        b+=box(x,y,200,52,col,t,s,r=10,fs=14,sfs=10.5)
        # arrow from agent
        b+=arrow(400,116,x+100,y,MUTE)
    b+=txt(400,304,"An agent binds a model + instructions + tools; threads persist the conversation state",MUTE,12,"400","middle")
    return svg(800,322,b,"Agent model instructions tools threads")
D["agent-anatomy"]=d_agent

# 6) Function-calling loop
def d_funccall():
    b=defs_arrow()
    b+=txt(400,30,"Function / tool calling loop",NAVY,19,"700","middle")
    b+=box(60,70,200,56,BLUE,"Model","decides a tool is needed",r=10,fs=15,sfs=10.5)
    b+=box(540,70,200,56,PURP,"Your function","runs code / calls API",r=10,fs=15,sfs=10.5)
    b+=arrow(260,88,540,88,BLUE)
    b+=txt(400,80,"1. tool call (name + JSON args)",MUTE,11.5,"600","middle")
    b+=arrow(540,112,260,112,OK)
    b+=txt(400,132,"2. tool result returned to model",MUTE,11.5,"600","middle")
    b+=box(300,170,200,50,NAVY,"Final answer","grounded in results",r=10,fs=14,sfs=10.5)
    b+=arrow(160,126,360,170,MUTE)
    b+=txt(400,246,"The model emits structured tool calls; your app executes them and feeds results back to complete the answer",MUTE,11.5,"400","middle")
    return svg(800,264,b,"Function calling loop")
D["function-calling"]=d_funccall

# 7) Multi-agent orchestration
def d_multiagent():
    b=defs_arrow()
    b+=txt(400,30,"Multi-agent orchestration",NAVY,19,"700","middle")
    b+=box(310,60,180,54,NAVY,"Orchestrator","main agent",r=12,fs=15,sfs=10.5)
    subs=[("Retrieval agent",BLUE,60),("Analysis agent",PURP,310),("Action agent",OK,560)]
    for name,col,x in subs:
        b+=box(x,168,180,50,col,name,"",r=10,fs=13.5)
        b+=arrow(400,114,x+90,168,BLUE)
        b+=arrow(x+90,168,400,114,MUTE,dash=True)
    b+=txt(400,250,"A lead agent delegates to connected specialist agents and composes their results",MUTE,12,"400","middle")
    return svg(800,268,b,"Multi-agent orchestrator and connected agents")
D["multi-agent"]=d_multiagent

# 8) Content safety layers
def d_safety():
    b=defs_arrow()
    b+=txt(400,30,"Content safety: input & output filtering",NAVY,19,"700","middle")
    b+=box(30,70,150,50,BLUEL,"User input","",r=10,fs=14)
    b+=box(210,64,180,62,WARN,"Input filter","prompt shields",r=10,fs=14,sfs=10.5)
    b+=box(420,70,150,50,BLUE,"Model","",r=10,fs=14)
    b+=box(600,64,170,62,WARN,"Output filter","categories+severity",r=10,fs=13.5,sfs=10)
    b+=arrow(180,95,210,95,MUTE); b+=arrow(390,95,420,95,MUTE); b+=arrow(570,95,600,95,MUTE)
    cats=["Hate","Sexual","Violence","Self-harm","Jailbreak","Protected material"]
    x=40
    for c in cats:
        b+=chip(x,160,118,30,c,PALE,NAVY,11.5)
        x+=124
    b+=txt(400,224,"Filters screen both prompts and completions across categories at configurable severity thresholds",MUTE,11.5,"400","middle")
    return svg(800,242,b,"Content safety input and output filters")
D["content-safety"]=d_safety

# 9) Evaluation flow
def d_eval():
    b=defs_arrow()
    b+=txt(400,30,"Evaluating generative apps",NAVY,19,"700","middle")
    b+=box(40,66,180,54,BLUE,"Test dataset","queries + context",r=10,fs=14,sfs=10.5)
    b+=box(300,66,180,54,NAVY,"App / model","generates output",r=10,fs=14,sfs=10.5)
    b+=box(560,66,200,54,PURP,"Evaluators","score each response",r=10,fs=14,sfs=10.5)
    b+=arrow(220,93,300,93,MUTE); b+=arrow(480,93,560,93,MUTE)
    metrics=[("Groundedness",OK),("Relevance",BLUE),("Coherence",BLUEL),("Fluency",NAVY),("Safety",WARN)]
    x=40
    for m,col in metrics:
        b+=box(x,160,140,34,col,m,"",r=7,fs=12.5)
        x+=148
    b+=txt(400,226,"Score outputs for groundedness/relevance/safety to catch fabrications before and after deployment",MUTE,11.5,"400","middle")
    return svg(800,244,b,"Evaluation metrics for generative apps")
D["evaluation-flow"]=d_eval

# 10) Observability
def d_observ():
    b=defs_arrow()
    b+=txt(400,30,"Observability for AI apps",NAVY,19,"700","middle")
    b+=box(300,60,200,50,NAVY,"Instrumented app","OpenTelemetry traces",r=10,fs=14,sfs=10)
    sinks=[("Traces / spans",BLUE,40),("Token analytics",OK,230),("Safety signals",WARN,420),("Latency breakdown",PURP,610)]
    for name,col,x in sinks:
        b+=box(x,150,170,46,col,name,"",r=9,fs=12.8)
        b+=arrow(400,110,x+85,150,MUTE)
    b+=box(250,220,300,42,PALE,"Azure Monitor / Foundry dashboards",tc=NAVY,r=9,fs=13,stroke=LINE)
    for x in [125,315,505,695]:
        b+=arrow(x,196,400,220,MUTE,dash=True)
    b+=txt(400,286,"Emit traces and token/latency/safety telemetry, then analyze in Monitor and Foundry",MUTE,11.5,"400","middle")
    return svg(800,304,b,"Observability tracing token latency safety")
D["observability"]=d_observ

# 11) Identity & security
def d_security():
    b=defs_arrow()
    b+=txt(400,30,"Securing an AI solution",NAVY,19,"700","middle")
    b+=box(300,60,200,50,BLUE,"App / agent","",r=10,fs=15)
    layers=[("Managed identity","no keys in code",OK,40,150),
            ("Microsoft Entra ID","keyless RBAC tokens",NAVY,300,150),
            ("Private endpoints","traffic off public net",PURP,560,150),
            ("RBAC role policies","least-privilege access",BLUEL,300,232)]
    for t,s,col,x,y in layers:
        b+=box(x,y,200,52,col,t,s,r=10,fs=13.5,sfs=10)
        b+=arrow(400,110,x+100,y,MUTE)
    b+=txt(400,304,"Prefer managed identity + Entra tokens (keyless), lock networking with private endpoints, scope RBAC tightly",MUTE,11,"400","middle")
    return svg(800,322,b,"Managed identity Entra private endpoints RBAC")
D["identity-security"]=d_security

# 12) Responsible AI governance
def d_rai():
    b=""
    b+=txt(400,30,"Responsible AI: layered controls",NAVY,19,"700","middle")
    layers=[("Content safety filters","block harmful input/output",WARN),
            ("Evaluators & safety tests","measure groundedness & risk",BLUE),
            ("Auditing & provenance","trace logs, approval workflows",NAVY),
            ("Agent oversight","constraints & tool-access limits",PURP)]
    y=58
    for t,s,col in layers:
        b+=box(120,y,560,44,col,"","",r=9)
        b+=txt(140,y+20,t,WHITE,13.5,"700")
        b+=txt(140,y+37,s,PALE,11,"400")
        y+=52
    b+=txt(400,y+14,"Combine prevention, measurement, auditing, and human oversight across the lifecycle",MUTE,11.5,"400","middle")
    return svg(800,y+30,b,"Responsible AI layered controls")
D["rai-governance"]=d_rai

# 13) Image generation & editing
def d_imagegen():
    b=defs_arrow()
    b+=txt(400,30,"Image generation & editing",NAVY,19,"700","middle")
    b+=box(40,70,170,50,BLUEL,"Text prompt","(+ reference img)",r=10,fs=13.5,sfs=10)
    b+=box(250,70,180,50,BLUE,"Image model","size / quality / n",r=10,fs=14,sfs=10)
    b+=box(470,70,150,50,OK,"Generated image","",r=10,fs=13.5)
    b+=arrow(210,95,250,95,MUTE); b+=arrow(430,95,470,95,MUTE)
    b+=box(470,150,150,50,PURP,"Edited image","",r=10,fs=13.5)
    b+=box(250,150,180,50,NAVY,"Inpaint / mask","prompt-driven edit",r=10,fs=13.5,sfs=10)
    b+=arrow(545,120,545,150,OK)
    b+=arrow(430,175,470,175,MUTE)
    b+=txt(400,232,"Generate from prompts and reference media, then refine with mask-based inpainting and prompt edits",MUTE,11.5,"400","middle")
    return svg(800,250,b,"Image generation and inpainting editing")
D["image-generation"]=d_imagegen

# 14) Multimodal understanding
def d_multimodal():
    b=defs_arrow()
    b+=txt(400,30,"Multimodal understanding",NAVY,19,"700","middle")
    b+=box(40,80,150,44,BLUEL,"Image / video","",r=10,fs=13.5)
    b+=box(40,134,150,44,BLUE,"Question","",r=10,fs=13.5)
    b+=box(300,100,200,60,NAVY,"Multimodal model","reasons over pixels",r=12,fs=14,sfs=10.5)
    b+=arrow(190,102,300,120,MUTE); b+=arrow(190,156,300,140,MUTE)
    outs=[("Caption",OK),("Grounded answer",BLUE),("Alt-text",PURP)]
    y=72
    for o,col in outs:
        b+=box(600,y,170,42,col,o,"",r=9,fs=13)
        b+=arrow(500,130,600,y+21,MUTE)
        y+=58
    b+=txt(400,258,"One model captions images, answers questions grounded in the visual, and writes accessibility alt-text",MUTE,11.5,"400","middle")
    return svg(800,276,b,"Multimodal captioning QA alt-text")
D["multimodal-understanding"]=d_multimodal

# 15) Content Understanding analyzers
def d_contentund():
    b=defs_arrow()
    b+=txt(400,30,"Azure AI Content Understanding",NAVY,19,"700","middle")
    ins=["Documents","Images","Audio","Video"]
    y=64
    for i,s in enumerate(ins):
        b+=box(40,y,140,40,BLUEL,s,"",r=8,fs=13)
        b+=arrow(180,y+20,300,132,MUTE)
        y+=48
    b+=box(300,108,200,60,NAVY,"Analyzer","field schema + prompts",r=12,fs=15,sfs=10.5)
    b+=box(600,80,170,44,OK,"Structured JSON","",r=9,fs=13)
    b+=box(600,148,170,44,BLUE,"Markdown output","",r=9,fs=13)
    b+=arrow(500,128,600,102,MUTE); b+=arrow(500,148,600,170,MUTE)
    b+=txt(400,272,"Define an analyzer to turn any modality into clean structured or markdown output for RAG and agents",MUTE,11.5,"400","middle")
    return svg(800,290,b,"Content Understanding analyzers structured output")
D["content-understanding"]=d_contentund

# 16) Speech pipeline
def d_speech():
    b=defs_arrow()
    b+=txt(400,30,"Speech for agentic interactions",NAVY,19,"700","middle")
    b+=box(40,80,150,48,BLUEL,"Microphone","spoken input",r=10,fs=13.5,sfs=10)
    b+=box(240,80,160,48,BLUE,"Speech to text","(custom models)",r=10,fs=13.5,sfs=10)
    b+=box(450,80,150,48,NAVY,"Agent / LLM","reasons on text",r=10,fs=13,sfs=10)
    b+=box(240,158,160,48,OK,"Text to speech","spoken reply",r=10,fs=13.5,sfs=10)
    b+=box(450,158,150,48,PURP,"Speech translation","cross-language",r=10,fs=12.5,sfs=10)
    b+=arrow(190,104,240,104,MUTE); b+=arrow(400,104,450,104,MUTE)
    b+=arrow(525,128,320,158,MUTE,dash=True)
    b+=arrow(240,182,190,120,OK,dash=True)
    b+=txt(400,238,"STT feeds the agent; TTS voices replies; speech translation bridges languages",MUTE,11.5,"400","middle")
    return svg(800,256,b,"Speech to text and text to speech for agents")
D["speech-pipeline"]=d_speech

# 17) Search / retrieval indexing
def d_search():
    b=defs_arrow()
    b+=txt(400,30,"Azure AI Search: indexing pipeline",NAVY,19,"700","middle")
    b+=box(30,80,150,50,BLUEL,"Data source","blobs, docs",r=10,fs=13.5,sfs=10)
    b+=box(210,80,150,50,BLUE,"Indexer","pulls + tracks",r=10,fs=13.5,sfs=10)
    b+=box(390,80,160,50,PURP,"Skillset","OCR, split, embed",r=10,fs=13,sfs=10)
    b+=box(580,80,180,50,NAVY,"Index","vectors + text fields",r=10,fs=13.5,sfs=10)
    b+=arrow(180,105,210,105,MUTE); b+=arrow(360,105,390,105,MUTE); b+=arrow(550,105,580,105,MUTE)
    b+=box(300,168,200,46,OK,"Query: hybrid + semantic",r=10,fs=13.5)
    b+=arrow(670,130,500,168,MUTE,dash=True)
    b+=txt(400,240,"An indexer runs a skillset to enrich and vectorize content into an index that serves hybrid search",MUTE,11.5,"400","middle")
    return svg(800,258,b,"Search indexer skillset index pipeline")
D["search-indexing"]=d_search

# 18) Hybrid search + rerank
def d_hybrid():
    b=defs_arrow()
    b+=txt(400,30,"Hybrid search + semantic ranking",NAVY,19,"700","middle")
    b+=box(320,60,160,46,NAVY,"Query","",r=10,fs=15)
    b+=box(120,140,200,50,BLUE,"Keyword (BM25)","exact terms",r=10,fs=13.5,sfs=10)
    b+=box(480,140,200,50,PURP,"Vector (kNN)","semantic similarity",r=10,fs=13.5,sfs=10)
    b+=arrow(360,106,240,140,MUTE); b+=arrow(440,106,560,140,MUTE)
    b+=box(300,214,200,46,BLUEL,"Fuse (RRF)",r=10,fs=14)
    b+=arrow(220,190,360,214,MUTE); b+=arrow(580,190,440,214,MUTE)
    b+=box(300,282,200,44,OK,"Semantic reranker",r=10,fs=13.5)
    b+=arrow(400,260,400,282,BLUE)
    b+=txt(400,350,"Combine keyword and vector results, fuse with RRF, then re-rank the top hits for the best grounding",MUTE,11.5,"400","middle")
    return svg(800,368,b,"Hybrid search fusion and semantic rerank")
D["hybrid-search"]=d_hybrid

# 19) Document extraction
def d_docextract():
    b=defs_arrow()
    b+=txt(400,30,"Document information extraction",NAVY,19,"700","middle")
    b+=box(40,90,150,54,BLUEL,"Document","PDF / image",r=10,fs=14,sfs=10)
    stages=[("OCR","read text",BLUE,240),("Layout","tables & structure",NAVY,410),("Fields","key-value pairs",PURP,580)]
    for t,s,col,x in stages:
        b+=box(x,90,150,54,col,t,s,r=10,fs=14,sfs=10)
    b+=arrow(190,117,240,117,MUTE); b+=arrow(390,117,410,117,MUTE); b+=arrow(560,117,580,117,MUTE)
    b+=box(280,184,240,46,OK,"Grounded structured output",r=10,fs=13.5)
    b+=arrow(655,144,500,184,MUTE,dash=True)
    b+=txt(400,256,"Combine OCR, layout analysis, and field extraction into clean data for downstream RAG and agents",MUTE,11.5,"400","middle")
    return svg(800,274,b,"OCR layout field extraction pipeline")
D["doc-extraction"]=d_docextract

# 20) Generation parameters
def d_params():
    b=""
    b+=txt(400,30,"Tuning generation behavior",NAVY,19,"700","middle")
    rows=[("temperature","0 = deterministic \u2192 higher = more creative/random",BLUE),
          ("top_p","nucleus sampling; lower = safer word choices",BLUEL),
          ("max tokens","caps the length of the completion",NAVY),
          ("system prompt","sets role, tone, and guardrails",OK),
          ("stop / seed","control termination and reproducibility",PURP)]
    y=58
    for name,desc,col in rows:
        b+=box(40,y,180,40,col,name,"",r=8,fs=13.5)
        b+=box(230,y,530,40,PALE,"",r=8,stroke=LINE)
        b+=txt(248,y+25,desc,INK,12.2,"500")
        y+=48
    b+=txt(400,y+12,"Prompt engineering plus parameter tuning shape determinism, length, and style",MUTE,11.5,"400","middle")
    return svg(800,y+30,b,"Generation parameters temperature top_p")
D["generation-params"]=d_params

# write all + catalog
def main():
    cat=["# Diagram catalog (id \u2014 concept). Reference in HTML via <figure class=\"diagram\" data-svg=\"ID\">.",""]
    for did,fn in D.items():
        s=fn()
        open(os.path.join(OUT,did+".svg"),"w",encoding="utf-8").write(s)
        cat.append(f"- {did}")
    open(os.path.join(HERE,"content","diagram_catalog.md"),"w",encoding="utf-8").write("\n".join(cat))
    print(f"wrote {len(D)} SVG diagrams to {OUT}")
    for did in D: print("  -", did)

if __name__=="__main__":
    main()
