"""Generate the ORIGINAL inline-SVG diagram library for the public DP-600 guide.

Clean-room: these are original schematic diagrams in our own visual style, expressing
well-documented, factual Microsoft Fabric concepts (architecture, layering, storage modes,
security layers, DAX context, etc.). No Microsoft images/slides are used or reproduced.
Each diagram is saved to assets/diagrams/<id>.svg with a responsive viewBox.
"""
import os, html

# Script-relative: writes SVGs to <this guide>/assets/diagrams and the catalog to <guide>/content.
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

# 1) Fabric + OneLake overview
def d_onelake():
    b=defs_arrow()
    b+=txt(400,34,"Microsoft Fabric on OneLake",NAVY,20,"700","middle")
    b+=txt(400,56,"One unified SaaS platform \u2014 one copy of data for every workload",MUTE,13,"400","middle")
    wls=["Data\nEngineering","Data\nWarehouse","Real-Time\nIntelligence","Data\nScience","Power BI\n "]
    xs=[40,190,340,490,640]
    for x,w in zip(xs,wls):
        line1,line2=w.split("\n")
        b+=box(x,86,130,64,BLUE,"","",r=9)
        b+=txt(x+65,116,line1,WHITE,13.5,"600","middle")
        b+=txt(x+65,134,line2,WHITE,13.5,"600","middle")
        b+=arrow(x+65,150,x+65,182,BLUE)
    b+=box(40,186,730,74,NAVY,"","",r=12)
    b+=txt(405,218,"OneLake",WHITE,20,"700","middle")
    b+=txt(405,240,"Single tenant-wide data lake \u2014 open Delta Parquet format, governed once",PALE,12.5,"400","middle")
    return svg(800,280,b,"Microsoft Fabric workloads on a single OneLake")
D["fabric-onelake-overview"]=d_onelake

# 2) Medallion
def d_medallion():
    b=defs_arrow()
    b+=txt(400,32,"Medallion architecture",NAVY,19,"700","middle")
    layers=[("Bronze","Raw / ingested","As-is source data","#a97142"),
            ("Silver","Cleaned / conformed","Validated, de-duplicated","#8a9199"),
            ("Gold","Curated / modeled","Star schemas, aggregates","#c9a227")]
    x=40
    for i,(t,s1,s2,col) in enumerate(layers):
        b+=box(x,70,200,110,col,"","",r=12)
        b+=txt(x+100,110,t,WHITE,20,"700","middle")
        b+=txt(x+100,135,s1,WHITE,12.5,"600","middle")
        b+=txt(x+100,155,s2,PALE,11.5,"400","middle")
        if i<2: b+=arrow(x+200,125,x+258,125,MUTE)
        x+=258
    b+=txt(400,205,"Refine data left \u2192 right; each layer adds quality and business meaning",MUTE,12.5,"400","middle")
    return svg(800,230,b,"Medallion bronze silver gold layers")
D["medallion"]=d_medallion

# 3) Store comparison
def d_stores():
    b=""
    b+=txt(400,30,"Choosing a Fabric data store",NAVY,19,"700","middle")
    cols=[("Lakehouse",BLUEL,["Mixed / unstructured","Spark + read-only T-SQL","Notebooks, Dataflows","Delta in OneLake"]),
          ("Warehouse",BLUE,["Structured BI","Full T-SQL (read/write)","INSERT/UPDATE/MERGE","Delta in OneLake"]),
          ("Eventhouse",NAVY,["Streaming / time-series","KQL (pipe syntax)","Append-only ingest","KQL + OneLake"])]
    rows=["Best for","Query language","Write pattern","Storage"]
    x0=210; colw=190; y0=58; rh=52
    for i,r in enumerate(rows):
        b+=txt(40,y0+rh*i+rh/2+18,r,NAVY,12.5,"700")
    for j,(name,col,cells) in enumerate(cols):
        x=x0+j*colw
        b+=box(x,y0,colw-12,34,col,name,"",r=8)
        for i,c in enumerate(cells):
            yy=y0+34+rh*i
            fill=PALE if i%2 else WHITE
            b+=f"<rect x='{x}' y='{yy}' width='{colw-12}' height='{rh}' fill='{fill}' stroke='{LINE}' stroke-width='1'/>"
            b+=txt(x+(colw-12)/2,yy+rh/2+4,c,INK,11.8,"400","middle")
    return svg(800,300,b,"Lakehouse vs warehouse vs eventhouse comparison")
