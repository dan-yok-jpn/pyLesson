
import matplotlib.pyplot as plt

class Section:

    def __init__(self, xys):
        self.n = len(xys)
        self.xs = [xy[0] for xy in xys]
        self.ys = [xy[1] for xy in xys]
        self.xmin = self.xs[ 0]
        self.xmax = self.xs[-1]
        self.i0 = 0

    def x2y(self, xx):
        if not (self.xmin <= xx and xx <= self.xmax):
            return 9999 # never select at min()
        x0 = self.xs[self.i0]
        for i in range(self.i0 + 1, self.n):
            x1 = self.xs[i]
            if x0 <= xx and xx <= x1:
                self.i0 = i - 1
                y0, y1 = self.ys[self.i0], self.ys[i]
                # not thinking about 0 divide
                return y0 + (xx - x0) * (y1 - y0) / (x1 - x0)
            x0 = x1

def cross_at(x0, x1, f0, f1, g0, g1):
    dx, df, dg = x1 - x0, f1 - f0, g1 - g0
    xc = x0 - (f0 - g0) * dx / (df - dg)
    return xc, f0 + df * (xc - x0) / dx

def pic_lower(xys_1, xys_2):
    sec_1, sec_2 = Section(xys_1), Section(xys_2)
    xset = sorted(set(sec_1.xs + sec_2.xs))

    x0 = xset[0]
    f0, g0 = sec_1.x2y(x0), sec_2.x2y(x0)
    d0 = f0 - g0
    xs, ys = [x0], [min([f0, g0])]
    for x1 in xset[1:]:
        f1, g1 = sec_1.x2y(x1), sec_2.x2y(x1)
        d1 = f1 - g1
        has_cross = (d0 >= 0 and d1 < 0) or (d0 <= 0 and d1 > 0)
        if has_cross:
            xc, yc = cross_at(x0, x1, f0, f1, g0, g1)
            xs, ys = xs + [xc], ys + [yc]
        xs, ys = xs + [x1], ys + [min([f1, g1])]
        x0, f0, g0, d0 = x1, f1, g1, d1

    plt.plot(sec_1.xs, sec_1.ys, label="$y_1$")
    plt.plot(sec_2.xs, sec_2.ys, label="$y_2$")
    plt.plot(   xs,       ys   , label="$y_L$")
    plt.legend()
    plt.show()

