"""
make_starfields.py -- AI Galaxy Traveler, Phase 5
Two additional star populations in the SAME Sun-centred equatorial light-year
frame as the 100 ly catalogue:

  bright_stars()  -- ~45 REAL famous stars out to ~1300 ly (measured RA/Dec/dist)
  galaxy_stars()  -- a procedural Milky Way (exponential disk + 4 spiral arms +
                     central bulge) with the Sun in its real place (~26,700 ly
                     from the centre). Individual stars are synthetic; the
                     structure, scale and Sun position are real.
"""
import math, random

# --- equatorial Cartesian (Sun origin), x->RA0/Dec0, z->Dec+90 ---------------
def cart(ra_h, dec_deg, d):
    ra = math.radians(ra_h * 15.0); dec = math.radians(dec_deg)
    return (d*math.cos(dec)*math.cos(ra), d*math.cos(dec)*math.sin(ra), d*math.sin(dec))

SP_COLOR = {"O":"#9bb0ff","B":"#aabfff","A":"#cad7ff","F":"#f8f7ff","G":"#fff4ea",
            "K":"#ffd2a1","M":"#ffb56c"}
def sp_color(s): return SP_COLOR.get(s[0].upper(), "#ffffff")

# name, common, RA(h), Dec(deg), dist(ly), spectral
BRIGHT = [
    ("Aldebaran","Aldebaran",4.5987,16.509,65.3,"K5III"),
    ("Regulus","Regulus",10.139,11.967,79.3,"B8V"),
    ("Mizar","Mizar",13.399,54.925,83,"A2V"),
    ("Alkaid","Alkaid",13.792,49.313,104,"B3V"),
    ("Dubhe","Dubhe",11.062,61.751,123,"K0III"),
    ("Alioth","Alioth",12.900,55.960,81,"A1III"),
    ("Algol","Algol",3.136,40.956,90,"B8V"),
    ("Hamal","Hamal",2.119,23.462,66,"K1III"),
    ("Polaris","Polaris",2.530,89.264,433,"F7Ib"),
    ("Alphard","Alphard",9.460,-8.659,177,"K3II"),
    ("Spica","Spica",13.420,-11.161,250,"B1V"),
    ("Bellatrix","Bellatrix",5.418,6.350,250,"B2III"),
    ("Betelgeuse","Betelgeuse",5.919,7.407,548,"M2Iab"),
    ("Rigel","Rigel",5.242,-8.202,863,"B8Ia"),
    ("Saiph","Saiph",5.796,-9.670,650,"B0Ia"),
    ("Alnitak","Alnitak",5.679,-1.943,1260,"O9Ib"),
    ("Mintaka","Mintaka",5.533,-0.299,1200,"O9V"),
    ("Antares","Antares",16.490,-26.432,550,"M1.5Iab"),
    ("Shaula","Shaula",17.560,-37.104,570,"B1.5IV"),
    ("Hadar","Hadar",14.064,-60.373,390,"B1III"),
    ("Mimosa","Mimosa",12.795,-59.689,280,"B0.5III"),
    ("Acrux","Acrux",12.443,-63.099,320,"B0.5IV"),
    ("Gacrux","Gacrux",12.519,-57.113,88,"M3.5III"),
    ("Adhara","Adhara",6.977,-28.972,430,"B2II"),
    ("Naos","Naos",8.060,-40.003,1080,"O4If"),
    ("Miaplacidus","Miaplacidus",9.220,-69.717,113,"A2IV"),
    ("Suhail","Suhail",9.133,-43.433,545,"K4Ib"),
    ("Gamma Velorum","Regor",8.158,-47.337,1100,"WC8"),
    ("Atria","Atria",16.811,-69.028,391,"K2Ib"),
    ("Peacock","Peacock",20.427,-56.735,179,"B2IV"),
    ("Alnair","Alnair",22.137,-46.961,101,"B6V"),
    ("Diphda","Diphda",0.726,-17.987,96,"K0III"),
    ("Menkar","Menkar",3.038,4.090,250,"M1.5III"),
    ("Mirfak","Mirfak",3.405,49.861,510,"F5Ib"),
    ("Almach","Almach",2.065,42.330,390,"K3II"),
    ("Schedar","Schedar",0.675,56.537,228,"K0III"),
    ("Caph","Caph",0.153,59.150,54,"F2III"),
    ("Enif","Enif",21.736,9.875,690,"K2Ib"),
    ("Sadalsuud","Sadalsuud",21.525,-5.571,540,"G0Ib"),
    ("Markab","Markab",23.079,15.205,133,"B9III"),
    ("Scheat","Scheat",23.063,28.083,196,"M2II"),
    ("Alpheratz","Alpheratz",0.139,29.090,97,"B8IV"),
    ("Pleiades","Pleiades (Alcyone)",3.791,24.105,444,"B7III"),
    ("Algieba","Algieba",10.333,19.841,130,"K1III"),
    ("Zosma","Zosma",11.235,20.524,58,"A4V"),
]

