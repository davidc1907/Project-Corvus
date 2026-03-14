const SUPABASE_URL = 'https://bqergkmgcauypelsvohc.supabase.co';
const SUPABASE_KEY = 'sb_publishable_v2LGPra6wnORPbPKDF1RBw_WxYdltEf';
mapboxgl.accessToken = 'pk.eyJ1IjoiZGF2aWRjMTkwNyIsImEiOiJjbW1xZnE4c24wd2M2MnBzZHAxZTJ3OGdkIn0.DuQ9I53OqjAt4m2k4JzYqg';

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/davidc1907/cmmqg2h8e000k01qq6s9p11gl',
    center: [10, 51],
    zoom: 4.5
});

let activePlanes = {
    "type": "FeatureCollection",
    "features": []
};

function processSighting(newSighting) {
    if (newSighting.lat && newSighting.lon) {
        const feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [newSighting.lon, newSighting.lat]
            },
            "properties": {
                "callsign": newSighting.callsign,
                "hex": newSighting.hex_code,
                "lastSeen": Date.now()
            }
        };

        const index = activePlanes.features.findIndex(f => f.properties.hex === newSighting.hex_code);

        if (index > -1) {
            activePlanes.features[index] = feature;
        } else {
            activePlanes.features.push(feature);
        }
    }
}

map.on('load', async () => {
    map.addSource('planes-source', {
        type: 'geojson',
        data: activePlanes
    });

    map.addLayer({
        id: 'planes-layer',
        type: 'circle',
        source: 'planes-source',
        paint: {
            'circle-radius': 7,
            'circle-color': '#ff3344',
            'circle-stroke-width': 1,
            'circle-stroke-color': '#ffffff'
        }
    });

    map.on('click', 'planes-layer', (e) => {
        const coordinates = e.features[0].geometry.coordinates.slice();
        const callsign = e.features[0].properties.callsign;
        const hex = e.features[0].properties.hex;

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(`
                <div style="color: #000; font-family: 'Inter', sans-serif;">
                    <strong style="font-size: 1.1em;">${callsign}</strong><br>
                    <span style="color: #666; font-size: 0.9em;">HEX: ${hex}</span>
                </div>
            `)
            .addTo(map);
    });

    map.on('mouseenter', 'planes-layer', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'planes-layer', () => {
        map.getCanvas().style.cursor = '';
    });

    const { data } = await supabaseClient
        .from('sightings')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(100);

    if (data) {
        data.reverse().forEach(sighting => {
            processSighting(sighting);
        });
        map.getSource('planes-source').setData(activePlanes);
    }

    supabaseClient
        .channel('public:sightings')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'sightings' }, payload => {
            processSighting(payload.new);
            map.getSource('planes-source').setData(activePlanes);
        })
        .subscribe();

    setInterval(() => {
        const now = Date.now();
        const timeout = 2 * 60 * 60 * 1000;

        const oldLength = activePlanes.features.length;

        activePlanes.features = activePlanes.features.filter(f => (now - f.properties.lastSeen) < timeout);

        if (activePlanes.features.length < oldLength) {
            map.getSource('planes-source').setData(activePlanes);
        }
    }, 60000);
});