def read_file():
    sec1 = (
        (-49.73480359,6.303159753),
        (-21.27769236,6.287524206),
        (-19.03850758,4.665987476),
        (-18.80908201,3.832615221),
        (-18.65913688,3.758330455),
        (-18.3597274,3.835227569),
        (-18.20812473,3.752880828),
        (-17.49335054,3.846510652),
        (-14.52694877,3.867262542),
        (-14.18,3.903001532),
        (-14.17920138,3.934927692),
        (-14.07132261,3.98079629),
        (-8.459937767,6.448164443),
        (-7.381256975,6.50673196),
        (-1.462003138,6.571321462),
        (0.002913536,6.513506116),
        (0.715182214,6.232311915),
        (5.726577026,3.831320441),
        (8.737078308,3.824468434),
        (9.932541504,3.823866578),
        (12.50818477,2.656683865),
        (23.83029693,2.535928331),
        (23.98,2.543152036),
        (23.98055169,2.455626658),
        (24.24335281,2.447356959),
        (30.25486117,2.502600409),
        (30.76393702,2.504230928),
        (38.15006026,2.570688192),
        (38.29557036,2.581590323),
        (53.39396065,2.351901554),
        (69.21538914,2.316578719),
        (85.41775316,2.163349002),
        (101.6235874,2.02925643),
        (118.5366591,1.951935916),
        (134.3915757,1.761878088),
        (140.2809131,1.584492213),
        (140.4530555,1.546969227),
        (140.9894611,1.52422704),
        (146.8451232,1.534527231),
        (147.4233549,1.651180115),
        (147.5884422,1.781750229),
        (149.9706511,1.896304477),
        (150.0909704,1.861783292),
        (152.0181819,1.972018049),
        (154.093165,1.947321847),
        (157.641301,1.808600053),
        (158.6406243,1.899705036),
        (168.4903095,1.769948665),
        (179.1688193,1.705728255),
        (189.5972907,1.682086543),
        (198.8000195,1.677782219),
        (205.9427168,1.75144713),
        (211.8227677,2.070270283),
        (223.6374728,2.280706208),
        (226.2989052,1.228597121),
        (229.932248,1.1744723),
        (252.1175207,1.077550711),
        (270.8791307,1.331121728),
        (281.0044425,0.918184336),
        (294.2566708,0.127425935),
        (295.4188155,-0.022048075),
        (298.5229757,-0.807255863),
        (305.0272423,-1.985378072),
        (311.6141837,-2.054791094),
        (317.6132733,-2.253263959),
        (325.4012241,-2.572540804),
        (328.9197382,-2.768926166),
        (334.2155039,-1.927505808),
        (338.2038805,-1.234225653),
        (340.9590469,-1.173263034),
        (348.751,-0.340939136),
        (348.7564362,0.177085422),
        (350.0651337,0.938462003),
        (357.411,1.030504168),
        (357.4176668,1.292356764),
        (359.021,1.34252879),
        (359.0279978,1.489113302),
        (360.141,1.583420194),
        (360.1504996,1.698566272),
        (361.211,1.815651832),
        (361.2201655,1.998377677),
        (362.8258314,2.075010754),
        (367.131,2.005206357),
        (367.1318433,1.873988284),
        (369.3524756,1.869266844),
        (370.9057561,2.568623457),
        (371.7228144,2.67392686),
        (373.0440471,2.649019214),
        (374.701601,2.648604793),
        (377.0479018,3.83467456),
        (378.4686986,3.784810581),
        (383.9961132,6.364286994),
        (389.7545445,6.530062821),
        (392.4486551,6.533856572),
        (395.205817,6.451161419),
        (396.9151986,6.351142425),
        (400.1347629,6.036702995),
        (400.5333247,6.052073352),
        (402.8724059,5.994869359),
        (403.021,5.954470377),
        (403.0270675,5.915300224),
        (403.6810508,5.905462764),
        (403.881,5.937952102),
        (403.8851372,5.788177067),
        (404.5084336,5.695842212),
        (408.2915816,5.816374668),
        (408.475458,5.802661513),
        (413.7422616,5.723680705),
        (414.541,5.710202826),
        (414.5429484,5.686957385),
        (414.7941038,5.703578303),
        (416.0718592,5.695176038),
        (416.1746303,5.687264954),
        (417.1403142,5.611284302),
        (420.285866,4.882560336),
        (423.3956762,4.672212145),
        (423.8810048,4.742225908),
        (423.8937653,4.703196065),
        (429.2801096,4.524774083),
        (434.1039632,4.370968421)
    )

    sec2 = (
        (-21.5046699,6.423692902),
        (-19.24801544,4.757458195),
        (-19.05,3.880898752),
        (-19.04773554,3.37189498),
        (-18.75,3.320134248),
        (-18.71394879,3.857680316),
        (-13.920475,3.929485301),
        (-9.171367673,6.394243222),
        (0,6.667385987),
        (0.002241986,6.337232402),
        (0.253862149,6.388171561),
        (0.727812987,6.295438864),
        (5.74798674,3.887347715),
        (9.06198024,3.829733303),
        (10.04783993,3.851851275),
        (13.01720648,2.541862116),
        (21.3161738,2.369552904),
        (22.0219591,2.38994855),
        (25.82659105,2.983745699),
        (36.70252455,2.980343877),
        (48.72188358,2.613348062),
        (49.83649296,3.03930571),
        (52.44623022,2.1191227),
        (60.36924465,2.093352107),
        (71.40203006,2.056007571),
        (83.38766502,2.138797225),
        (92.90371481,2.258763462),
        (104.8216504,1.888706745),
        (113.4124815,1.866267858),
        (128.9355221,1.711022235),
        (138.335693,1.779556709),
        (146.1966372,1.739072627),
        (160.7290506,1.718099712),
        (165.8313836,1.750046477),
        (169.1176713,2.075136776),
        (175.3256656,1.066900011),
        (180.3259435,0.365732039),
        (185.6062263,-0.245200376),
        (189.6133921,-1.007581656),
        (194.389956,-0.853225774),
        (199.4145643,-0.346844458),
        (205.1173288,-0.167229631),
        (211.5951849,0.040190654),
        (216.6906032,0.090883665),
        (219.6133302,-0.202601149),
        (223.8176117,-0.399539747),
        (228.3825324,-0.810577955),
        (232.0953,-0.90675686),
        (236.1084029,-1.124018207),
        (242.0963392,-1.390408841),
        (247.2017669,-1.627352726),
        (250.6172656,-1.697909732),
        (255.0883125,-1.441823866),
        (259.4108207,-1.536502552),
        (264.2869519,-1.785999778),
        (269.0802893,-1.9299081),
        (275.9177661,-1.910241619),
        (280.8888207,-1.875510261),
        (285.9063154,-1.853273918),
        (290.9123274,-1.833133724),
        (295.8989902,-1.797624371),
        (300.8732219,-1.797534311),
        (305.9895326,-1.86684386),
        (310.881101,-1.974829395),
        (315.9119295,-1.871547517),
        (320.9138323,-1.829681327),
        (325.8743624,-1.802125644),
        (330.8821197,-1.572709683),
        (335.9137612,-1.658746966),
        (340.8957026,-1.647691483),
        (345.8746475,-1.39600449),
        (350.9152572,-1.527334907),
        (355.9190297,-1.45280515),
        (360.8933169,-1.355467094),
        (363.3729096,-0.311669598),
        (363.8907542,0.514178314),
        (366.3237035,0.497536495),
        (371.8237124,2.725100141),
        (372.72,2.848517652),
        (372.7214405,2.862977237),
        (372.94,3.322072844),
        (372.9536026,2.881555486),
        (374.7275866,3.085656527),
        (378.1197851,3.953021941),
        (382.5738038,4.021708264),
        (389.1567443,6.476949276),
        (390.84,6.470216998),
        (390.8912239,6.607910827),
        (396.0661241,6.453772999),
        (400.8706657,6.35908575),
        (400.97,6.387761439),
        (400.9744681,6.230081639),
        (403.34,6.214312459),
        (403.3412344,6.418373004),
        (404.34,6.36242992),
        (404.3426797,6.112689628),
        (405.04,6.149326192),
        (405.0716395,6.090178901),
        (412.99,6.109744693),
        (412.99543,6.217916462),
        (413.56,6.151326443),
        (413.5669607,6.371457499),
        (414.44,6.389489868),
        (414.4517172,6.286244337),
        (415.5950029,6.364078846)
    )
    return sec1, sec2

if __name__ == "__main__":

    xys_1, xys_2 = read_file() # instead of actual file reading
    pic_lower(xys_1, xys_2)