def bright_stars():
    out = []
    for name, common, ra, dec, d, sp in BRIGHT:
        x, y, z = cart(ra, dec, d)
        out.append({"name": name, "common": common, "dist": round(d,1),
                    "x": round(x,1), "y": round(y,1), "z": round(z,1),
                    "color": sp_color(sp), "spectral": sp})
    return out

# --- procedural Milky Way ----------------------------------------------------
R_SUN = 26_700.0          # Sun's distance from Galactic Centre, ly
H_R   = 8_500.0           # disk radial scale length, ly
H_Z   = 350.0             # disk vertical scale height, ly
R_MAX = 50_000.0          # disk edge, ly
N_ARMS = 4
PITCH  = math.radians(12.5)

# galactic -> equatorial basis (GC at RA266.405/Dec-28.936, NGP at RA192.859/Dec27.128)
def _u(ra_deg, dec_deg):
    ra = math.radians(ra_deg); dec = math.radians(dec_deg)
    return (math.cos(dec)*math.cos(ra), math.cos(dec)*math.sin(ra), math.sin(dec))
def _cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def _norm(a):
    m=math.sqrt(sum(c*c for c in a)); return (a[0]/m,a[1]/m,a[2]/m)
E_GC = _u(266.405, -28.936)              # toward Galactic Centre  (galactic +x)
E_NGP = _u(192.859, 27.128)              # toward North Galactic Pole (galactic +z)
E_L90 = _norm(_cross(E_NGP, E_GC))       # toward l=90 (rotation dir, galactic +y)
E_NGP = _norm(_cross(E_GC, E_L90))       # re-orthogonalise +z

def _gal_to_eq(xg, yg, zg):              # galactic Cartesian -> equatorial ly
    return (xg*E_GC[0]+yg*E_L90[0]+zg*E_NGP[0],
            xg*E_GC[1]+yg*E_L90[1]+zg*E_NGP[1],
            xg*E_GC[2]+yg*E_L90[2]+zg*E_NGP[2])

def galaxy_stars(n=2500, seed=42):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        u = rng.random()
        if u < 0.16:                                  # central bulge
            r = min(rng.expovariate(1/3000.0), 6000.0)
            ct = rng.uniform(-1,1); ph = rng.uniform(0,2*math.pi)
            st = math.sqrt(1-ct*ct)
            X = r*st*math.cos(ph); Y = r*st*math.sin(ph); Z = r*ct*0.55
            comp = "bulge"; col = "#ffe2b0"
        else:                                         # disk (+ spiral arms)
            while True:
                r = rng.expovariate(1/H_R)
                if 1500.0 < r <= R_MAX: break
            if rng.random() < 0.55:                    # snap toward a spiral arm
                base = math.log(r/3000.0)/math.tan(PITCH)
                k = rng.randrange(N_ARMS)
                phi = base + 2*math.pi*k/N_ARMS + rng.gauss(0, 0.18)
                comp, col = "arm", "#dbe6ff"
            else:
                phi = rng.uniform(0, 2*math.pi); comp, col = "disk", "#c4d2ff"
            X = r*math.cos(phi); Y = r*math.sin(phi)
            Z = rng.gauss(0, H_Z)
        # galactocentric (GC origin, Sun at (R_SUN,0,0)) -> Sun-centred galactic
        xg, yg, zg = R_SUN - X, -Y, Z
        ex, ey, ez = _gal_to_eq(xg, yg, zg)
        out.append({"x": round(ex), "y": round(ey), "z": round(ez),
                    "d": round(math.sqrt(xg*xg+yg*yg+zg*zg)), "c": col, "comp": comp})
    return out

def gc_marker():
    ex, ey, ez = _gal_to_eq(R_SUN, 0.0, 0.0)
    return {"x": round(ex), "y": round(ey), "z": round(ez), "d": R_SUN}

if __name__ == "__main__":
    import json
    b = bright_stars(); g = galaxy_stars()
    json.dump(b, open("bright_stars.json","w"))
    json.dump(g, open("galaxy_stars.json","w"))
    print(f"bright_stars: {len(b)}  (e.g. Betelgeuse d={[s for s in b if s['name']=='Betelgeuse'][0]['dist']} ly)")
    print(f"galaxy_stars: {len(g)}; GC marker dist = {gc_marker()['d']:.0f} ly")
