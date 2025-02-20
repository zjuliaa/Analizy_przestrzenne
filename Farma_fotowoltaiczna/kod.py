import arcpy
from arcpy import sa
#Ustawienie środowiska geoprzetwarzania oraz włączenie opcji nadpisywania się wyników
arcpy.env.workspace = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb"
arcpy.env.overwriteOutput = True

#warstwy wejściowe (wszystkie warstwy przed uruchomieniem algorytmu są połączone, jeżeli jest taka konieczność
# i przycięte do np. 200 metrowego bufora gminy): OT_SULN_L, swrs, skjzl, skdr, swieradow_zdroj, 
#ptwp, ptlz, PT_merge_cliped, dzialki, bubda, nmt_clip, dojazd

#---------------------------------------------------------------------------
#kryterium 1 -> odległość od rzek i zbiorników wodnych, jak najbliżej; 
#nieprzekraczalna strefa ochronna + bezpieczeństwo powyżej 100m
#---------------------------------------------------------------------------

# W celu połączenia warstw swrs i ptwp, należy zmienić geometrię swrs, zrobiono to poprzez 
#utworzenia bufora o wielkości 1 metr, nowa wynikowa warstwa, która jest poligonem
#jest przechowywana w geobazie
nowe_rzeki=arcpy.analysis.Buffer(
    in_features="swrs",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\nowe_rzeki",
    buffer_distance_or_field="1 Meters",
    line_side="FULL",
    line_end_type="ROUND",
    dissolve_option="NONE",
    dissolve_field=None,
    method="PLANAR"
)

#Obie warstwy są poligonami, połączenie warstw w celu otrzymania 
#warstwy zawierającej wszytskie zbiorniki wodne
woda = arcpy.management.Merge(
    inputs="nowe_rzeki;ptwp",
    output=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\woda",
    field_mappings='TERYT "TERYT" true true false 4 Text 0 0,First,#,nowe_rzeki,TERYT,0,4,ptwp,TERYT,0,4;LOKALNYID "LOKALNYID" true true false 254 Text 0 0,First,#,nowe_rzeki,LOKALNYID,0,254,ptwp,LOKALNYID,0,254;PRZES_NAZW "PRZES_NAZW" true true false 254 Text 0 0,First,#,nowe_rzeki,PRZES_NAZW,0,254,ptwp,PRZES_NAZW,0,254;WERSJA "WERSJA" true true false 21 Text 0 0,First,#,nowe_rzeki,WERSJA,0,21,ptwp,WERSJA,0,21;POCZ_WERSJ "POCZ_WERSJ" true true false 21 Text 0 0,First,#,nowe_rzeki,POCZ_WERSJ,0,21,ptwp,POCZ_WERSJ,0,21;OZNA_ZMIAN "OZNA_ZMIAN" true true false 254 Text 0 0,First,#,nowe_rzeki,OZNA_ZMIAN,0,254,ptwp,OZNA_ZMIAN,0,254;ZRO_DANYCH "ZRO_DANYCH" true true false 254 Text 0 0,First,#,nowe_rzeki,ZRO_DANYCH,0,254,ptwp,ZRO_DANYCH,0,254;KAT_ISTNIE "KAT_ISTNIE" true true false 254 Text 0 0,First,#,nowe_rzeki,KAT_ISTNIE,0,254,ptwp,KAT_ISTNIE,0,254;UWAGI "UWAGI" true true false 254 Text 0 0,First,#,nowe_rzeki,UWAGI,0,254,ptwp,UWAGI,0,254;INFO_DODAT "INFO_DODAT" true true false 254 Text 0 0,First,#,nowe_rzeki,INFO_DODAT,0,254,ptwp,INFO_DODAT,0,254;KOD10K "KOD10K" true true false 254 Text 0 0,First,#,nowe_rzeki,KOD10K,0,254,ptwp,KOD10K,0,254;SKROT_KART "SKROT_KART" true true false 254 Text 0 0,First,#,nowe_rzeki,SKROT_KART,0,254,ptwp,SKROT_KART,0,254;IDPRNG "IDPRNG" true true false 254 Text 0 0,First,#,nowe_rzeki,IDPRNG,0,254,ptwp,IDPRNG,0,254;POLOZENIE "POLOZENIE" true true false 254 Text 0 0,First,#,nowe_rzeki,POLOZENIE,0,254;SZEROKOSC "SZEROKOSC" true true false 8 Double 0 0,First,#,nowe_rzeki,SZEROKOSC,-1,-1;NAZWA "NAZWA" true true false 254 Text 0 0,First,#,nowe_rzeki,NAZWA,0,254,ptwp,NAZWA,0,254;RODZAJ "RODZAJ" true true false 254 Text 0 0,First,#,nowe_rzeki,RODZAJ,0,254,ptwp,RODZAJ,0,254;STAT_EKSPL "STAT_EKSPL" true true false 254 Text 0 0,First,#,nowe_rzeki,STAT_EKSPL,0,254;PRZEBIEG "PRZEBIEG" true true false 254 Text 0 0,First,#,nowe_rzeki,PRZEBIEG,0,254;CECHA_GEOM "CECHA_GEOM" true true false 254 Text 0 0,First,#,nowe_rzeki,CECHA_GEOM,0,254;IDMPHP "IDMPHP" true true false 254 Text 0 0,First,#,nowe_rzeki,IDMPHP,0,254,ptwp,IDMPHP,0,254;BUFF_DIST "BUFF_DIST" true true false 8 Double 0 0,First,#,nowe_rzeki,BUFF_DIST,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,nowe_rzeki,ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,nowe_rzeki,Shape_Length,-1,-1,ptwp,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,nowe_rzeki,Shape_Area,-1,-1,ptwp,Shape_Area,-1,-1;BDOT500 "BDOT500" true true false 254 Text 0 0,First,#,ptwp,BDOT500,0,254',
    add_source="NO_SOURCE_INFO"
)

#konwersja bufora gminy na linie, aby możliwe było użycie bufora jako granicy dla używanych funkcji
arcpy.management.FeatureToLine(
    in_features="swieradow_zdroj_Buffer",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\swieradow_zdroj_Buffer_line",
    cluster_tolerance=None,
    attributes="ATTRIBUTES"
)

#Obliczenie mapy odległości euklidesowych od warstwy "woda", wynik to raster przechowujący odległość
#od najbliższych obiketów w warstwie "woda"
EucDist_woda1 = arcpy.sa.EucDistance(
    in_source_data="woda",
    maximum_distance=None,
    cell_size=r"C:\Sem5\Analizy_przestrzenne\farma_foto\dane\nmt_clip",
    out_direction_raster=None,
    distance_method="PLANAR",
    in_barrier_data="swieradow_zdroj_Buffer_line",
    out_back_direction_raster=None
)
EucDist_woda1.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_woda1")

#Funkcja przekształca wartość rastra EucDist_woda1 na stopień przynależności za pomocą funkcji liniowej, 
#warstwa wyjściowa przyjmuje wartości od 0 do 1, min = 100, maksymalna odległość od wody, dla której
#przydatność jest równa 0, max = 100,1
Fuzzy1_woda = arcpy.sa.FuzzyMembership(
    in_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_woda1",
    fuzzy_function="LINEAR 100 100,1",
    hedge="NONE"
)
Fuzzy1_woda.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy1_woda")

