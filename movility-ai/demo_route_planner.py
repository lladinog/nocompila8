from movility_ai.tools.providers.gtfs_metro import SimpleMetroGTFS

m = SimpleMetroGTFS()
print("Estaciones cargadas:", len(m.stops))
for i,(sid,(name,lat,lon)) in enumerate(m.stops.items()):
    if i>=10: break
    print(f"- {sid}: {name} ({lat}, {lon})")
