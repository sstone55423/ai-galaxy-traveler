"""
build_catalog.py  --  AI Galaxy Traveler, Phase 1
Builds a curated catalogue of real stars within ~100 light-years of the Sun.
Outputs: stars_100ly.csv, stars_100ly.json
Positions are real measured values (Hipparcos / Gaia DR3 / RECONS). This is a
curated subset (nearest systems + notable named / planet-host stars), not a
complete census. Frame: equatorial Cartesian, Sun at origin, units = light-years.
    x = d*cos(Dec)*cos(RA); y = d*cos(Dec)*sin(RA); z = d*sin(Dec)   (RA in hours)
"""
import csv, json, math, os

STAR_DATA = [
    ("Sun", "Sun", 0.0, 0.0, 0.0, "G2V", -26.7, True, "sun"),
    ("Proxima Centauri", "Proxima Centauri", 14.4956, -62.6794, 4.246, "M5.5Ve", 11.13, True, "planet-host"),
    ("Alpha Centauri A", "Rigil Kentaurus", 14.6601, -60.8340, 4.344, "G2V", 0.01, True, "named"),
    ("Alpha Centauri B", "Toliman", 14.6601, -60.8370, 4.344, "K1V", 1.33, True, "named"),
    ("Barnard's Star", "Barnard's Star", 17.9634, 4.6933, 5.963, "M4.0Ve", 9.53, True, "planet-host"),
    ("Wolf 359", "Wolf 359", 10.9385, 7.0144, 7.856, "M6.0V", 13.54, True, "nearest"),
    ("Lalande 21185", "Lalande 21185", 11.0556, 35.9698, 8.307, "M2.0V", 7.52, True, "planet-host"),
    ("Sirius A", "Sirius", 6.7525, -16.7161, 8.601, "A1V", -1.46, True, "named"),
    ("Sirius B", "Sirius B", 6.7525, -16.7161, 8.601, "DA2", 8.44, True, "white-dwarf"),
    ("Luyten 726-8 A", "BL Ceti", 1.6492, -17.9572, 8.728, "M5.5V", 12.54, False, "nearest"),
    ("Luyten 726-8 B", "UV Ceti", 1.6492, -17.9572, 8.728, "M6.0V", 12.99, False, "nearest"),
    ("Ross 154", "Ross 154", 18.8311, -23.8367, 9.706, "M3.5Ve", 10.43, False, "nearest"),
    ("Ross 248", "Ross 248", 23.6979, 44.1772, 10.300, "M5.0V", 12.29, False, "nearest"),
    ("Epsilon Eridani", "Ran", 3.5483, -9.4583, 10.475, "K2V", 3.73, True, "planet-host"),
    ("Lacaille 9352", "Lacaille 9352", 23.0983, -35.8531, 10.742, "M0.5V", 7.34, True, "planet-host"),
    ("Ross 128", "Ross 128", 11.7975, 0.8003, 11.007, "M4.0V", 11.13, True, "planet-host"),
    ("EZ Aquarii A", "EZ Aquarii", 22.6431, -15.2961, 11.103, "M5.0V", 13.33, False, "nearest"),
    ("61 Cygni A", "61 Cygni A", 21.1075, 38.7508, 11.403, "K5.0V", 5.21, True, "named"),
    ("61 Cygni B", "61 Cygni B", 21.1100, 38.7419, 11.403, "K7.0V", 6.03, True, "named"),
    ("Procyon A", "Procyon", 7.6550, 5.2250, 11.464, "F5IV-V", 0.34, True, "named"),
    ("Procyon B", "Procyon B", 7.6550, 5.2250, 11.464, "DQZ", 10.70, True, "white-dwarf"),
    ("Struve 2398 A", "Gliese 725 A", 18.7128, 59.6281, 11.525, "M3.0V", 8.90, False, "nearest"),
    ("Struve 2398 B", "Gliese 725 B", 18.7128, 59.6281, 11.525, "M3.5V", 9.69, False, "nearest"),
    ("Groombridge 34 A", "GX Andromedae", 0.3069, 44.0228, 11.624, "M1.5V", 8.08, True, "planet-host"),
    ("Groombridge 34 B", "GQ Andromedae", 0.3069, 44.0231, 11.624, "M3.5V", 11.06, False, "nearest"),
    ("DX Cancri", "DX Cancri", 8.4972, 26.7767, 11.680, "M6.5V", 14.78, False, "nearest"),
    ("Tau Ceti", "Tau Ceti", 1.7344, -15.9375, 11.912, "G8.5V", 3.50, True, "planet-host"),
    ("Epsilon Indi A", "Epsilon Indi", 22.0575, -56.7858, 11.867, "K5Ve", 4.69, True, "planet-host"),
    ("GJ 1061", "GJ 1061", 3.5994, -44.5108, 11.984, "M5.5V", 13.09, True, "planet-host"),
    ("YZ Ceti", "YZ Ceti", 1.2089, -16.9939, 12.132, "M4.5V", 12.02, True, "planet-host"),
    ("Luyten's Star", "Gliese 273", 7.4569, 5.2253, 12.348, "M3.5V", 9.86, True, "planet-host"),
    ("Teegarden's Star", "Teegarden's Star", 2.8831, 16.8797, 12.497, "M7.0V", 15.40, True, "planet-host"),
    ("SCR 1845-6357", "SCR 1845-6357", 18.7503, -63.9583, 12.571, "M8.5V", 17.40, False, "nearest"),
    ("Kapteyn's Star", "Kapteyn's Star", 5.1947, -45.0181, 12.832, "sdM1", 8.85, True, "planet-host"),
    ("Lacaille 8760", "AX Microscopii", 21.2881, -38.8672, 12.945, "M0.0V", 6.69, True, "nearest"),
    ("Kruger 60 A", "Kruger 60 A", 22.4667, 57.6969, 13.149, "M3.0V", 9.79, False, "nearest"),
    ("Kruger 60 B", "Kruger 60 B", 22.4667, 57.6969, 13.149, "M4.0V", 11.41, False, "nearest"),
    ("DEN 1048-3956", "DEN 1048-3956", 10.8033, -39.9392, 13.169, "M8.5V", 17.39, False, "nearest"),
    ("Ross 614 A", "Gliese 234 A", 6.4900, -2.8264, 13.349, "M4.5V", 11.15, False, "nearest"),
    ("Wolf 1061", "Gliese 628", 16.5050, -12.6614, 14.050, "M3.0V", 10.07, True, "planet-host"),
    ("Van Maanen's Star", "Van Maanen 2", 0.8197, 5.3897, 14.066, "DZ8", 12.38, True, "white-dwarf"),
    ("Gliese 1", "Gliese 1", 0.0903, -37.3575, 14.170, "M1.5V", 8.55, False, "nearest"),
    ("Wolf 424 A", "Wolf 424", 12.5553, 9.0114, 14.312, "M5.5V", 13.18, False, "nearest"),
    ("TZ Arietis", "Gliese 83.1", 2.0028, 13.0506, 14.591, "M4.5V", 12.27, False, "nearest"),
    ("Gliese 687", "Gliese 687", 17.6072, 68.3589, 14.793, "M3.0V", 9.17, True, "planet-host"),
    ("LHS 292", "LHS 292", 10.8033, -11.2647, 14.805, "M6.5V", 15.73, False, "nearest"),
    ("Gliese 674", "Gliese 674", 17.4783, -46.8992, 14.809, "M3.0V", 9.38, True, "planet-host"),
    ("Gliese 1245 A", "Gliese 1245 A", 19.8981, 44.4250, 14.812, "M5.5V", 13.46, False, "nearest"),
    ("LP 145-141", "Gliese 440", 11.7619, -64.8425, 15.060, "DQ6", 11.50, True, "white-dwarf"),
    ("GJ 1002", "GJ 1002", 0.1119, -7.5350, 15.313, "M5.5V", 13.76, True, "planet-host"),
    ("Gliese 876", "Ross 780", 22.8881, -14.2625, 15.238, "M3.5V", 10.17, True, "planet-host"),
    ("LHS 288", "Luyten 143-23", 10.7422, -61.2003, 15.610, "M5.5V", 13.92, False, "nearest"),
    ("Gliese 412 A", "Gliese 412 A", 11.0925, 43.5267, 15.832, "M1.0V", 8.77, False, "nearest"),
    ("Gliese 412 B", "WX Ursae Majoris", 11.0925, 43.5236, 15.832, "M6.0V", 14.43, False, "nearest"),
    ("Groombridge 1618", "Gliese 380", 10.1897, 49.4669, 15.890, "K7.0V", 6.59, True, "named"),
    ("AD Leonis", "Gliese 388", 10.3272, 19.8700, 15.942, "M3.0V", 9.32, True, "named"),
    ("Gliese 832", "Gliese 832", 21.5603, -49.0089, 16.163, "M1.5V", 8.66, True, "planet-host"),
    ("Gliese 682", "Gliese 682", 17.6181, -44.3094, 16.327, "M4.0V", 10.96, False, "nearest"),
    ("40 Eridani A", "Keid", 4.2553, -7.6528, 16.335, "K0.5V", 4.43, True, "planet-host"),
    ("40 Eridani B", "Keid B", 4.2553, -7.6528, 16.335, "DA4", 9.52, True, "white-dwarf"),
    ("40 Eridani C", "Keid C", 4.2553, -7.6531, 16.335, "M4.5V", 11.17, False, "nearest"),
    ("EV Lacertae", "Gliese 873", 22.7806, 44.3331, 16.467, "M3.5V", 10.09, False, "nearest"),
    ("70 Ophiuchi A", "70 Ophiuchi", 18.0922, 2.5006, 16.587, "K0V", 4.03, True, "named"),
    ("70 Ophiuchi B", "70 Ophiuchi B", 18.0922, 2.5000, 16.587, "K5V", 6.00, False, "named"),
    ("Altair", "Altair", 19.8464, 8.8683, 16.730, "A7V", 0.76, True, "named"),
    ("Gliese 1245 B", "Gliese 1245 B", 19.8981, 44.4253, 14.812, "M6.0V", 14.01, False, "nearest"),
    ("Gliese 581", "Gliese 581", 15.3231, -7.7228, 20.376, "M3.0V", 10.56, True, "planet-host"),
    ("Gliese 667 C", "Gliese 667 C", 17.3164, -34.9986, 23.620, "M1.5V", 10.22, True, "planet-host"),
    ("Sigma Draconis", "Alsafi", 19.6053, 69.6611, 18.798, "K0V", 4.67, True, "named"),
    ("36 Ophiuchi A", "36 Ophiuchi", 17.2581, -26.6006, 19.494, "K2V", 5.07, True, "named"),
    ("82 Eridani", "82 G. Eridani", 3.3322, -43.0697, 19.710, "G8V", 4.26, True, "planet-host"),
    ("Delta Pavonis", "Delta Pavonis", 20.1453, -66.1819, 19.920, "G8IV", 3.56, True, "named"),
    ("Eta Cassiopeiae A", "Achird", 0.8181, 57.8156, 19.420, "G0V", 3.45, True, "named"),
    ("HR 8832", "Gliese 892", 23.2225, 57.1697, 21.354, "K3V", 5.57, True, "planet-host"),
    ("Gliese 570 A", "Gliese 570", 14.9961, -21.0667, 19.327, "K4V", 5.72, False, "named"),
    ("EQ Pegasi A", "EQ Pegasi", 23.5319, 19.9342, 20.400, "M4.0V", 10.30, False, "nearest"),
    ("Xi Bootis A", "Xi Bootis", 14.8567, 19.1006, 21.890, "G7V", 4.55, True, "named"),
    ("Mu Cassiopeiae", "Marfak", 1.1392, 54.9181, 24.600, "G5VI", 5.17, True, "named"),
    ("Beta Hydri", "Beta Hydri", 0.4292, -77.2542, 24.330, "G2IV", 2.80, True, "named"),
    ("107 Piscium", "107 Piscium", 1.7050, 20.2722, 24.360, "K1V", 5.24, False, "named"),
    ("Vega", "Vega", 18.6156, 38.7836, 25.040, "A0V", 0.03, True, "named"),
    ("Fomalhaut", "Fomalhaut", 22.9608, -29.6222, 25.130, "A3V", 1.16, True, "planet-host"),
    ("TW Piscis Austrini", "Fomalhaut B", 22.9347, -32.3464, 24.980, "K4Ve", 6.48, False, "named"),
    ("61 Virginis", "61 Virginis", 13.3067, -18.2978, 27.840, "G6V", 4.74, True, "planet-host"),
    ("Beta Comae Berenices", "Beta Comae", 13.1981, 27.8783, 29.950, "G0V", 4.26, True, "named"),
    ("Zeta Tucanae", "Zeta Tucanae", 0.3347, -64.8742, 28.010, "F9.5V", 4.23, True, "named"),
    ("Chara", "Beta Canum Venaticorum", 12.5622, 41.3578, 27.630, "G0V", 4.26, True, "named"),
    ("Groombridge 1830", "Groombridge 1830", 11.8825, 37.7186, 29.700, "G8V", 6.42, True, "named"),
    ("Gliese 436", "Gliese 436", 11.7036, 26.7064, 31.800, "M2.5V", 10.61, True, "planet-host"),
    ("Pollux", "Pollux", 7.7553, 28.0264, 33.780, "K0III", 1.14, True, "planet-host"),
    ("Denebola", "Beta Leonis", 11.8178, 14.5719, 35.900, "A3V", 2.11, True, "named"),
    ("Arcturus", "Arcturus", 14.2611, 19.1825, 36.700, "K1.5III", -0.05, True, "giant"),
    ("Gamma Leporis", "Gamma Leporis", 5.7444, -22.4481, 29.300, "F6V", 3.59, False, "named"),
    ("p Eridani A", "p Eridani", 1.6650, -56.1986, 26.640, "K2V", 5.76, False, "named"),
    ("12 Ophiuchi", "12 Ophiuchi", 16.6128, -2.2256, 31.900, "K2V", 5.77, False, "named"),
    ("54 Piscium", "54 Piscium", 0.9656, 21.2436, 36.200, "K0.5V", 5.88, True, "planet-host"),
    ("Upsilon Andromedae", "Titawin", 1.6128, 41.4056, 44.000, "F8V", 4.10, True, "planet-host"),
    ("47 Ursae Majoris", "Chalawan", 10.9925, 40.4314, 45.900, "G1V", 5.03, True, "planet-host"),
    ("55 Cancri A", "Copernicus (55 Cnc)", 8.8769, 28.3306, 41.060, "K0IV-V", 5.95, True, "planet-host"),
    ("Capella Aa", "Capella", 5.2781, 45.9981, 42.900, "G3III", 0.08, True, "giant"),
    ("Castor A", "Castor", 7.5764, 31.8883, 51.000, "A1V", 1.58, True, "named"),
    ("51 Pegasi", "Helvetios", 22.9581, 20.7686, 50.450, "G2IV", 5.49, True, "planet-host"),
    ("Tau Bootis A", "Tau Bootis", 13.7892, 17.4569, 51.000, "F7V", 4.50, True, "planet-host"),
    ("TRAPPIST-1", "TRAPPIST-1", 23.1083, -5.0414, 40.660, "M8.0V", 18.80, True, "planet-host"),
    ("LHS 1140", "LHS 1140", 0.7489, -15.2728, 48.900, "M4.5V", 14.18, True, "planet-host"),
    ("Gliese 1214", "Gliese 1214", 17.2517, 4.9636, 47.500, "M4.5V", 14.71, True, "planet-host"),
    ("HD 189733", "HD 189733", 20.0078, 22.7108, 64.500, "K1.5V", 7.65, True, "planet-host"),
    ("Gamma Pavonis", "Gamma Pavonis", 21.4419, -65.3661, 30.210, "F9V", 4.22, True, "named"),
    ("Pi3 Orionis", "Tabit", 4.8311, 6.9611, 26.320, "F6V", 3.19, True, "named"),
    ("Chi1 Orionis", "Chi1 Orionis", 5.9072, 20.2761, 28.260, "G0V", 4.39, False, "named"),
    ("HD 10647", "Gliese 65.1", 1.7283, -53.7411, 57.000, "F9V", 5.52, True, "planet-host"),
    ("Iota Persei", "Iota Persei", 3.1500, 49.6131, 34.400, "G0V", 4.05, False, "named"),
    ("Beta Aquilae", "Alshain", 19.9214, 6.4069, 44.700, "G8IV", 3.71, True, "named"),
    ("Gamma Cephei", "Errai", 23.6558, 77.6322, 44.900, "K1IV", 3.21, True, "planet-host"),
    ("Pi Mensae", "Pi Mensae", 5.6606, -80.4694, 59.700, "G0V", 5.65, True, "planet-host"),
    ("HD 192310", "Gliese 785", 20.2536, -27.0203, 28.700, "K2V", 5.73, True, "planet-host"),
    ("Eta Bootis", "Muphrid", 13.9111, 18.3975, 37.000, "G0IV", 2.68, True, "named"),
    ("HD 219134", "Gliese 892 (HD 219134)", 23.2261, 57.1697, 21.250, "K3V", 5.57, True, "planet-host"),
    ("Chi Draconis", "Chi Draconis", 18.3439, 72.7339, 26.300, "F7V", 3.57, False, "named"),
    ("Alpha Mensae", "Alpha Mensae", 6.1717, -74.7536, 33.100, "G7V", 5.09, False, "named"),
    ("HD 147513", "HD 147513", 16.4072, -39.1936, 42.000, "G1V", 5.37, True, "planet-host"),
    ("HD 69830", "HD 69830", 8.3097, -12.6364, 41.000, "K0V", 5.95, True, "planet-host"),
    ("Gamma Virginis A", "Porrima", 12.6942, -1.4494, 38.100, "F0V", 2.74, True, "named"),
    ("Beta Trianguli Australis", "Beta TrA", 15.9192, -63.4306, 40.400, "F1V", 2.83, False, "named"),
    ("Rasalhague", "Alpha Ophiuchi", 17.5822, 12.5600, 48.600, "A5III", 2.08, True, "named"),
    ("Gamma Serpentis", "Gamma Serpentis", 15.9442, 15.6619, 36.300, "F6V", 3.85, False, "named"),
    ("Theta Persei A", "Theta Persei", 2.7156, 49.2286, 36.600, "F8V", 4.10, False, "named"),
]