#wyznaczenie maksymalnego zasięgu warstwy 
warstwa = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_woda1"
max_value = arcpy.GetRasterProperties_management(warstwa, "MAXIMUM")
max_value = float(max_value.getOutput(0).replace(",", "."))
max_value = math.floor(max_value * 10) / 10
fuzzy = f"LINEAR {max_value} 150"

#Funkcja przekształca wartości rastra EucDist_woda1 na stopień przynależności za pomocą funkcji liniowej,
#warstwa przyjmuje wartości od 0 do 1, min= wartość maksymalna zasięgu rastra EucDist_woda1, minimlana
#odległośc od zbiorników wodnych dla których przydatność wynosi 0,
#max = 150, maksymalna odległość od zbiorników wodnych, dla których przydatność to 1, powyżej tej 
#odległości przydatność zaczyna maleć 
Fuzzy2_woda = arcpy.sa.FuzzyMembership(
    in_raster="EucDist_woda1",
    fuzzy_function= fuzzy,
    hedge="NONE"
)
Fuzzy2_woda.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy2_woda")

#Połączenie warstw Fuzzy1_woda i Fuzzy2_woda, za pomocą operatora logicznego AND, 
#warstwa wynikowa to wynik realizacji kryterium 1
Fuzzy_woda = arcpy.sa.FuzzyOverlay(
    in_rasters="Fuzzy2_woda;Fuzzy1_woda",
    overlay_type="AND",
    gamma=0.9
)
Fuzzy_woda.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_woda")

#---------------------------------------------------------------------------
#kryterium 2 -> odległość od budynków mieszkalnych, jak najdalej, powyżej 150m 
#---------------------------------------------------------------------------

#Wybranie z warstwy z budynkami, tylko budynków mieszkalnych, ponieważ tylko ich dotyczy kryterium
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="bubda",
    selection_type="NEW_SELECTION",
    where_clause="FOBUD = 'budynki mieszkalne'",
    invert_where_clause=None
)

#Obliczenie mapy odległości euklidesowych od warstwy "bubda", wynik to raster przechowujący odległość
#od najbliższych obiektów w warstwie "bubda"
EucDist_budynki = arcpy.sa.EucDistance(
    in_source_data="bubda",
    maximum_distance=None,
    cell_size=r"C:\Sem5\Analizy_przestrzenne\farma_foto\dane\nmt_clip",
    out_direction_raster=None,
    distance_method="PLANAR",
    in_barrier_data="swieradow_zdroj_buffer_line",
    out_back_direction_raster=None
)
EucDist_budynki.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_budynki")

#Wyczyszczenie selekcji budynków mieszkalnych, nie jest już potrzebna
arcpy.management.SelectLayerByAttribute("bubda", "CLEAR_SELECTION")

#Wyznaczenie maksymalnego zasięgu rastra EucDist_budynki 
warstwa = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_budynki"
max_value = arcpy.GetRasterProperties_management(warstwa, "MAXIMUM")
max_value = float(max_value.getOutput(0).replace(",", "."))
max_value = math.floor(max_value * 10) / 10
fuzzy = f"LINEAR 150,1 {max_value}"

#Przeliczenie wartości EucDist_budynki na wartości od 0 do 1, wartości wyznaczają przydatność dla kryterium
#min = 150,1, maksymalna wartość od budynków mieszkalnych, dla której przydatność jest równa 0,
#max = maksymalna wartość zasięgu ratsra, minimalna odległość od budynków mieszkanych, dla której
#przydatność jest równa 1
Fuzzy_budynki = arcpy.sa.FuzzyMembership(
    in_raster="EucDist_budynki",
    fuzzy_function=fuzzy,
    hedge="NONE"
)
Fuzzy_budynki.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_budynki")

#---------------------------------------------------------------------------
# kryterium 3 -> pokrycie terenu, nie w lesie, powyżej 15m od lasu, optymalnie
#powyżej 100m od lasu
#---------------------------------------------------------------------------

#Wybranie z warstwy ptlz, obiketów las, ponieważ kryerium nie dotyczy całej warstwy
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="ptlz",
    selection_type="NEW_SELECTION",
    where_clause="RODZAJ = 'las'",
    invert_where_clause=None
)

#Obliczenie mapy odległości euklidesowych od warstwy "ptlz", wynik to raster przechowujący odległość
#od najbliższych obiketów las w warstwie "ptlz"
EucDist_las = arcpy.sa.EucDistance(
    in_source_data="ptlz",
    maximum_distance=None,
    cell_size=r"C:\Sem5\Analizy_przestrzenne\farma_foto\dane\nmt_clip",
    out_direction_raster=None,
    distance_method="PLANAR",
    in_barrier_data="swieradow_zdroj_buffer_line",
    out_back_direction_raster=None
)
EucDist_las.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\EucDist_las")

#Wyczyszczenie selekcji
arcpy.management.SelectLayerByAttribute("ptlz", "CLEAR_SELECTION")

#Przeliczenie wartości rastra EucDist_las na wartości od 0 do 1, min=15,1, maksymalna odległość, 
#dla której przydatność jest jeszcze równa 0, max = 100,1, minimalna odległość dla której przydatność
#jest równa 1
Fuzzy_las = arcpy.sa.FuzzyMembership(
    in_raster="EucDist_las",
    fuzzy_function="LINEAR 15,1 100,1",
    hedge="NONE"
)
Fuzzy_las.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_las")

#---------------------------------------------------------------------------
# kryterium 4 -> dostęp do dróg utwardzonych, jak największe zagęszczenie
#---------------------------------------------------------------------------

#Wybranie dróg utwardzonych z warstwy skjzl, w tym celu wybrano wszystkie obikety
# poza: drogami z gruntu naturalnego, tłuczenia, żwiru
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="skjzl",
    selection_type="NEW_SELECTION",
    where_clause="MATE_NAWIE NOT IN ('grunt naturalny', 'tłuczeń', 'żwir')",
    invert_where_clause=None
)

#Obliczenie gęstości dróg
gestosc_drog = arcpy.sa.KernelDensity(
    in_features="skjzl",
    population_field="NONE",
    cell_size=r"C:\Sem5\Analizy_przestrzenne\farma_foto\dane\nmt_clip",
    search_radius=None,
    area_unit_scale_factor="SQUARE_METERS",
    out_cell_values="DENSITIES",
    method="PLANAR",
    in_barriers=None
)
gestosc_drog.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\gestosc_drog")

#Wyczyszczenie selekcji dla warstwy skjzl
arcpy.management.SelectLayerByAttribute("skjzl", "CLEAR_SELECTION")

#Wyznaczenie wartości max dla FuzzyMembership
warstwa = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\gestosc_drog"
max_value = arcpy.GetRasterProperties_management(warstwa, "MAXIMUM")
max_value = float(max_value.getOutput(0).replace(",", "."))
max_val = max_value/2
max_value = math.floor(max_val * 1000) / 1000
fuzzy = f"LINEAR 0 {max_value}"

