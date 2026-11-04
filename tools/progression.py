"""Fifty permanent achievements and their equipable cosmetic rewards."""
EFFECT_NAMES=['Normal','Fire','Water','Ice','Rainbow','Lightning','Void','Confetti','Honey','Galaxy']
SKIN_NAMES=['Classic','Ember','Frost','Prism','Neon Wire','Obsidian','Honeycomb','Plasma','Marble']
AURA_NAMES=['None','Gold','Rainbow','Inferno','Tidal','Glacial','Nebula','Hive']
DIFFICULTY_NAMES=['Easy','Normal','Hard','Expert','Nightmare']
# name, metric, threshold, readable requirement
CATALOG=[
 ('FIRST CLEAR','lifetime lines',1,'Clear one line'),('TEN LINES','lifetime lines',10,'Clear 10 lifetime lines'),
 ('CHAIN REACTION','best combo',5,'Reach combo 5'),('FOUR AT ONCE','lifetime quads',1,'Clear four rows together'),
 ('SPIN ARTIST','lifetime spins',1,'Lock a T-spin'),('HIGH ROLLER','BEST SCORE',5000,'Score 5,000 points')]
GROUPS=[
 ('lifetime lines',[25,50,100,250,500,1000],['LINE ART','WELL TRAVELLED','CENTURY','STACK MASTER','LINE LEGEND','THOUSAND FLOW'],'Clear {} lifetime lines'),
 ('BEST SCORE',[10000,25000,50000,100000],['FIVE DIGITS','SCORE SURGE','SCORE LEGEND','SIX FIGURES'],'Score {:,} points'),
 ('best combo',[7,10,15,20],['CHAIN LIGHTNING','DOUBLE DIGITS','BEYOND LIMITS','CHAIN GOD'],'Reach combo {}'),
 ('lifetime quads',[5,10,25,50],['QUAD CREW','QUAD ENGINE','QUAD MASTER','QUAD LEGEND'],'Make {} four-line clears'),
 ('lifetime spins',[5,10,25,50],['SPIN DOCTOR','SPIN CYCLE','SPIN MASTER','SPIN LEGEND'],'Lock {} T-spins'),
 ('lifetime rotations',[25,100,250,1000,2500],['TURNING POINT','ROTATION STATION','TWISTED','ORBITAL','GYROSCOPE'],'Make {} successful rotations'),
 ('lifetime drops',[10,50,100,250,500],['DROP IN','DROP ZONE','HARD LANDING','GRAVITY PILOT','ORBITAL DROP'],'Make {} hard drops'),
 ('lifetime runs',[1,5,10,25,50],['NEW ARRIVAL','REGULAR','PERSISTENT','VETERAN','LIFER'],'Start {} runs'),
 ('max bees',[1,5,10],['BEE FRIEND','BUSY HIVE','FULL SWARM'],'Gather {} flying bees'),
 ('expert starts',[1],['EXPERT ENTRY'],'Start an Expert run'),('nightmare starts',[1],['FEARLESS'],'Start a Nightmare run'),
 ('rainbow lines',[10],['COLOR STORM'],'Clear 10 lines with Rainbow'),('beeswarm lines',[25],['POLLEN POWER'],'Clear 25 Bee Swarm lines')]
for metric,thresholds,names,pattern in GROUPS:
 for threshold,name in zip(thresholds,names):CATALOG.append((name,metric,threshold,pattern.format(threshold)))
assert len(CATALOG)==50

def achievement_id(metric,threshold):return next(i for i,r in enumerate(CATALOG,1) if r[1:3]==(metric,threshold))
SKIN_REQUIREMENTS={2:1,3:2,4:3,5:achievement_id('lifetime lines',25),6:achievement_id('lifetime lines',100),7:achievement_id('max bees',5),8:achievement_id('BEST SCORE',25000),9:achievement_id('lifetime rotations',1000)}
AURA_REQUIREMENTS={1:4,2:6,3:achievement_id('lifetime quads',5),4:achievement_id('lifetime lines',50),5:achievement_id('lifetime spins',5),6:achievement_id('best combo',10),7:achievement_id('max bees',10)}
EFFECT_REQUIREMENTS={6:achievement_id('best combo',7),7:achievement_id('lifetime spins',10),8:achievement_id('lifetime drops',50),9:achievement_id('max bees',1),10:achievement_id('BEST SCORE',10000)}
rewards={i:'Achievement badge' for i in range(1,51)}
for mapping,names,kind in [(SKIN_REQUIREMENTS,SKIN_NAMES,' blocks'),(AURA_REQUIREMENTS,AURA_NAMES,' aura'),(EFFECT_REQUIREMENTS,EFFECT_NAMES,' clears')]:
 for option,aid in mapping.items():rewards[aid]=names[option-1 if kind!=' aura' else option]+kind
rewards[5]='Spin Artist title'
ACHIEVEMENTS=[(row[0],row[3],rewards[i]) for i,row in enumerate(CATALOG,1)]
