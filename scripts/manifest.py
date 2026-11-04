"""Print every 2026 race the site covers: id chamber state district nbc_path."""
SEATS={'AL':7,'AK':1,'AZ':9,'AR':4,'CA':52,'CO':8,'CT':5,'DE':1,'FL':28,'GA':14,'HI':2,'ID':2,'IL':17,'IN':9,'IA':4,'KS':4,'KY':6,'LA':6,'ME':2,'MD':8,'MA':9,'MI':13,'MN':8,'MS':4,'MO':8,'MT':2,'NE':3,'NV':4,'NH':2,'NJ':12,'NM':3,'NY':26,'NC':14,'ND':1,'OH':15,'OK':5,'OR':6,'PA':17,'RI':2,'SC':7,'SD':1,'TN':9,'TX':38,'UT':4,'VT':1,'VA':11,'WA':10,'WV':2,'WI':8,'WY':1}
N={'AL':'alabama','AK':'alaska','AZ':'arizona','AR':'arkansas','CA':'california','CO':'colorado','CT':'connecticut','DE':'delaware','FL':'florida','GA':'georgia','HI':'hawaii','ID':'idaho','IL':'illinois','IN':'indiana','IA':'iowa','KS':'kansas','KY':'kentucky','LA':'louisiana','ME':'maine','MD':'maryland','MA':'massachusetts','MI':'michigan','MN':'minnesota','MS':'mississippi','MO':'missouri','MT':'montana','NE':'nebraska','NV':'nevada','NH':'new-hampshire','NJ':'new-jersey','NM':'new-mexico','NY':'new-york','NC':'north-carolina','ND':'north-dakota','OH':'ohio','OK':'oklahoma','OR':'oregon','PA':'pennsylvania','RI':'rhode-island','SC':'south-carolina','SD':'south-dakota','TN':'tennessee','TX':'texas','UT':'utah','VT':'vermont','VA':'virginia','WA':'washington','WV':'west-virginia','WI':'wisconsin','WY':'wyoming'}
SENATE=['AL','AK','AR','CO','DE','FL','GA','ID','IL','IA','KS','KY','LA','ME','MA','MI','MN','MS','MT','NE','NH','NJ','NM','NC','OH','OK','OR','RI','SC','SD','TN','TX','VA','WV','WY']
SPECIAL={'FL','OH'}
GOV=['AL','AK','AZ','AR','CA','CO','CT','FL','GA','HI','ID','IL','IA','KS','ME','MD','MA','MI','MN','NE','NV','NH','NM','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','VT','WI','WY']
assert sum(SEATS.values())==435 and len(GOV)==36 and len(SENATE)==35
for st in SENATE:
    print(f"S-{st} senate {st} 0 "+("2026-special-elections/" if st in SPECIAL else "2026-elections/")+N[st]+"-senate-results")
for st in GOV:
    print(f"G-{st} governor {st} 0 2026-elections/{N[st]}-governor-results")
for st,n in SEATS.items():
    for d in range(1,n+1):
        dist=0 if n==1 else d
        print(f"H-{st}-{dist:02d} house {st} {dist} 2026-elections/{N[st]}-us-house-district-{d}-results")