#Przekształcenie wartości rastra gestosc_drog, na wartości od 0 do 1, min=0, max = wartość średnia rastra
Fuzzy_gestosc = arcpy.sa.FuzzyMembership(
    in_raster="gestosc_drog",
    fuzzy_function= fuzzy,
    hedge="NONE"
)
Fuzzy_gestosc.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_gestosc")

#---------------------------------------------------------------------------
#kryterium 5 -> nachylenie stoków, optymalnie płasko, maksymalnie 10%
#---------------------------------------------------------------------------

#Obliczenie procentowego nachylenia stoków na podstawie warstwy nmt_clip
arcpy.ddd.Slope(
    in_raster="nmt_clip",
    out_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Slope",
    output_measurement="PERCENT_RISE",
    z_factor=1,
    method="PLANAR",
    z_unit="METER",
    analysis_target_device="GPU_THEN_CPU"
)

#Przeliczenie warstwy Slope na wartości 0-1, min= 10, minimalna wartość nachylenia, dla której przydatność
#wynosi 0, max=5, maksymalna wartość nachylenia, dla ktorej przydatność wynosi 1
Fuzzy_stoki = arcpy.sa.FuzzyMembership(
    in_raster="Slope",
    fuzzy_function="LINEAR 10 5",
    hedge="NONE"
)
Fuzzy_stoki.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_stoki")

# ---------------------------------------------------------------------------
# kryterium 6 -> dostęp światła słonecznego, optymalnie: stoki południowe (SW-SE) 
# ---------------------------------------------------------------------------

#Wyznaczenie kierunku nachylenia stoku w każdeym pikselu rastra na podstawie warstwy nmt_clip,
#wykorzystanie azymutów geodezyjnych pozwala uzyskać bardziej precyzyjne wyniki
aspect=arcpy.sa.Aspect(
    in_raster="nmt_clip",
    method="PLANAR",
    z_unit="METER",
    project_geodesic_azimuths="GEODESIC_AZIMUTHS",
    analysis_target_device="GPU_THEN_CPU"
)
aspect.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\aspect")

#Przeliczenie wartości aspect na wartości 0-1, min=270, minimalna wartość, od której przydatność
#przyjmuje wartość 0, max = 247,5, maksymalna wartość, dla której przydatność wynosi 1
Fuzzy1_slonce = arcpy.sa.FuzzyMembership(
    in_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\aspect",
    fuzzy_function="LINEAR 270 247,5",
    hedge="NONE"
)
Fuzzy1_slonce.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy1_slonce")

#Przeliczenie wartości aspect na wartości 0-1, min=90, maksymalna wartość, dla której przydatność
#przyjmuje wartość 0, max = 112,5, minimalna wartość, dla której przydatność wynosi 1
Fuzzy2_slonce = arcpy.sa.FuzzyMembership(
    in_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\aspect",
    fuzzy_function="LINEAR 90 112,5",
    hedge="NONE"
)
Fuzzy2_slonce.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy2_slonce")

#Połączenie warstw Fuzzy1_slonce, Fuzzy2_slonce za pomocą operatora logicznego AND
Fuzzy_slonce = arcpy.sa.FuzzyOverlay(
    in_rasters="Fuzzy2_slonce;Fuzzy1_slonce",
    overlay_type="AND",
    gamma=0.9
)
Fuzzy_slonce.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_slonce")

# ---------------------------------------------------------------------------
# kryterium 7 -> dobry dojazd od istotnych drogowych węzłów komunikacyjnych, 
#jak najkrótszy czas dojazdu
# ---------------------------------------------------------------------------

#Przycięte dane zawierają wartości NULL, należy jest zastąpić wartości 0, aby dalsze operacje 
#były możliwe
con_dojazd = arcpy.ia.Con(
    in_conditional_raster="dojazd_clip",
    in_true_raster_or_constant=0,
    in_false_raster_or_constant="dojazd_clip",
    where_clause="VALUE IS NULL"
)
con_dojazd.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\con_dojazd")

#Wyznaczenie maksymalnego zasięgu warstwy con_dojazd
warstwa = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\con_dojazd"
max_value = arcpy.GetRasterProperties_management(warstwa, "MAXIMUM")
max_value = float(max_value.getOutput(0).replace(",", "."))
max_value = math.floor(max_value * 10) / 10
fuzzy = f"LINEAR 0 {max_value}"

#Przeliczenie wartości warstwy na 0-1, min=0, maksymalna wartość, dla której przydatność to 0, 
#max=maksymalny zasięg warstwy, minimalna odległość, dla której przydatność wynosi 1
Fuzzy_dojazd = arcpy.sa.FuzzyMembership(
    in_raster="con_dojazd",
    fuzzy_function=fuzzy,
    hedge="NONE"
)
Fuzzy_dojazd.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\Fuzzy_dojazd")

# ---------------------------------------------------------------------------
#łączenie kryteriów
#takie same wagi
# ---------------------------------------------------------------------------

# Definicja zmiennej (wagi dla wszytskich kryteriów są takie same, dlatego należy podzielić
#1 na ilość kryteriów, czyli 7)
a = 1 / 7

# Przygotowanie tabeli wag
weighted_sum_table = (
    f"Fuzzy_woda VALUE {a};"
    f"Fuzzy_budynki VALUE {a};"
    f"Fuzzy_las VALUE {a};"
    f"Fuzzy_gestosc VALUE {a};"
    f"Fuzzy_stoki VALUE {a};"
    f"Fuzzy_slonce VALUE {a};"
    f"Fuzzy_dojazd VALUE {a}"
)

#Połączenie wynikowych rastrów dla wszytskich kryteriów, z uwzględnieniem takich samych wag
rozmyte = arcpy.ia.WeightedSum(in_weighted_sum_table=weighted_sum_table)
rozmyte.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte")

#Przygotowanie warstw dla kryterium 1., 2., 3., 5., w podejściu ostrym z zastosowaniem logiki Boola
woda_ostre = arcpy.ia.Con(
    in_conditional_raster="Fuzzy_woda",
    in_true_raster_or_constant=0,
    in_false_raster_or_constant=1,
    where_clause="VALUE = 0"
)
woda_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\woda_ostre")

las_ostre = arcpy.ia.Con(
    in_conditional_raster="Fuzzy_las",
    in_true_raster_or_constant=0,
    in_false_raster_or_constant=1,
    where_clause="VALUE = 0"
)
las_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\las_ostre")

stoki_ostre = arcpy.ia.Con(
    in_conditional_raster="Fuzzy_stoki",
    in_true_raster_or_constant=0,
    in_false_raster_or_constant=1,
    where_clause="VALUE = 0"
)
stoki_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\stoki_ostre")

budynki_ostre = arcpy.ia.Con(
    in_conditional_raster="Fuzzy_budynki",
    in_true_raster_or_constant=0,
    in_false_raster_or_constant=1,
    where_clause="VALUE = 0"
)
budynki_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\budynki_ostre")