D["store-comparison"]=d_stores

# 4) Star schema
def d_star():
    b=defs_arrow()
    b+=txt(400,28,"Star schema",NAVY,19,"700","middle")
    cx,cy=400,175
    b+=box(cx-85,cy-45,170,90,BLUE,"","",r=10)
    b+=txt(cx,cy-12,"Fact_Sales",WHITE,15,"700","middle")
    b+=txt(cx,cy+8,"OrderKey, DateKey,",PALE,11,"400","middle")
    b+=txt(cx,cy+24,"ProductKey, Qty, Amount",PALE,11,"400","middle")
    dims=[("Dim_Date",130,60),("Dim_Product",650,60),("Dim_Customer",130,290),("Dim_Store",650,290)]
    for name,dx,dy in dims:
        b+=box(dx-70,dy-26,140,52,BLUEL,name,"",r=9,fs=13.5)
        b+=arrow(dx+(0 if dx>cx else 0), dy+(26 if dy<cy else -26), cx+(-60 if dx<cx else 60), cy+(-30 if dy<cy else 30),MUTE)
    b+=txt(400,340,"One central fact table joins to denormalized dimensions via surrogate keys",MUTE,12,"400","middle")
    return svg(800,360,b,"Star schema fact and dimension tables")
D["star-schema"]=d_star

# 5) SCD types
def d_scd():
    b=""
    b+=txt(400,28,"Slowly changing dimensions",NAVY,19,"700","middle")
    # Type 1
    b+=txt(200,62,"Type 1 \u2014 overwrite (no history)",NAVY,13.5,"700","middle")
    b+=chip(70,78,260,30,"Cust 7 \u00b7 Region: West",WHITE,INK,12)
    b+=txt(200,128,"\u2193 region changes",MUTE,11.5,"400","middle")
    b+=chip(70,138,260,30,"Cust 7 \u00b7 Region: East",PALE,NAVY,12)
    b+=txt(200,188,"Old value is lost",WARN,11.5,"600","middle")
    # Type 2
    b+=txt(600,62,"Type 2 \u2014 add row (keep history)",NAVY,13.5,"700","middle")
    b+=chip(470,78,260,30,"Cust 7 \u00b7 West \u00b7 Current=N",WHITE,INK,11.5)
    b+=txt(600,128,"\u2193 region changes",MUTE,11.5,"400","middle")
    b+=chip(470,138,260,30,"Cust 7 \u00b7 West \u00b7 2019\u20132023",WHITE,MUTE,11.5)
    b+=chip(470,172,260,30,"Cust 7 \u00b7 East \u00b7 Current=Y",PALE,NAVY,11.5)
    b+=txt(600,222,"History preserved with validity flags",OK,11.5,"600","middle")
    return svg(800,240,b,"SCD type 1 versus type 2")
D["scd-types"]=d_scd

# 6) Storage modes
def d_modes():
    b=""
    b+=txt(400,28,"Semantic model storage modes",NAVY,19,"700","middle")
    modes=[("Import","Cached copy in memory","Fastest; scheduled refresh",OK),
           ("DirectQuery","Live query to source","Always current; slower",WARN),
           ("Direct Lake","Reads OneLake Delta","Import speed + fresh",BLUE),
           ("Dual / Composite","Mix modes per table","Engine picks best path",NAVY)]
    x=40
    for name,s1,s2,col in modes:
        b+=box(x,64,175,96,col,"","",r=10)
        b+=txt(x+87,96,name,WHITE,14.5,"700","middle")
        b+=txt(x+87,122,s1,PALE,11,"400","middle")
        b+=txt(x+87,142,s2,PALE,10.5,"400","middle")
        x+=185
    b+=txt(400,186,"Storage mode is set per table \u2014 it drives freshness, speed, cost, and features",MUTE,12,"400","middle")
    return svg(800,206,b,"Import DirectQuery Direct Lake Dual Composite storage modes")
D["storage-modes"]=d_modes

