"""Generate the ORIGINAL inline-SVG diagram library for the public GH-300 guide.

Clean-room: these are original schematic diagrams in our own visual style, expressing
well-documented, factual GitHub Copilot concepts (responsible-AI principles, plan tiers,
interaction surfaces, data flow, code-suggestion lifecycle, prompt structure, etc.).
No Microsoft/GitHub images or slides are used or reproduced.
Each diagram is saved to assets/diagrams/<id>.svg with a responsive viewBox.
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "diagrams")
os.makedirs(OUT, exist_ok=True)

# palette
NAVY="#0b3d63"; BLUE="#0f6cbd"; BLUEL="#3a9bdc"; PALE="#eaf3fb"; INK="#1b2733"
MUTE="#5b6b7a"; OK="#107c41"; WARN="#b45309"; LINE="#c9d6e2"; WHITE="#ffffff"; PALE2="#dcebf8"
FONT="font-family='Segoe UI,Arial,sans-serif'"

def esc(s): return html.escape(str(s), quote=True)

def svg(w, h, body, title=""):
    t = f"<title>{esc(title)}</title>" if title else ""
    return (f"<svg viewBox='0 0 {w} {h}' xmlns='http://www.w3.org/2000/svg' "
            f"role='img' aria-label='{esc(title)}' {FONT}>{t}"
            f"<rect x='0' y='0' width='{w}' height='{h}' fill='{WHITE}'/>{body}</svg>")

def box(x,y,w,h,fill=BLUE,txt="",sub="",tc=WHITE,r=10,fs=17,sfs=12.5,stroke="none",tcsub=None):
    o=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='1.5'/>"
    if txt and sub:
        o+=f"<text x='{x+w/2}' y='{y+h/2-4}' text-anchor='middle' fill='{tc}' font-size='{fs}' font-weight='600'>{esc(txt)}</text>"
        o+=f"<text x='{x+w/2}' y='{y+h/2+15}' text-anchor='middle' fill='{tcsub or tc}' font-size='{sfs}'>{esc(sub)}</text>"
    elif txt:
        o+=f"<text x='{x+w/2}' y='{y+h/2+6}' text-anchor='middle' fill='{tc}' font-size='{fs}' font-weight='600'>{esc(txt)}</text>"
    return o

def txt(x,y,s,fill=INK,fs=13,w="400",anchor="start",italic=False):
    st=" font-style='italic'" if italic else ""
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}' font-size='{fs}' font-weight='{w}'{st}>{esc(s)}</text>"

def defs_arrow():
    return (f"<defs><marker id='ah' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>"
            f"<path d='M0,0 L8,3 L0,6 Z' fill='{MUTE}'/></marker>"
            f"<marker id='ahb' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto' markerUnits='strokeWidth'>"
            f"<path d='M0,0 L8,3 L0,6 Z' fill='{BLUE}'/></marker></defs>")

def arrow(x1,y1,x2,y2,color=MUTE,dash=False,w=2):
    d=" stroke-dasharray='6 5'" if dash else ""
    mk="ahb" if color==BLUE else "ah"
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='{w}'{d} marker-end='url(#{mk})'/>"

def chip(x,y,w,h,s,fill=PALE,tc=NAVY,fs=12.5,r=6,stroke=LINE):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{fill}' stroke='{stroke}' stroke-width='1'/>"
            + txt(x+w/2,y+h/2+4,s,fill=tc,fs=fs,w="600",anchor="middle"))

D={}

# 1) Responsible AI principles
def d_rai():
    b=""
    b+=txt(400,30,"Microsoft's responsible AI principles",NAVY,19,"700","middle")
    items=[("Fairness","treat all people equitably",BLUEL),
           ("Reliability & safety","perform safely & consistently",BLUE),
           ("Privacy & security","protect data, respect consent",NAVY),
           ("Inclusiveness","empower & engage everyone",BLUEL),
           ("Transparency","understandable & explainable",BLUE),
           ("Accountability","people stay responsible",NAVY)]
    x0=40; y0=58; cw=240; ch=70; gx=20; gy=18
    for i,(t,s,col) in enumerate(items):
        r=i//3; c=i%3
        x=x0+c*(cw+gx); y=y0+r*(ch+gy)
        b+=box(x,y,cw,ch,col,"",r=10)
        b+=txt(x+cw/2,y+30,t,WHITE,14.5,"700","middle")
        b+=txt(x+cw/2,y+50,s,PALE,11,"400","middle")
    return svg(800,244,b,"Six Microsoft responsible AI principles")
D["responsible-ai-principles"]=d_rai

# 2) Generative AI limitations
def d_limits():
    b=""
    b+=txt(400,30,"Limitations of generative AI to plan for",NAVY,19,"700","middle")
    items=[("Hallucination","plausible but wrong output"),
           ("Bias","reflects biased training data"),
           ("Stale knowledge","cutoff / no live context"),
           ("No true reasoning","predicts likely tokens"),
           ("Security risks","may suggest vulnerable code"),
           ("IP / matching","may echo public code")]
    x0=40; y0=58; cw=240; ch=56; gx=20; gy=16
    for i,(t,s) in enumerate(items):
        r=i//3; c=i%3
        x=x0+c*(cw+gx); y=y0+r*(ch+gy)
        b+=f"<rect x='{x}' y='{y}' width='{cw}' height='{ch}' rx='9' fill='{PALE}' stroke='{WARN}' stroke-width='1.3'/>"
        b+=txt(x+cw/2,y+24,t,WARN,13.5,"700","middle")
        b+=txt(x+cw/2,y+43,s,INK,10.8,"400","middle")
    b+=txt(400,214,"Human review is required \u2014 Copilot assists, it does not decide",MUTE,12.5,"400","middle")
    return svg(800,232,b,"Common limitations of generative AI tools")
D["genai-limitations"]=d_limits

# 3) Validate output loop (human in the loop)
def d_validate():
    b=defs_arrow()
    b+=txt(400,30,"Validate every suggestion (human in the loop)",NAVY,18,"700","middle")
    steps=[("Copilot\nsuggests",BLUEL),("Read &\nunderstand",BLUE),("Test &\nverify",NAVY),("Accept /\nedit / reject",OK)]
    x=60
    for i,(t,col) in enumerate(steps):
        l1,l2=t.split("\n")
        b+=box(x,70,150,66,col,"",r=10)
        b+=txt(x+75,98,l1,WHITE,13.5,"700","middle")
        b+=txt(x+75,118,l2,WHITE,13.5,"700","middle")
        if i<3: b+=arrow(x+150,103,x+178,103,MUTE)
        x+=178
    b+=txt(400,168,"You remain accountable for correctness, security, and licensing of accepted code",MUTE,12,"400","middle")
    return svg(800,188,b,"Human-in-the-loop validation of AI output")
D["validate-output-loop"]=d_validate

# 4) Copilot plans
def d_plans():
    b=""
    b+=txt(400,28,"GitHub Copilot plans",NAVY,19,"700","middle")
    plans=[("Free","limited monthly\ncompletions & chat",MUTE),
           ("Pro / Pro+","full individual\nfeatures",BLUEL),
           ("Business","org policy &\nmanagement",BLUE),
           ("Enterprise","knowledge bases,\nadvanced controls",NAVY)]
    x=40; cw=180; gx=8
    for name,s,col in plans:
        l1,l2=s.split("\n")
        b+=box(x,60,cw,92,col,"",r=11)
        b+=txt(x+cw/2,92,name,WHITE,15,"700","middle")
        b+=txt(x+cw/2,116,l1,PALE,11,"400","middle")
        b+=txt(x+cw/2,133,l2,PALE,11,"400","middle")
        x+=cw+gx
    b+=txt(400,176,"Higher tiers add org-wide policy, audit logs, content exclusions, and admin controls",MUTE,12,"400","middle")
    return svg(800,196,b,"GitHub Copilot plan tiers")
D["copilot-plans"]=d_plans

# 5) Copilot surfaces
def d_surfaces():
    b=defs_arrow()
    b+=txt(400,30,"Where GitHub Copilot works",NAVY,19,"700","middle")
    surfaces=["IDE\n(VS Code, JetBrains)","Copilot Chat","Copilot CLI",
              "github.com","Mobile","Windows Terminal"]
    xs=[30,160,290,420,550,650]; ws=[120,120,120,120,90,120]
    x0=[30,160,290,420,550]
    cells=[("IDE","VS Code, Visual Studio, JetBrains"),("Chat","ask, explain, fix"),
            ("CLI","terminal commands"),("github.com","PRs, docs, web"),("Mobile","GitHub Mobile")]
    x=30
    for name,s in cells:
        b+=box(x,66,146,64,BLUE,"",r=9)
        b+=txt(x+73,92,name,WHITE,13,"700","middle")
        b+=txt(x+73,112,s,PALE,9.6,"400","middle")
        b+=arrow(x+73,130,x+73,152,MUTE)
        x+=150
    b+=box(120,154,510,44,NAVY,"One Copilot subscription \u2014 consistent AI across surfaces",r=10,fs=13.5)
    return svg(800,214,b,"GitHub Copilot interaction surfaces")
D["copilot-surfaces"]=d_surfaces

# 6) Interaction modes in the IDE
def d_modes():
    b=""
    b+=txt(400,28,"Ways to interact with Copilot in the editor",NAVY,18,"700","middle")
    modes=[("Inline / ghost text","autocomplete as you type","Tab to accept",BLUEL),
           ("Chat","ask questions, /commands","conversational",BLUE),
           ("Copilot Edits","multi-file changes","review a change set",NAVY),
           ("Agent Mode","autonomous multi-step","plans, edits, runs, iterates","#062338")]
    x=30; cw=182; gx=6
    for m in modes:
        name,s1,s2=m[0],m[1],m[2]; col=m[3]
        b+=box(x,58,cw,96,col,"",r=10)
        b+=txt(x+cw/2,86,name,WHITE,13.2,"700","middle")
        b+=txt(x+cw/2,110,s1,PALE,10.2,"400","middle")
        b+=txt(x+cw/2,128,s2,PALE,10.2,"400","middle")
        x+=cw+gx
    b+=txt(400,178,"Pick the lightest mode that fits the task; escalate to Agent Mode for larger work",MUTE,12,"400","middle")
    return svg(800,196,b,"Copilot interaction modes in the IDE")
D["interaction-modes"]=d_modes

# 7) Copilot CLI flow
def d_cli():
    b=defs_arrow()
    b+=txt(400,30,"GitHub Copilot in the terminal (CLI)",NAVY,18,"700","middle")
    b+=box(40,80,150,60,BLUEL,"You ask",r=10,fs=13.5)
    b+=txt(115,150,"natural language",MUTE,10.5,"400","middle")
    b+=box(250,80,180,60,BLUE,"Copilot CLI",r=10,fs=14)
    b+=txt(340,150,"suggests / explains",MUTE,10.5,"400","middle")
    b+=box(490,80,130,60,NAVY,"You review",r=10,fs=13.5)
    b+=box(660,80,110,60,OK,"Run",r=10,fs=14)
    b+=arrow(190,110,250,110,BLUE); b+=arrow(430,110,490,110,MUTE); b+=arrow(620,110,660,110,MUTE)
    b+=f"<rect x='120' y='170' width='560' height='34' rx='7' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(400,192,"Nothing runs until you confirm \u2014 the command is only executed after you approve it",WARN,11.5,"600","middle")
    return svg(800,220,b,"GitHub Copilot CLI request and approval flow")
D["copilot-cli-flow"]=d_cli

# 8) Agent mode loop
def d_agent():
    b=defs_arrow()
    b+=txt(400,30,"Agent Mode: an autonomous edit loop",NAVY,18,"700","middle")
    cx,cy=400,140; r=78
    nodes=[("Plan",cx-190,cy),("Edit files",cx-60,cy-70),("Run / test",cx+90,cy-70),
            ("Evaluate",cx+200,cy),("Iterate",cx+60,cy+72)]
    coords=[(cx-210,cy),(cx-70,cy-72),(cx+70,cy-72),(cx+210,cy),(cx,cy+78)]
    labels=["Plan","Edit files","Run tools","Evaluate","Iterate"]
    cols=[BLUEL,BLUE,NAVY,BLUE,OK]
    pts=[]
    for i,(lab,col) in enumerate(zip(labels,cols)):
        ang=-90+i*72
        import math
        x=cx+150*math.cos(math.radians(ang)); y=cy+58*math.sin(math.radians(ang))+8
        pts.append((x,y))
        b+=box(x-62,y-22,124,44,col,lab,r=9,fs=13)
    for i in range(len(pts)):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%len(pts)]
        b+=arrow(x1+ (x2-x1)*0.18, y1+(y2-y1)*0.18, x1+(x2-x1)*0.82, y1+(y2-y1)*0.82, BLUE)
    b+=txt(400,214,"Repeats until the goal is met or it needs your input; you approve the result",MUTE,12,"400","middle")
    return svg(800,232,b,"Agent Mode autonomous iterate loop")
D["agent-mode-loop"]=d_agent

# 9) MCP architecture
def d_mcp():
    b=defs_arrow()
    b+=txt(400,30,"Model Context Protocol (MCP)",NAVY,18,"700","middle")
    b+=box(40,80,200,80,BLUE,"",r=11)
    b+=txt(140,110,"Copilot (MCP host)",WHITE,13.5,"700","middle")
    b+=txt(140,132,"agent / chat client",PALE,10.5,"400","middle")
    b+=box(320,60,150,50,NAVY,"MCP server A",r=9,fs=12.5)
    b+=txt(395,96,"e.g. GitHub tools",MUTE,10,"400","middle")
    b+=box(320,130,150,50,NAVY,"MCP server B",r=9,fs=12.5)
    b+=txt(395,166,"e.g. database / API",MUTE,10,"400","middle")
    b+=box(560,95,200,50,OK,"Tools / data / actions",r=9,fs=12.5)
    b+=arrow(240,110,320,85,BLUE); b+=arrow(240,130,320,155,BLUE)
    b+=arrow(470,85,560,115,MUTE); b+=arrow(470,155,560,125,MUTE)
    b+=txt(400,208,"MCP is an open standard that lets Copilot call external tools and context sources",MUTE,12,"400","middle")
    return svg(800,226,b,"Model Context Protocol connects Copilot to external tools")
D["mcp-architecture"]=d_mcp

# 10) Data flow
def d_dataflow():
    b=defs_arrow()
    b+=txt(400,30,"How a Copilot request flows",NAVY,18,"700","middle")
    stages=[("Editor / client","context assembled",BLUEL),
            ("Copilot proxy","filters & safeguards",BLUE),
            ("LLM","generates candidates",NAVY),
            ("Post-processing","filter, then return",OK)]
    x=30
    for i,(t,s,col) in enumerate(stages):
        b+=box(x,72,175,66,col,"",r=10)
        b+=txt(x+87,100,t,WHITE,13,"700","middle")
        b+=txt(x+87,120,s,PALE,10.2,"400","middle")
        if i<3: b+=arrow(x+175,105,x+188,105,BLUE)
        x+=188
    b+=txt(400,168,"Prompts are transient; the proxy applies filtering before and after the model",MUTE,12,"400","middle")
    b+=txt(400,188,"Business/Enterprise: prompts & suggestions are not retained to train the models",MUTE,11.5,"400","middle")
    return svg(800,206,b,"GitHub Copilot request data flow")
D["data-flow"]=d_dataflow

# 11) Code suggestion lifecycle
def d_lifecycle():
    b=defs_arrow()
    b+=txt(400,30,"Code suggestion lifecycle",NAVY,18,"700","middle")
    stages=[("Capture context","open files, cursor, comments"),
            ("Build prompt","assemble & trim to fit"),
            ("Model inference","generate candidates"),
            ("Filter","safety & public-code match"),
            ("Show suggestion","you accept or reject")]
    y=64
    for i,(t,s) in enumerate(stages):
        b+=box(60,y,300,44,BLUE if i%2 else NAVY,"",r=8)
        b+=txt(210,y+20,t,WHITE,13,"700","middle")
        b+=txt(210,y+37,s,PALE,10,"400","middle")
        if i<4: b+=arrow(210,y+44,210,y+56,BLUE)
        y+=56
    b+=chip(400,120,340,44,"Accepted code becomes yours to review, test, and own",PALE,NAVY,12)
    return svg(800,y+8,b,"The lifecycle of a Copilot code suggestion")
D["suggestion-lifecycle"]=d_lifecycle

# 12) Prompt structure
def d_prompt():
    b=""
    b+=txt(400,28,"Anatomy of an effective prompt",NAVY,19,"700","middle")
    parts=[("Goal / intent","what you want done",BLUEL),
           ("Context","files, language, constraints",BLUE),
           ("Specifics","inputs, edge cases, style",NAVY),
           ("Examples","sample in / out (few-shot)",OK)]
    y=58
    for t,s,col in parts:
        b+=box(60,y,220,42,col,t,r=8,fs=13.5)
        b+=txt(300,y+26,s,INK,12,"400")
        y+=54
    b+=txt(400,y+4,"Be clear and specific; give relevant context and break big asks into steps",MUTE,12,"400","middle")
    return svg(800,y+24,b,"Structure of a good Copilot prompt")
D["prompt-structure"]=d_prompt

# 13) Zero-shot vs few-shot
def d_shot():
    b=defs_arrow()
    b+=txt(400,30,"Zero-shot vs few-shot prompting",NAVY,18,"700","middle")
    b+=box(50,66,330,130,BLUEL,"",r=12)
    b+=txt(215,92,"Zero-shot",WHITE,15,"700","middle")
    b+=chip(70,108,290,30,"instruction only, no examples",WHITE,NAVY,11)
    b+=chip(70,146,290,30,"fast; good for simple tasks",WHITE,NAVY,11)
    b+=box(420,66,330,130,BLUE,"",r=12)
    b+=txt(585,92,"Few-shot",WHITE,15,"700","middle")
    b+=chip(440,108,290,30,"include 1\u2013few input/output examples",WHITE,NAVY,11)
    b+=chip(440,146,290,30,"steers format & style; better for complex",WHITE,NAVY,11)
    b+=txt(400,216,"Add examples when you need a specific pattern or output shape",MUTE,12.5,"400","middle")
    return svg(800,234,b,"Zero-shot versus few-shot prompting")
D["zero-few-shot"]=d_shot

# 14) Prompt process flow with chat history
def d_promptflow():
    b=defs_arrow()
    b+=txt(400,30,"Prompt process flow in Copilot Chat",NAVY,18,"700","middle")
    b+=box(40,80,140,58,BLUEL,"Your prompt",r=10,fs=13)
    b+=box(210,80,170,58,BLUE,"+ context",r=10,fs=13.5)
    b+=txt(295,150,"open files, selection",MUTE,10,"400","middle")
    b+=box(410,80,150,58,NAVY,"+ chat history",r=10,fs=13)
    b+=box(590,80,170,58,OK,"Model response",r=10,fs=13)
    b+=arrow(180,109,210,109,BLUE); b+=arrow(380,109,410,109,BLUE); b+=arrow(560,109,590,109,BLUE)
    b+=f"<rect x='120' y='166' width='560' height='34' rx='7' fill='{PALE}' stroke='{LINE}'/>"
    b+=txt(400,188,"Follow-up turns reuse prior messages \u2014 start a new chat to drop stale context",NAVY,11.5,"600","middle")
    return svg(800,216,b,"How chat history feeds the prompt")
D["prompt-process-flow"]=d_promptflow

# 15) Productivity across the SDLC
def d_sdlc():
    b=defs_arrow()
    b+=txt(400,30,"Copilot across the development lifecycle",NAVY,18,"700","middle")
    stages=[("Learn","explain code & APIs"),("Write","generate & refactor"),
            ("Test","unit & edge-case tests"),("Document","comments & docs"),
            ("Review","PR summaries & review")]
    x=24
    for i,(t,s) in enumerate(stages):
        col=[BLUEL,BLUE,NAVY,BLUE,BLUEL][i]
        b+=box(x,70,140,60,col,"",r=10)
        b+=txt(x+70,96,t,WHITE,14,"700","middle")
        b+=txt(x+70,116,s,PALE,9.6,"400","middle")
        if i<4: b+=arrow(x+140,100,x+154,100,MUTE)
        x+=154
    b+=txt(400,158,"Fewer context switches; more time on design and problem solving",MUTE,12,"400","middle")
    return svg(800,178,b,"GitHub Copilot across the SDLC")
D["productivity-sdlc"]=d_sdlc

# 16) Test generation flow
def d_tests():
    b=defs_arrow()
    b+=txt(400,30,"Generating tests with Copilot",NAVY,18,"700","middle")
    steps=[("Select code","function under test",BLUEL),
           ("Ask for tests","/tests or chat",BLUE),
           ("Review cases","happy path + edges",NAVY),
           ("Run & refine","fix gaps, add asserts",OK)]
    x=40
    for i,(t,s,col) in enumerate(steps):
        b+=box(x,72,170,64,col,"",r=10)
        b+=txt(x+85,99,t,WHITE,13,"700","middle")
        b+=txt(x+85,119,s,PALE,10,"400","middle")
        if i<3: b+=arrow(x+170,104,x+182,104,MUTE)
        x+=182
    b+=txt(400,166,"Always run generated tests; verify they assert real behavior, not just pass",MUTE,12,"400","middle")
    return svg(800,186,b,"Test generation workflow with Copilot")
D["test-generation-flow"]=d_tests

# 17) Content exclusion scope
def d_exclusions():
    b=defs_arrow()
    b+=txt(400,30,"Content exclusions scope",NAVY,18,"700","middle")
    b+=box(250,60,300,46,NAVY,"Organization / Enterprise",r=10,fs=13.5)
    b+=box(180,130,200,46,BLUE,"Repository",r=10,fs=13.5)
    b+=box(430,130,200,46,BLUE,"Repository",r=10,fs=13.5)
    b+=box(180,196,200,40,BLUEL,"Paths / files",r=9,fs=12.5)
    b+=box(430,196,200,40,BLUEL,"Paths / files",r=9,fs=12.5)
    b+=arrow(360,106,300,130,MUTE); b+=arrow(440,106,500,130,MUTE)
    b+=arrow(280,176,280,196,MUTE); b+=arrow(530,176,530,196,MUTE)
    b+=f"<rect x='120' y='250' width='560' height='34' rx='7' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(400,272,"Excluded content is not used as context and no suggestions are shown for it",WARN,11.5,"600","middle")
    return svg(800,300,b,"Content exclusion configuration scope")
D["content-exclusion-scope"]=d_exclusions

# 18) Public code matching filter
def d_pubfilter():
    b=defs_arrow()
    b+=txt(400,30,"Suggestions matching public code",NAVY,18,"700","middle")
    b+=box(40,84,170,58,BLUEL,"Candidate\nsuggestion",r=10,fs=13)
    b+=box(280,84,200,58,BLUE,"Duplication filter",r=10,fs=13.5)
    b+=txt(380,158,"matches ~150 chars of public code?",MUTE,10.5,"400","middle")
    b+=box(560,50,200,44,WARN,"Blocked",r=9,fs=13)
    b+=box(560,120,200,44,OK,"Shown",r=9,fs=13)
    b+=arrow(210,113,280,113,BLUE)
    b+=arrow(480,100,560,72,MUTE); b+=txt(520,88,"match",WARN,10,"700","middle")
    b+=arrow(480,126,560,142,MUTE); b+=txt(520,150,"no match",OK,10,"700","middle")
    b+=txt(400,196,"Admins can enable the filter to block suggestions that match public code",MUTE,12,"400","middle")
    return svg(800,214,b,"Public code matching filter")
D["public-code-filter"]=d_pubfilter

# 19) Org policy & management layers
def d_policy():
    b=defs_arrow()
    b+=txt(400,30,"Organization management & policy",NAVY,18,"700","middle")
    layers=[("Enterprise policies","set defaults for all orgs",NAVY),
            ("Organization settings","features, exclusions, seats",BLUE),
            ("Audit log","who did what, when",BLUEL),
            ("REST API","manage seats & subscriptions",OK)]
    y=64
    for t,s,col in layers:
        b+=box(120,y,560,44,col,"",r=9)
        b+=txt(250,y+27,t,WHITE,13.5,"700","middle")
        b+=txt(560,y+27,s,PALE,11,"400","middle")
        y+=54
    b+=txt(400,y+6,"Admins govern access, enforce policies, and monitor usage centrally",MUTE,12,"400","middle")
    return svg(800,y+26,b,"Organization-wide Copilot management layers")
D["org-policy-layers"]=d_policy

# 20) Code review with Copilot
def d_review():
    b=defs_arrow()
    b+=txt(400,30,"Copilot code review",NAVY,18,"700","middle")
    b+=box(40,80,160,60,BLUEL,"Pull request",r=10,fs=13.5)
    b+=box(240,80,180,60,BLUE,"Copilot reviews",r=10,fs=13.5)
    b+=txt(330,152,"finds issues, suggests fixes",MUTE,10,"400","middle")
    b+=box(460,80,150,60,NAVY,"You decide",r=10,fs=13.5)
    b+=box(650,80,110,60,OK,"Merge",r=10,fs=13.5)
    b+=arrow(200,110,240,110,BLUE); b+=arrow(420,110,460,110,MUTE); b+=arrow(610,110,650,110,MUTE)
    b+=txt(400,176,"Copilot review augments \u2014 human reviewers still approve the change",MUTE,12,"400","middle")
    return svg(800,196,b,"Copilot-assisted pull request review")
D["code-review-flow"]=d_review

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