#Połączenie warstwy zawierającej połączone wszytskie kryteria rozmyte z warstwami zawierającymi 
#wartości 0 i 1 dla podejscia ostrego
rozmyte_ostre = arcpy.sa.FuzzyOverlay(
    in_rasters="rozmyte;woda_ostre;budynki_ostre;las_ostre;stoki_ostre",
    overlay_type="AND",
    gamma=0.9
)
rozmyte_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte_ostre")

#---------------------------------------------------------------------------
# wyznaczenie obszarów spełniających kryterium przydatności (takie same wagi
#dla kryteriów), instrukcja zakłada przyjecie, że dany obszar spełnia kryterium, 
#jeżeli kryteria są spełnione na poziomie 80/90%, jednak przy takim założeniu
#obszarów spełniających kryetria jest bardzo mało, dlatego próg zaotsał obniżony
#do 60%
#---------------------------------------------------------------------------

#Wyznaczenie maksymalnej wartości rastra wynikowego
raster_path = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte_ostre"
max_value1 = arcpy.GetRasterProperties_management(raster_path, "MAXIMUM")
max_value1 = float(max_value1.getOutput(0).replace(",", "."))

#Wyznaczenie progu, dla jakiego teren można uznać za spełniający kryteria
threshold_value = max_value1 * 0.6
where_clause = f"VALUE >= {threshold_value}"

#Tereny przydatne przyjmują wartości 1, a tereny poniżej progu wartość 0
przydatnosc = arcpy.ia.Con(
    in_conditional_raster=raster_path,
    in_true_raster_or_constant=1,
    in_false_raster_or_constant=0,
    where_clause= where_clause
)
przydatnosc.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\przydatnosc")

#---------------------------------------------------------------------------
#łączenie kryteriów
#różne wagi -> wagi zostały wyznaczone za pomocą internetowego kalkulatora ahp
#proces zachodzi analogicznie jak dla takich samych wag
#---------------------------------------------------------------------------
weighted_sum_table = (
    f"Fuzzy_woda VALUE 0.038;"
    f"Fuzzy_budynki VALUE 0.03;"
    f"Fuzzy_las VALUE 0.11;"
    f"Fuzzy_gestosc VALUE 0.066;"
    f"Fuzzy_stoki VALUE 0.292;"
    f"Fuzzy_slonce VALUE 0.402;"
    f"Fuzzy_dojazd VALUE 0.062"
)

rozmyte_ahp = arcpy.ia.WeightedSum(in_weighted_sum_table=weighted_sum_table)
rozmyte_ahp.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte_ahp")

rozmyte_ostre_ahp = arcpy.sa.FuzzyOverlay(
    in_rasters="rozmyte_ahp;woda_ostre;budynki_ostre;las_ostre;stoki_ostre",
    overlay_type="AND",
    gamma=0.9
)
rozmyte_ostre_ahp.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte_ostre_ahp")

#---------------------------------------------------------------------------
# wyznaczenie obszarów spełniających kryterium przydatności(różne wagi)
#proces zachodzi analogicznie jak dla takich samych wag
#---------------------------------------------------------------------------

raster_path = r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\rozmyte_ostre_ahp"
max_value = arcpy.GetRasterProperties_management(raster_path, "MAXIMUM")
max_value = float(max_value.getOutput(0).replace(",", "."))

threshold_value = max_value * 0.6
where_clause = f"VALUE >= {threshold_value}"

przydatnosc_ahp = arcpy.ia.Con(
    in_conditional_raster=raster_path,
    in_true_raster_or_constant=1,
    in_false_raster_or_constant=0,
    where_clause= where_clause
)
przydatnosc_ahp.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\przydatnosc_ahp")


#---------------------------------------------------------------------------
# wybór działek spełniających kryteria (podejscie z takimi 
#samymi wagami) -> działka jest uznawana za obszar przydatny
# jeżeli conajmnej 60% powierzchni jest uznawane za obszary przydatne
#---------------------------------------------------------------------------

#Konwersja warstwy zawierającej informacje o spełnianiu kryteriów przez obszar
#na warstwę poligonową, gdzie obszary przydatne są łączone razem w poligony, 
#tak samo dzieje się z obszarami nie spełniającymi kryteriów
przydatnosc_poligon = arcpy.conversion.RasterToPolygon(
    in_raster="przydatnosc",
    out_polygon_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\przydatnosc_poligon",
    simplify="SIMPLIFY",
    raster_field="Value",
    create_multipart_features="SINGLE_OUTER_PART",
    max_vertices_per_feature=None
)

#Selekcja obszarów uznawanych za przydatne
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="przydatnosc_poligon",
    selection_type="NEW_SELECTION",
    where_clause="gridcode = 1",
    invert_where_clause=None
)

#Wykonanie intersekcji, czyli wybranie części działek, które częściowo lub całkowicie pokrywają się z obszarami przydatnymi
intersekcja = arcpy.analysis.Intersect(
    in_features="przydatnosc_poligon #;dzialki_clip #",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)

#Wyczyszczenie selekcji przydatnych poligonów
arcpy.management.SelectLayerByAttribute("przydatnosc_poligon", "CLEAR_SELECTION")

#Stworzenie tabeli zawierającej informacje jaką powierzchnie mają 
#obszary (dla danej działki) wybrane podczas procesu intersekcji
statystyki = arcpy.analysis.Statistics(
    in_table="intersekcja",
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja_Statistics1",
    statistics_fields="Shape_Area SUM",
    case_field="FID_dzialki_clip",
    concatenation_separator=""
)

#Stworzenie kopii warstwy zawierającej przycięte działki
arcpy.management.CopyFeatures(
    in_features="dzialki_clip",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dzialki_clip_copy",
    config_keyword="",
    spatial_grid_1=None,
    spatial_grid_2=None,
    spatial_grid_3=None
)