# 7) Direct Lake architecture + fallback
def d_dl_arch():
    b=defs_arrow()
    b+=txt(300,30,"Direct Lake architecture",NAVY,19,"700","middle")
    b+=box(90,58,420,58,BLUEL,"","",r=10)
    b+=txt(300,82,"Lakehouse / Warehouse",WHITE,15,"700","middle")
    b+=txt(300,101,"Delta Parquet tables in OneLake",PALE,12,"400","middle")
    b+=arrow(300,116,300,150,BLUE)
    b+=box(90,152,420,58,NAVY,"","",r=10)
    b+=txt(300,176,"Direct Lake engine",WHITE,15,"700","middle")
    b+=txt(300,195,"Loads columns on demand \u2014 no copy, no translation",PALE,11.5,"400","middle")
    b+=arrow(300,210,300,244,BLUE)
    b+=box(90,246,420,50,BLUE,"Semantic model \u2192 reports",r=10,fs=15)
    # fallback
    b+=f"<rect x='545' y='150' width='210' height='108' rx='10' fill='{PALE}' stroke='{WARN}' stroke-width='1.5' stroke-dasharray='6 5'/>"
    b+=txt(650,174,"Fallback (DL on SQL)",WARN,12.5,"700","middle")
    b+=chip(560,186,180,28,"SQL analytics endpoint",WHITE,NAVY,11)
    b+=chip(560,220,180,28,"DirectQuery",WHITE,NAVY,11)
    b+=arrow(510,181,545,196,WARN,dash=True)
    b+=txt(650,272,"used when Delta can't be read directly",MUTE,10.5,"400","middle")
    b+=txt(300,320,"Refresh = 'framing': a metadata-only pointer update to the latest Delta files (seconds)",MUTE,12,"400","middle")
    return svg(800,336,b,"Direct Lake architecture and DirectQuery fallback")
D["direct-lake-arch"]=d_dl_arch

# 8) DL OneLake vs SQL
def d_dl_variants():
    b=""
    b+=txt(400,28,"Direct Lake: two flavors",NAVY,19,"700","middle")
    rows=["Data source","DirectQuery fallback","Composite models","SQL-endpoint RLS/OLS"]
    cols=[("Direct Lake on OneLake",BLUE,["One or more Fabric Delta sources","Never falls back","Supported (+ Import tables)","Not applied (OneLake file access)"]),
          ("Direct Lake on SQL endpoint",NAVY,["Single lakehouse / warehouse","Falls back to DirectQuery","Not supported","Honored (may fall back)"])]
    x0=250; colw=270; y0=56; rh=52
    for i,r in enumerate(rows):
        b+=txt(40,y0+34+rh*i+rh/2+4,r,NAVY,12,"700")
    for j,(name,col,cells) in enumerate(cols):
        x=x0+j*colw
        b+=box(x,y0,colw-12,34,col,name,"",r=8,fs=13)
        for i,c in enumerate(cells):
            yy=y0+34+rh*i; fill=PALE if i%2 else WHITE
            b+=f"<rect x='{x}' y='{yy}' width='{colw-12}' height='{rh}' fill='{fill}' stroke='{LINE}' stroke-width='1'/>"
            b+=txt(x+(colw-12)/2,yy+rh/2+4,c,INK,11.3,"400","middle")
    return svg(800,300,b,"Direct Lake on OneLake versus on SQL analytics endpoint")
D["direct-lake-onelake-vs-sql"]=d_dl_variants

# 9) Security layers
def d_seclayers():
    b=""
    b+=txt(400,28,"Layers of access control",NAVY,19,"700","middle")
    layers=[("Workspace roles","Admin / Member / Contributor / Viewer",BLUEL,720),
            ("Item permissions","Share individual items",BLUE,600),
            ("Row / Column / Object security","RLS, CLS, OLS in the model & SQL",NAVY,480),
            ("OneLake file-level","Data access roles on /Files & /Tables","#062338",360)]
    y=58
    for name,sub,col,w in layers:
        x=(800-w)/2
        b+=box(x,y,w,52,col,"","",r=9)
        b+=txt(400,y+24,name,WHITE,14,"700","middle")
        b+=txt(400,y+42,sub,PALE,11,"400","middle")
        y+=62
    b+=txt(400,y+8,"Broad \u2192 narrow: combine layers for defense in depth",MUTE,12,"400","middle")
    return svg(800,y+24,b,"Workspace item row column object and file access layers")
D["security-layers"]=d_seclayers

