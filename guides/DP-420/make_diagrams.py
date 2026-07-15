"""Generate the ORIGINAL inline-SVG diagram library for the public DP-420 guide.

Clean-room: these are original schematic diagrams in our own visual style, expressing
well-documented, factual Azure Cosmos DB concepts (resource hierarchy, request units,
partitioning, consistency levels, global distribution, change feed, analytical store,
indexing, backup, security). No Microsoft images/slides are used or reproduced.
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

# 1) Cosmos DB resource hierarchy
def d_hierarchy():
    b=defs_arrow()
    b+=txt(400,30,"Azure Cosmos DB resource model",NAVY,19,"700","middle")
    b+=box(280,54,240,46,NAVY,"Account",r=10,fs=15)
    b+=txt(400,90,"URI + keys \u00b7 APIs \u00b7 regions",PALE,10.5,"400","middle")
    b+=arrow(400,100,400,124,BLUE)
    b+=box(300,126,200,44,BLUE,"Database",r=10,fs=14.5)
    b+=arrow(400,170,400,192,BLUE)
    b+=box(230,194,340,50,BLUEL,"","",r=10)
    b+=txt(400,216,"Container",WHITE,15,"700","middle")
    b+=txt(400,234,"unit of scale \u2014 throughput + partition key + index policy",PALE,10.3,"400","middle")
    b+=arrow(400,244,400,266,BLUE)
    xs=[150,290,430,570]
    for x in xs:
        b+=box(x,268,120,44,PALE,"","",r=8,stroke=LINE)
        b+=txt(x+60,295,"{ item }",NAVY,12.5,"600","middle")
    b+=txt(400,332,"Items are JSON documents; each has an id and a partition key value",MUTE,12,"400","middle")
    return svg(800,348,b,"Account database container items hierarchy")
D["cosmos-hierarchy"]=d_hierarchy

# 2) Request Units
def d_ru():
    b=defs_arrow()
    b+=txt(400,30,"Request Units (RU/s) \u2014 the currency of throughput",NAVY,18,"700","middle")
    b+=txt(400,54,"Every operation costs RUs; provisioned RU/s is your per-second budget",MUTE,12,"400","middle")
    ops=[("Point read (1 KB)","~1 RU",OK),("Query (indexed)","few\u2013many RU",BLUE),
         ("Create / replace","~5+ RU",BLUE),("Cross-partition query","fan-out cost",WARN)]
    x=40
    for name,cost,col in ops:
        b+=box(x,80,175,72,col,"",r=10)
        b+=txt(x+87,108,name,WHITE,12.5,"700","middle")
        b+=txt(x+87,130,cost,PALE,12,"600","middle")
        x+=185
    b+=f"<rect x='60' y='170' width='680' height='34' rx='8' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(400,192,"Exceed provisioned RU/s \u2192 request is rate-limited with HTTP 429 (retry after)",WARN,11.8,"600","middle")
    return svg(800,222,b,"Request unit cost model")
D["request-units"]=d_ru

# 3) Throughput modes
def d_throughput():
    b=""
    b+=txt(400,28,"Choosing a throughput / capacity mode",NAVY,18,"700","middle")
    cols=[("Provisioned\n(manual)",BLUE,["Steady, predictable load","Set fixed RU/s","Billed for provisioned RU/s"]),
          ("Provisioned\n(autoscale)",BLUEL,["Variable / spiky load","Scales 10% \u2013 100% of max","Billed for peak RU/s used"]),
          ("Serverless\n ",NAVY,["Bursty / dev / low traffic","No RU/s to set","Billed per RU consumed"]),
          ("Free tier\n ",OK,["First 1000 RU/s + 25 GB free","One per subscription","Great for learning"])]
    x0=30; colw=188; y0=52; rh=44
    for j,(name,col,cells) in enumerate(cols):
        x=x0+j*colw
        l1,l2=name.split("\n")
        b+=box(x,y0,colw-12,44,col,l1,l2,r=8,fs=13,sfs=11)
        for i,c in enumerate(cells):
            yy=y0+48+rh*i; fill=PALE if i%2 else WHITE
            b+=f"<rect x='{x}' y='{yy}' width='{colw-12}' height='{rh}' fill='{fill}' stroke='{LINE}' stroke-width='1'/>"
            b+=txt(x+(colw-12)/2,yy+rh/2+4,c,INK,10.8,"400","middle")
    return svg(800,y0+48+rh*3+16,b,"Provisioned autoscale serverless free tier")
D["throughput-modes"]=d_throughput

# 4) Logical vs physical partitions
def d_partitions():
    b=defs_arrow()
    b+=txt(400,30,"Logical and physical partitions",NAVY,18,"700","middle")
    # logical partitions
    lps=[("PK=A",120),("PK=B",270),("PK=C",420),("PK=D",570)]
    for name,x in lps:
        b+=box(x,64,110,44,BLUEL,name,r=8,fs=13)
    b+=txt(400,128,"Logical partition = all items sharing one partition key value (max 20 GB)",MUTE,11.5,"400","middle")
    # physical partitions
    b+=box(120,150,260,56,NAVY,"","",r=10)
    b+=txt(250,174,"Physical partition 1",WHITE,13,"700","middle")
    b+=txt(250,193,"hosts PK=A, PK=B",PALE,10.5,"400","middle")
    b+=box(420,150,260,56,NAVY,"","",r=10)
    b+=txt(550,174,"Physical partition 2",WHITE,13,"700","middle")
    b+=txt(550,193,"hosts PK=C, PK=D",PALE,10.5,"400","middle")
    b+=arrow(175,108,230,150,MUTE); b+=arrow(325,108,270,150,MUTE)
    b+=arrow(475,108,530,150,MUTE); b+=arrow(625,108,570,150,MUTE)
    b+=txt(400,228,"Cosmos DB maps logical partitions to physical partitions and splits them as data/RU grows",MUTE,11.8,"400","middle")
    return svg(800,244,b,"Logical partitions map to physical partitions")
D["logical-physical-partitions"]=d_partitions

# 5) Partition key quality
def d_pkquality():
    b=""
    b+=txt(400,28,"Partition key quality",NAVY,19,"700","middle")
    # good: even
    b+=txt(210,60,"Good \u2014 high cardinality, even",OK,13,"700","middle")
    for i,x in enumerate([70,140,210,280,350]):
        b+=f"<rect x='{x}' y='74' width='50' height='70' rx='6' fill='{BLUEL}'/>"
        b+=txt(x+25,115,"25%",WHITE,11,"600","middle")
    b+=txt(210,164,"Requests & storage spread evenly",MUTE,11,"400","middle")
    # bad: hot
    b+=txt(600,60,"Bad \u2014 low cardinality, hot",WARN,13,"700","middle")
    heights=[130,20,16,16,14]
    for i,x in enumerate([470,540,610,680,750]):
        hh=heights[i]; col=WARN if i==0 else "#9fb0bf"
        b+=f"<rect x='{x-460+470-10}' y='{144-hh}' width='40' height='{hh}' rx='5' fill='{col}'/>"
    b+=txt(600,164,"One 'hot' partition throttles (429) while others idle",WARN,11,"600","middle")
    return svg(800,184,b,"Even distribution versus a hot partition")
D["partition-key-quality"]=d_pkquality

# 6) Synthetic partition key
def d_synthetic():
    b=defs_arrow()
    b+=txt(400,30,"Synthetic partition key",NAVY,18,"700","middle")
    b+=chip(70,70,150,40,"deviceId: 'D5'",WHITE,NAVY,12)
    b+=txt(245,95,"+",MUTE,20,"700","middle")
    b+=chip(270,70,150,40,"date: '2026-07'",WHITE,NAVY,12)
    b+=arrow(430,90,478,90,BLUE)
    b+=box(480,66,250,48,BLUE,"pk = 'D5-2026-07'",r=10,fs=14)
    b+=txt(400,150,"Concatenate fields (or add a random suffix) to raise cardinality and spread load",MUTE,12,"400","middle")
    b+=f"<rect x='120' y='170' width='560' height='34' rx='8' fill='{PALE}' stroke='{LINE}'/>"
    b+=txt(400,192,"Turns a low-cardinality key into many evenly-loaded logical partitions",NAVY,11.8,"600","middle")
    return svg(800,220,b,"Synthetic partition key composition")
D["synthetic-partition-key"]=d_synthetic

# 7) Hierarchical partition key
def d_hpk():
    b=defs_arrow()
    b+=txt(400,30,"Hierarchical partition key (subpartitioning)",NAVY,18,"700","middle")
    b+=box(300,58,200,42,NAVY,"TenantId",r=9,fs=13.5)
    b+=arrow(360,100,250,126,BLUE); b+=arrow(440,100,550,126,BLUE)
    b+=box(150,128,200,40,BLUE,"UserId",r=9,fs=13)
    b+=box(450,128,200,40,BLUE,"UserId",r=9,fs=13)
    b+=arrow(250,168,250,192,BLUE); b+=arrow(550,168,550,192,BLUE)
    b+=box(150,194,200,40,BLUEL,"SessionId",r=9,fs=13)
    b+=box(450,194,200,40,BLUEL,"SessionId",r=9,fs=13)
    b+=txt(400,262,"Up to three levels \u2014 routes a query on the prefix to a subset of partitions",MUTE,12,"400","middle")
    b+=txt(400,282,"Lets a single logical-partition prefix exceed 20 GB across subpartitions",MUTE,11.5,"400","middle")
    return svg(800,298,b,"Hierarchical partition key three levels")
D["hierarchical-partition-key"]=d_hpk

# 8) Embed vs reference
def d_embedref():
    b=defs_arrow()
    b+=txt(400,28,"Embedding vs referencing",NAVY,19,"700","middle")
    # embed
    b+=txt(210,58,"Embed (denormalize)",BLUE,13.5,"700","middle")
    b+=box(60,70,300,120,PALE,"",r=10,stroke=LINE)
    b+=txt(80,96,"{ orderId, customer:{...},",INK,11.5,"400")
    b+=txt(80,118,"  lines:[ {...}, {...} ] }",INK,11.5,"400")
    b+=txt(210,150,"One read gets everything",OK,11.5,"600","middle")
    b+=txt(210,172,"Best: read together, bounded, rarely changes",MUTE,10,"400","middle")
    # reference
    b+=txt(600,58,"Reference (normalize)",NAVY,13.5,"700","middle")
    b+=box(450,70,140,44,BLUEL,"order",r=9,fs=13)
    b+=box(650,70,110,44,BLUE,"customer",r=9,fs=12)
    b+=box(450,132,140,44,BLUE,"lineItem",r=9,fs=12.5)
    b+=arrow(590,92,650,92,MUTE)
    b+=arrow(520,114,520,132,MUTE)
    b+=txt(600,196,"Best: large, unbounded, or shared/updated data",MUTE,10,"400","middle")
    return svg(800,212,b,"Embedding versus referencing data")
D["embed-vs-reference"]=d_embedref

# 9) Consistency levels
def d_consistency():
    b=defs_arrow()
    b+=txt(400,28,"Five consistency levels",NAVY,19,"700","middle")
    b+=txt(120,54,"Stronger \u00b7 higher RU \u00b7 higher latency",MUTE,10.5,"400","middle")
    b+=txt(690,54,"Weaker \u00b7 lower RU \u00b7 lower latency",MUTE,10.5,"400","end")
    levels=[("Strong","linearizable",NAVY),("Bounded\nStaleness","lag by K / t",BLUE),
            ("Session","default; per-client",BLUEL),("Consistent\nPrefix","in-order",BLUEL),
            ("Eventual","fastest",MUTE)]
    x=30
    for name,sub,col in levels:
        w=140
        l=name.split("\n")
        b+=box(x,72,w,72,col,"",r=10)
        if len(l)==2:
            b+=txt(x+w/2,98,l[0],WHITE,13.5,"700","middle")
            b+=txt(x+w/2,116,l[1],WHITE,13.5,"700","middle")
        else:
            b+=txt(x+w/2,104,l[0],WHITE,14.5,"700","middle")
        b+=txt(x+w/2,136,sub,PALE,10.3,"400","middle")
        x+=152
    b+=arrow(60,158,740,158,MUTE)
    b+=txt(400,182,"Session is the default; each level trades guarantees against RU cost & latency",MUTE,12,"400","middle")
    return svg(800,198,b,"Consistency levels spectrum")
D["consistency-levels"]=d_consistency

# 10) Global distribution
def d_global():
    b=defs_arrow()
    b+=txt(400,30,"Global (turnkey) distribution",NAVY,18,"700","middle")
    b+=box(320,60,160,48,NAVY,"Write region",r=10,fs=13.5)
    b+=txt(400,98,"East US",PALE,10.5,"400","middle")
    reads=[("West US",120,180),("North Europe",340,180),("Southeast Asia",560,180)]
    for name,x,y in reads:
        b+=box(x,y,150,46,BLUE,name,r=9,fs=12.5)
        b+=arrow(400,108,x+75,y,BLUE)
    b+=txt(400,254,"Add/remove read regions with a click; data replicates automatically",MUTE,12,"400","middle")
    b+=txt(400,274,"Apps connect to the nearest region for low-latency reads",MUTE,11.5,"400","middle")
    return svg(800,290,b,"Single write region with global read replicas")
D["global-distribution"]=d_global

# 11) Multi-region writes / conflict resolution
def d_mrw():
    b=defs_arrow()
    b+=txt(400,30,"Multi-region writes & conflict resolution",NAVY,18,"700","middle")
    b+=box(90,64,180,48,BLUE,"Write: East US",r=9,fs=13)
    b+=box(530,64,180,48,BLUE,"Write: West EU",r=9,fs=13)
    b+=arrow(270,88,530,88,MUTE); b+=arrow(530,104,270,104,MUTE)
    b+=box(300,150,200,50,NAVY,"","",r=10)
    b+=txt(400,172,"Conflict resolution",WHITE,13.5,"700","middle")
    b+=txt(400,190,"same item edited in two regions",PALE,10,"400","middle")
    b+=arrow(180,112,360,150,MUTE); b+=arrow(620,112,440,150,MUTE)
    b+=chip(120,224,270,34,"Last-Writer-Wins (default, _ts)",WHITE,NAVY,11.5)
    b+=chip(410,224,270,34,"Custom \u2014 policy path or stored procedure",WHITE,NAVY,11)
    return svg(800,278,b,"Multi-region writes conflict resolution policies")
D["multi-region-writes"]=d_mrw

# 12) Connectivity modes
def d_connmodes():
    b=defs_arrow()
    b+=txt(400,30,"SDK connectivity modes",NAVY,18,"700","middle")
    # gateway
    b+=txt(200,60,"Gateway mode",BLUEL,13.5,"700","middle")
    b+=box(70,74,120,44,BLUEL,"App / SDK",r=9,fs=12.5)
    b+=box(240,74,120,44,BLUE,"Gateway",r=9,fs=13)
    b+=arrow(190,96,240,96,BLUE)
    b+=arrow(360,96,360,130,BLUE)
    b+=box(240,132,120,40,NAVY,"Replicas",r=9,fs=12.5)
    b+=txt(200,196,"HTTPS 443 \u00b7 firewall-friendly \u00b7 one hop",MUTE,10.5,"400","middle")
    # direct
    b+=txt(600,60,"Direct mode",BLUE,13.5,"700","middle")
    b+=box(470,74,120,44,BLUEL,"App / SDK",r=9,fs=12.5)
    b+=box(640,132,120,40,NAVY,"Replicas",r=9,fs=12.5)
    b+=arrow(590,100,640,140,BLUE)
    b+=txt(600,196,"TCP direct to replicas \u00b7 lowest latency & best throughput",MUTE,10.5,"400","middle")
    return svg(800,214,b,"Gateway versus direct connectivity mode")
D["connectivity-modes"]=d_connmodes

# 13) Point vs query
def d_pointquery():
    b=""
    b+=txt(400,28,"Point operation vs query",NAVY,19,"700","middle")
    b+=box(60,60,320,120,BLUE,"",r=12)
    b+=txt(220,88,"Point read / write",WHITE,15,"700","middle")
    b+=txt(220,112,"needs id + partition key",PALE,11.5,"400","middle")
    b+=chip(90,126,260,30,"~1 RU for a 1 KB read \u00b7 fastest",WHITE,NAVY,11)
    b+=chip(90,160,260,14,"",WHITE,NAVY,11)
    b+=txt(220,170,"ReadItem / CreateItem / ReplaceItem",MUTE,10.3,"400","middle")
    b+=box(420,60,320,120,NAVY,"",r=12)
    b+=txt(580,88,"Query",WHITE,15,"700","middle")
    b+=txt(580,112,"filter/scan many items",PALE,11.5,"400","middle")
    b+=chip(450,126,260,30,"cost scales with items & RU used",WHITE,NAVY,11)
    b+=txt(580,170,"single-partition cheaper than cross-partition",MUTE,10.3,"400","middle")
    return svg(800,200,b,"Point operations versus queries")
D["point-vs-query"]=d_pointquery

# 14) Transactional batch
def d_batch():
    b=defs_arrow()
    b+=txt(400,30,"Transactional batch",NAVY,18,"700","middle")
    b+=box(280,58,240,44,NAVY,"Same logical partition",r=9,fs=13)
    xs=[("Create",120),("Replace",320),("Delete",520)]
    for name,x in xs:
        b+=box(x,120,160,44,BLUE,name,r=9,fs=13)
    b+=arrow(400,102,400,112,BLUE)
    b+=f"<rect x='100' y='110' width='600' height='64' rx='12' fill='none' stroke='{OK}' stroke-width='2' stroke-dasharray='6 5'/>"
    b+=txt(400,196,"All operations commit together or all roll back \u2014 one partition key only",OK,12,"600","middle")
    return svg(800,214,b,"Transactional batch all-or-nothing within a partition")
D["transactional-batch"]=d_batch

# 15) Change feed
def d_changefeed():
    b=defs_arrow()
    b+=txt(400,30,"Change feed",NAVY,18,"700","middle")
    b+=box(60,80,180,60,BLUEL,"","",r=10)
    b+=txt(150,106,"Container",WHITE,13.5,"700","middle")
    b+=txt(150,126,"inserts & updates",PALE,10.5,"400","middle")
    b+=arrow(240,110,300,110,BLUE)
    b+=box(300,80,200,60,NAVY,"","",r=10)
    b+=txt(400,106,"Change feed",WHITE,13.5,"700","middle")
    b+=txt(400,126,"ordered per partition",PALE,10.5,"400","middle")
    b+=arrow(500,110,560,110,BLUE)
    b+=box(560,66,180,40,BLUE,"Azure Functions",r=8,fs=12.5)
    b+=box(560,116,180,40,BLUE,"Change feed processor",r=8,fs=11.5)
    b+=txt(400,186,"Persistent, ordered record of changes \u2014 no deletes unless you use TTL soft-deletes",MUTE,11.8,"400","middle")
    return svg(800,204,b,"Change feed to functions or processor")
D["change-feed"]=d_changefeed

# 16) Change feed patterns
def d_cfpatterns():
    b=""
    b+=txt(400,28,"Change feed patterns",NAVY,19,"700","middle")
    pats=[("Denormalize","copy changes into a second container",BLUE),
          ("Referential","validate/cascade related items",BLUEL),
          ("Aggregate","maintain running totals / reports",NAVY),
          ("Archive","write cold data to cheap storage",MUTE)]
    x=30
    for name,desc,col in pats:
        b+=box(x,60,182,96,col,"",r=10)
        b+=txt(x+91,92,name,WHITE,14.5,"700","middle")
        b+=txt(x+91,118,desc,PALE,10,"400","middle")
        x+=190
    return svg(800,172,b,"Change feed denormalize referential aggregate archive")
D["change-feed-patterns"]=d_cfpatterns

# 17) Analytical store / HTAP
def d_analytical():
    b=defs_arrow()
    b+=txt(400,30,"HTAP: transactional + analytical store",NAVY,18,"700","middle")
    b+=box(90,66,260,60,BLUE,"","",r=10)
    b+=txt(220,90,"Transactional store",WHITE,13.5,"700","middle")
    b+=txt(220,110,"row-based \u00b7 RU-billed \u00b7 OLTP",PALE,10.3,"400","middle")
    b+=box(450,66,260,60,NAVY,"","",r=10)
    b+=txt(580,90,"Analytical store",WHITE,13.5,"700","middle")
    b+=txt(580,110,"column-based \u00b7 auto-sync \u00b7 no RU",PALE,10.3,"400","middle")
    b+=arrow(350,96,450,96,BLUE)
    b+=txt(400,140,"auto-sync (no ETL)",BLUE,10.5,"600","middle")
    b+=box(150,166,180,46,BLUEL,"Synapse Spark",r=9,fs=12.5)
    b+=box(360,166,180,46,BLUEL,"Synapse SQL",r=9,fs=12.5)
    b+=box(570,166,150,46,OK,"Fabric mirror",r=9,fs=12)
    b+=arrow(580,126,450,166,MUTE)
    b+=txt(400,238,"Queries on the analytical store don't consume transactional RU/s",MUTE,12,"400","middle")
    return svg(800,254,b,"Transactional and analytical store HTAP")
D["analytical-store-htap"]=d_analytical

# 18) Indexing policy
def d_indexing():
    b=defs_arrow()
    b+=txt(400,30,"Indexing policy",NAVY,18,"700","middle")
    b+=box(60,64,300,150,PALE,"",r=10,stroke=LINE)
    b+=txt(210,88,"By default: index everything",NAVY,13,"700","middle")
    b+=chip(80,102,260,30,"includedPaths: /*",WHITE,OK,11.5)
    b+=chip(80,138,260,30,"excludedPaths: /\"_etag\"/?",WHITE,WARN,11.5)
    b+=txt(210,196,"Range, spatial, and composite index kinds",MUTE,10.3,"400","middle")
    b+=box(430,64,310,150,PALE,"",r=10,stroke=LINE)
    b+=txt(585,88,"Tune for the workload",NAVY,13,"700","middle")
    b+=chip(450,102,270,30,"Write-heavy \u2192 exclude unqueried paths",WHITE,NAVY,10.5)
    b+=chip(450,138,270,30,"Read-heavy \u2192 add composite indexes",WHITE,NAVY,10.5)
    b+=txt(585,196,"Fewer indexed paths = cheaper writes",MUTE,10.3,"400","middle")
    return svg(800,230,b,"Indexing policy included excluded composite")
D["indexing-policy"]=d_indexing

# 19) Composite index
def d_composite():
    b=defs_arrow()
    b+=txt(400,30,"Composite index",NAVY,18,"700","middle")
    b+=box(230,60,340,50,BLUE,"",r=10)
    b+=txt(400,82,"ORDER BY category ASC, price DESC",WHITE,13,"700","middle")
    b+=txt(400,101,"multi-property filter + sort",PALE,10,"400","middle")
    b+=arrow(400,110,400,140,BLUE)
    b+=box(230,142,340,50,NAVY,"",r=10)
    b+=txt(400,164,"Composite index (category, price)",WHITE,12.5,"700","middle")
    b+=txt(400,182,"order & direction must match the query",PALE,9.8,"400","middle")
    b+=f"<rect x='120' y='210' width='560' height='34' rx='8' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(400,232,"Needed for multi-property ORDER BY and to cut RU on multi-filter queries",WARN,11.5,"600","middle")
    return svg(800,260,b,"Composite index for multi-property sort")
D["composite-index"]=d_composite

# 20) Integrated cache
def d_cache():
    b=defs_arrow()
    b+=txt(400,30,"Integrated cache (dedicated gateway)",NAVY,18,"700","middle")
    b+=box(60,90,150,50,BLUEL,"App / SDK",r=9,fs=13)
    b+=box(280,72,220,86,NAVY,"","",r=10)
    b+=txt(390,98,"Dedicated gateway",WHITE,13.5,"700","middle")
    b+=chip(300,112,180,32,"Integrated cache",BLUE,WHITE,11.5,stroke="none")
    b+=box(570,90,170,50,BLUE,"Backend replicas",r=9,fs=12.5)
    b+=arrow(210,115,280,115,BLUE)
    b+=arrow(500,115,570,115,BLUE,dash=True)
    b+=txt(400,186,"Cache hits cost 0 RU \u2014 requires gateway mode + session/eventual consistency",MUTE,11.8,"400","middle")
    return svg(800,204,b,"Integrated cache on the dedicated gateway")
D["integrated-cache"]=d_cache

# 21) Backup modes
def d_backup():
    b=""
    b+=txt(400,28,"Backup & restore modes",NAVY,19,"700","middle")
    cols=[("Periodic backup",BLUE,["Snapshots every N hours","Restore via support ticket","Keeps a fixed # of copies","Default on older accounts"]),
          ("Continuous backup",NAVY,["Point-in-time restore (PITR)","Self-service restore","7-day or 30-day retention","Restore to any second"])]
    x0=90; colw=310; y0=52; rh=42
    for j,(name,col,cells) in enumerate(cols):
        x=x0+j*colw
        b+=box(x,y0,colw-16,38,col,name,r=8,fs=14)
        for i,c in enumerate(cells):
            yy=y0+42+rh*i; fill=PALE if i%2 else WHITE
            b+=f"<rect x='{x}' y='{yy}' width='{colw-16}' height='{rh}' fill='{fill}' stroke='{LINE}' stroke-width='1'/>"
            b+=txt(x+(colw-16)/2,yy+rh/2+4,c,INK,11.3,"400","middle")
    return svg(800,y0+42+rh*4+16,b,"Periodic versus continuous backup")
D["backup-modes"]=d_backup

# 22) Security layers
def d_security():
    b=""
    b+=txt(400,28,"Layers of Cosmos DB security",NAVY,18,"700","middle")
    layers=[("Network","Firewall, VNet service endpoints, Private Link",BLUEL,720),
            ("Identity & access","Control plane RBAC \u00b7 data plane Entra ID \u00b7 keys",BLUE,600),
            ("Encryption","At rest (service or customer-managed keys) + in transit",NAVY,480),
            ("Field-level","Always Encrypted for sensitive properties","#062338",360)]
    y=54
    for name,sub,col,w in layers:
        x=(800-w)/2
        b+=box(x,y,w,50,col,"",r=9)
        b+=txt(400,y+22,name,WHITE,13.5,"700","middle")
        b+=txt(400,y+40,sub,PALE,10.3,"400","middle")
        y+=60
    b+=txt(400,y+6,"Combine layers for defense in depth",MUTE,11.5,"400","middle")
    return svg(800,y+22,b,"Network identity encryption field-level security")
D["security-layers"]=d_security

# 23) RBAC planes
def d_rbac():
    b=defs_arrow()
    b+=txt(400,30,"Control plane vs data plane access",NAVY,18,"700","middle")
    b+=box(70,66,300,120,BLUE,"",r=12)
    b+=txt(220,92,"Control plane",WHITE,15,"700","middle")
    b+=txt(220,114,"manage the account/resources",PALE,10.5,"400","middle")
    b+=chip(90,128,260,30,"Azure RBAC \u00b7 e.g. Cosmos DB Operator",WHITE,NAVY,10.5)
    b+=txt(220,174,"portal, ARM, keys, regions, firewall",MUTE,10,"400","middle")
    b+=box(430,66,300,120,NAVY,"",r=12)
    b+=txt(580,92,"Data plane",WHITE,15,"700","middle")
    b+=txt(580,114,"read/write items in containers",PALE,10.5,"400","middle")
    b+=chip(450,128,260,30,"Cosmos DB data-plane RBAC (Entra ID)",WHITE,NAVY,10)
    b+=txt(580,174,"role definitions + assignments, no keys",MUTE,10,"400","middle")
    return svg(800,204,b,"Control plane and data plane RBAC")
D["rbac-planes"]=d_rbac

# 24) Data movement options
def d_movement():
    b=defs_arrow()
    b+=txt(400,30,"Ways to move data in/out of Cosmos DB",NAVY,18,"700","middle")
    opts=[("SDK bulk","high-throughput import",BLUEL),("Data Factory","pipelines & copy",BLUE),
          ("Spark connector","batch/stream in Spark",NAVY),("Kafka connector","stream from/to Kafka",BLUEL),
          ("Stream Analytics","real-time as output sink",BLUE)]
    x=25
    for name,s,col in opts:
        b+=box(x,70,148,66,col,"",r=9)
        b+=txt(x+74,98,name,WHITE,12.3,"700","middle")
        b+=txt(x+74,118,s,PALE,9.5,"400","middle")
        x+=152
    b+=box(240,158,320,42,"#062338","Azure Cosmos DB",r=10,fs=14)
    b+=arrow(400,140,400,158,BLUE)
    return svg(800,214,b,"Data movement options")
D["data-movement"]=d_movement

# 25) DevOps / declarative provisioning
def d_devops():
    b=defs_arrow()
    b+=txt(400,30,"Declarative provisioning (IaC)",NAVY,18,"700","middle")
    b+=box(70,74,190,60,BLUEL,"","",r=10)
    b+=txt(165,100,"ARM / Bicep",WHITE,13.5,"700","middle")
    b+=txt(165,120,"desired-state template",PALE,10.3,"400","middle")
    b+=arrow(260,104,320,104,BLUE)
    b+=box(320,74,180,60,BLUE,"","",r=10)
    b+=txt(410,100,"Deployment",WHITE,13.5,"700","middle")
    b+=txt(410,120,"idempotent apply",PALE,10.3,"400","middle")
    b+=arrow(500,104,560,104,BLUE)
    b+=box(560,74,180,60,NAVY,"","",r=10)
    b+=txt(650,100,"Cosmos DB",WHITE,13.5,"700","middle")
    b+=txt(650,120,"account/db/container",PALE,10.3,"400","middle")
    b+=txt(400,168,"Declarative = describe the end state; imperative (CLI/PowerShell) = run steps",MUTE,11.8,"400","middle")
    b+=txt(400,188,"Keep throughput & indexing policy in source control for repeatable environments",MUTE,11.3,"400","middle")
    return svg(800,204,b,"Declarative ARM Bicep provisioning")
D["devops-arm"]=d_devops

# 26) TTL
def d_ttl():
    b=defs_arrow()
    b+=txt(400,30,"Time to live (TTL)",NAVY,18,"700","middle")
    b+=box(60,70,220,54,BLUEL,"","",r=10)
    b+=txt(170,94,"Container DefaultTimeToLive",WHITE,12,"700","middle")
    b+=txt(170,112,"-1 = on, no expiry \u00b7 N = seconds",PALE,9.8,"400","middle")
    b+=box(320,70,180,54,BLUE,"","",r=10)
    b+=txt(410,94,"Item ttl overrides",WHITE,12.5,"700","middle")
    b+=txt(410,112,"per-document seconds",PALE,10,"400","middle")
    b+=arrow(500,97,560,97,BLUE)
    b+=box(560,70,180,54,MUTE,"","",r=10)
    b+=txt(650,94,"Auto-delete",WHITE,13,"700","middle")
    b+=txt(650,112,"uses leftover RU/s",PALE,10,"400","middle")
    b+=f"<rect x='100' y='146' width='600' height='34' rx='8' fill='{PALE}' stroke='{LINE}'/>"
    b+=txt(400,168,"Container TTL must be enabled for item-level ttl to take effect",NAVY,11.8,"600","middle")
    return svg(800,196,b,"Time to live container and item level")
D["ttl"]=d_ttl

# 27) Monitoring metrics
def d_monitor():
    b=defs_arrow()
    b+=txt(400,30,"Monitoring with Azure Monitor",NAVY,18,"700","middle")
    metrics=[("Normalized RU %","hot partition / throttle signal",BLUE),
             ("429 rate","rate-limited requests",WARN),
             ("Server-side latency","p50/p99 read & write",BLUEL),
             ("Replication latency","P[R]ITR & multi-region health",NAVY)]
    y=60
    for name,desc,col in metrics:
        b+=box(60,y,250,44,col,name,r=8,fs=12.5)
        b+=txt(330,y+27,desc,MUTE,11.5,"400")
        y+=54
    b+=f"<rect x='560' y='60' width='180' height='206' rx='10' fill='{PALE}' stroke='{LINE}'/>"
    b+=txt(650,86,"Alerts + logs",NAVY,13,"700","middle")
    b+=chip(575,100,150,28,"Metric alerts",WHITE,NAVY,10.5)
    b+=chip(575,136,150,28,"Diagnostic settings",WHITE,NAVY,10)
    b+=chip(575,172,150,28,"Log Analytics / KQL",WHITE,NAVY,10)
    b+=chip(575,208,150,28,"Audit & security logs",WHITE,NAVY,10)
    return svg(800,282,b,"Azure Monitor metrics alerts and logs")
D["monitor-metrics"]=d_monitor

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