#Połączenie warstwy z przyciętymi działkiami z tabelą zawierającą informacje na temat pola 
#powierzchni wybranej podczas intersekcji
arcpy.management.AddJoin(
    in_layer_or_view="dzialki_clip",
    in_field="OBJECTID",
    join_table="intersekcja_Statistics1",
    join_field="FID_dzialki_clip",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

#Dodanie do warstwy z działkami kolumny ,,procent", obliczenie jaki procent powierzchni danej działki
#został wybrany w procesie intersekcji
arcpy.management.CalculateField(
    in_table="dzialki_clip",
    field="Procent",
    expression="None if !intersekcja_Statistics1.SUM_Shape_Area! == None or !dzialki_Clip.Shape_Area! == None else (!intersekcja_Statistics1.SUM_Shape_Area! / !dzialki_Clip.Shape_Area!) * 100",
    expression_type="PYTHON3",
    code_block="",
    field_type="DOUBLE",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

#Dodanie kolejnej kolumny, jezeli procent jest większy od 60%, w kolumnie zostaje wpisana 1, 
# w innym przypadku 0 (jezeli procent nie jest Null) 
arcpy.management.CalculateField(
    in_table="dzialki_clip",
    field="Przydatnosc",
    expression="""0 if !dzialki_clip.Procent! == None else (1 if !dzialki_clip.Procent! > 60 else 0)
""",
    expression_type="PYTHON3",
    code_block="",
    field_type="SHORT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

#Stworzenie nowej warstwy zawierającej tylko działki, których przynajmenj 60% powierzchni spełnia 
#kryetria
dobre_dzialki = arcpy.conversion.ExportFeatures(
    in_features="dzialki_clip",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki",
    where_clause="dzialki_clip.Przydatnosc = 1",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='NUMER_DZIA "NUMER_DZIA" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.NUMER_DZIA,0,253;NUMER_OBRE "NUMER_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.NUMER_OBRE,0,253;NUMER_JEDN "NUMER_JEDN" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.NUMER_JEDN,0,253;NAZWA_OBRE "NAZWA_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.NAZWA_OBRE,0,253;NAZWA_GMIN "NAZWA_GMIN" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.NAZWA_GMIN,0,253;POLE_EWIDE "POLE_EWIDE" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.POLE_EWIDE,0,253;KLASOUZYTK "KLASOUZYTK" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.KLASOUZYTK,0,253;GRUPA_REJE "GRUPA_REJE" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.GRUPA_REJE,0,253;DATA "DATA" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.DATA,0,253;ID_DZIALKI "ID_DZIALKI" true true false 254 Text 0 0,First,#,dzialki_clip,dzialki_clip.ID_DZIALKI,0,253;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dzialki_clip,dzialki_clip.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dzialki_clip,dzialki_clip.Shape_Area,-1,-1;Przydatnosc "Przydatnosc" true true false 2 Short 0 0,First,#,dzialki_clip,dzialki_clip.Przydatnosc,-1,-1;Procent "Procent" true true false 8 Double 0 0,First,#,dzialki_clip,dzialki_clip.Procent,-1,-1;OBJECTID "OBJECTID" false true false 4 Long 0 9,First,#,dzialki_clip,intersekcja_Statistics1.OBJECTID,-1,-1,dzialki_clip,intersekcja_Statistics1.OBJECTID,-1,-1;FID_dzialki_clip "FID_dzialki_clip" true true false 4 Long 0 0,First,#,dzialki_clip,intersekcja_Statistics1.FID_dzialki_clip,-1,-1,dzialki_clip,intersekcja_Statistics1.FID_dzialki_clip,-1,-1;FREQUENCY "FREQUENCY" true true false 4 Long 0 0,First,#,dzialki_clip,intersekcja_Statistics1.FREQUENCY,-1,-1,dzialki_clip,intersekcja_Statistics1.FREQUENCY,-1,-1;SUM_Shape_Area "SUM_Shape_Area" true true false 8 Double 0 0,First,#,dzialki_clip,intersekcja_Statistics1.SUM_Shape_Area,-1,-1,dzialki_clip,intersekcja_Statistics1.SUM_Shape_Area,-1,-1',
    sort_field=None
)

#Połączenie sąsiadujących działek
arcpy.cartography.AggregatePolygons(
    in_features="dobre_dzialki",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg1",
    aggregation_distance="0.1 Meters",
    minimum_area="0 SquareMeters",
    minimum_hole_size="0 SquareMeters",
    orthogonality_option="NON_ORTHOGONAL",
    barrier_features=None,
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg_Tbl1",
    aggregate_field=None
)

#Stworzenie warstwy zawierającej tylko działki, których powierzchnia jest równa lub większa niż
#20000 metrów kwadratowych
arcpy.conversion.ExportFeatures(
    in_features="dobre_dzialki_AggregatePolyg1",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\powierzchnia_dzialki",
    where_clause="Shape_Area >= 20000",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg1,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg1,Shape_Area,-1,-1',
    sort_field=None
)

#Stworzenie wokół wybranych w poprzednim kroku działek prostokąta otaczającego 
arcpy.management.MinimumBoundingGeometry(
    in_features="powierzchnia_dzialki",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki__MinimumBoundi",
    geometry_type="RECTANGLE_BY_WIDTH",
    group_option="NONE",
    group_field=None,
    mbg_fields_option="NO_MBG_FIELDS"
)

#Wyznaczenie szerokości działki, dodanie pól: wysokość i szerokość, za pomocą kursora 
#obliczenie szerokości i wysokości (różnica skrajnych współrzędnych)
input_fc = "dobre_dzialki__MinimumBoundi"
arcpy.AddField_management(input_fc, "Width", "DOUBLE")
arcpy.AddField_management(input_fc, "Height", "DOUBLE")
with arcpy.da.UpdateCursor(input_fc, ["SHAPE@", "Width", "Height"]) as cursor:
    for row in cursor:
        extent = row[0].extent
        width = extent.XMax - extent.XMin
        height = extent.YMax - extent.YMin
        row[1] = width  
        row[2] = height  
        cursor.updateRow(row)

#Dodanie do warstwy z wybranymi działkami informacji na temat ich szerokości i wysokości
arcpy.management.AddJoin(
    in_layer_or_view="powierzchnia_dzialki",
    in_field="OBJECTID",
    join_table="dobre_dzialki__MinimumBoundi",
    join_field="OBJECTID",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

#Stworzenie warstwy wynikowej zawierającej jedynie działki 
#spełniające wymaganie: szerokość obszaru>= 50 metrów
arcpy.conversion.ExportFeatures(
    in_features="powierzchnia_dzialki",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\pow_szer_dzialki",
    where_clause="dobre_dzialki__MinimumBoundi.Width >= 50 And dobre_dzialki__MinimumBoundi.Height >= 50",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,powierzchnia_dzialki,powierzchnia_dzialki.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,powierzchnia_dzialki,powierzchnia_dzialki.Shape_Area,-1,-1;Width "Width" true true false 8 Double 0 0,First,#,powierzchnia_dzialki,dobre_dzialki__MinimumBoundi.Width,-1,-1,powierzchnia_dzialki,dobre_dzialki__MinimumBoundi.Width,-1,-1;Height "Height" true true false 8 Double 0 0,First,#,powierzchnia_dzialki,dobre_dzialki__MinimumBoundi.Height,-1,-1,powierzchnia_dzialki,dobre_dzialki__MinimumBoundi.Height,-1,-1',
    sort_field=None
)

#---------------------------------------------------------------------------
# wybór działek spełniających kryteria (podejscie z różnymi wagami) -> 
#proces analogiczny jak dla podejścia z takimi samymi wagami
#---------------------------------------------------------------------------

arcpy.management.CopyFeatures(
    in_features="dzialki_clip_copy",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dzialki_clip_copy_copy",
    config_keyword="",
    spatial_grid_1=None,
    spatial_grid_2=None,
    spatial_grid_3=None
)

przydatnosc_ahp_poligon = arcpy.conversion.RasterToPolygon(
    in_raster="przydatnosc_ahp",
    out_polygon_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\przydatnosc_ahp_poligon",
    simplify="SIMPLIFY",
    raster_field="Value",
    create_multipart_features="SINGLE_OUTER_PART",
    max_vertices_per_feature=None
)

arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="przydatnosc_ahp_poligon",
    selection_type="NEW_SELECTION",
    where_clause="gridcode = 1",
    invert_where_clause=None
)

intersekcja_ahp = arcpy.analysis.Intersect(
    in_features="przydatnosc_ahp_poligon #;dzialki_clip_copy_copy #",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja_ahp",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)

arcpy.management.SelectLayerByAttribute("przydatnosc_ahp_poligon", "CLEAR_SELECTION")

statystyki_ahp = arcpy.analysis.Statistics(
    in_table="intersekcja_ahp",
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja_Statistics1_ahp",
    statistics_fields="Shape_Area SUM",
    case_field="FID_dzialki_clip_copy_copy",
    concatenation_separator=""
)

arcpy.management.AddJoin(
    in_layer_or_view="dzialki_clip_copy_copy",
    in_field="OBJECTID",
    join_table="intersekcja_Statistics1_ahp",
    join_field="FID_dzialki_clip_copy_copy",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

arcpy.management.CalculateField(
    in_table="dzialki_clip_copy_copy",
    field="Procent",
    expression="None if !intersekcja_Statistics1_ahp.SUM_Shape_Area! == None or !dzialki_clip_copy_copy.Shape_Area! == None else (!intersekcja_Statistics1_ahp.SUM_Shape_Area! / !dzialki_clip_copy_copy.Shape_Area!) * 100",
    expression_type="PYTHON3",
    code_block="",
    field_type="DOUBLE",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

arcpy.management.CalculateField(
    in_table="dzialki_clip_copy_copy",
    field="Przydatnosc",
    expression="""0 if !dzialki_clip_copy_copy.Procent! == None else (1 if !dzialki_clip_copy_copy.Procent! > 60 else 0)
""",
    expression_type="PYTHON3",
    code_block="",
    field_type="SHORT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

arcpy.conversion.ExportFeatures(
    in_features="dzialki_clip_copy_copy",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_ahp",
    where_clause="dzialki_clip_copy_copy.Przydatnosc = 1",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='NUMER_DZIA "NUMER_DZIA" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.NUMER_DZIA,0,253;NUMER_OBRE "NUMER_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.NUMER_OBRE,0,253;NUMER_JEDN "NUMER_JEDN" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.NUMER_JEDN,0,253;NAZWA_OBRE "NAZWA_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.NAZWA_OBRE,0,253;NAZWA_GMIN "NAZWA_GMIN" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.NAZWA_GMIN,0,253;POLE_EWIDE "POLE_EWIDE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.POLE_EWIDE,0,253;KLASOUZYTK "KLASOUZYTK" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.KLASOUZYTK,0,253;GRUPA_REJE "GRUPA_REJE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.GRUPA_REJE,0,253;DATA "DATA" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.DATA,0,253;ID_DZIALKI "ID_DZIALKI" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.ID_DZIALKI,0,253;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.Shape_Area,-1,-1;Procent "Procent" true true false 8 Double 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.Procent,-1,-1;Przydatnosc "Przydatnosc" true true false 2 Short 0 0,First,#,dzialki_clip_copy_copy,dzialki_clip_copy_copy.Przydatnosc,-1,-1;OBJECTID "OBJECTID" false true false 4 Long 0 9,First,#,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.OBJECTID,-1,-1,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.OBJECTID,-1,-1;FID_dzialki_clip_copy_copy "FID_dzialki_clip_copy_copy" true true false 4 Long 0 0,First,#,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.FID_dzialki_clip_copy_copy,-1,-1,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.FID_dzialki_clip_copy_copy,-1,-1;FREQUENCY "FREQUENCY" true true false 4 Long 0 0,First,#,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.FREQUENCY,-1,-1,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.FREQUENCY,-1,-1;SUM_Shape_Area "SUM_Shape_Area" true true false 8 Double 0 0,First,#,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.SUM_Shape_Area,-1,-1,dzialki_clip_copy_copy,intersekcja_Statistics1_ahp.SUM_Shape_Area,-1,-1',
    sort_field=None
)
arcpy.cartography.AggregatePolygons(
    in_features="dobre_dzialki_ahp",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg_ahp",
    aggregation_distance="0.1 Meters",
    minimum_area="0 SquareMeters",
    minimum_hole_size="0 SquareMeters",
    orthogonality_option="NON_ORTHOGONAL",
    barrier_features=None,
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg_Tbl1_ahp",
    aggregate_field=None
)

arcpy.conversion.ExportFeatures(
    in_features="dobre_dzialki_AggregatePolyg_ahp",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\powierzchnia_dzialki_ahp",
    where_clause="Shape_Area >= 20000",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg_ahp,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg_ahp,Shape_Area,-1,-1',
    sort_field=None
)
arcpy.management.MinimumBoundingGeometry(
    in_features="powierzchnia_dzialki_ahp",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki__MinimumBoundi_ahp",
    geometry_type="RECTANGLE_BY_WIDTH",
    group_option="NONE",
    group_field=None,
    mbg_fields_option="NO_MBG_FIELDS"
)

input_fc = "dobre_dzialki__MinimumBoundi_ahp"
arcpy.AddField_management(input_fc, "Width", "DOUBLE")
arcpy.AddField_management(input_fc, "Height", "DOUBLE")
with arcpy.da.UpdateCursor(input_fc, ["SHAPE@", "Width", "Height"]) as cursor:
    for row in cursor:
        extent = row[0].extent
        width = extent.XMax - extent.XMin
        height = extent.YMax - extent.YMin
        row[1] = width  
        row[2] = height  
        cursor.updateRow(row)
        
arcpy.management.AddJoin(
    in_layer_or_view="powierzchnia_dzialki_ahp",
    in_field="OBJECTID",
    join_table="dobre_dzialki__MinimumBoundi_ahp",
    join_field="OBJECTID",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

arcpy.conversion.ExportFeatures(
    in_features="powierzchnia_dzialki_ahp",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\pow_szer_dzialki_ahp1",
    where_clause="dobre_dzialki__MinimumBoundi_ahp.Width >= 50  And dobre_dzialki__MinimumBoundi_ahp.Height >=50 ",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,powierzchnia_dzialki_ahp.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,powierzchnia_dzialki_ahp.Shape_Area,-1,-1;OBJECTID "OBJECTID" false true false 4 Long 0 9,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.OBJECTID,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.OBJECTID,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.ORIG_FID,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Shape_Length,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Shape_Area,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Shape_Area,-1,-1;Width "Width" true true false 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Width,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Width,-1,-1;Height "Height" true true false 8 Double 0 0,First,#,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Height,-1,-1,powierzchnia_dzialki_ahp,dobre_dzialki__MinimumBoundi_ahp.Height,-1,-1',
    sort_field=None
)

#---------------------------------------------------------------------------
# wybór działek spełniających kryteria ostre -> 
#proces analogiczny jak dla podejścia z takimi samymi wagami
#---------------------------------------------------------------------------

#Połączenie kryteriów ostrych za pomocą operatora logicznego AND
ostre = arcpy.sa.FuzzyOverlay(
    in_rasters="woda_ostre;las_ostre;stoki_ostre;budynki_ostre",
    overlay_type="AND",
    gamma=0.9
)
ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\ostre")

arcpy.management.CopyFeatures(
    in_features="dzialki_clip_copy",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dzialki_clip_copy_copy_copy",
    config_keyword="",
    spatial_grid_1=None,
    spatial_grid_2=None,
    spatial_grid_3=None
)

przydatnosc_ahp_poligon = arcpy.conversion.RasterToPolygon(
    in_raster="ostre",
    out_polygon_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\przydatnosc_ostre",
    simplify="SIMPLIFY",
    raster_field="Value",
    create_multipart_features="SINGLE_OUTER_PART",
    max_vertices_per_feature=None
)

arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="przydatnosc_ostre",
    selection_type="NEW_SELECTION",
    where_clause="gridcode = 1",
    invert_where_clause=None
)

intersekcja_ostre = arcpy.analysis.Intersect(
    in_features="przydatnosc_ostre #;dzialki_clip_copy_copy_copy #",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja_ostre",
    join_attributes="ALL",
    cluster_tolerance=None,
    output_type="INPUT"
)

arcpy.management.SelectLayerByAttribute("przydatnosc_ostre", "CLEAR_SELECTION")

statystyki_ostre = arcpy.analysis.Statistics(
    in_table="intersekcja_ostre",
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\intersekcja_Statistics1_ostre",
    statistics_fields="Shape_Area SUM",
    case_field="FID_dzialki_clip_copy_copy_copy",
    concatenation_separator=""
)

arcpy.management.AddJoin(
    in_layer_or_view="dzialki_clip_copy_copy_copy",
    in_field="OBJECTID",
    join_table="intersekcja_Statistics1_ostre",
    join_field="FID_dzialki_clip_copy_copy_copy",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

arcpy.management.CalculateField(
    in_table="dzialki_clip_copy_copy_copy",
    field="Procent",
    expression="None if !intersekcja_Statistics1_ostre.SUM_Shape_Area! == None or !dzialki_clip_copy_copy_copy.Shape_Area! == None else (!intersekcja_Statistics1_ostre.SUM_Shape_Area! / !dzialki_clip_copy_copy_copy.Shape_Area!) * 100",
    expression_type="PYTHON3",
    code_block="",
    field_type="DOUBLE",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

arcpy.management.CalculateField(
    in_table="dzialki_clip_copy_copy_copy",
    field="Przydatnosc",
    expression="""0 if !dzialki_clip_copy_copy_copy.Procent! == None else (1 if !dzialki_clip_copy_copy_copy.Procent! > 60 else 0)
""",
    expression_type="PYTHON3",
    code_block="",
    field_type="SHORT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

arcpy.conversion.ExportFeatures(
    in_features="dzialki_clip_copy_copy_copy",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_ostre",
    where_clause="dzialki_clip_copy_copy_copy.Przydatnosc = 1",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='NUMER_DZIA "NUMER_DZIA" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.NUMER_DZIA,0,253;NUMER_OBRE "NUMER_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.NUMER_OBRE,0,253;NUMER_JEDN "NUMER_JEDN" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.NUMER_JEDN,0,253;NAZWA_OBRE "NAZWA_OBRE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.NAZWA_OBRE,0,253;NAZWA_GMIN "NAZWA_GMIN" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.NAZWA_GMIN,0,253;POLE_EWIDE "POLE_EWIDE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.POLE_EWIDE,0,253;KLASOUZYTK "KLASOUZYTK" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.KLASOUZYTK,0,253;GRUPA_REJE "GRUPA_REJE" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.GRUPA_REJE,0,253;DATA "DATA" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.DATA,0,253;ID_DZIALKI "ID_DZIALKI" true true false 254 Text 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.ID_DZIALKI,0,253;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.Shape_Area,-1,-1;Procent "Procent" true true false 8 Double 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.Procent,-1,-1;Przydatnosc "Przydatnosc" true true false 2 Short 0 0,First,#,dzialki_clip_copy_copy_copy,dzialki_clip_copy_copy_copy.Przydatnosc,-1,-1;OBJECTID "OBJECTID" false true false 4 Long 0 9,First,#,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.OBJECTID,-1,-1,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.OBJECTID,-1,-1;FID_dzialki_clip_copy_copy_copy "FID_dzialki_clip_copy_copy_copy" true true false 4 Long 0 0,First,#,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.FID_dzialki_clip_copy_copy_copy,-1,-1,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.FID_dzialki_clip_copy_copy_copy,-1,-1;FREQUENCY "FREQUENCY" true true false 4 Long 0 0,First,#,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.FREQUENCY,-1,-1,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.FREQUENCY,-1,-1;SUM_Shape_Area "SUM_Shape_Area" true true false 8 Double 0 0,First,#,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.SUM_Shape_Area,-1,-1,dzialki_clip_copy_copy_copy,intersekcja_Statistics1_ostre.SUM_Shape_Area,-1,-1',
    sort_field=None
)
arcpy.cartography.AggregatePolygons(
    in_features="dobre_dzialki_ostre",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg_ostre",
    aggregation_distance="0.1 Meters",
    minimum_area="0 SquareMeters",
    minimum_hole_size="0 SquareMeters",
    orthogonality_option="NON_ORTHOGONAL",
    barrier_features=None,
    out_table=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki_AggregatePolyg_Tbl1_ostre",
    aggregate_field=None
)

arcpy.conversion.ExportFeatures(
    in_features="dobre_dzialki_AggregatePolyg_ostre",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\powierzchnia_dzialki_ostre",
    where_clause="Shape_Area >= 20000",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg_ostre,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,dobre_dzialki_AggregatePolyg_ostre,Shape_Area,-1,-1',
    sort_field=None
)

arcpy.management.MinimumBoundingGeometry(
    in_features="powierzchnia_dzialki_ostre",
    out_feature_class=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\dobre_dzialki__MinimumBoundi_ostre",
    geometry_type="RECTANGLE_BY_WIDTH",
    group_option="NONE",
    group_field=None,
    mbg_fields_option="NO_MBG_FIELDS"
)

input_fc = "dobre_dzialki__MinimumBoundi_ostre"
arcpy.AddField_management(input_fc, "Width", "DOUBLE")
arcpy.AddField_management(input_fc, "Height", "DOUBLE")
with arcpy.da.UpdateCursor(input_fc, ["SHAPE@", "Width", "Height"]) as cursor:
    for row in cursor:
        extent = row[0].extent
        width = extent.XMax - extent.XMin
        height = extent.YMax - extent.YMin
        row[1] = width  
        row[2] = height 
        cursor.updateRow(row)
        
arcpy.management.AddJoin(
    in_layer_or_view="powierzchnia_dzialki_ostre",
    in_field="OBJECTID",
    join_table="dobre_dzialki__MinimumBoundi_ostre",
    join_field="OBJECTID",
    join_type="KEEP_ALL",
    index_join_fields="INDEX_JOIN_FIELDS",
    rebuild_index="NO_REBUILD_INDEX"
)

arcpy.conversion.ExportFeatures(
    in_features="powierzchnia_dzialki_ostre",
    out_features=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\pow_szer_dzialki_ostre",
    where_clause="dobre_dzialki__MinimumBoundi_ostre.Width >= 50 And dobre_dzialki__MinimumBoundi_ostre.Height >= 50",
    use_field_alias_as_name="NOT_USE_ALIAS",
    field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,powierzchnia_dzialki_ostre.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,powierzchnia_dzialki_ostre.Shape_Area,-1,-1;OBJECTID "OBJECTID" false true false 4 Long 0 9,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.OBJECTID,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.OBJECTID,-1,-1;ORIG_FID "ORIG_FID" true true false 4 Long 0 0,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.ORIG_FID,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.ORIG_FID,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Shape_Length,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Shape_Area,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Shape_Area,-1,-1;Width "Width" true true false 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Width,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Width,-1,-1;Height "Height" true true false 8 Double 0 0,First,#,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Height,-1,-1,powierzchnia_dzialki_ostre,dobre_dzialki__MinimumBoundi_ostre.Height,-1,-1',
    sort_field=None
)

#---------------------------------------------------------------------------
#Stworzenie mapy kosztów
#---------------------------------------------------------------------------

#Do warstwy zawierającej połączone odpowiednie warstwy z BDOT10k, dodanie pola koszt,
#koszt jest wybierany na podstawie warunków
arcpy.management.CalculateField(
    in_table="PT_merge_cliped",
    field="KOSZT",
    expression="calculate(!X_KOD!)",
    expression_type="PYTHON3",
    code_block="""def calculate(nazwa):
    if nazwa in ["PTWP01", "PTWP03", "PTUT01", "PTKM04", "PTSO01", "PTSSO02", "PTWZ01", "PTWZ02"]:
        return 0
    elif nazwa in ["PTWP02", "PTZB01", "PTZB04", "PTZB03", "PTKM02", "PTKM03"]:
        return 200
    elif nazwa in ["PTZB02", "PTLZ01", "PTUT03", "PTKM01"]:
        return 100
    elif nazwa in ["PTZB05", "PTLZ02", "PTLZ03", "PTPL01"]:
        return 50
    elif nazwa in ["PTRK01", "PTRK02"]:
        return 15
    elif nazwa in ["PTUT02"]:
        return 90
    elif nazwa in ["PTUT04", "PTUT05", "PTTR01"]:
        return 20
    elif nazwa in ["PTTR02", "PTGN01", "PTGN02", "PTGN03", "PTGN04"]:
        return 1
    elif nazwa in ["PTNZ01", "PTNZ02"]:
        return 150
    else:
        return 0""",
    field_type="Short",
    enforce_domains="NO_ENFORCE_DOMAINS"
)

#Konwerswja warstwy na raster
arcpy.conversion.FeatureToRaster(
    in_features="PT_merge_cliped",
    field="KOSZT",
    out_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\koszty",
    cell_size=r"C:\Sem5\Analizy_przestrzenne\farma_foto\dane\nmt_clip"
)

#Ustawienie wartości Null dla wartości równych 0 (bariery absolutne)
koszty_null = arcpy.ia.SetNull(
    in_conditional_raster="koszty",
    in_false_raster_or_constant="koszty",
    where_clause="Value = 0"
)
koszty_null.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\koszty_null")


#---------------------------------------------------------------------------
#Stworzenie mapy kosztów skumulowanych oraz mapy kierunków 
#(podejście mieszane takie same wagi)
#---------------------------------------------------------------------------

#Sprawdzenie czy zaleziono działki spełnaijące kryteria, jeżeli tak mapy są tworzone
count_powi = arcpy.management.GetCount("pow_szer_dzialki")[0]
if int(count_powi) > 0:
    out_distance_raster = arcpy.sa.CostDistance(
        in_source_data="pow_szer_dzialki",
        in_cost_raster="koszty_null",
        maximum_distance=None,
        out_backlink_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\backlink_raster",
        source_cost_multiplier=None,
        source_start_cost=None,
        source_resistance_rate=None,
        source_capacity=None,
        source_direction=""
    )
    out_distance_raster.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostDis_powi1")

    CostPat_lini1 = arcpy.sa.CostPath(
        in_destination_data="linie_Clip",
        in_cost_distance_raster="CostDis_powi1",
        in_cost_backlink_raster="backlink_raster",
        path_type="BEST_SINGLE",
        destination_field="OBJECTID",
        force_flow_direction_convention="INPUT_RANGE"
    )
    CostPat_lini1.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostPat_lini1")
else:
    print("brak działek w podejściu z takimi samymi wagami")

#---------------------------------------------------------------------------
#Stworzenie mapy kosztów skumulowanych oraz mapy kierunków 
#(podejście mieszane różne same wagi) 
#---------------------------------------------------------------------------
count_powi_ahp1 = arcpy.management.GetCount("pow_szer_dzialki_ahp1")[0]
if int(count_powi_ahp1) > 0:
    CostDis_powi1_ahp = arcpy.sa.CostDistance(
        in_source_data="pow_szer_dzialki_ahp1",
        in_cost_raster="koszty_null",
        maximum_distance=None,
        out_backlink_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\backlink_raster_ahp",
        source_cost_multiplier=None,
        source_start_cost=None,
        source_resistance_rate=None,
        source_capacity=None,
        source_direction=""
    )
    CostDis_powi1_ahp.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostDis_powi1_ahp")

    CostPat_lini1_ahp = arcpy.sa.CostPath(
        in_destination_data="linie_Clip",
        in_cost_distance_raster="CostDis_powi1_ahp",
        in_cost_backlink_raster="backlink_raster_ahp",
        path_type="BEST_SINGLE",
        destination_field="OBJECTID",
        force_flow_direction_convention="INPUT_RANGE"
    )
    CostPat_lini1_ahp.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostPat_lini1_ahp")
else:
    print("brak działek w podejściu z różnymi wagami")
#---------------------------------------------------------------------------
#Stworzenie mapy kosztów skumulowanych oraz mapy kierunków 
#(podejście ostre)
#---------------------------------------------------------------------------
count_powi_ostre = arcpy.management.GetCount("pow_szer_dzialki_ostre")[0]
if int(count_powi_ostre) > 0:
    CostDis_powi1_ostre = arcpy.sa.CostDistance(
        in_source_data="pow_szer_dzialki_ostre",
        in_cost_raster="koszty_null",
        maximum_distance=None,
        out_backlink_raster=r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\backlink_raster_ostre",
        source_cost_multiplier=None,
        source_start_cost=None,
        source_resistance_rate=None,
        source_capacity=None,
        source_direction=""
    )
    CostDis_powi1_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostDis_powi1_ostre")

    CostPat_lini1_ostre = arcpy.sa.CostPath(
        in_destination_data="linie_Clip",
        in_cost_distance_raster="CostDis_powi1_ostre",
        in_cost_backlink_raster="backlink_raster_ostre",
        path_type="BEST_SINGLE",
        destination_field="OBJECTID",
        force_flow_direction_convention="INPUT_RANGE"
    )
    CostPat_lini1_ostre.save(r"C:\Sem5\Analizy_przestrzenne\farma_foto\farma_foto\farma_foto.gdb\CostPat_lini1_ostre")
else: 
    print("brak działek w podejściu ostrym")