# 10) Workspace roles
def d_roles():
    b=""
    b+=txt(400,28,"Workspace roles (most \u2192 least privilege)",NAVY,18,"700","middle")
    roles=[("Admin","Full control + manage access & settings",NAVY),
           ("Member","Add members, share, edit all items",BLUE),
           ("Contributor","Create and edit items",BLUEL),
           ("Viewer","Read / consume only",MUTE)]
    y=56
    for i,(name,desc,col) in enumerate(roles):
        w=640-i*70; x=(800-w)/2
        b+=box(x,y,w,48,col,"",r=8)
        b+=txt(x+16,y+30,name,WHITE,14.5,"700")
        b+=txt(x+w-16,y+30,desc,PALE,11.5,"400","end")
        y+=58
    return svg(800,y+8,b,"Workspace role hierarchy")
D["workspace-roles"]=d_roles

# 11) RLS flow
def d_rls():
    b=defs_arrow()
    b+=txt(400,30,"How row-level security filters data",NAVY,18,"700","middle")
    b+=box(70,70,220,70,BLUEL,"","",r=10)
    b+=txt(180,98,"RLS role filter",WHITE,14,"700","middle")
    b+=txt(180,118,"[Region] = \"West\"",PALE,12,"400","middle")
    b+=box(300,70,180,70,BLUE,"Dim_Region",r=10,fs=14)
    b+=box(510,70,220,70,NAVY,"","",r=10)
    b+=txt(620,98,"Fact_Sales",WHITE,14,"700","middle")
    b+=txt(620,118,"filtered via relationship",PALE,11,"400","middle")
    b+=arrow(290,105,300,105,BLUE)
    b+=arrow(480,105,510,105,BLUE)
    b+=txt(400,172,"Filter the dimension \u2014 the relationship propagates it to the fact automatically",MUTE,12.5,"400","middle")
    b+=f"<rect x='150' y='192' width='500' height='34' rx='6' fill='{PALE}' stroke='{WARN}' stroke-width='1'/>"
    b+=txt(400,214,"Gotcha: a Viewer in NO role sees ALL rows \u2014 RLS is not deny-by-default",WARN,11.5,"600","middle")
    return svg(800,240,b,"RLS filters a dimension and propagates to the fact table")
D["rls-flow"]=d_rls

# 12) Label propagation
def d_labels():
    b=defs_arrow()
    b+=txt(400,30,"Sensitivity label propagation",NAVY,18,"700","middle")
    stages=[("Lakehouse",BLUEL),("Semantic model",BLUE),("Report",NAVY),("Export (xlsx/pdf)",MUTE)]
    x=40
    for i,(name,col) in enumerate(stages):
        b+=box(x,70,165,56,col,name,r=9,fs=13.5)
        if i<3: b+=arrow(x+165,98,x+188,98,BLUE)
        x+=188
    b+=f"<rect x='40' y='150' width='688' height='36' rx='8' fill='{PALE}' stroke='{LINE}'/>"
    b+=txt(400,173,"\U0001F512 'Confidential' label + protection flows downstream automatically",NAVY,12.5,"600","middle")
    return svg(800,200,b,"Sensitivity label propagates downstream")
D["label-propagation"]=d_labels

# 13) Endorsement tiers
def d_endorse():
    b=defs_arrow()
    b+=txt(400,30,"Endorsement \u2014 trust signals",NAVY,18,"700","middle")
    tiers=[("Promoted","Any contributor can set \u2014 team-ready",BLUEL),
           ("Certified","Authorized reviewers \u2014 org gold standard",BLUE),
           ("Master data","Authoritative single source of truth",NAVY)]
    x=40
    for i,(name,desc,col) in enumerate(tiers):
        b+=box(x,66,230,80,col,"",r=10)
        b+=txt(x+115,98,name,WHITE,15,"700","middle")
        b+=txt(x+115,122,desc,PALE,11,"400","middle")
        if i<2: b+=arrow(x+230,106,x+250,106,BLUE)
        x+=250
    b+=txt(400,170,"Higher tiers rank higher in the OneLake catalog and search",MUTE,12,"400","middle")
    return svg(800,190,b,"Endorsement tiers promoted certified master data")
D["endorsement-tiers"]=d_endorse