SPECTRAL_COLORS = {
    "O": "#9bb0ff", "B": "#aabfff", "A": "#cad7ff", "F": "#f8f7ff",
    "G": "#fff4ea", "K": "#ffd2a1", "M": "#ffb56c", "D": "#e8f0ff",
    "L": "#a8553a", "T": "#7a3a2a",
}

def equatorial_to_cartesian(ra_hours, dec_deg, dist_ly):
    ra = math.radians(ra_hours * 15.0)
    dec = math.radians(dec_deg)
    return (dist_ly*math.cos(dec)*math.cos(ra),
            dist_ly*math.cos(dec)*math.sin(ra),
            dist_ly*math.sin(dec))

def spectral_color(spectral):
    if not spectral:
        return "#ffffff"
    s = spectral[2:] if spectral[:2].lower() == "sd" else spectral
    return SPECTRAL_COLORS.get(s[0].upper(), "#ffffff") if s else "#ffffff"

def build():
    rows, seen, skipped = [], set(), []
    for (name, common, ra_h, dec, dist, spec, vmag, notable, cat) in STAR_DATA:
        if dist > 100.0:
            skipped.append((name, dist)); continue
        if name in seen:
            skipped.append((name, "dup")); continue
        seen.add(name)
        x, y, z = equatorial_to_cartesian(ra_h, dec, dist)
        rows.append({"name": name, "common_name": common,
                     "ra_hours": round(ra_h, 4), "dec_deg": round(dec, 4),
                     "dist_ly": round(dist, 3), "spectral": spec, "vmag": vmag,
                     "notable": bool(notable), "category": cat,
                     "x": round(x, 4), "y": round(y, 4), "z": round(z, 4),
                     "color": spectral_color(spec)})
    rows.sort(key=lambda r: r["dist_ly"])
    here = os.path.dirname(os.path.abspath(__file__))
    fn = ["name","common_name","ra_hours","dec_deg","dist_ly","spectral",
          "vmag","notable","category","x","y","z","color"]
    with open(os.path.join(here,"stars_100ly.csv"),"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fn); w.writeheader(); w.writerows(rows)
    with open(os.path.join(here,"stars_100ly.json"),"w",encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"Wrote {len(rows)} stars (skipped {len(skipped)})")
    return rows

if __name__ == "__main__":
    build()