# 14) Git flow
def d_git():
    b=defs_arrow()
    b+=txt(400,30,"Workspace Git integration",NAVY,18,"700","middle")
    b+=box(60,72,200,70,BLUEL,"","",r=10)
    b+=txt(160,100,"Author locally",WHITE,13.5,"700","middle")
    b+=txt(160,120,".pbip in Desktop",PALE,11,"400","middle")
    b+=box(300,72,200,70,BLUE,"","",r=10)
    b+=txt(400,100,"Git repo",WHITE,13.5,"700","middle")
    b+=txt(400,120,"Azure DevOps / GitHub",PALE,11,"400","middle")
    b+=box(540,72,200,70,NAVY,"","",r=10)
    b+=txt(640,100,"Fabric workspace",WHITE,13.5,"700","middle")
    b+=txt(640,120,"Sync / update",PALE,11,"400","middle")
    b+=arrow(260,98,300,98,BLUE); b+=arrow(500,98,540,98,BLUE)
    b+=arrow(540,126,300,126,MUTE)
    b+=txt(400,168,"Commit, branch, and sync report/model source with version control",MUTE,12,"400","middle")
    return svg(800,188,b,"Git integration author commit sync")
D["git-flow"]=d_git

# 15) Deployment pipelines
def d_pipelines():
    b=defs_arrow()
    b+=txt(400,30,"Deployment pipelines",NAVY,18,"700","middle")
    stages=[("Development","Author & iterate",BLUEL),("Test","Validate & review",BLUE),("Production","Live for users",NAVY)]
    x=90
    for i,(name,desc,col) in enumerate(stages):
        b+=box(x,66,180,74,col,"",r=10)
        b+=txt(x+90,98,name,WHITE,15,"700","middle")
        b+=txt(x+90,120,desc,PALE,11,"400","middle")
        if i<2: b+=arrow(x+180,103,x+210,103,BLUE)
        x+=210
    b+=txt(400,164,"Promote content stage to stage; deployment rules swap data sources / parameters",MUTE,12,"400","middle")
    return svg(800,184,b,"Deployment pipeline dev test prod")
D["deployment-pipelines"]=d_pipelines

# 16) Reusable assets
def d_assets():
    b=""
    b+=txt(400,28,"Reusable assets",NAVY,19,"700","middle")
    items=[(".pbip","Power BI project","Git-friendly source (TMDL/PBIR)",BLUE),
           (".pbit","Template","Structure & layout, no data",BLUEL),
           (".pbids","Data source file","Predefined connection",NAVY),
           ("Shared model","Published semantic model","One definition, many reports","#062338")]
    x=30
    for name,t,s,col in items:
        b+=box(x,60,182,92,col,"",r=10)
        b+=txt(x+91,90,name,WHITE,15,"700","middle")
        b+=txt(x+91,114,t,PALE,11.5,"600","middle")
        b+=txt(x+91,133,s,PALE,10.3,"400","middle")
        x+=190
    return svg(800,172,b,"pbip pbit pbids shared model reusable assets")
D["reusable-assets"]=d_assets

# 17) Evaluation context
def d_context():
    b=""
    b+=txt(400,28,"DAX evaluation context",NAVY,19,"700","middle")
    b+=box(50,60,330,150,BLUEL,"",r=12)
    b+=txt(215,88,"Row context",WHITE,15,"700","middle")
    b+=txt(215,110,"'current row' during iteration",PALE,11.5,"400","middle")
    b+=chip(80,126,270,30,"calculated columns \u00b7 SUMX / iterators",WHITE,NAVY,11)
    b+=chip(80,164,270,30,"one row at a time",WHITE,NAVY,11)
    b+=box(420,60,330,150,BLUE,"",r=12)
    b+=txt(585,88,"Filter context",WHITE,15,"700","middle")
    b+=txt(585,110,"'which rows are visible'",PALE,11.5,"400","middle")
    b+=chip(450,126,270,30,"slicers \u00b7 relationships \u00b7 CALCULATE",WHITE,NAVY,11)
    b+=chip(450,164,270,30,"the set the measure sees",WHITE,NAVY,11)
    b+=txt(400,232,"CALCULATE transitions row \u2192 filter context and overrides filters",MUTE,12.5,"400","middle")
    return svg(800,250,b,"Row context versus filter context in DAX")
D["eval-context"]=d_context

# 18) Calculation groups
def d_calcgroups():
    b=defs_arrow()
    b+=txt(400,30,"Calculation groups",NAVY,18,"700","middle")
    b+=txt(200,64,"Without",WARN,13,"700","middle")
    b+=chip(60,78,280,32,"Revenue, Revenue YTD, Revenue PY \u2026",WHITE,INK,11)
    b+=chip(60,116,280,32,"Cost, Cost YTD, Cost PY \u2026",WHITE,INK,11)
    b+=txt(200,168,"measures \u00d7 patterns = explosion",MUTE,11,"400","middle")
    b+=box(430,74,140,44,BLUE,"Base measures",r=8,fs=12.5)
    b+=box(430,140,140,44,NAVY,"Calc group",r=8,fs=13)
    b+=txt(500,204,"Current / YTD / PY",MUTE,11,"400","middle")
    b+=arrow(500,118,500,140,BLUE)
    b+=txt(690,110,"One set of",NAVY,12,"600","middle")
    b+=txt(690,128,"time patterns",NAVY,12,"600","middle")
    b+=txt(690,150,"applies to ALL",MUTE,11,"400","middle")
    b+=txt(690,166,"measures",MUTE,11,"400","middle")
    b+=arrow(575,162,650,150,BLUE,dash=True)
    return svg(800,224,b,"Calculation groups reduce measure sprawl")
D["calc-groups"]=d_calcgroups

# 19) Incremental refresh
def d_incremental():
    b=defs_arrow()
    b+=txt(400,30,"Incremental refresh",NAVY,18,"700","middle")
    b+=txt(400,54,"RangeStart / RangeEnd parameters partition the table by date",MUTE,12,"400","middle")
    # partitions
    x=60; labels=["2019","2020","2021","2022","2023"]
    for i,l in enumerate(labels):
        col=MUTE if i<4 else BLUE
        b+=box(x,80,120,54,col if i==4 else "#9fb0bf","",r=8)
        b+=txt(x+60,104,l,WHITE,14,"700","middle")
        b+=txt(x+60,123,("refresh" if i==4 else "archived"),PALE,10.5,"400","middle")
        x+=134
    b+=f"<rect x='46' y='72' width='548' height='70' rx='10' fill='none' stroke='{MUTE}' stroke-dasharray='5 4'/>"
    b+=txt(300,164,"Stored (archive) period \u2014 not refreshed",MUTE,11,"400","middle")
    b+=f"<rect x='596' y='72' width='140' height='70' rx='10' fill='none' stroke='{BLUE}' stroke-width='2'/>"
    b+=txt(666,164,"Incremental window",BLUE,11,"600","middle")
    b+=txt(400,196,"Only recent partitions refresh \u2014 requires query folding on the source",MUTE,12,"400","middle")
    return svg(800,214,b,"Incremental refresh partitions with RangeStart RangeEnd")
D["incremental-refresh"]=d_incremental

# 20) Query folding
def d_folding():
    b=defs_arrow()
    b+=txt(400,30,"Query folding",NAVY,18,"700","middle")
    b+=box(60,70,180,60,BLUEL,"Power Query steps",r=10,fs=13.5)
    b+=box(320,70,180,60,BLUE,"Folded to SQL",r=10,fs=13.5)
    b+=box(580,70,160,60,NAVY,"Source database",r=10,fs=13.5)
    b+=arrow(240,100,320,100,BLUE); b+=arrow(500,100,580,100,BLUE)
    b+=txt(400,158,"Transforms are pushed to the source \u2014 less data moved, faster refresh",MUTE,12.5,"400","middle")
    b+=f"<rect x='150' y='178' width='500' height='32' rx='6' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(400,199,"Break folding (e.g. some custom steps) \u2192 all rows pulled locally = slow",WARN,11.5,"600","middle")
    return svg(800,224,b,"Query folding pushes transforms to the source")
D["query-folding"]=d_folding

# 21) Composite model
def d_composite():
    b=defs_arrow()
    b+=txt(400,30,"Composite model",NAVY,18,"700","middle")
    b+=box(300,64,200,50,NAVY,"One semantic model",r=10,fs=13.5)
    modes=[("Import",BLUEL,120,190),("Direct Lake",BLUE,320,190),("DirectQuery",MUTE,520,190),("Dual",OK,320,258)]
    for name,col,mx,my in [("Import",BLUEL,110,180),("Direct Lake",BLUE,330,180),("DirectQuery",MUTE,550,180)]:
        b+=box(mx,my,150,46,col,name,r=8,fs=13)
        b+=arrow(mx+75,my,400,114,MUTE,dash=True)
    b+=box(330,250,150,44,OK,"Dual",r=8,fs=13)
    b+=txt(405,284,"(Import + DirectQuery)",WHITE,10,"400","middle")
    b+=txt(400,318,"Mix storage modes per table; Dual lets the engine pick the cheapest path",MUTE,12,"400","middle")
    return svg(800,336,b,"Composite model mixes storage modes")
D["composite-model"]=d_composite

# 22) XMLA endpoint
def d_xmla():
    b=defs_arrow()
    b+=txt(400,30,"XMLA endpoint",NAVY,18,"700","middle")
    tools=["Tabular Editor","SSMS","DAX Studio","ALM Toolkit"]
    y=64
    for i,t in enumerate(tools):
        b+=chip(60,y+i*40,180,32,t,PALE,NAVY,12)
    b+=box(300,96,150,70,BLUE,"XMLA endpoint",r=10,fs=13.5)
    b+=box(520,96,210,70,NAVY,"","",r=10)
    b+=txt(625,124,"Semantic model",WHITE,14,"700","middle")
    b+=txt(625,144,"deploy / manage / refresh",PALE,10.5,"400","middle")
    for i in range(4):
        b+=arrow(240,y+i*40+16,300,131,MUTE)
    b+=arrow(450,131,520,131,BLUE)
    b+=f"<rect x='60' y='236' width='670' height='32' rx='6' fill='{PALE}' stroke='{WARN}'/>"
    b+=txt(395,257,"Read-only by default \u2014 a capacity admin must enable read-write",WARN,11.5,"600","middle")
    return svg(800,284,b,"XMLA endpoint external tools deploy semantic models")
D["xmla-endpoint"]=d_xmla

# 23) Impact analysis / lineage
def d_impact():
    b=defs_arrow()
    b+=txt(400,30,"Impact analysis & lineage",NAVY,18,"700","middle")
    b+=box(60,90,150,54,BLUEL,"Lakehouse",r=9,fs=13)
    b+=box(250,90,150,54,BLUE,"Semantic model",r=9,fs=12.5)
    b+=box(440,55,150,48,NAVY,"Report A",r=9,fs=13)
    b+=box(440,120,150,48,NAVY,"Report B",r=9,fs=13)
    b+=box(630,120,140,48,"#062338","Dashboard",r=9,fs=12.5)
    b+=arrow(210,117,250,117,MUTE)
    b+=arrow(400,110,440,84,MUTE); b+=arrow(400,120,440,140,MUTE)
    b+=arrow(590,144,630,144,MUTE)
    b+=txt(400,200,"See every downstream item a change affects before you make it",MUTE,12,"400","middle")
    return svg(800,220,b,"Impact analysis and lineage downstream dependencies")
D["impact-analysis"]=d_impact

# 24) Ingest paths
def d_ingest():
    b=defs_arrow()
    b+=txt(400,30,"Ways to ingest into a lakehouse",NAVY,18,"700","middle")
    paths=[("Upload","drag & drop files",BLUEL),("Dataflows Gen2","Power Query, low-code",BLUE),
           ("Pipelines","Copy activity, orchestrate",NAVY),("Notebooks","Spark / PySpark",BLUEL),
           ("Shortcuts","reference, no copy",BLUE)]
    x=30
    for name,s,col in paths:
        b+=box(x,64,140,64,col,"",r=9)
        b+=txt(x+70,92,name,WHITE,12.8,"700","middle")
        b+=txt(x+70,111,s,PALE,10,"400","middle")
        b+=arrow(x+70,128,x+70,150,MUTE)
        x+=150
    b+=box(120,152,560,44,"#062338","Lakehouse \u2014 Tables (Delta) + Files",r=10,fs=14)
    return svg(800,212,b,"Ingestion paths into a lakehouse")
D["ingest-paths"]=d_ingest

# 25) Views/functions/procs
def d_objects():
    b=""
    b+=txt(400,28,"Persistent warehouse objects",NAVY,19,"700","middle")
    items=[("View","Saved SELECT","Always current, reusable logic",BLUEL),
           ("Stored procedure","Runs T-SQL steps","Parameterized ETL / DML",BLUE),
           ("Function","Returns a value/table","Reusable logic in queries",NAVY)]
    x=40
    for name,t,s,col in items:
        b+=box(x,60,240,92,col,"",r=10)
        b+=txt(x+120,92,name,WHITE,15,"700","middle")
        b+=txt(x+120,116,t,PALE,11.5,"600","middle")
        b+=txt(x+120,135,s,PALE,10.3,"400","middle")
        x+=248
    return svg(800,172,b,"Views stored procedures and functions")
D["persistent-objects"]=d_objects

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
